"""
Verification Script 3: Complaint-Level Bottlenecks & Descriptors
Computes:
  - Top 15 highest volume complaint categories
  - Top 15 slowest complaint categories (min 100 records)
  - Descriptor-level breakdown for the slowest category
  - Horizontal bar chart of delay rates by complaint type
"""

import os
import sys
import numpy as np
import pandas as pd
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
    
    comp_agg = df.groupby(["complaint_type", "agency"]).agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        p25_days=("resolution_time_days", lambda x: np.percentile(x, 25)),
        p75_days=("resolution_time_days", lambda x: np.percentile(x, 75)),
        delay_7d_rate=("delayed_over_7d", "mean"),
        delay_30d_rate=("delayed_over_30d", "mean")
    ).reset_index()
    
    comp_agg["share_pct"] = (comp_agg["count"] / n_total) * 100
    comp_agg["delay_7d_pct"] = comp_agg["delay_7d_rate"] * 100
    comp_agg["delay_30d_pct"] = comp_agg["delay_30d_rate"] * 100
    
    # Filter for significant sample size
    comp_sig = comp_agg[comp_agg["count"] >= 100].copy()
    
    top_volume = comp_sig.sort_values("count", ascending=False).head(15)
    top_slowest = comp_sig.sort_values("median_days", ascending=False).head(15)
    
    print("=== TOP 10 SLOWEST COMPLAINT TYPES (min 100 cases) ===")
    print(top_slowest[["complaint_type", "agency", "count", "median_days", "delay_7d_pct"]].head(10).to_string(index=False))
    
    # Analyze descriptors of the #1 slowest complaint type
    slowest_type = top_slowest.iloc[0]["complaint_type"]
    desc_df = df[df["complaint_type"] == slowest_type].groupby("descriptor").agg(
        count=("unique_key", "count"),
        median_days=("resolution_time_days", "median"),
        delay_7d_rate=("delayed_over_7d", "mean")
    ).reset_index().sort_values("count", ascending=False).head(8)
    desc_df["delay_7d_pct"] = desc_df["delay_7d_rate"] * 100
    
    # Save markdown table
    os.makedirs("avaloka_artifacts", exist_ok=True)
    table_lines = [
        "# Complaint-Level Bottleneck & Typology Analysis",
        "",
        "## Top 15 Slowest Complaint Types (Minimum 100 Records)",
        "",
        "| Complaint Type | Primary Agency | Total Volume | Share (%) | Median Days | 7-Day Delay (%) | 30-Day Delay (%) |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    for _, row in top_slowest.iterrows():
        table_lines.append(
            f"| **{row['complaint_type']}** | {row['agency']} | {row['count']:,d} | {row['share_pct']:.1f}% | "
            f"**{row['median_days']:.2f}** | **{row['delay_7d_pct']:.1f}%** | {row['delay_30d_pct']:.1f}% |"
        )
        
    table_lines.extend([
        "",
        f"## Granular Descriptor Breakdown for Top Delayed Type: `{slowest_type}`",
        "",
        "| Descriptor Sub-Category | Cases | Median Days | 7-Day Delay Rate (%) |",
        "| :--- | :--- | :--- | :--- |"
    ])
    for _, row in desc_df.iterrows():
        table_lines.append(
            f"| `{row['descriptor']}` | {row['count']:,d} | {row['median_days']:.2f} | {row['delay_7d_pct']:.1f}% |"
        )
        
    with open("avaloka_artifacts/complaint_bottlenecks.md", "w") as f:
        f.write("\n".join(table_lines))

    # Figure 4: Horizontal Bar Chart of Slowest Complaint Types
    os.makedirs("figures", exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    
    # Sort for barh (slowest on top)
    plot_df = top_slowest.sort_values("median_days", ascending=True)
    y_pos = np.arange(len(plot_df))
    
    agency_colors = {
        "HPD": "#e41a1c",
        "DOB": "#377eb8",
        "DOT": "#4daf4a",
        "DEP": "#984ea3",
        "DSNY": "#ff7f00",
        "DPR": "#a65628",
        "DOHMH": "#f781bf",
        "NYPD": "#999999"
    }
    bar_colors = [agency_colors.get(ag, "#333333") for ag in plot_df["agency"]]
    
    bars = ax.barh(y_pos, plot_df["median_days"], color=bar_colors, edgecolor="black", alpha=0.85)
    ax.set_yticks(y_pos)
    labels = [f"{ct} ({ag})" for ct, ag in zip(plot_df["complaint_type"], plot_df["agency"])]
    ax.set_yticklabels(labels, fontsize=9, fontweight="bold")
    ax.set_xlabel("Median Resolution Duration in Days", fontsize=11, fontweight="bold")
    ax.set_title("Top 15 Slowest NYC 311 Complaint Categories (2024)", fontsize=13, fontweight="bold", pad=12)
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    
    # Value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, f"{width:.1f}d", 
                va="center", ha="left", fontsize=8.5, fontweight="bold")
                
    ax.set_xlim(0, max(plot_df["median_days"]) * 1.15)
    plt.tight_layout()
    fig.savefig("figures/fig4_slowest_complaint_types.png")
    plt.close(fig)
    print("Saved: figures/fig4_slowest_complaint_types.png")

if __name__ == "__main__":
    main()

