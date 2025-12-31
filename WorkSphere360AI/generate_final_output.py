# generate_final_output.py
import pandas as pd
from feature_engineering import compute_features
from model_xgboost import train_xgboost

def main():
    print("Loading leave data...")
    df = pd.read_csv("leave_data.csv")

    print("Running feature engineering...")
    df_feat = compute_features(df)

    print("Training ML model (Burnout Prediction)...")
    model = train_xgboost(df_feat)

    feature_cols = [
        "Tenure_Yrs",
        "Total_Days",
        "Is_Peak_Season",
        "Avg_Productivity",
        "Overtime_Hours",
        "Project_Risk_Score",
        "Disruption_Score"
    ]

    df_feat["Burnout_Probability"] = model.predict_proba(
        df_feat[feature_cols]
    )[:, 1]

    df_feat["Risk_Level"] = pd.cut(
        df_feat["Burnout_Probability"],
        bins=[0, 0.4, 0.7, 1.0],
        labels=["Low", "Medium", "High"]
    )

    df_feat.to_csv("final_ai_output.csv", index=False)
    print(" SUCCESS: final_ai_output.csv generated")

if __name__ == "__main__":
    main()
