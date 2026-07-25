import streamlit as st
import plotly.express as px
import pandas as pd
import sys

sys.path.insert(0, "app")
from ingestion.scheduler import run_all
from reports.generator import generate_market_briefing

st.set_page_config(page_title="UK Market Intelligence", layout="wide")
st.title("🇬🇧 UK Market Intelligence Platform")

# Sidebar refresh button
st.sidebar.header("📊 Data Controls")
if st.sidebar.button("Refresh All Data"):
    st.session_state.data = run_all()
    st.session_state.briefing = generate_market_briefing(st.session_state.data)
    st.sidebar.success("Data refreshed!")

# Load initial data if not present
if "data" not in st.session_state:
    st.session_state.data = run_all()
    st.session_state.briefing = generate_market_briefing(st.session_state.data)

data = st.session_state.data
market = data.get("market_data", {})
ftse100 = market.get("ftse100", {})
ftse250 = market.get("ftse250", {})
banks = market.get("banks", [])

# ---- KPI Row ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("FTSE 100", f"{ftse100.get('latest_close', 0):,.1f}", f"{ftse100.get('change_pct', 0):+.2f}%")
col2.metric("FTSE 250", f"{ftse250.get('latest_close', 0):,.1f}", f"{ftse250.get('change_pct', 0):+.2f}%")
if banks:
    col3.metric(banks[0]["symbol"], f"{banks[0]['latest_close']}p", f"{banks[0]['change_pct']:+.2f}%")
    col4.metric(banks[1]["symbol"] if len(banks)>1 else "N/A", 
                f"{banks[1]['latest_close']}p" if len(banks)>1 else "N/A",
                f"{banks[1]['change_pct']:+.2f}%" if len(banks)>1 else "")

# ---- Market Briefing ----
st.subheader("📝 AI-Generated Weekly Market Briefing")
st.write(st.session_state.briefing)

# ---- Bank Stock Chart ----
if banks:
    st.subheader("🏦 UK Bank Stocks – Daily Change")
    df_banks = pd.DataFrame(banks)
    df_banks["change_pct"] = df_banks["change_pct"].astype(float)
    fig = px.bar(df_banks, x="symbol", y="change_pct", color="change_pct",
                 color_continuous_scale=["red", "green"], title="Daily Change (%)")
    st.plotly_chart(fig, use_container_width=True)

# ---- Economic Indicators (if available) ----
econ = data.get("economic_indicators", {})
if econ:
    st.subheader("📉 Economic Indicators")
    cols = st.columns(3)
    for i, (key, val) in enumerate(econ.items()):
        if isinstance(val, dict) and "error" not in val:
            cols[i % 3].metric(key.replace("_", " ").title(), val.get("latest_value", "N/A"))

st.caption(f"Last refreshed: {data.get('generated_at', 'N/A')}")