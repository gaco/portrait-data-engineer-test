import os
import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine

# --- APP SETUP ---
st.set_page_config(page_title="Healthcare Dashboard", layout="wide")

# --- DB CONNECTION ---
@st.cache_resource
def get_connection():
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "postgres")
    host = os.environ.get("DB_HOST", "localhost")
    db = os.environ.get("DB_NAME", "healthcare")
    db_url = f"postgresql://{user}:{password}@{host}:5432/{db}"
    return create_engine(db_url)

engine = get_connection()

# --- NAVIGATION ---
st.sidebar.title("🗂️ Navigation")
section = st.sidebar.radio("Go to section", [
    "Patient Analysis", "Appointment Analysis", "Prescription Analysis", "Conclusions"
])

# --- HELPER ---
@st.cache_data(ttl=600)
def load_data(query):
    return pd.read_sql_query(query, engine)


if section == "Patient Analysis":
    st.title("📊 Healthcare Analytics Dashboard")
    st.header("Patient Analysis")
    # 1. Patient Distribution by Age Group
    st.subheader("1. Patient distribution across age groups")
    df_patients = load_data("SELECT * FROM analytics_marts.patient_distribution_by_age_group")
    chart1 = alt.Chart(df_patients).mark_bar(color='green').encode(
        x=alt.X("age_group", sort=None, title="Age Group", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("num_patients", title="Number of Patients")
    ).properties(width=600)
    text1 = chart1.mark_text(dy=-10, color='black').encode(text='num_patients')
    st.altair_chart(chart1 + text1, use_container_width=True)

    # 2. Appointment Frequency by Patient Type (as Pie Chart)
    st.subheader("2. Appointment frequency by patient types")
    df_appt_freq = load_data("SELECT * FROM analytics_marts.appointment_frequency_by_patient_type")

    df_appt_freq['percentage'] = (df_appt_freq['total_appointments'] /
                                  df_appt_freq['total_appointments'].sum()
                                  )
    chart2 = alt.Chart(df_appt_freq).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="total_appointments", type="quantitative"),
        color=alt.Color(field="patient_type", type="nominal", title="Patient Type"),
        tooltip=["patient_type", "total_appointments", alt.Tooltip("percentage:Q", format=".1%")]
    )
    # text2 = alt.Chart(df_appt_freq).mark_text(radius=120, size=12).encode(
    #     theta=alt.Theta("total_appointments", type="quantitative"),
    #     text=alt.Text("percentage:Q", format=".1%")
    # )
    st.altair_chart(chart2, use_container_width=True)

    # Appointment Breakdown
    st.markdown("**Appointment Breakdown:**")
    st.dataframe(
        df_appt_freq[["patient_type", "total_appointments"]]
        .assign(percentage=(df_appt_freq["percentage"] * 100).round(1).astype(str) + "%")
        .rename(columns={"patient_type": "Type", "total_appointments": "Total", "percentage": "%"})
        .sort_values("Total", ascending=False),
        hide_index=True,
        use_container_width=True
    )

elif section == "Appointment Analysis":
    st.title("📊 Healthcare Analytics Dashboard")
    st.header("Appointment Analysis")
    # 1. Appointment Types by Age Group
    st.subheader("1. Appointment types across age groups")
    df_appt_type = load_data("SELECT * FROM analytics_marts.appointment_distribution_by_age_group")
    chart3 = alt.Chart(df_appt_type).mark_bar().encode(
        x=alt.X("age_group:N", title="Age Group", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("total:Q", title="Total Appointments"),
        color=alt.Color("appointment_type:N", title="Appointment Type"),
        tooltip=["age_group", "appointment_type", "total"]
    ).properties(width=700)
    st.altair_chart(chart3, use_container_width=True)

    # Appointment Breakdown
    st.markdown("**Appointment types breakdown**")
    df_appt_pivot = df_appt_type.pivot_table(index="age_group", columns="appointment_type", values="total",
                                             aggfunc="sum", fill_value=0)
    df_appt_pivot["Total"] = df_appt_pivot.sum(axis=1)
    df_appt_pivot = df_appt_pivot.reset_index().sort_values("Total", ascending=False)
    st.dataframe(df_appt_pivot, use_container_width=True)

    # 2. Emergency Visits by Day
    st.subheader("2. Emergency visits by week days")
    df_emerg = load_data("SELECT * FROM analytics_marts.emergency_visits_by_day")
    chart4 = alt.Chart(df_emerg).mark_bar(color="#E15759").encode(
        x=alt.X("day_of_week", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                title="Day of Week", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("emergency_visits", title="Emergency Visits")
    ).properties(width=600)
    text4 = chart4.mark_text(dy=-10, color='black').encode(text='emergency_visits')
    st.altair_chart(chart4 + text4, use_container_width=True)

elif section == "Prescription Analysis":
    st.title("📊 Healthcare Analytics Dashboard")
    st.header("Prescription Analysis")

    # 1. Medication Categories by Age Group
    st.subheader("1. Medication categories across age groups")
    df_rx_age = load_data("SELECT * FROM analytics_marts.prescription_distribution_by_age_group")
    chart5 = alt.Chart(df_rx_age).mark_bar().encode(
        x=alt.X("age_group", sort=None, title="Age Group", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("total", title="Total Prescriptions"),
        color=alt.Color("category", title="Category")
    ).properties(width=700)
    st.altair_chart(chart5, use_container_width=True)

    # Medication Breakdown
    st.markdown("**Medication Category Breakdown**")
    df_rx_pivot = df_rx_age.pivot_table(index="age_group", columns="category", values="total", aggfunc="sum",
                                        fill_value=0)
    df_rx_pivot["Total"] = df_rx_pivot.sum(axis=1)
    df_rx_pivot = df_rx_pivot.reset_index().sort_values("Total", ascending=False)

    # Add total row
    totals_row = df_rx_pivot.drop(columns="age_group").sum(numeric_only=True)
    totals_row["age_group"] = "Total"
    df_rx_pivot_total = pd.concat([df_rx_pivot, pd.DataFrame([totals_row])], ignore_index=True)

    st.dataframe(df_rx_pivot_total, use_container_width=True)

    # 2. Prescription Frequency vs Average Appointments
    st.subheader("2. Correlation between prescription frequency and appointment frequency")

    df_rx_corr = load_data("SELECT * FROM analytics_marts.prescription_appointment_correlation")

    # Melt into long format
    df_corr_melted = df_rx_corr.melt(
        id_vars=["prescription_frequency_bucket"],
        value_vars=["avg_appointments", "avg_prescriptions"],
        var_name="Metric",
        value_name="Value"
    )

    df_corr_melted["Metric"] = df_corr_melted["Metric"].replace({
        "avg_appointments": "Avg Appointments",
        "avg_prescriptions": "Avg Prescriptions"
    })

    # Base chart with grouped bars
    bar = alt.Chart(df_corr_melted).mark_bar(width=30).encode(
        x=alt.X("prescription_frequency_bucket:N", title="Prescription Frequency Bucket",
                axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("Value:Q", title="Average Count"),
        color=alt.Color("Metric:N", title="Metric"),
        xOffset=alt.XOffset("Metric:N"),
        tooltip=[
            alt.Tooltip("prescription_frequency_bucket", title="Bucket"),
            alt.Tooltip("Metric", title="Metric"),
            alt.Tooltip("Value", title="Avg", format=".2f")
        ]
    )

    # Add value labels
    text = alt.Chart(df_corr_melted).mark_text(
        dy=-10,
        color='black',
        fontSize=11
    ).encode(
        x=alt.X("prescription_frequency_bucket:N"),
        xOffset=alt.XOffset("Metric:N"),
        y=alt.Y("Value:Q"),
        text=alt.Text("Value:Q", format=".2f")
    )

    # Display combined chart
    st.altair_chart(bar + text, use_container_width=True)

    # 3. Prescription Frequency Trend Over Time
    st.subheader("3. Trend of prescription frequency over time")

    # Load updated result with year and month
    df_rx_trend = load_data("SELECT * FROM analytics_marts.prescription_frequency_trend")

    # Ensure year/month are integers before datetime conversion
    df_rx_trend["year"] = df_rx_trend["year"].astype(int)
    df_rx_trend["month"] = df_rx_trend["month"].astype(int)

    # Create a datetime column
    df_rx_trend["date"] = pd.to_datetime({
        "year": df_rx_trend["year"],
        "month": df_rx_trend["month"],
        "day": 1
    })

    # Main chart
    chart7 = alt.Chart(df_rx_trend).mark_line(point=True).encode(
        x=alt.X("date:T", title="Month", axis=alt.Axis(format="%b %Y", labelAngle=-45)),
        y=alt.Y("total:Q", title="Total Prescriptions"),
        color=alt.Color("prescription_frequency:N", title="Prescription Frequency"),
        tooltip=["year", "month", "prescription_frequency", "total"]
    ).properties(width=800, height=400)

    # Labels
    text7 = alt.Chart(df_rx_trend).mark_text(
        align="left", baseline="middle", dx=5, dy=-10, fontSize=12
    ).encode(
        x="date:T",
        y="total:Q",
        detail="prescription_frequency:N",
        text=alt.Text("total:Q", format=".0f")
    )

    st.altair_chart(chart7 + text7, use_container_width=True)

elif section == "Conclusions":
    st.title("📊 Healthcare Analytics Dashboard")
    st.header("Conclusions")
    st.markdown("""
    - **Patients 51–70 and 71+** have the highest appointment counts, particularly for checkups.
    - **Emergency appointments** has a spike on Friday.
    - **Pain medications** are the most prescribed medications, especially in older age groups.
    - **No linear correlation between prescription frequency and appointments**. Further investigation is suggested, as patients with "Few" and "Moderate" prescriptions had higher appointment averages.
    - **First-time prescriptions** declined sharply over time, while **repeat prescriptions** grew, indicating ongoing care.
    """)