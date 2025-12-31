# dashboard.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="WorkSphere360 | HR AI Dashboard", layout="wide")

st.title(" WorkSphere360 – AI Workforce Intelligence")

# Load data
df = pd.read_csv("final_ai_output.csv")

# -------------------------------
# KPI ROW
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Avg Burnout Risk",
    round(df["Burnout_Probability"].mean(), 2)
)

col2.metric(
    "Avg Productivity",
    round(df["Avg_Productivity"].mean(), 2)
)

col3.metric(
    "Avg Overtime (hrs)",
    round(df["Overtime_Hours"].mean(), 2)
)

col4.metric(
    "High Risk Employees",
    int((df["Risk_Level"] == "High").sum())
)

st.divider()

# -------------------------------
# Risk Distribution
# -------------------------------
st.subheader("Burnout Risk Distribution")
st.bar_chart(df["Risk_Level"].value_counts())

# -------------------------------
# Department Risk Heatmap
# -------------------------------
st.subheader("Department Burnout Risk")

dept_risk = (
    df.groupby("Dept_ID")["Burnout_Probability"]
    .mean()
    .reset_index()
)

st.dataframe(dept_risk)

# -------------------------------
# Employee-Level Table
# -------------------------------
st.subheader("Employee Risk Detail")

st.dataframe(
    df[
        [
            "Employee_ID",
            "Dept_ID",
            "Tenure_Yrs",
            "Avg_Productivity",
            "Overtime_Hours",
            "Burnout_Probability",
            "Risk_Level"
        ]
    ]
)
