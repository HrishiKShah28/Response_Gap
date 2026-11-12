"""
Verification Script 1: Distribution Analysis & Quantiles
Computes:
  - Exact parametric & non-parametric resolution metrics (Mean, Std, Median, IQR, P90, P99)
  - 7-Day & 30-Day delay rates with 95% Wilson Score confidence intervals
  - Monthly time-series of delay rates
  - Plots: Distribution histogram (log-scale) and monthly trend
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
os.environ["MPLCONFIGDIR"] = os.path.abspath("scratch")
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def wilson_ci(k, n, confidence=0.95):
    if n == 0:
        return 0, 0
    z = 1.95996  # 95% confidence
    p = k / n
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half_width = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return centre - half_width, centre + half_width

def main():
    data_path = "data/processed/nyc_311_analytical_full.csv"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Run acquisition first.", file=sys.stderr)
        sys.exit(1)
        
    df = pd.read_csv(data_path, low_memory=False)
    durations = df["resolution_time_days"].values
    n = len(durations)
    
    mean_val = np.mean(durations)
    std_val = np.std(durations)
    median_val = np.median(durations)
    p25 = np.percentile(durations, 25)
    p75 = np.percentile(durations, 75)
    iqr_val = p75 - p25
    p90 = np.percentile(durations, 90)
    p95 = np.percentile(durations, 95)
    p99 = np.percentile(durations, 99)
    
    k_7d = np.sum(durations > 7.0)
    k_30d = np.sum(durations > 30.0)
    
    pct_7d = (k_7d / n) * 100
    ci_7d_low, ci_7d_high = wilson_ci(k_7d, n)
    
    pct_30d = (k_30d / n) * 100
    ci_30d_low, ci_30d_high = wilson_ci(k_30d, n)
    
    print("=== RESOLUTION TIME DISTRIBUTION SUMMARY ===")
    print(f"Total Valid Completed Requests: {n:,d}")
    print(f"Mean (Arithmetic): {mean_val:.2f} days (Std Dev: {std_val:.2f})")
    print(f"Median: {median_val:.2f} days ({median_val*24:.1f} hours)")
    print(f"25th Percentile: {p25:.2f} days ({p25*24:.1f} hours)")
    print(f"75th Percentile: {p75:.2f} days ({p75*24:.1f} hours)")
    print(f"Interquartile Range (IQR): {iqr_val:.2f} days")
    print(f"90th Percentile: {p90:.2f} days")
    print(f"95th Percentile: {p95:.2f} days")
    print(f"99th Percentile: {p99:.2f} days")
    print(f"7-Day Delay Rate: {pct_7d:.2f}% [{ci_7d_low*100:.2f}%, {ci_7d_high*100:.2f}%]")
    print(f"30-Day Delay Rate: {pct_30d:.2f}% [{ci_30d_low*100:.2f}%, {ci_30d_high*100:.2f}%]")
    
    # Save markdown table artifact
    os.makedirs("avaloka_artifacts", exist_ok=True)
    summary_md = f"""# Citywide Resolution Duration Distribution
| Metric | Value (Days) | Value (Hours) | 95% Confidence Interval |
| :--- | :--- | :--- | :--- |
| **Sample Size ($N$)** | {n:,d} | - | - |
| **Mean (Skewed)** | {mean_val:.2f} | {mean_val*24:.1f} | [{mean_val - 1.96*std_val/np.sqrt(n):.2f}, {mean_val + 1.96*std_val/np.sqrt(n):.2f}] |
| **Median ($P_{{50}}$)** | **{median_val:.2f}** | **{median_val*24:.1f}** | - |
| **25th Percentile ($P_{{25}}$)** | {p25:.2f} | {p25*24:.1f} | - |
| **75th Percentile ($P_{{75}}$)** | {p75:.2f} | {p75*24:.1f} | - |
| **Interquartile Range (IQR)** | {iqr_val:.2f} | {iqr_val*24:.1f} | - |
| **90th Percentile ($P_{{90}}$)** | {p90:.2f} | {p90*24:.1f} | - |
| **99th Percentile ($P_{{99}}$)** | {p99:.2f} | {p99*24:.1f} | - |
| **7-Day Delay Rate ($R_{{7d}}$)** | **{pct_7d:.2f}%** | - | [{ci_7d_low*100:.2f}%, {ci_7d_high*100:.2f}%] |
| **30-Day Delay Rate ($R_{{30d}}$)**| **{pct_30d:.2f}%** | - | [{ci_30d_low*100:.2f}%, {ci_30d_high*100:.2f}%] |
"""
    with open("avaloka_artifacts/distribution_summary.md", "w") as f:
        f.write(summary_md)

    # Plot 1: Log-scale distribution histogram
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    
    # Clip zero/tiny durations for log plot
    positive_durations = np.clip(durations, 0.01, 365.0)
    bins = np.logspace(np.log10(0.01), np.log10(365.0), 50)
    
    ax.hist(positive_durations, bins=bins, color="#1f77b4", edgecolor="black", alpha=0.7, label="Complaints")
    ax.axvline(median_val, color="red", linestyle="--", linewidth=2, label=f"Median ({median_val:.2f} days)")
    ax.axvline(7.0, color="orange", linestyle="-", linewidth=2, label=f"7-Day Threshold ({pct_7d:.1f}% delayed)")
    ax.axvline(30.0, color="purple", linestyle=":", linewidth=2, label=f"30-Day Threshold ({pct_30d:.1f}% delayed)")
    
    ax.set_xscale("log")
    ax.set_xlabel("Resolution Duration in Days (Log Scale)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Number of Complaints", fontsize=11, fontweight="bold")
    ax.set_title("NYC 311 Resolution Duration Distribution (2024 Cohort)", fontsize=13, fontweight="bold", pad=12)
    ax.grid(True, which="both", ls="--", alpha=0.3)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    fig.savefig("figures/fig1_resolution_distribution.png")
    plt.close(fig)
    print("Saved: figures/fig1_resolution_distribution.png")

    # Plot 2: Monthly 7-day delay rate trend
    monthly = df.groupby("created_month").agg(
        total=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d=("delayed_over_7d", "mean")
    ).reset_index()
    monthly["delay_7d_pct"] = monthly["delay_7d"] * 100
    
    fig, ax1 = plt.subplots(figsize=(9, 4.5), dpi=300)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    x = monthly["created_month"].values
    
    color = "#d95f02"
    ax1.set_xlabel("Month of Creation (2024)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("7-Day Delay Rate (%)", color=color, fontsize=11, fontweight="bold")
    line = ax1.plot(x, monthly["delay_7d_pct"], color=color, marker="o", linewidth=2.5, label="7-Day Delay Rate (%)")
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_xticks(x)
    ax1.set_xticklabels([month_names[i-1] for i in x])
    ax1.set_ylim(0, max(monthly["delay_7d_pct"])*1.25)
    ax1.grid(True, linestyle="--", alpha=0.4)
    
    ax2 = ax1.twinx()
    color2 = "#7570b3"
    ax2.set_ylabel("Median Resolution Time (Days)", color=color2, fontsize=11, fontweight="bold")
    line2 = ax2.plot(x, monthly["median_days"], color=color2, marker="s", linestyle="--", linewidth=2, label="Median Days")
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.set_ylim(0, max(monthly["median_days"])*1.3)
    
    plt.title("Seasonality of NYC 311 Resolution Velocity (Month-by-Month 2024)", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    fig.savefig("figures/fig2_monthly_trend.png")
    plt.close(fig)
    print("Saved: figures/fig2_monthly_trend.png")

if __name__ == "__main__":
    main()
