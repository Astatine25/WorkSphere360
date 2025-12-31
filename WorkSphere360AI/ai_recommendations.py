# ai_recommendations.py

def generate_employee_recommendation(row):
    recommendations = []

    # Burnout logic
    if row["Overtime_Hours"] > 40 and row["Productivity_Score"] < 75:
        recommendations.append(
            "High overtime with declining productivity. Recommend mandatory leave or workload redistribution."
        )

    # Leave balance underuse
    if row["EL_Balance"] > 15:
        recommendations.append(
            "Excess earned leave balance. Encourage planned vacation to reduce burnout risk."
        )

    # Peak season risk
    if row["Is_Peak_Season"] == 1 and row["Overtime_Hours"] > 30:
        recommendations.append(
            "Employee working long hours during peak season. Suggest staggered leave or backup allocation."
        )

    if not recommendations:
        recommendations.append("No immediate risk detected. Maintain current workload.")

    return " | ".join(recommendations)


def add_ai_recommendations(df):
    df["AI_Recommendation"] = df.apply(generate_employee_recommendation, axis=1)
    return df
