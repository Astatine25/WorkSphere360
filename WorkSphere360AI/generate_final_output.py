"""
WorkSphere360 – AI Leave Management System
Generate Final AI Output for Dashboard

This script:
1. Loads leave_data.csv
2. Performs feature engineering
3. Trains XGBoost / RF model
4. Predicts burnout probability
5. Generates AI recommendations
6. Saves final_ai_output.csv
"""

# --------------------------------------------------
# PATH & IMPORT SAFETY (DO NOT REMOVE)
# --------------------------------------------------
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

# --------------------------------------------------
# STANDARD IMPORTS
# --------------------------------------------------
import pandas as pd

# --------------------------------------------------
# PROJECT MODULES
# --------------------------------------------------
from feature_engineering import compute_features
from model_xgboost import train_xgboost
from ai_recommendations import generate_ai_actions

# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------
INPUT_FILE = BASE_DIR / "leave_data.csv"
OUTPUT_FILE = BASE_DIR / "final_ai_output.csv"

# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------
def main():
    print("Loading leave data...")
    df = pd.read_csv(INPUT_FILE)

    print("Running feature engineering...")
    df_features = compute_features(df)

    # Deduplicate to employee level for ML
    ml_df = (
        df_features
        .groupby("Employee_ID", as_index=False)
        .last()
    )

    print("Training ML model (Burnout Prediction)...")
    model = train_xgboost(ml_df)

    FEATURE_COLS = [
        "Tenure",
        "Bradford_Factor",
        "Overtime_Hours_Last_30_Days",
        "Days_Since_Last_Vacation",
        "Average_Productivity_Score",
        "Burnout_Risk_Score"
    ]

    print("Predicting burnout probability...")
    ml_df["Burnout_Probability"] = model.predict_proba(
        ml_df[FEATURE_COLS]
    )[:, 1]

    print("Generating AI recommendations...")
    ml_df["AI_Recommendation"] = ml_df.apply(
        generate_ai_actions,
        axis=1
    )

    print("Saving final AI output...")
    ml_df.to_csv(OUTPUT_FILE, index=False)

    print("SUCCESS!")
    print(f"Output generated: {OUTPUT_FILE}")

# --------------------------------------------------
# ENTRY POINT
# --------------------------------------------------
if __name__ == "__main__":
    main()
