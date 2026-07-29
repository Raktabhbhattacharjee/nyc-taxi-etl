from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

import pandas as pd
import streamlit as st

try:
    from .api import APIError
except ImportError:
    from api import APIError


T = TypeVar("T")

PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#10b981"
ACCENT_COLOR = "#f59e0b"
CHART_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#6366f1"]

VENDOR_MAP = {
    1: "Creative Mobile Technologies",
    2: "VeriFone Inc.",
    6: "Digital Dispatch",
}

PAYMENT_TYPE_MAP = {
    1: "Credit Card",
    2: "Cash",
    3: "No Charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided Trip",
}

LOCATION_LOOKUP = {
    132: "JFK Airport",
    138: "LaGuardia Airport",
    161: "Midtown Center",
    162: "Midtown East",
    163: "Midtown North",
    230: "Times Sq / Theatre Dist",
    236: "Upper East Side North",
    237: "Upper East Side South",
    238: "Upper West Side North",
    239: "Upper West Side South",
    249: "West Village",
    79: "East Village",
    48: "Clinton East",
    142: "Lincoln Square East",
    186: "Penn Station / Madison Sq",
    170: "Murray Hill",
    107: "Gramercy",
    141: "Lenox Hill West",
    140: "Lenox Hill East",
    234: "Union Square",
    90: "Flatiron",
    68: "East Chelsea",
    231: "TriBeCa / Civic Center",
    13: "Battery Park City",
    114: "Greenwich Village South",
    113: "Greenwich Village North",
}


def get_provider_label(vendor_id: object) -> str:
    """Return clean business label for technology provider."""
    try:
        vid = int(vendor_id)
        name = VENDOR_MAP.get(vid, f"Vendor {vid}")
        return f"Technology Provider {vid} ({name})" if name else f"Technology Provider {vid}"
    except (ValueError, TypeError):
        return str(vendor_id)


def get_provider_detail(vendor_id: object) -> str:
    """Return detail for hover tooltips."""
    try:
        vid = int(vendor_id)
        name = VENDOR_MAP.get(vid, "")
        return f"TPEP Recording Source {vid}: {name}" if name else f"Source {vid}"
    except (ValueError, TypeError):
        return str(vendor_id)


def get_payment_label(payment_code: object) -> str:
    """Return clean business label for payment method."""
    try:
        code = int(payment_code)
        return PAYMENT_TYPE_MAP.get(code, f"Payment Method {code}")
    except (ValueError, TypeError):
        return str(payment_code)


def get_area_label(location_id: object) -> str:
    """Return clean business area name."""
    try:
        lid = int(location_id)
        return LOCATION_LOOKUP.get(lid, f"Zone {lid}")
    except (ValueError, TypeError):
        return str(location_id)


def get_area_detail(location_id: object) -> str:
    """Return area details for hover tooltips."""
    try:
        lid = int(location_id)
        area = LOCATION_LOOKUP.get(lid, "")
        return f"{area} (Location Zone {lid})" if area else f"Location Zone {lid}"
    except (ValueError, TypeError):
        return str(location_id)


def configure_page(title: str) -> None:
    """Apply shared Streamlit page settings, branding header, and custom CSS styling."""
    st.set_page_config(
        page_title=f"{title} | Public Taxi Trip Data Platform",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Branded Header in Sidebar
    st.sidebar.markdown(
        """
        <div style="padding-bottom: 12px; margin-bottom: 16px; border-bottom: 1px solid rgba(128,128,128,0.2);">
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #2563eb;">Public Taxi Trip Data Platform</h3>
            <p style="margin: 4px 0 8px 0; font-size: 0.8rem; opacity: 0.8; line-height: 1.3;">
                Analytics platform for exploring taxi mobility patterns and operational insights.
            </p>
            <span style="font-size: 0.73rem; background-color: rgba(37, 99, 235, 0.1); color: #2563eb; padding: 3px 7px; border-radius: 4px; font-weight: 600;">
                Dataset: NYC TLC Yellow Taxi — January 2026
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Global CSS for consistent KPI Cards & Layouts across all 4 pages
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 95%;
        }

        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(128, 128, 128, 0.18);
            border-radius: 8px;
            padding: 12px 18px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        div[data-testid="stMetric"]:hover {
            border-color: #2563eb;
            transform: translateY(-1px);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.85;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.65rem !important;
            font-weight: 700 !important;
            color: #2563eb;
        }

        .insight-box {
            background-color: rgba(37, 99, 235, 0.07);
            border-left: 4px solid #2563eb;
            padding: 10px 14px;
            border-radius: 0 6px 6px 0;
            font-size: 0.88rem;
            margin-top: 10px;
            margin-bottom: 10px;
            color: inherit;
        }

        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_chart(fig, height: int = 360):
    """Apply consistent, professional Plotly chart styling across all pages."""
    fig.update_layout(
        height=height,
        margin={"l": 10, "r": 10, "t": 15, "b": 10},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif", "size": 12},
        hoverlabel={"namelength": -1},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(128,128,128,0.12)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.12)")
    return fig


def load_with_spinner(label: str, loader: Callable[[], T]) -> T | None:
    """Run a loader with a spinner and clean error handling without technical jargon."""
    try:
        with st.spinner(label):
            return loader()
    except APIError:
        st.error("Data service is currently unavailable. Please verify the service is running.")
        return None


def to_dataframe(records: list[dict[str, object]] | None) -> pd.DataFrame:
    """Convert records to a DataFrame."""
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def show_empty_message(df: pd.DataFrame, message: str = "No analytics data available.") -> bool:
    """Show an empty-state message and return True when dataframe is empty."""
    if df.empty:
        st.info(message)
        return True
    return False


def sum_column(df: pd.DataFrame, column: str) -> int:
    """Return a safe integer total for a dataframe column."""
    if df.empty or column not in df.columns:
        return 0
    return int(df[column].sum())
