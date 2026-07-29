from pathlib import Path
import sys

import plotly.express as px
import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parents[1]
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import api
from utils import (
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    configure_page,
    load_with_spinner,
    show_empty_message,
    style_chart,
    sum_column,
    to_dataframe,
)

configure_page("Demand Analytics")

st.title("Demand Analytics")
st.caption("When does taxi demand peak throughout the day and across operating dates?")
st.markdown("<br>", unsafe_allow_html=True)

daily_data = load_with_spinner("Loading daily metrics...", api.get_trips_per_day)
hourly_data = load_with_spinner("Loading hourly demand...", api.get_hourly_demand)

daily_df = to_dataframe(daily_data)
hourly_df = to_dataframe(hourly_data)

total_trips = sum_column(daily_df, "trip_count")
active_days = len(daily_df)
avg_daily_trips = (total_trips / active_days) if active_days > 0 else 0

peak_hour_str = "N/A"
peak_hour_trips = 0
if not hourly_df.empty:
    peak_row = hourly_df.sort_values("trip_count", ascending=False).iloc[0]
    peak_hour_str = f"{int(peak_row['pickup_hour']):02d}:00"
    peak_hour_trips = int(peak_row["trip_count"])

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Trip Volume", f"{total_trips:,}")
kpi2.metric("Average Daily Trips", f"{int(avg_daily_trips):,}")
kpi3.metric(
    "Peak Demand Hour",
    peak_hour_str,
    delta=f"{peak_hour_trips:,} trips at peak" if peak_hour_trips > 0 else None,
    delta_color="off",
)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Hourly Demand Curve (24-Hour Cycle)")
if not show_empty_message(hourly_df):
    hourly_df_styled = hourly_df.assign(
        Hour=hourly_df["pickup_hour"].apply(lambda h: f"{int(h):02d}:00"),
        pickup_hour_num=hourly_df["pickup_hour"].astype(int),
    ).sort_values("pickup_hour_num")

    fig_hourly = px.area(
        hourly_df_styled,
        x="Hour",
        y="trip_count",
        markers=True,
        labels={"Hour": "Hour of Day (00:00 - 23:00)", "trip_count": "Trip Volume"},
        color_discrete_sequence=[SECONDARY_COLOR],
    )
    fig_hourly.update_traces(fillcolor="rgba(16, 185, 129, 0.15)")
    st.plotly_chart(style_chart(fig_hourly, height=360), use_container_width=True)

st.subheader("Daily Trip Volume Comparison")
if not show_empty_message(daily_df):
    fig_daily = px.bar(
        daily_df,
        x="pickup_date",
        y="trip_count",
        labels={"pickup_date": "Date", "trip_count": "Trip Volume"},
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    st.plotly_chart(style_chart(fig_daily, height=350), use_container_width=True)

if peak_hour_trips > 0:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Demand Finding:</b> Demand increases during late-night hours, peaking at <b>{peak_hour_str}</b> with {peak_hour_trips:,} trips — indicating stronger taxi usage during nighttime travel periods.
        </div>
        """,
        unsafe_allow_html=True,
    )
