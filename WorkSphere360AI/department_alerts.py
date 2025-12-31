# department_alerts.py

def generate_department_alerts(df):
    alerts = []

    dept_summary = df.groupby("Department").agg(
        avg_overtime=("Overtime_Hours", "mean"),
        avg_productivity=("Productivity_Score", "mean"),
        peak_load=("Is_Peak_Season", "sum"),
        headcount=("Employee_ID", "count")
    ).reset_index()

    for _, row in dept_summary.iterrows():
        if row["avg_overtime"] > 35 and row["avg_productivity"] < 75:
            alerts.append({
                "Department": row["Department"],
                "Alert": "High burnout risk detected. Recommend workload rebalancing or temporary staffing."
            })
        elif row["peak_load"] > row["headcount"] * 0.6:
            alerts.append({
                "Department": row["Department"],
                "Alert": "Peak season overlap detected. Freeze non-essential leave approvals."
            })

    return alerts
