import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="WorkSphere360 – AI Leave Intelligence",
    layout="wide"
)

st.title(" WorkSphere360 – AI Leave Management Dashboard")

# ======================================================
# Load Data
# ======================================================
@st.cache_data
def load_data():
    return (
        pd.read_csv("final_ai_output.csv"),
        pd.read_csv("hr_executive_summaries.csv")
    )

df, summaries = load_data()

# ======================================================
# KPI Metrics
# ======================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Employees", len(df))
col2.metric("Avg Productivity", round(df["Productivity_Score"].mean(), 2))
col3.metric("High Burnout %", round((df["Burnout_Score"] > 0.75).mean() * 100, 2))
col4.metric("Peak Season %", round(df["Is_Peak_Season"].mean() * 100, 2))

st.divider()

# ======================================================
# Department Alerts
# ======================================================
st.subheader(" Departmental Risk Alerts")

for dept, g in df.groupby("Department"):
    risk = (g["Burnout_Score"] > 0.75).mean()
    if risk > 0.3:
        st.error(f"{dept}: High burnout risk ({round(risk*100,1)}%)")
    else:
        st.success(f"{dept}: Capacity stable")

st.divider()

# ======================================================
# Employee-Level AI Decisions
# ======================================================
st.subheader("👤 Employee AI Leave Decisions")

st.dataframe(
    df[[
        "Employee_ID",
        "Employee_Name",
        "Department",
        "Burnout_Score",
        "Approval_Decision",
        "AI_Recommendation",
        "Suggested_Alternate_Dates"
    ]].sort_values("Burnout_Score", ascending=False),
    use_container_width=True
)

st.divider()

# ======================================================
# Burnout Visualization
# ======================================================
st.subheader(" Burnout Risk by Department")
st.bar_chart(df.groupby("Department")["Burnout_Score"].mean())

st.divider()

# ======================================================
# HR Executive Summaries (LLM Output)
# ======================================================
st.subheader(" AI-Generated HR Executive Summaries")

for _, row in summaries.iterrows():
    with st.expander(f" {row['Department']}"):
        st.write(row["HR_Summary"])

st.divider()

# ======================================================
# Email Alert Preview
# ======================================================
st.subheader(" Auto-Email Alert Preview")

critical = df[df["Burnout_Score"] > 0.85]
if not critical.empty:
    st.warning(f"{len(critical)} employees require immediate HR outreach.")
else:
    st.success("No critical alerts detected today.")
