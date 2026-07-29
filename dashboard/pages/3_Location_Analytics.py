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
    get_area_detail,
    get_area_label,
    load_with_spinner,
    show_empty_message,
    style_chart,
    sum_column,
    to_dataframe,
)

configure_page("Location Analytics")

st.title("Location Analytics")
st.caption("Where are the busiest pickup and dropoff areas in New York City?")
st.markdown("<br>", unsafe_allow_html=True)

pickup_data = load_with_spinner("Loading pickup hotspots...", api.get_top_pickup_locations)
dropoff_data = load_with_spinner("Loading dropoff hotspots...", api.get_top_dropoff_locations)

pickup_df = to_dataframe(pickup_data)
dropoff_df = to_dataframe(dropoff_data)

total_pickups = sum_column(pickup_df, "trip_count")
total_dropoffs = sum_column(dropoff_df, "trip_count")

top_pu_label = "N/A"
top_pu_count = 0
top_pu_pct = 0.0
if not pickup_df.empty and total_pickups > 0:
    top_pu = pickup_df.iloc[0]
    top_pu_label = get_area_label(top_pu["pu_location_id"])
    top_pu_count = int(top_pu["trip_count"])
    top_pu_pct = (top_pu_count / total_pickups) * 100

top_do_label = "N/A"
top_do_count = 0
top_do_pct = 0.0
if not dropoff_df.empty and total_dropoffs > 0:
    top_do = dropoff_df.iloc[0]
    top_do_label = get_area_label(top_do["do_location_id"])
    top_do_count = int(top_do["trip_count"])
    top_do_pct = (top_do_count / total_dropoffs) * 100

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Top Pickup Area", top_pu_label)
kpi2.metric("Top Pickup Volume", f"{top_pu_count:,}", delta=f"{top_pu_pct:.1f}% of total" if top_pu_pct > 0 else None, delta_color="off")
kpi3.metric("Top Dropoff Area", top_do_label)
kpi4.metric("Dropoff Volume", f"{top_do_count:,}", delta=f"{top_do_pct:.1f}% of total" if top_do_pct > 0 else None, delta_color="off")

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Busiest Pickup Areas")
    if not show_empty_message(pickup_df):
        pickup_df_styled = pickup_df.assign(
            Area=pickup_df["pu_location_id"].apply(get_area_label),
            Details=pickup_df["pu_location_id"].apply(get_area_detail),
            pct=(pickup_df["trip_count"] / total_pickups * 100).round(1),
        ).sort_values("trip_count", ascending=True)

        pickup_df_styled["label_display"] = pickup_df_styled.apply(
            lambda r: f"{r['trip_count']:,} ({r['pct']:.1f}%)", axis=1
        )

        fig_pu = px.bar(
            pickup_df_styled,
            x="trip_count",
            y="Area",
            orientation="h",
            text="label_display",
            hover_data={"Area": True, "Details": False, "trip_count": ":,", "pct": ":.1f%"},
            labels={"trip_count": "Pickups", "Area": "Pickup Area", "pct": "% of Total Trips"},
            color_discrete_sequence=[PRIMARY_COLOR],
        )
        fig_pu.update_traces(textposition="outside")
        st.plotly_chart(style_chart(fig_pu, height=380), use_container_width=True)

with right_col:
    st.subheader("Busiest Dropoff Areas")
    if not show_empty_message(dropoff_df):
        dropoff_df_styled = dropoff_df.assign(
            Area=dropoff_df["do_location_id"].apply(get_area_label),
            Details=dropoff_df["do_location_id"].apply(get_area_detail),
            pct=(dropoff_df["trip_count"] / total_dropoffs * 100).round(1),
        ).sort_values("trip_count", ascending=True)

        dropoff_df_styled["label_display"] = dropoff_df_styled.apply(
            lambda r: f"{r['trip_count']:,} ({r['pct']:.1f}%)", axis=1
        )

        fig_do = px.bar(
            dropoff_df_styled,
            x="trip_count",
            y="Area",
            orientation="h",
            text="label_display",
            hover_data={"Area": True, "Details": False, "trip_count": ":,", "pct": ":.1f%"},
            labels={"trip_count": "Dropoffs", "Area": "Dropoff Area", "pct": "% of Total Trips"},
            color_discrete_sequence=[SECONDARY_COLOR],
        )
        fig_do.update_traces(textposition="outside")
        st.plotly_chart(style_chart(fig_do, height=380), use_container_width=True)

if top_pu_count > 0:
    st.markdown(
        f"""
        <div class="insight-box">
            <b>Geographic Finding:</b> <b>{top_pu_label}</b> represents {top_pu_pct:.1f}% of overall pickup activity — reflecting heavy demand concentration in core commercial and residential transit hubs.
        </div>
        """,
        unsafe_allow_html=True,
    )
