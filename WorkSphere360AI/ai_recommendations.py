def generate_ai_actions(row):
    actions = []

    if row["Burnout_Probability"] > 0.8:
        actions.append("Mandatory 3-day recovery leave")
        actions.append("Reduce workload for next sprint")

    elif row["Burnout_Probability"] > 0.6:
        actions.append("Recommend PTO within 30 days")

    if row["Bradford_Factor"] > 200:
        actions.append("Monitor frequent short-term absences")

    if row["Days_Since_Last_Vacation"] > 180:
        actions.append("Employee overdue for vacation")

    return " | ".join(actions)
