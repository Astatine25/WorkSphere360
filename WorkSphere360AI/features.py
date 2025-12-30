import pandas as pd
import numpy as np
from datetime import datetime

def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Dates
    df["Start_Date"] = pd.to_datetime(df["Start_Date"], format="%Y%m%d")
    df["End_Date"] = pd.to_datetime(df["End_Date"], format="%Y%m%d")

    today = pd.Timestamp.today()

    # Leave Frequency (for Bradford Factor)
    leave_counts = df.groupby("Employee_ID")["Total_Days"].agg(
        Absence_Count="count",
        Total_Absence_Days="sum"
    ).reset_index()

    leave_counts["Bradford_Factor"] = (
        leave_counts["Absence_Count"] ** 2
    ) * leave_counts["Total_Absence_Days"]

    df = df.merge(leave_counts, on="Employee_ID", how="left")

    # Days since last vacation
    last_leave = df.groupby("Employee_ID")["End_Date"].max().reset_index()
    last_leave["Days_Since_Last_Vacation"] = (
        today - last_leave["End_Date"]
    ).dt.days

    df = df.merge(
        last_leave[["Employee_ID", "Days_Since_Last_Vacation"]],
        on="Employee_ID",
        how="left"
    )

    # Burnout Risk Score (normalized)
    df["Burnout_Risk_Score"] = (
        0.5 * (df["Overtime_Hours_Last_30_Days"] / 80) +
        0.3 * (1 / (df["Days_Since_Last_Vacation"] + 1)) +
        0.2 * (1 - df["Average_Productivity_Score"] / 100)
    )

    return df
