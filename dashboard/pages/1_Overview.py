from pathlib import Path
import sys

import plotly.express as px
import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parents[1]
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import api
from utils import (
    CHART_COLORS,
    PRIMARY_COLOR,
    configure_page,
    get_payment_label,
    load_with_spinner,
    show_empty_message,
    style_chart,
    sum_column,
    to_dataframe,
)

configure_page("Overview")

st.title("Overview")
st.caption("How much taxi activity happened?")
st.markdown("<br>", unsafe_allow_html=True)

daily_data = load_with_spinner("Loading daily metrics...", api.get_trips_per_day)
payment_data = load_with_spinner("Loading payment metrics...", api.get_trips_by_payment_type)

daily_df = to_dataframe(daily_data)
payment_df = to_dataframe(payment_data)

total_trips = sum_column(daily_df, "trip_count")
total_payment_trips = sum_column(payment_df, "trip_count")
active_days = len(daily_df)
avg_daily_trips = (total_trips / active_days) if active_days > 0 else 0

date_range_str = "N/A"
peak_date_str = "N/A"
if not daily_df.empty:
    min_date = daily_df["pickup_date"].min()
    max_date = daily_df["pickup_date"].max()
    date_range_str = f"{min_date} to {max_date}"
    peak_row = daily_df.sort_values("trip_count", ascending=False).iloc[0]
    peak_date_str = str(peak_row["pickup_date"])

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Trips", f"{total_trips:,}")
kpi2.metric("Average Daily Trips", f"{int(avg_daily_trips):,}")
kpi3.metric("Date Range Covered", date_range_str)

st.markdown("<br>", unsafe_allow_html=True)

# Month-at-a-glance narrative sentence
if total_trips > 0:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Month at a Glance:</b> In January 2026, the platform recorded <b>{total_trips:,} total trips</b> across {active_days} operating days, averaging <b>{int(avg_daily_trips):,} trips per day</b> with peak daily activity on {peak_date_str}.
        </div>
        """,
        unsafe_allow_html=True,
    )

left_col, right_col = st.columns([1.4, 1])

with left_col:
    st.subheader("Daily Trip Volume")
    if not show_empty_message(daily_df):
        fig_daily = px.bar(
            daily_df,
            x="pickup_date",
            y="trip_count",
            labels={"pickup_date": "Date", "trip_count": "Trip Volume"},
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        st.plotly_chart(style_chart(fig_daily, height=360), use_container_width=True)

with right_col:
    st.subheader("Payment Method Distribution")
    if not show_empty_message(payment_df):
        payment_df_styled = payment_df.assign(
            Payment=payment_df["payment_type"].apply(get_payment_label)
        )
        fig_payment = px.pie(
            payment_df_styled,
            names="Payment",
            values="trip_count",
            hole=0.4,
            color_discrete_sequence=CHART_COLORS,
        )
        fig_payment.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(style_chart(fig_payment, height=360), use_container_width=True)
