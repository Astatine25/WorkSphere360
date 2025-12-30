# feature_engineering.py
# ---------------------------------------------
# Feature engineering for AI Leave & Burnout Analysis
# Author: WorkSphere360
# ---------------------------------------------

import pandas as pd
import numpy as np


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes HR analytics and burnout-related features.
    Ensures no NaN / Inf values enter ML models.
    """

    df = df.copy()

    # -------------------------------
    # Parse Dates Safely
    # -------------------------------
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
    df["End_Date"] = pd.to_datetime(df["End_Date"], errors="coerce")

    today = pd.Timestamp.today()

    # -------------------------------
    # Absence Aggregations
    # -------------------------------
    absence_stats = (
        df.groupby("Employee_ID")["Total_Days"]
        .agg(
            Absence_Count="count",
            Total_Absence_Days="sum"
        )
        .reset_index()
    )

    # Bradford Factor (Disruption Index)
    absence_stats["Bradford_Factor"] = (
        absence_stats["Absence_Count"] ** 2
    ) * absence_stats["Total_Absence_Days"]

    df = df.merge(absence_stats, on="Employee_ID", how="left")

    # -------------------------------
    # Days Since Last Leave
    # -------------------------------
    last_leave = (
        df.groupby("Employee_ID")["End_Date"]
        .max()
        .reset_index()
    )

    last_leave["Days_Since_Last_Vacation"] = (
        today - last_leave["End_Date"]
    ).dt.days

    # Guardrails
    last_leave["Days_Since_Last_Vacation"] = (
        last_leave["Days_Since_Last_Vacation"]
        .clip(lower=0, upper=365)
    )

    df = df.merge(
        last_leave[["Employee_ID", "Days_Since_Last_Vacation"]],
        on="Employee_ID",
        how="left"
    )

    # -------------------------------
    # Burnout Risk Score (Weighted)
    # -------------------------------
    df["Overtime_Hours_Last_30_Days"] = df["Overtime_Hours_Last_30_Days"].clip(0, 120)
    df["Average_Productivity_Score"] = df["Average_Productivity_Score"].clip(0, 100)

    df["Burnout_Risk_Score"] = (
        0.45 * (df["Overtime_Hours_Last_30_Days"] / 120) +
        0.35 * (1 / (df["Days_Since_Last_Vacation"] + 10)) +
        0.20 * (1 - df["Average_Productivity_Score"] / 100)
    )

    # -------------------------------
    # Final Data Hygiene
    # -------------------------------
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    return df
