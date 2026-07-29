from pathlib import Path
import sys

import streamlit as st

DASHBOARD_DIR = Path(__file__).resolve().parent
if str(DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(DASHBOARD_DIR))

pages = [
    st.Page("pages/1_Overview.py", title="Overview", default=True),
    st.Page("pages/2_Demand_Analytics.py", title="Demand Analytics"),
    st.Page("pages/3_Location_Analytics.py", title="Location Analytics"),
    st.Page("pages/4_Trip_Details.py", title="Trip Details"),
]

pg = st.navigation(pages)
pg.run()
