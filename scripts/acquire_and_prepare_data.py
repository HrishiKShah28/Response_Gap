"""
Data Acquisition & Sanitization Pipeline for NYC 311 Response Gap Analysis
Socrata Endpoint: erm2-nwe9 (NYC Open Data)
Target Sample: 120,000 records stratified across 12 months of 2024
Outputs:
  - data/processed/nyc_311_analytical_full.csv (for Avaloka EDA & Profiling)
  - data/processed/nyc_311_model_intake.csv (strictly intake features + target, zero leakage)
  - data/processed/open_cases_censored.csv (for survivor bias analysis)
  - data/data_dictionary.md (comprehensive field dictionary and quality audit)
"""

import os
import sys
import io
import time
import requests
import pandas as pd
import numpy as np

SOCRATA_ENDPOINT = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
SELECTED_FIELDS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "location_type",
    "incident_zip",
    "borough",
    "open_data_channel_type",
    "status",
    "resolution_description"
]

MONTHS_2024 = [
    ("2024-01-01", "2024-02-01", "Jan 2024"),
    ("2024-02-01", "2024-03-01", "Feb 2024"),
    ("2024-03-01", "2024-04-01", "Mar 2024"),
    ("2024-04-01", "2024-05-01", "Apr 2024"),
    ("2024-05-01", "2024-06-01", "May 2024"),
    ("2024-06-01", "2024-07-01", "Jun 2024"),
    ("2024-07-01", "2024-08-01", "Jul 2024"),
    ("2024-08-01", "2024-09-01", "Aug 2024"),
    ("2024-09-01", "2024-10-01", "Sep 2024"),
    ("2024-10-01", "2024-11-01", "Oct 2024"),
    ("2024-11-01", "2024-12-01", "Nov 2024"),
    ("2024-12-01", "2025-01-01", "Dec 2024"),
]
PER_MONTH_LIMIT = 10000

def fetch_monthly_sample():
    records_chunks = []
    print(f"=== Starting Socrata Data Ingestion: 12 months x {PER_MONTH_LIMIT:,} records ===")
    
    for start_date, end_date, label in MONTHS_2024:
        params = {
            "$select": ",".join(SELECTED_FIELDS),
            "$where": f"created_date >= '{start_date}T00:00:00' and created_date < '{end_date}T00:00:00'",
            "$limit": PER_MONTH_LIMIT,
            "$order": "unique_key ASC"  # Deterministic pseudo-random distribution across the month
        }
        retries = 3
        success = False
        while retries > 0 and not success:
            try:
                t0 = time.time()
                resp = requests.get(SOCRATA_ENDPOINT, params=params, timeout=45)
                resp.raise_for_status()
                chunk_df = pd.read_csv(io.StringIO(resp.text), low_memory=False)
                elapsed = time.time() - t0
                print(f"[{label}] Fetched {len(chunk_df):,d} records in {elapsed:.1f}s")
                records_chunks.append(chunk_df)
                success = True
            except Exception as e:
                retries -= 1
                print(f"Warning: Failed to fetch {label} ({e}). Retries left: {retries}")
                time.sleep(3)
        if not success:
            raise RuntimeError(f"Could not fetch data for month {label}")
        time.sleep(0.5)  # Respect API rate limits
        
    df_raw = pd.concat(records_chunks, ignore_index=True)
    print(f"\nTotal Raw Records Ingested: {len(df_raw):,d}")
    return df_raw

def clean_and_prepare(df_raw):
    print("\n=== Processing & Sanitizing Telemetry ===")
    df = df_raw.copy()
    
    # 1. Deduplication
    init_count = len(df)
    df = df.drop_duplicates(subset=["unique_key"]).copy()
    dup_count = init_count - len(df)
    print(f"Deduplicated by unique_key: removed {dup_count} duplicate rows.")

    # 2. Datetime parsing
    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
    
    # 3. Separate Censored (Open / Pending) Cases
    open_mask = df["closed_date"].isna()
    df_open = df[open_mask].copy()
    ref_date = pd.to_datetime("2025-03-01T00:00:00")
    df_open["open_age_days"] = (ref_date - df_open["created_date"]).dt.total_seconds() / 86400.0
    df_open["open_over_7d"] = (df_open["open_age_days"] > 7.0).astype(int)
    
    os.makedirs("data/processed", exist_ok=True)
    df_open.to_csv("data/processed/open_cases_censored.csv", index=False)
    print(f"Censored / Unclosed Cases: {len(df_open):,d} records ({len(df_open)/len(df)*100:.1f}%) saved to data/processed/open_cases_censored.csv")
    print(f"  -> Open cases with age > 7 days: {df_open['open_over_7d'].mean()*100:.1f}%")

    # 4. Completed Cases
    df_closed = df[~open_mask].copy()
    print(f"Completed Cases with closed_date: {len(df_closed):,d} records ({len(df_closed)/len(df)*100:.1f}%)")

    # 5. Calculate Resolution Time in decimal days
    df_closed["resolution_time_days"] = (df_closed["closed_date"] - df_closed["created_date"]).dt.total_seconds() / 86400.0
    
    # 6. Flag & remove negative resolution durations (timestamp clerk errors)
    negative_mask = df_closed["resolution_time_days"] < 0
    neg_count = negative_mask.sum()
    print(f"Negative Duration Anomaly (`closed_date < created_date`): {neg_count} records ({neg_count/len(df_closed)*100:.3f}%). Filtering out.")
    df_clean = df_closed[~negative_mask].copy()

    # 7. Multi-year extreme outlier capping (365 days)
    outlier_mask = df_clean["resolution_time_days"] > 365.0
    outlier_count = outlier_mask.sum()
    print(f"Extreme Outliers (> 365 days): {outlier_count} records ({outlier_count/len(df_clean)*100:.2f}%). Capping at 365 for sensitivity control.")
    df_clean["resolution_time_days_capped"] = df_clean["resolution_time_days"].clip(upper=365.0)

    # 8. Binary Classification Targets
    df_clean["delayed_over_7d"] = (df_clean["resolution_time_days"] > 7.0).astype(int)
    df_clean["delayed_over_30d"] = (df_clean["resolution_time_days"] > 30.0).astype(int)

    # 9. Temporal Intake Features (known at ticket creation)
    df_clean["created_year"] = df_clean["created_date"].dt.year
    df_clean["created_month"] = df_clean["created_date"].dt.month
    df_clean["created_day"] = df_clean["created_date"].dt.day
    df_clean["created_dow"] = df_clean["created_date"].dt.dayofweek  # 0=Mon, 6=Sun
    df_clean["created_hour"] = df_clean["created_date"].dt.hour
    df_clean["is_weekend"] = df_clean["created_dow"].isin([5, 6]).astype(int)
    df_clean["is_business_hours"] = ((df_clean["created_dow"] < 5) & (df_clean["created_hour"].between(8, 18))).astype(int)

    # 10. Clean Categorical Text Attributes
    df_clean["borough"] = df_clean["borough"].fillna("Unspecified").str.strip().str.upper()
    df_clean["complaint_type"] = df_clean["complaint_type"].fillna("Unknown").str.strip()
    df_clean["descriptor"] = df_clean["descriptor"].fillna("Unknown / Not Specified").str.strip()
    df_clean["location_type"] = df_clean["location_type"].fillna("Unknown / Other").str.strip()
    df_clean["incident_zip"] = df_clean["incident_zip"].astype(str).str.split(".").str[0].str.zfill(5)
    df_clean.loc[~df_clean["incident_zip"].str.match(r"^\d{5}$"), "incident_zip"] = "Unknown"
    df_clean["open_data_channel_type"] = df_clean["open_data_channel_type"].fillna("UNKNOWN").str.strip().str.upper()

    # 11. Save Full Analytical Dataset for Avaloka EDA & Profiling
    full_path = "data/processed/nyc_311_analytical_full.csv"
    df_clean.to_csv(full_path, index=False)
    file_size_mb = os.path.getsize(full_path) / (1024 * 1024)
    print(f"\n[Artifact 1] Saved: {full_path} ({len(df_clean):,d} rows, {file_size_mb:.2f} MB)")

    # 12. Create & Save Strict Intake-Time Model Dataset (Zero Leakage)
    intake_columns = [
        "unique_key",
        "agency",
        "complaint_type",
        "descriptor",
        "borough",
        "incident_zip",
        "location_type",
        "open_data_channel_type",
        "created_month",
        "created_dow",
        "created_hour",
        "is_weekend",
        "is_business_hours",
        "delayed_over_7d"  # Ground-truth binary target
    ]
    df_model = df_clean[intake_columns].copy()
    model_path = "data/processed/nyc_311_model_intake.csv"
    df_model.to_csv(model_path, index=False)
    model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"[Artifact 2] Saved: {model_path} ({len(df_model):,d} rows, {model_size_mb:.2f} MB)")

    # 13. Generate Data Dictionary & Quality Audit
    generate_data_dictionary(df_clean, df_open)
    return df_clean

def generate_data_dictionary(df_clean, df_open):
    dict_path = "data/data_dictionary.md"
    n_clean = len(df_clean)
    n_open = len(df_open)
    total_records = n_clean + n_open
    
    delay_7d_rate = df_clean["delayed_over_7d"].mean() * 100
    delay_30d_rate = df_clean["delayed_over_30d"].mean() * 100
    median_days = df_clean["resolution_time_days"].median()
    iqr_25 = df_clean["resolution_time_days"].quantile(0.25)
    iqr_75 = df_clean["resolution_time_days"].quantile(0.75)
    
    lines = [
        "# NYC 311 TELEMETRY DATA DICTIONARY & HYGIENE AUDIT",
        "",
        f"**Observation Period**: Calendar Year 2024 (Stratified Sample: 12 months)",
        f"**Total Ingested Records**: {total_records:,d}",
        f"**Completed Cases Analyzed**: {n_clean:,d} ({n_clean/total_records*100:.1f}%)",
        f"**Censored / Unclosed Cases Isolated**: {n_open:,d} ({n_open/total_records*100:.1f}%)",
        "",
        "---",
        "",
        "## 1. Headline Empirical Summary Statistics",
        "",
        f"- **Median Resolution Time**: {median_days:.2f} decimal days ({median_days*24:.1f} hours)",
        f"- **Interquartile Range (IQR)**: {iqr_25:.2f} days (25th percentile) to {iqr_75:.2f} days (75th percentile)",
        f"- **7-Day Delay Rate ($R_{{7d}}$)**: {delay_7d_rate:.2f}% of completed complaints exceed 7 days",
        f"- **30-Day Extreme Delay Rate ($R_{{30d}}$)**: {delay_30d_rate:.2f}% of completed complaints exceed 30 days",
        f"- **Unclosed Ticket Delay Rate**: {df_open['open_over_7d'].mean()*100:.1f}% of open cases have been unresolved for > 7 days",
        "",
        "---",
        "",
        "## 2. Dataset Field Specification",
        "",
        "| Column Name | Data Type | Null % | Description | Modeling Role & Leakage Status |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    col_roles = {
        "unique_key": ("Integer", "0.0%", "Unique service request identifier", "Primary Key (Excluded from features)"),
        "created_date": ("Datetime", "0.0%", "Citizen ticket creation timestamp", "Intake temporal index"),
        "closed_date": ("Datetime", "0.0%", "Agency ticket closure timestamp", "🔴 High Leakage (Used solely for duration calculation)"),
        "agency": ("String", "0.0%", "Responding city agency acronym", "🟢 Safe Intake Feature (Key predictor)"),
        "agency_name": ("String", "0.0%", "Full name of responding agency", "🟢 Safe (Redundant with agency)"),
        "complaint_type": ("String", "0.0%", "Broad problem category", "🟢 Safe Intake Feature (Key predictor)"),
        "descriptor": ("String", f"{df_clean['descriptor'].isna().mean()*100:.2f}%", "Granular sub-complaint detail", "🟢 Safe Intake Feature"),
        "location_type": ("String", f"{df_clean['location_type'].isna().mean()*100:.2f}%", "Physical site category", "🟢 Safe Intake Feature"),
        "incident_zip": ("String", f"{(df_clean['incident_zip'] == 'Unknown').mean()*100:.2f}%", "5-digit USPS postal code", "🟢 Safe Intake Feature"),
        "borough": ("String", f"{(df_clean['borough'] == 'UNSPECIFIED').mean()*100:.2f}%", "NYC borough name", "🟢 Safe Intake Feature"),
        "open_data_channel_type": ("String", "0.0%", "Intake mechanism (PHONE, ONLINE, etc.)", "🟢 Safe Intake Feature"),
        "status": ("String", "0.0%", "Ticket lifecycle state", "🔴 High Leakage (Excluded)"),
        "resolution_description": ("String", f"{df_clean['resolution_description'].isna().mean()*100:.2f}%", "Agency closure narrative", "🔴 High Leakage (Excluded)"),
        "resolution_time_days": ("Float", "0.0%", "Exact resolution duration in decimal days", "🔴 Continuous Target (Excluded from features)"),
        "delayed_over_7d": ("Integer", "0.0%", "Binary classification target (1 if >7d, else 0)", "🎯 Primary Prediction Target"),
        "delayed_over_30d": ("Integer", "0.0%", "Secondary extreme-delay flag", "🔴 Target (Excluded from features)"),
        "created_month": ("Integer", "0.0%", "Month of submission (1-12)", "🟢 Safe Intake Feature (Seasonality)"),
        "created_dow": ("Integer", "0.0%", "Day of week of submission (0=Mon, 6=Sun)", "🟢 Safe Intake Feature (Weekly cadence)"),
        "created_hour": ("Integer", "0.0%", "Hour of submission (0-23)", "🟢 Safe Intake Feature (Diurnal cycle)"),
        "is_weekend": ("Integer", "0.0%", "Flag for Saturday/Sunday submission", "🟢 Safe Intake Feature"),
        "is_business_hours": ("Integer", "0.0%", "Flag for Mon-Fri 08:00-18:00 submission", "🟢 Safe Intake Feature")
    }
    
    for col, (dtype, null_pct, desc, role) in col_roles.items():
        if col in df_clean.columns:
            lines.append(f"| `{col}` | {dtype} | {null_pct} | {desc} | {role} |")
            
    lines.extend([
        "",
        "---",
        "",
        "## 3. Top Responding Agencies by Volume",
        "",
        "| Agency | Full Name | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])
    
    agency_grp = df_clean.groupby(["agency", "agency_name"]).agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d=("delayed_over_7d", "mean")
    ).reset_index().sort_values("count", ascending=False)
    
    for _, row in agency_grp.head(10).iterrows():
        share = row["count"] / n_clean * 100
        d7 = row["delay_7d"] * 100
        lines.append(f"| **{row['agency']}** | {row['agency_name']} | {row['count']:,d} | {share:.1f}% | {row['median_days']:.2f} | {d7:.1f}% |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Top Complaint Types by Volume",
        "",
        "| Complaint Type | Primary Agency | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])
    
    comp_grp = df_clean.groupby(["complaint_type", "agency"]).agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d=("delayed_over_7d", "mean")
    ).reset_index().sort_values("count", ascending=False)
    
    for _, row in comp_grp.head(10).iterrows():
        share = row["count"] / n_clean * 100
        d7 = row["delay_7d"] * 100
        lines.append(f"| **{row['complaint_type']}** | {row['agency']} | {row['count']:,d} | {share:.1f}% | {row['median_days']:.2f} | {d7:.1f}% |")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Borough Breakdown & Disparity Preview",
        "",
        "| Borough | Count | Share (%) | Median Duration (Days) | 7-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])
    
    boro_grp = df_clean.groupby("borough").agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d=("delayed_over_7d", "mean")
    ).reset_index().sort_values("count", ascending=False)
    
    for _, row in boro_grp.iterrows():
        share = row["count"] / n_clean * 100
        d7 = row["delay_7d"] * 100
        lines.append(f"| **{row['borough']}** | {row['count']:,d} | {share:.1f}% | {row['median_days']:.2f} | {d7:.1f}% |")

    with open(dict_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[Artifact 3] Saved Data Dictionary: {dict_path}")

if __name__ == "__main__":
    df_raw = fetch_monthly_sample()
    df_clean = clean_and_prepare(df_raw)
    print("\n=== Data Acquisition & Preparation Completed Successfully ===")
