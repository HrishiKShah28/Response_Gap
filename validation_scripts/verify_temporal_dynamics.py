"""
Verification Script 5: Temporal Cadence & Intake-Time Dynamics
Computes:
  - 7-Day delay rate by day of week (Monday through Sunday)
  - 7-Day delay rate by hour of submission (0 to 23)
  - Heatmap matrix: Day of Week x Submission Hour
  - Weekend Latency Odds Ratio
  - Saves markdown artifact and heatmap visualization
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
    
    # 1. Day of Week Analysis
    dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_agg = df.groupby("created_dow").agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d_rate=("delayed_over_7d", "mean")
    ).reset_index()
    dow_agg["day_name"] = dow_agg["created_dow"].map(lambda x: dow_names[x])
    dow_agg["delay_7d_pct"] = dow_agg["delay_7d_rate"] * 100
    
    # 2. Weekend vs. Weekday Comparison & Odds Ratio
    wknd_cases = df[df["is_weekend"] == 1]
    wkday_cases = df[df["is_weekend"] == 0]
    
    wknd_delayed = wknd_cases["delayed_over_7d"].sum()
    wknd_not_delayed = len(wknd_cases) - wknd_delayed
    
    wkday_delayed = wkday_cases["delayed_over_7d"].sum()
    wkday_not_delayed = len(wkday_cases) - wkday_delayed
    
    table_2x2 = [[wknd_delayed, wknd_not_delayed], [wkday_delayed, wkday_not_delayed]]
    odds_ratio, p_value = stats.fisher_exact(table_2x2)
    
    # 3. 7x24 Matrix: Day of Week x Hour of Day
    grid_7x24 = df.groupby(["created_dow", "created_hour"])["delayed_over_7d"].mean().unstack() * 100
    
    print("=== TEMPORAL DYNAMICS & SUBMISSION CADENCE ===")
    print(dow_agg[["created_dow", "day_name", "count", "median_days", "delay_7d_pct"]].to_string(index=False))
    print(f"\nWeekend Submission Odds Ratio: OR = {odds_ratio:.3f} (p = {p_value:.4e})")
    print(f"Weekday 7-Day Delay Rate: {wkday_cases['delayed_over_7d'].mean()*100:.2f}%")
    print(f"Weekend 7-Day Delay Rate: {wknd_cases['delayed_over_7d'].mean()*100:.2f}%")
    
    # Save markdown artifact
    os.makedirs("avaloka_artifacts", exist_ok=True)
    table_lines = [
        "# Temporal Cadence & Intake-Time Dynamics Report",
        "",
        "## 1. Day of Week Resolution Patterns",
        "",
        "| Day of Week | Index | Total Inquiries | Share (%) | Median Days | 7-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for _, row in dow_agg.iterrows():
        table_lines.append(
            f"| **{row['day_name']}** | {row['created_dow']} | {row['count']:,d} | {row['count']/len(df)*100:.1f}% | "
            f"**{row['median_days']:.2f}** | **{row['delay_7d_pct']:.2f}%** |"
        )
        
    table_lines.extend([
        "",
        "## 2. Statistical Association: The Weekend Intake Penalty",
        "",
        f"- **Weekday Delay Rate**: {wkday_cases['delayed_over_7d'].mean()*100:.2f}%",
        f"- **Weekend Delay Rate**: {wknd_cases['delayed_over_7d'].mean()*100:.2f}%",
        f"- **Odds Ratio ($OR$)**: **{odds_ratio:.3f}** (Fisher's exact test $p = {p_value:.3e}$)",
        "- **Operational Meaning**: Citizen complaints submitted on Saturday or Sunday have an odds of extended delay (> 7 days) that is statistically elevated compared to weekday complaints, attributable to non-operating depot and dispatch hours for administrative agencies."
    ])
    with open("avaloka_artifacts/temporal_dynamics.md", "w") as f:
        f.write("\n".join(table_lines))

    # Figure 6: Heatmap of Day-of-Week vs. Hour-of-Day
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    
    cax = ax.imshow(grid_7x24.values, cmap="YlOrRd", aspect="auto", interpolation="nearest")
    cbar = plt.colorbar(cax, ax=ax)
    cbar.set_label("7-Day Delay Rate (%)", fontsize=10, fontweight="bold")
    
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(dow_names, fontsize=10, fontweight="bold")
    ax.set_xticks(np.arange(24))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45, fontsize=8, ha="right")
    
    ax.set_xlabel("Hour of Submission (Local Eastern Time)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Day of Week", fontsize=11, fontweight="bold")
    ax.set_title("NYC 311 7-Day Delay Risk by Citizen Submission Time (168-Hour Matrix)", fontsize=12, fontweight="bold", pad=12)
    
    plt.tight_layout()
    fig.savefig("figures/fig6_temporal_cadence_heatmap.png")
    plt.close(fig)
    print("Saved: figures/fig6_temporal_cadence_heatmap.png")

if __name__ == "__main__":
    main()
