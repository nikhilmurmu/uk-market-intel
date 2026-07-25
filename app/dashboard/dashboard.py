import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys
from datetime import datetime

sys.path.insert(0, "app")
from ingestion.scheduler import run_all
from reports.generator import generate_market_briefing

# ---- Custom Dark Theme ----
st.set_page_config(page_title="UK Market Intelligence", layout="wide")
st.markdown("""
<style>
    .reportview-container {background: #0e1117}
    .sidebar .sidebar-content {background: #262730}
    .stMetric {background: #1f2937; border-radius: 10px; padding: 15px; color: white}
    .stPlotlyChart {border-radius: 10px; overflow: hidden}
</style>
""", unsafe_allow_html=True)

# ---- Load Data (cached to avoid repeated API calls) ----
@st.cache_data(ttl=3600)
def load_data():
    return run_all()

data = load_data()
market = data.get("market_data", {})
econ = data.get("economic_indicators", {})

# ---- Sidebar ----
st.sidebar.title("📊 Market Intelligence")
st.sidebar.caption("Last update: " + datetime.now().strftime("%H:%M"))
refresh = st.sidebar.button("🔄 Refresh Data")
if refresh:
    st.cache_data.clear()
    st.rerun()

# ---- KPI Row ----
ftse100 = market.get("ftse100", {})
ftse250 = market.get("ftse250", {})
banks = market.get("banks", [])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("FTSE 100", f"{ftse100.get('latest_close', 0):,.1f}", f"{ftse100.get('change_pct', 0):+.2f}%")
with col2:
    st.metric("FTSE 250", f"{ftse250.get('latest_close', 0):,.1f}", f"{ftse250.get('change_pct', 0):+.2f}%")
with col3:
    if banks:
        st.metric(banks[0]["symbol"], f"{banks[0]['latest_close']}p", f"{banks[0]['change_pct']:+.2f}%")
with col4:
    if len(banks) > 1:
        st.metric(banks[1]["symbol"], f"{banks[1]['latest_close']}p", f"{banks[1]['change_pct']:+.2f}%")

# ---- Main Tabs ----
tab1, tab2, tab3 = st.tabs(["📈 Market Overview", "📝 AI Briefing", "📉 Economic Indicators"])

with tab1:
    st.subheader("FTSE Indices – Historical Performance")
    # Download historical data for a simple line chart
    ftse100_hist = yf.Ticker("^FTSE").history(period="3mo")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ftse100_hist.index, y=ftse100_hist.Close, name="FTSE 100"))
    st.plotly_chart(fig, use_container_width=True)

    if banks:
        st.subheader("UK Bank Stocks – Daily Change")
        df_banks = pd.DataFrame(banks)
        fig2 = px.bar(df_banks, x="symbol", y="change_pct", color="change_pct",
                      color_continuous_scale=["red", "green"])
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("AI‑Generated Weekly Market Briefing")
    if "briefing" not in st.session_state:
        st.session_state.briefing = generate_market_briefing(data)
    st.write(st.session_state.briefing)

with tab3:
    if econ:
        for key, val in econ.items():
            if isinstance(val, dict) and "error" not in val:
                st.metric(key.replace("_", " ").title(), val.get("latest_value", "N/A"))