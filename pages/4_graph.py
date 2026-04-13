import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from visualization.tx_graph import build_graph
from visualization.risk_charts import risk_time_series

st.set_page_config(layout="wide")

st.title("📊 AML Graph Center")

if "txs" not in st.session_state or not st.session_state.txs:
    st.warning("No data yet")
    st.stop()

txs = st.session_state.txs[-100:]
df = pd.DataFrame(txs)

graph_type = st.selectbox(
    "Select Graph",
    [
        "📈 Risk Time Series",
        "🔗 Network Graph",
        "📊 Amount Distribution",
        "📉 Fee vs Amount",
        "⚠️ Risk Distribution",
        "🔥 Drift Timeline"
    ]
)

if graph_type == "📈 Risk Time Series":
    fig = risk_time_series(txs)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

elif graph_type == "🔗 Network Graph":
    build_graph(txs)
    with open("graph.html", "r") as f:
        components.html(f.read(), height=700)

elif graph_type == "📊 Amount Distribution":
    st.bar_chart(df["amount"])

elif graph_type == "📉 Fee vs Amount":
    st.scatter_chart(df[["amount", "fee"]])

elif graph_type == "⚠️ Risk Distribution":
    st.bar_chart(df["risk"])

elif graph_type == "🔥 Drift Timeline":
    drift_df = df[df["drift"] == True]

    if drift_df.empty:
        st.info("No drift detected yet (system learning...)")
    else:
        st.dataframe(drift_df)