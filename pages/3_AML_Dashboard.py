import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚨 AML Monitoring Dashboard")

if "txs" not in st.session_state or not st.session_state.txs:
    st.info("No AML data available.")
    st.stop()

df = pd.DataFrame(st.session_state.txs)

col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(df))
col2.metric("Illicit Transactions", (df["prediction"] == "ILLICIT").sum())
col3.metric("Drift Alerts", df["drift"].sum())

st.subheader("🔍 Flagged Transactions")

flagged = df[df["prediction"] == "ILLICIT"]
st.dataframe(flagged, use_container_width=True)

st.subheader("🧠 Explainable AML Reasons")
for _, row in flagged.tail(5).iterrows():
    st.warning(f"TX at {row['timestamp']}")
    for reason in row["explanation"]:
        st.write(f"• {reason}")
