import streamlit as st
import pandas as pd

from visualization.tx_graph import draw_graph


st.set_page_config(layout="wide", page_title="Transaction Explorer")

st.title("🧭 Transaction Explorer")
st.caption(
    "Real-time Bitcoin-like transaction intelligence with AML risk, drift detection, and explainable analysis"
)

# -------------------- DATA CHECK --------------------
if "txs" not in st.session_state or len(st.session_state.txs) == 0:
    st.info("No transactions available. Start ingestion from the Home page.")
    st.stop()

df = pd.DataFrame(st.session_state.txs)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -------------------- NETWORK OVERVIEW --------------------
st.subheader("🌐 Network Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Transactions", len(df))
col2.metric("Active Wallets", df["sender"].nunique())
col3.metric("Illicit TXs", (df["prediction"] == "ILLICIT").sum())
col4.metric(
    "Illicit %",
    f"{(df['prediction'].eq('ILLICIT').mean() * 100):.2f}%"
)
col5.metric(
    "Drift Alerts",
    int(df["drift"].sum())
)

st.divider()

# -------------------- SEARCH & FILTERS --------------------
st.subheader("🔍 Search & Filters")

c1, c2, c3, c4 = st.columns(4)

with c1:
    wallet_filter = st.text_input("Wallet Address (Sender)")

with c2:
    show_illicit_only = st.checkbox("Show Only Illicit")

with c3:
    min_risk = st.slider(
        "Minimum Risk Score",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.05
    )

with c4:
    recent_minutes = st.selectbox(
        "Time Window",
        ["All", "Last 1 min", "Last 5 min", "Last 15 min"]
    )

filtered = df.copy()

# Wallet filter
if wallet_filter:
    filtered = filtered[filtered["sender"].str.contains(wallet_filter)]

# Illicit filter
if show_illicit_only:
    filtered = filtered[filtered["prediction"] == "ILLICIT"]

# Risk filter
filtered = filtered[filtered["risk"] >= min_risk]

# Time filter
if recent_minutes != "All":
    minutes = int(recent_minutes.split()[1])
    cutoff = pd.Timestamp.utcnow() - pd.Timedelta(minutes=minutes)
    filtered = filtered[filtered["timestamp"] >= cutoff]

st.caption(f"Showing {len(filtered)} transactions")

# -------------------- TRANSACTION TABLE --------------------
st.subheader("📡 Live Transaction Stream")

display_df = filtered.copy()
display_df["TX_ID"] = display_df.index
display_df = display_df[
    [
        "TX_ID",
        "timestamp",
        "sender",
        "amount",
        "risk",
        "prediction",
        "drift"
    ]
].sort_values("timestamp", ascending=False)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# -------------------- TRANSACTION INSPECTOR --------------------
st.subheader("🔬 Transaction Inspector")

if len(display_df) == 0:
    st.info("No transaction selected.")
    st.stop()

tx_id = st.selectbox(
    "Select Transaction ID",
    display_df["TX_ID"].tolist(),
    format_func=lambda x: f"TX {x}"
)

selected_tx = st.session_state.txs[tx_id]

# ---- Metadata ----
colA, colB = st.columns(2)

with colA:
    st.markdown("### 📄 Transaction Details")
    st.write(f"**Timestamp:** {selected_tx['timestamp']}")
    st.write(f"**Amount:** {selected_tx['amount']} BTC")
    st.write(f"**Fee:** {selected_tx['fee']}")
    st.write(f"**Inputs:** {selected_tx['inputs']}")
    st.write(f"**Outputs:** {len(selected_tx['receivers'])}")

with colB:
    st.markdown("### 🚨 AML Assessment")
    st.write(f"**Prediction:** {selected_tx['prediction']}")
    st.write(f"**Risk Score:** {selected_tx['risk']}")
    st.write(f"**Behavior Drift:** {'YES' if selected_tx['drift'] else 'NO'}")

# ---- Explainable AML ----
st.markdown("### 🧠 Explainable AML Decision")

if selected_tx["prediction"] == "ILLICIT":
    for reason in selected_tx["explanation"]:
        st.warning(f"• {reason}")
else:
    st.success("Transaction behavior aligns with licit patterns.")

# -------------------- TRANSACTION GRAPH --------------------
st.markdown("### 🧩 Transaction Flow Analysis")

draw_graph(st.session_state.txs)
