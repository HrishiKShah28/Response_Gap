"""
Script to extract and plot top predictive features from the logistic regression model
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib
os.environ["MPLCONFIGDIR"] = os.path.abspath("scratch")
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    data_path = "data/processed/nyc_311_model_intake.csv"
    df = pd.read_csv(data_path, low_memory=False)
    
    train_df = df[df["created_month"] <= 9].copy()
    
    top_descriptors = train_df["descriptor"].value_counts().head(50).index
    train_df["descriptor_clean"] = train_df["descriptor"].where(train_df["descriptor"].isin(top_descriptors), "Other")
    
    cat_cols_clean = ["agency", "complaint_type", "descriptor_clean", "borough", "location_type", "open_data_channel_type"]
    num_features = ["created_dow", "created_hour", "is_weekend", "is_business_hours"]
    
    X_train = train_df[cat_cols_clean + num_features]
    y_train = train_df["delayed_over_7d"].values
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols_clean),
            ("num", "passthrough", num_features)
        ]
    )
    clf = LogisticRegression(C=0.5, max_iter=1000, class_weight="balanced", random_state=42)
    pipe = Pipeline([("prep", preprocessor), ("clf", clf)])
    pipe.fit(X_train, y_train)
    
    # Feature names
    ohe = pipe.named_steps["prep"].named_transformers_["cat"]
    feature_names = list(ohe.get_feature_names_out(cat_cols_clean)) + num_features
    coefs = pipe.named_steps["clf"].coef_[0]
    
    feat_df = pd.DataFrame({"feature": feature_names, "coefficient": coefs, "odds_ratio": np.exp(coefs)})
    feat_df["abs_coef"] = feat_df["coefficient"].abs()
    
    # Top 15 positive (delay drivers) and top 5 negative (speed drivers)
    top_pos = feat_df.sort_values("coefficient", ascending=False).head(12)
    top_neg = feat_df.sort_values("coefficient", ascending=True).head(6)
    plot_df = pd.concat([top_neg, top_pos]).sort_values("coefficient", ascending=True)
    
    # Clean feature names for display
    plot_df["clean_name"] = plot_df["feature"].str.replace("complaint_type_", "Type: ").str.replace("agency_", "Agency: ").str.replace("descriptor_clean_", "Desc: ").str.replace("borough_", "Borough: ")
    
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    colors = ["#2ca02c" if c < 0 else "#d62728" for c in plot_df["coefficient"]]
    
    bars = ax.barh(np.arange(len(plot_df)), plot_df["coefficient"], color=colors, edgecolor="black", alpha=0.85)
    ax.set_yticks(np.arange(len(plot_df)))
    ax.set_yticklabels(plot_df["clean_name"], fontsize=9, fontweight="bold")
    ax.set_xlabel("Logistic Regression Coefficient (Log Odds of > 7-Day Delay)", fontsize=10, fontweight="bold")
    ax.set_title("Intake-Time Predictors of NYC 311 Resolution Velocity", fontsize=12, fontweight="bold", pad=12)
    ax.axvline(0, color="black", linestyle="--", lw=1)
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    
    for bar in bars:
        width = bar.get_width()
        ha = "left" if width > 0 else "right"
        offset = 0.08 if width > 0 else -0.08
        ax.text(width + offset, bar.get_y() + bar.get_height()/2, f"{width:+.2f}", va="center", ha=ha, fontsize=8, fontweight="bold")
        
    plt.tight_layout()
    fig.savefig("figures/fig9_feature_importances.png")
    plt.close(fig)
    print("Saved: figures/fig9_feature_importances.png")

if __name__ == "__main__":
    main()
