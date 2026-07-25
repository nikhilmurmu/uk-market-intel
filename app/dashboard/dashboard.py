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
from ingestion.sectors import fetch_sector_performance

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

# ---- Load Data with error handling ----
@st.cache_data(ttl=1800)
def load_data():
    try:
        return run_all()
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(ttl=3600)
def load_sectors():
    try:
        return fetch_sector_performance()
    except Exception as e:
        return {}

data = load_data()
sectors = load_sectors()

if "error" in data:
    st.error(f"Could not load market data: {data['error']}")
    st.stop()

market = data.get("market_data", {})
econ = data.get("economic_indicators", {})

# ---- Sidebar ----
st.sidebar.title("📊 Market Intelligence")
st.sidebar.caption(f"Last update: {datetime.now().strftime('%H:%M')}")
refresh = st.sidebar.button("🔄 Refresh All Data")
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
    if banks and "error" not in banks[0]:
        st.metric(banks[0].get("symbol","N/A"), f"{banks[0].get('latest_close','N/A')}p", f"{banks[0].get('change_pct',0):+.2f}%")
with col4:
    if len(banks) > 1 and "error" not in banks[1]:
        st.metric(banks[1].get("symbol","N/A"), f"{banks[1].get('latest_close','N/A')}p", f"{banks[1].get('change_pct',0):+.2f}%")

# ---- Main Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["📈 Market Overview", "🏗️ Sector Analysis", "📝 AI Briefing", "📉 Economic Indicators"])

with tab1:
    st.subheader("FTSE 100 – 3‑Month Performance")
    try:
        import yfinance as yf
        ftse = yf.Ticker("^FTSE")
        hist = ftse.history(period="3mo")
        if not hist.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist.Close, name="FTSE 100"))
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Could not load historical data.")
    except Exception as e:
        st.warning(f"Historical chart unavailable: {e}")

    if banks:
        st.subheader("UK Bank Stocks – Daily Change")
        df_banks = pd.DataFrame([b for b in banks if "error" not in b])
        if not df_banks.empty:
            fig2 = px.bar(df_banks, x="symbol", y="change_pct", color="change_pct",
                          color_continuous_scale=["red", "green"])
            fig2.update_layout(template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("UK Sector Performance – Daily Change (%)")
    if sectors:
        df_sectors = pd.DataFrame(list(sectors.items()), columns=["Sector", "Change %"])
        df_sectors["Color"] = df_sectors["Change %"].apply(lambda x: "green" if x > 0 else "red")
        fig3 = px.bar(df_sectors, x="Sector", y="Change %", color="Change %",
                      color_continuous_scale=["red", "yellow", "green"])
        fig3.update_layout(template="plotly_dark")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Sector data unavailable. Try refreshing.")

with tab3:
    st.subheader("AI‑Generated Weekly Market Briefing")
    if "briefing" not in st.session_state:
        with st.spinner("Generating briefing..."):
            st.session_state.briefing = generate_market_briefing(data)
    st.write(st.session_state.briefing)

with tab4:
    if econ:
        cols = st.columns(3)
        for i, (key, val) in enumerate(econ.items()):
            if isinstance(val, dict) and "error" not in val:
                with cols[i % 3]:
                    st.metric(key.replace("_", " ").title(), val.get("latest_value", "N/A"))
    else:
        st.info("Economic indicators from ONS will appear here once data fetching is updated.")