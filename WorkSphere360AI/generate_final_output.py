import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ======================================================
# Burnout Score Calculation
# ======================================================
def compute_burnout_score(df):
    df["Burnout_Score"] = (
        0.4 * (df["Overtime_Hours"] / df["Overtime_Hours"].max()) +
        0.4 * (1 - df["Productivity_Score"] / 100) +
        0.2 * df["Is_Peak_Season"]
    )
    df["Burnout_Score"] = df["Burnout_Score"].clip(0, 1)
    return df

# ======================================================
# AI Recommendation Generator
# ======================================================
def ai_recommendation(row):
    if row["Burnout_Score"] >= 0.8:
        return "Critical burnout risk. Recommend immediate leave approval."
    if row["Overtime_Hours"] >= 40:
        return "Sustained overtime detected. Recommend workload redistribution."
    if row["Productivity_Score"] < 70:
        return "Productivity decline detected. Suggest short recovery leave."
    return "No immediate risk. Leave can be approved."

# ======================================================
# Leave Approval Optimizer
# ======================================================
def approval_decision(row):
    if row["Burnout_Score"] >= 0.8:
        return "AUTO-APPROVE"
    if row["Is_Peak_Season"] == 1 and row["Burnout_Score"] < 0.5:
        return "SUGGEST ALTERNATE DATES"
    return "APPROVE"

# ======================================================
# Calendar-Based Alternate Leave Generator
# ======================================================
def generate_alternate_dates(month, total_days, peak):
    if peak == 1:
        month = month + 1 if month < 12 else 1
    start = datetime(2025, int(month), 1)
    end = start + timedelta(days=int(total_days))
    return f"{start.date()} → {end.date()}"

# ======================================================
# HR Executive Summary (LLM-style, rule-based)
# ======================================================
def generate_hr_summaries(df):
    summaries = {}
    for dept, g in df.groupby("Department"):
        summaries[dept] = (
            f"Department {dept} has an average burnout score of "
            f"{round(g['Burnout_Score'].mean(),2)}. "
            f"{(g['Burnout_Score'] > 0.75).sum()} employees are at high burnout risk. "
            f"Recommended actions include proactive leave approvals, workload balancing, "
            f"and closer productivity monitoring."
        )
    return summaries

# ======================================================
# MAIN PIPELINE
# ======================================================
def main():
    print("Loading leave data...")
    df = pd.read_csv("leave_data.csv")

    print("Computing burnout score...")
    df = compute_burnout_score(df)

    print("Generating AI recommendations...")
    df["AI_Recommendation"] = df.apply(ai_recommendation, axis=1)

    print("Optimizing approval decisions...")
    df["Approval_Decision"] = df.apply(approval_decision, axis=1)

    print("Generating alternate leave dates...")
    df["Suggested_Alternate_Dates"] = df.apply(
        lambda r: generate_alternate_dates(r["Month"], r["Total_Days"], r["Is_Peak_Season"]),
        axis=1
    )

    print("Generating HR summaries...")
    summaries = generate_hr_summaries(df)
    summary_df = pd.DataFrame([
        {"Department": k, "HR_Summary": v} for k, v in summaries.items()
    ])

    print("Saving outputs...")
    df.to_csv("final_ai_output.csv", index=False)
    summary_df.to_csv("hr_executive_summaries.csv", index=False)

    print(" Pipeline complete. Files generated successfully.")

if __name__ == "__main__":
    main()
