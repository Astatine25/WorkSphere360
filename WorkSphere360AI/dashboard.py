import streamlit as st
import pandas as pd

st.set_page_config(page_title="WorkSphere360 – HR AI Dashboard", layout="wide")

df = pd.read_csv("final_ai_output.csv")

st.title("🏢 WorkSphere360 – AI Workforce Intelligence")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Employees at High Burnout Risk", (df["Burnout_Probability"] > 0.8).sum())
col2.metric("Avg Productivity", round(df["Average_Productivity_Score"].mean(), 2))
col3.metric("Teams Below Capacity", (df["Capacity_Zone"] == "RED").sum())

# Department Heatmap
st.subheader("🔥 Department Risk Heatmap")
st.dataframe(
    df.groupby("Department")["Burnout_Probability"].mean().sort_values(ascending=False)
)

# AI Recommendations
st.subheader("🤖 AI Prescriptive Actions")
st.dataframe(
    df[["Employee_ID", "Department", "Burnout_Probability", "AI_Recommendation"]]
)
