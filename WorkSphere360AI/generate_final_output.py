import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# -----------------------------
# Utility: Burnout Score
# -----------------------------
def compute_burnout_score(df):
    df["Burnout_Score"] = (
        0.4 * (df["Overtime_Hours"] / df["Overtime_Hours"].max()) +
        0.4 * (1 - df["Productivity_Score"] / 100) +
        0.2 * (df["Is_Peak_Season"])
    )
    return df

# -----------------------------
# AI Recommendation Generator
# -----------------------------
def generate_ai_recommendation(row):
    if row["Burnout_Score"] > 0.75:
        return "High burnout risk. Recommend immediate leave and workload redistribution."
    elif row["Overtime_Hours"] > 40:
        return "Excessive overtime detected. Recommend manager intervention."
    elif row["Productivity_Score"] < 70:
        return "Productivity dip observed. Suggest short recovery leave."
    else:
        return "No immediate risk. Leave can be approved."

# -----------------------------
# Calendar-Based Alternate Leave Generator
# -----------------------------
def suggest_alternate_leave(month, total_days, is_peak):
    if is_peak == 1:
        alt_month = month + 1 if month < 12 else 1
    else:
        alt_month = month

    start_date = datetime(2025, alt_month, 1)
    end_date = start_date + timedelta(days=int(total_days))

    return f"{start_date.date()} → {end_date.date()}"

# -----------------------------
# Leave Approval Optimizer
# -----------------------------
def approval_decision(row):
    if row["Burnout_Score"] > 0.8:
        return "Auto-Approve"
    if row["Is_Peak_Season"] == 1 and row["Burnout_Score"] < 0.5:
        return "Suggest Alternate Dates"
    return "Approve"

# -----------------------------
# Department Alerts
# -----------------------------
def department_alerts(df):
    alerts = []
    grouped = df.groupby("Department")

    for dept, g in grouped:
        burnout_pct = (g["Burnout_Score"] > 0.75).mean()
        if burnout_pct > 0.3:
            alerts.append(f" {dept}: High burnout concentration ({round(burnout_pct*100,1)}%)")

    return alerts

# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main():
    print("Loading leave data...")
    df = pd.read_csv("leave_data.csv")

    print("Computing burnout risk...")
    df = compute_burnout_score(df)

    print("Generating AI recommendations...")
    df["AI_Recommendation"] = df.apply(generate_ai_recommendation, axis=1)

    print("Optimizing leave approvals...")
    df["Approval_Decision"] = df.apply(approval_decision, axis=1)

    print("Generating alternate leave dates...")
    df["Suggested_Alternate_Dates"] = df.apply(
        lambda r: suggest_alternate_leave(r["Month"], r["Total_Days"], r["Is_Peak_Season"]),
        axis=1
    )

    print("Generating department alerts...")
    alerts = department_alerts(df)
    for a in alerts:
        print(a)

    print("Saving final AI output...")
    df.to_csv("final_ai_output.csv", index=False)

    print("Done  File: final_ai_output.csv")

if __name__ == "__main__":
    main()
