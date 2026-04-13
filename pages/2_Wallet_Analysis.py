import streamlit as st
import pandas as pd
from visualization.risk_charts import risk_time_series

st.set_page_config(layout="wide")
st.title("👛 Wallet Risk Analysis")

if "txs" not in st.session_state or not st.session_state.txs:
    st.info("No transaction data available.")
    st.stop()

df = pd.DataFrame(st.session_state.txs)

wallets = sorted(df["sender"].unique())
wallet = st.selectbox("Select Wallet Address", wallets)

wallet_df = df[df["sender"] == wallet]

st.subheader("📊 Wallet Transaction History")
st.dataframe(wallet_df, use_container_width=True)

st.subheader("📈 Wallet Risk Timeline")
fig = risk_time_series(wallet_df.to_dict("records"))
if fig:
    st.plotly_chart(fig, use_container_width=True)
