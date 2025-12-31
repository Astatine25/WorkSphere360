import pandas as pd

# -----------------------------
# Fallback Rule-Based Summary
# -----------------------------
def rule_based_summary(dept, df):
    high_burnout = df[df["Burnout_Score"] > 0.75]
    overtime = df["Overtime_Hours"].mean()

    summary = f"""
Department: {dept}

Key Insights:
- Average burnout risk is {round(df["Burnout_Score"].mean(),2)}
- {len(high_burnout)} employees flagged for high burnout
- Average overtime: {round(overtime,1)} hours

Recommended Actions:
- Approve recovery leave for high-risk employees
- Rebalance workloads in peak weeks
- Monitor productivity trends weekly
"""
    return summary.strip()

# -----------------------------
# LLM-Based Summary Generator
# -----------------------------
def generate_hr_summary(df):
    summaries = {}

    for dept, g in df.groupby("Department"):
        try:
            # ⚠️ Replace with OpenAI / Gemini if enabled
            summaries[dept] = rule_based_summary(dept, g)
        except Exception:
            summaries[dept] = rule_based_summary(dept, g)

    return summaries
