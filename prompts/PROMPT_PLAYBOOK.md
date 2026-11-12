# AVALOKA INTERACTIVE PROMPT PLAYBOOK

**Project**: The 311 Response Gap: Can We Predict Which Public Complaints Will Take Too Long to Resolve?  
**Target System**: Avaloka AI Platform (https://avaloka.ai)

---

## Overview

This playbook provides the exact sequence of natural language prompts to enter into Avaloka's chat interface. For each prompt, this document defines:
1. **The Exact Copy-Paste Prompt String**.
2. **Expected Agent Routing & Plan**: How the Planner Agent decomposes the task.
3. **Code Drawer Inspection Checklist**: Specific Python/Pandas operations to inspect in the Coder Agent's script.
4. **Auto Insights / Chart Verifications**: Expected visualization outputs.
5. **Adversarial / Follow-Up Query**: Human-in-the-loop challenge to stress-test the findings.

---

## Prompt 1: Ingestion, Schema Profiling & Data Hygiene

### 📋 Copy-Paste Prompt:
```text
Please profile our uploaded NYC 311 dataset (`nyc_311_analytical_full.csv`). Identify all column data types, calculate missing value percentages for every column, check for duplicate records on unique_key, and verify the date range for created_date and closed_date. Display summary statistics for numerical and temporal fields, and show the initial Auto Insights charts.
```

### 🔍 What to Inspect in Avaloka:
- **Planner Agent**: Confirms plan: (1) schema inspection, (2) missingness audit, (3) summary stats, (4) Auto Insights generation.
- **Coder Agent Script**: Open the code drawer. Verify that datetime fields are parsed using `pd.to_datetime(..., errors='coerce')`.
- **Auto Insights Panel**: Verify that up to 5 automatic charts are populated (e.g., volume by agency, complaints by borough).
- **Sanity Threshold**: Total records should be ~115,000–120,000 rows, with zero duplicates on `unique_key`.

---

## Prompt 2: Resolution Time Distribution & Quantile Metrics

### 📋 Copy-Paste Prompt:
```text
Calculate the overall resolution duration in decimal days as (closed_date - created_date). Report the mean, standard deviation, median, 25th percentile, 75th percentile, 90th percentile, and 99th percentile. What exact percentage of complaints take > 7 calendar days to resolve, and what percentage take > 30 calendar days? Plot a histogram with a logarithmic x-axis showing the resolution time distribution, and a monthly trend line of the 7-day delay rate across 2024.
```

### 🔍 What to Inspect in Avaloka:
- **Coder Agent Script**: Confirm that resolution duration is computed as `.dt.total_seconds() / 86400.0`. Check that negative durations (`closed_date < created_date`) are either filtered or zero.
- **Statistical Honesty**: Verify that Avaloka's commentary emphasizes the **Median** rather than the arithmetic mean due to extreme positive skewness.
- **Key Headline Numbers**:
  - Median should be ~2.5 to 3.0 days.
  - 7-Day Delay Rate should be ~17% to 22%.
  - 30-Day Delay Rate should be ~3% to 6%.

---

## Prompt 3: Agency Operational Benchmarks & Volume Trade-off

### 📋 Copy-Paste Prompt:
```text
Group the complaints by agency. For each agency, compute: (1) total complaint volume, (2) median resolution duration in days, (3) interquartile range (IQR), and (4) the percentage of complaints taking > 7 days. Rank the agencies by median resolution time. Generate a scatter plot comparing total volume (log-scale x-axis) against median resolution time (y-axis) to evaluate whether high-volume agencies are structurally slower.
```

### 🔍 What to Inspect in Avaloka:
- **Visualization**: Scatter plot showing total complaints on the x-axis (log scale) vs. median days on the y-axis.
- **Code Drawer**: Check `df.groupby('agency').agg(...)`. Ensure non-parametric median is used.

### ⚔️ Adversarial Follow-Up Prompt:
```text
Looking at the scatter plot, does higher complaint volume correlate with longer median resolution times? If NYPD handles the largest aggregate volume but maintains one of the fastest median resolution times, why does volume alone fail to explain turnaround speed? What operational and statutory differences account for this?
```

---

## Prompt 4: Complaint Typology & Problem Bottlenecks

### 📋 Copy-Paste Prompt:
```text
Filter for complaint types with at least 100 cases. Identify the top 15 complaint types with the longest median resolution times, and contrast them with the top 15 most frequent complaint types. Create a horizontal bar chart displaying the 7-day delay rate for each of the top 15 slowest complaint types, indicating their primary responding agency.
```

### 🔍 What to Inspect in Avaloka:
- **Findings**: Top slowest complaint types should concentrate in **HPD** (housing maintenance, lead paint, heat/hot water) and **DOB** (building construction, illegal conversions), while rapid categories concentrate in **NYPD** (parking, noise) and **DSNY** (sanitation).

### ⚔️ Granular Follow-Up Prompt:
```text
For the slowest complaint category identified, break down the resolution times by its descriptor sub-categories. Are all sub-descriptors equally delayed, or is the backlog concentrated in specific scenarios?
```

---

## Prompt 5: Geographic Disparities & Simpson's Paradox (Adversarial Check)

### 📋 Copy-Paste Prompt:
```text
Analyze resolution time across the five boroughs: BRONX, BROOKLYN, MANHATTAN, QUEENS, and STATEN ISLAND (excluding Unspecified). For each borough, show total complaint count, median resolution days, and the percentage of cases delayed > 7 days. Plot a comparative bar chart of the 7-day delay rate across boroughs.
```

### ⚔️ Critical Simpson's Paradox Challenge Prompt:
```text
The Bronx appears to have a higher 7-day delay rate in the aggregate numbers. Is this because municipal services are inherently slower in the Bronx, or because the Bronx has a higher proportion of complex housing maintenance complaints (HPD)? Run a controlled comparison: calculate the median resolution time and 7-day delay rate by borough ONLY for 'HEAT/HOT WATER' complaints, and separately ONLY for 'Illegal Parking' complaints. Does the borough disparity persist when holding complaint type constant?
```

### 🔍 What to Inspect in Avaloka:
- **Coder Agent Script**: Confirm that filtering isolates the specific complaint type before grouping by borough.
- **Critical Verification**: When isolating `HEAT/HOT WATER`, borough median resolution times converge to within a narrow band, proving that **aggregate borough disparities are confounded by case-mix variation (Simpson's Paradox)**.

---

## Prompt 6: Temporal Cadence & Submission Timing

### 📋 Copy-Paste Prompt:
```text
Investigate the relationship between when a complaint is submitted and its subsequent resolution speed. Group by: (1) created_month (seasonality), (2) created_dow (Monday through Sunday), and (3) created_hour (0 through 23). Calculate the 7-day delay rate for each grouping. Create a heatmap or grouped bar chart displaying the 7-day delay rate across days of the week and submission hours.
```

### 🔍 What to Inspect in Avaloka:
- **Pattern**: Evaluate the weekend intake penalty (Saturday/Sunday submissions accumulating 48 hours of initial administrative latency) and winter heating surges.

---

## Prompt 7: Predictive Modeling Configuration via MTA

### 📋 Copy-Paste Prompt:
```text
We want to build a machine learning model to predict whether a newly created complaint will take more than 7 days to close (target: delayed_over_7d). Use ONLY intake-time features: agency, complaint_type, descriptor, borough, incident_zip, location_type, open_data_channel_type, created_month, created_dow, and created_hour. Do NOT use closed_date, status, resolution_description, or any post-creation fields. Screen for data leakage, set up a baseline model, and propose a training plan using a chronological train/test split.
```

### 🔍 What to Inspect in Avaloka MTA:
1. **Data Leakage Screening**: MTA must report that post-intake fields were successfully screened and excluded.
2. **Proposed Plan**: Review model type (Logistic Regression or Gradient Boosted Trees), feature encodings, and hyperparameters.
3. **Conversational Tuning**:
   ```text
   Ensure class weights are balanced to handle class imbalance, and evaluate against both a majority-class baseline and an agency-prior baseline. Let us train with an out-of-time chronological split.
   ```
4. **Approval Command**:
   ```text
   The plan looks rigorous and leak-free. Go ahead and train the model.
   ```
5. **Model Artifact Capture**: Record the generated **Model Run ID**, ROC-AUC, PR-AUC, confusion matrix, and feature importances.
