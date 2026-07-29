from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parents[1]
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

import api
from utils import (
    configure_page,
    get_area_label,
    get_payment_label,
    get_provider_detail,
    get_provider_label,
    load_with_spinner,
    show_empty_message,
    style_chart,
    to_dataframe,
)

configure_page("Trip Details")

st.title("Trip Details")
st.caption("What do individual completed trip records show across fare, distance, and location attributes?")
st.markdown("<br>", unsafe_allow_html=True)

# Fetch limit records from backend API
trip_data = load_with_spinner("Loading trip records...", lambda: api.get_trips(limit=100))
vendor_data = load_with_spinner("Loading provider metrics...", api.get_trips_by_vendor)

trips_df = to_dataframe(trip_data)
vendor_df = to_dataframe(vendor_data)

# Interactive Filters
if not trips_df.empty:
    display_df = trips_df.copy()

    # Pre-populate readable columns for filtering
    if "pu_location_id" in display_df.columns:
        display_df["pickup_area"] = display_df["pu_location_id"].apply(get_area_label)
    if "do_location_id" in display_df.columns:
        display_df["dropoff_area"] = display_df["do_location_id"].apply(get_area_label)
    if "payment_type" in display_df.columns:
        display_df["payment_method"] = display_df["payment_type"].apply(get_payment_label)
    if "vendor_id" in display_df.columns:
        display_df["recording_provider"] = display_df["vendor_id"].apply(get_provider_label)

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        all_areas = sorted(display_df["pickup_area"].unique().tolist())
        selected_areas = st.multiselect("Filter by Pickup Area:", options=all_areas, default=[])

    with filter_col2:
        all_payments = sorted(display_df["payment_method"].unique().tolist())
        selected_payments = st.multiselect("Filter by Payment Method:", options=all_payments, default=[])

    with filter_col3:
        record_limit = st.slider("Select Display Limit:", min_value=10, max_value=100, value=25, step=5)

    # Apply interactive filters over sample dataset
    filtered_df = display_df.copy()
    if selected_areas:
        filtered_df = filtered_df[filtered_df["pickup_area"].isin(selected_areas)]
    if selected_payments:
        filtered_df = filtered_df[filtered_df["payment_method"].isin(selected_payments)]

    filtered_df = filtered_df.head(record_limit)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Trips Displayed", len(filtered_df))

    avg_fare = filtered_df["fare_amount"].astype(float).mean() if not filtered_df.empty and "fare_amount" in filtered_df.columns else 0.0
    avg_total = filtered_df["total_amount"].astype(float).mean() if not filtered_df.empty and "total_amount" in filtered_df.columns else 0.0
    avg_dist = filtered_df["trip_distance"].astype(float).mean() if not filtered_df.empty and "trip_distance" in filtered_df.columns else 0.0

    kpi2.metric("Avg Fare Amount", f"${avg_fare:,.2f}")
    kpi3.metric("Avg Trip Distance", f"{avg_dist:,.2f} mi")
    kpi4.metric(
        "Avg Total Amount",
        f"${avg_total:,.2f}",
        delta="includes tip & surcharges",
        delta_color="off",
    )
    st.caption("Note: Avg Fare Amount represents base meter fare, while Avg Total Amount includes tips, tolls, and surcharges.")

    st.markdown("<br>", unsafe_allow_html=True)

    if not show_empty_message(filtered_df):
        column_config = {
            "id": st.column_config.NumberColumn("Trip ID", format="%d"),
            "pickup_date": st.column_config.TextColumn("Pickup Date"),
            "pickup_hour": st.column_config.NumberColumn("Pickup Hour", format="%02d:00"),
            "pickup_area": st.column_config.TextColumn("Pickup Area"),
            "dropoff_area": st.column_config.TextColumn("Dropoff Area"),
            "payment_method": st.column_config.TextColumn("Payment Method"),
            "trip_distance": st.column_config.NumberColumn("Trip Distance", format="%.2f mi"),
            "fare_amount": st.column_config.NumberColumn("Fare Amount", format="$%.2f"),
            "tip_amount": st.column_config.NumberColumn("Tip Amount", format="$%.2f"),
            "total_amount": st.column_config.NumberColumn("Total Amount", format="$%.2f"),
        }

        preferred_columns = [
            "id",
            "pickup_date",
            "pickup_hour",
            "pickup_area",
            "dropoff_area",
            "payment_method",
            "trip_distance",
            "fare_amount",
            "tip_amount",
            "total_amount",
        ]
        existing_cols = [c for c in preferred_columns if c in filtered_df.columns]

        st.dataframe(
            filtered_df[existing_cols],
            column_config=column_config,
            use_container_width=True,
            hide_index=True,
            height=440,
        )

st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1.5rem; opacity: 0.2;'>", unsafe_allow_html=True)

# Visually de-emphasized Data Source Breakdown Section for TPEP Technology Vendors
with st.expander("📊 Data Source Breakdown (Data Recording Technology Providers)", expanded=False):
    st.caption(
        "Note: This field identifies the TPEP technology hardware/software vendor that recorded the trip data, not the fleet operator or driver."
    )
    if not show_empty_message(vendor_df):
        vendor_df_styled = vendor_df.assign(
            Provider=vendor_df["vendor_id"].apply(get_provider_label),
            Details=vendor_df["vendor_id"].apply(get_provider_detail),
        )
        fig_vendor = px.bar(
            vendor_df_styled,
            x="Provider",
            y="trip_count",
            hover_data={"Provider": False, "Details": True, "trip_count": ":,"},
            labels={"Provider": "Recording Technology Provider", "trip_count": "Trip Records", "Details": "Vendor Info"},
            color="Provider",
            color_discrete_sequence=["#64748b", "#94a3b8", "#cbd5e1"],
        )
        st.plotly_chart(style_chart(fig_vendor, height=280), use_container_width=True)
