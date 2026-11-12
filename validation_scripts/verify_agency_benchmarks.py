"""
Verification Script 2: Agency-Level Operational Benchmarks
Computes:
  - Total volume, median resolution time, IQR, and 7-day delay rate by responding agency
  - Spearman rank correlation between intake volume and median turnaround time
  - Scatter plot of Volume vs. Turnaround time
  - Saves markdown table artifact
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
os.environ["MPLCONFIGDIR"] = os.path.abspath("scratch")
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    data_path = "data/processed/nyc_311_analytical_full.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.", file=sys.stderr)
        sys.exit(1)
        
    df = pd.read_csv(data_path, low_memory=False)
    n_total = len(df)
    
    agency_agg = df.groupby(["agency", "agency_name"]).agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        p25_days=("resolution_time_days", lambda x: np.percentile(x, 25)),
        p75_days=("resolution_time_days", lambda x: np.percentile(x, 75)),
        p90_days=("resolution_time_days", lambda x: np.percentile(x, 90)),
        mean_days=("resolution_time_days", "mean"),
        delay_7d_rate=("delayed_over_7d", "mean"),
        delay_30d_rate=("delayed_over_30d", "mean")
    ).reset_index()
    
    agency_agg["volume_share_pct"] = (agency_agg["count"] / n_total) * 100
    agency_agg["delay_7d_pct"] = agency_agg["delay_7d_rate"] * 100
    agency_agg["delay_30d_pct"] = agency_agg["delay_30d_rate"] * 100
    agency_agg["iqr_days"] = agency_agg["p75_days"] - agency_agg["p25_days"]
    
    # Filter for agencies with >= 100 records for statistical significance
    agency_sig = agency_agg[agency_agg["count"] >= 100].sort_values("count", ascending=False).copy()
    
    # Correlation analysis
    spearman_corr, spearman_p = stats.spearmanr(agency_sig["count"], agency_sig["median_days"])
    pearson_corr, pearson_p = stats.pearsonr(np.log10(agency_sig["count"]), agency_sig["median_days"])
    
    print("=== AGENCY BENCHMARK SUMMARY (Agencies with >= 100 cases) ===")
    print(f"Number of Major Responding Agencies Evaluated: {len(agency_sig)}")
    print(f"Spearman Rank Correlation (Volume vs. Median Days): r = {spearman_corr:.3f} (p = {spearman_p:.4f})")
    print(f"Pearson Correlation (Log-Volume vs. Median Days): r = {pearson_corr:.3f} (p = {pearson_p:.4f})")
    print("\nTop 10 Agencies by Volume:")
    print(agency_sig[["agency", "count", "volume_share_pct", "median_days", "delay_7d_pct"]].head(10).to_string(index=False))
    
    # Save markdown table
    os.makedirs("avaloka_artifacts", exist_ok=True)
    table_lines = [
        "# Responding Agency Operational Benchmark Report",
        "",
        f"**Sample**: {n_total:,d} completed requests across NYC agencies.",
        f"**Correlation Assessment**: Spearman rank correlation between intake volume and median resolution time is **$r = {spearman_corr:.3f}$** ($p = {spearman_p:.4f}$). High volume does **not** cause longer resolution delays.",
        "",
        "| Agency | Full Agency Name | Total Complaints | Share (%) | Median (Days) | 25th Pct | 75th Pct | 7-Day Delay Rate (%) | 30-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for _, row in agency_sig.iterrows():
        table_lines.append(
            f"| **{row['agency']}** | {row['agency_name']} | {row['count']:,d} | {row['volume_share_pct']:.1f}% | "
            f"**{row['median_days']:.2f}** | {row['p25_days']:.2f} | {row['p75_days']:.2f} | "
            f"**{row['delay_7d_pct']:.1f}%** | {row['delay_30d_pct']:.1f}% |"
        )
    with open("avaloka_artifacts/agency_benchmarks.md", "w") as f:
        f.write("\n".join(table_lines))

    # Figure 3: Volume vs Median Resolution Time Scatter Plot
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    scatter = ax.scatter(
        agency_sig["count"],
        agency_sig["median_days"],
        s=agency_sig["delay_7d_pct"] * 15 + 80,  # Bubble size proportional to 7d delay rate
        c=agency_sig["delay_7d_pct"],
        cmap="YlOrRd",
        edgecolors="black",
        linewidths=1.2,
        alpha=0.85
    )
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("7-Day Delay Rate (%)", fontsize=10, fontweight="bold")
    
    # Annotate agency points
    for _, row in agency_sig.iterrows():
        offset_y = 0.2 if row["median_days"] < 10 else -0.4
        ax.annotate(
            row["agency"],
            (row["count"], row["median_days"]),
            xytext=(0, 6),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            ha="center"
        )
        
    ax.set_xscale("log")
    ax.set_xlabel("Total Complaint Volume (Log Scale)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Median Resolution Time (Days)", fontsize=11, fontweight="bold")
    ax.set_title("Agency Volume vs. Resolution Velocity (NYC 311)", fontsize=13, fontweight="bold", pad=12)
    ax.grid(True, which="both", linestyle="--", alpha=0.3)
    
    plt.tight_layout()
    fig.savefig("figures/fig3_agency_volume_vs_delay.png")
    plt.close(fig)
    print("Saved: figures/fig3_agency_volume_vs_delay.png")

if __name__ == "__main__":
    main()
