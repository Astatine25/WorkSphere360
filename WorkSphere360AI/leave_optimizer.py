# leave_optimizer.py
def optimize_leave_decision(row, dept_capacity):
    """
    dept_capacity: dict {Department: current_capacity_percentage}
    """

    dept = row["Department"]

    # Capacity guardrail
    if dept_capacity.get(dept, 1) < 0.7:
        return {
            "Decision": "Defer",
            "Reason": "Department capacity below 70%. Risk of understaffing."
        }

    # Peak season constraint
    if row["Is_Peak_Season"] == 1 and row["Total_Days"] > 3:
        return {
            "Decision": "Suggest Alternate Dates",
            "Reason": "Peak season leave exceeds safe duration."
        }

    # High burnout override
    if row["Burnout_Probability"] > 0.75:
        return {
            "Decision": "Approve",
            "Reason": "High burnout risk. Health-first approval recommended."
        }

    return {
        "Decision": "Approve",
        "Reason": "No operational risk detected."
    }


def apply_leave_optimizer(df):
    dept_capacity = (
        df.groupby("Department")["Employee_ID"]
        .count()
        .to_dict()
    )

    results = df.apply(
        lambda r: optimize_leave_decision(r, dept_capacity),
        axis=1
    )

    df["Leave_Decision"] = results.apply(lambda x: x["Decision"])
    df["Decision_Reason"] = results.apply(lambda x: x["Reason"])

    return df
