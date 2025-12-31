# feature_engineering.py
import pandas as pd
import numpy as np

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Safety
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Normalize inputs
    df["Overtime_Hours"] = df["Overtime_Hours"].clip(0, 120)
    df["Avg_Productivity"] = df["Avg_Productivity"].clip(0, 100)
    df["Tenure_Yrs"] = df["Tenure_Yrs"].clip(0, 40)
    df["Total_Days"] = df["Total_Days"].clip(0, 30)

    # Bradford-style disruption proxy
    df["Disruption_Score"] = df["Total_Days"] * (1 + df["Is_Peak_Season"])

    # Burnout Risk Score (derived)
    df["Burnout_Risk_Score"] = (
        0.35 * (df["Overtime_Hours"] / 120) +
        0.30 * (1 - df["Avg_Productivity"] / 100) +
        0.20 * df["Project_Risk_Score"] +
        0.15 * (df["Disruption_Score"] / 30)
    )

    df["Burnout_Risk_Score"] = df["Burnout_Risk_Score"].clip(0, 1)

    # Fill numeric NaNs
    df.fillna(df.median(numeric_only=True), inplace=True)

    return df
