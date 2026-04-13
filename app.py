import streamlit as st
import json
import time
from streamlit_lottie import st_lottie

# ======================================================
# CONFIG
# ======================================================
st.set_page_config(
    page_title="Bitcoin AML Analytics Platform",
    layout="wide"
)

# ======================================================
# LOAD LOTTIE
# ======================================================
def load_lottie_once(path):
    if "lottie_anim" not in st.session_state:
        try:
            with open(path, "r") as f:
                st.session_state.lottie_anim = json.load(f)
        except:
            st.session_state.lottie_anim = None
    return st.session_state.lottie_anim

lottie_bitcoin = load_lottie_once("assets/coin.json")

# ======================================================
# HEADER
# ======================================================
col_left, col_right = st.columns([9, 2])

with col_left:
    st.markdown(
        """
        <h1>🧠 Bitcoin AML Analytics Platform</h1>
        <span style="color:gray;">
        Intent-Flow • Drift-Adaptive • Explainable AML
        </span>
        """,
        unsafe_allow_html=True
    )

with col_right:
    if lottie_bitcoin:
        st_lottie(lottie_bitcoin, height=90)

st.divider()

# ======================================================
# IMPORTS
# ======================================================
from simulator.transaction_generator import generate_transaction
from aml.feature_extractor import extract_features
from aml.classifier import AMLClassifier
from aml.drift_detector import DriftMonitor
from aml.explainability import explain
from visualization.risk_charts import risk_time_series

# ======================================================
# SESSION STATE
# ======================================================
if "txs" not in st.session_state:
    st.session_state.txs = []

if "run" not in st.session_state:
    st.session_state.run = False

if "classifier" not in st.session_state:
    st.session_state.classifier = AMLClassifier()

if "drift_monitor" not in st.session_state:
    st.session_state.drift_monitor = DriftMonitor()

classifier = st.session_state.classifier
drift_monitor = st.session_state.drift_monitor

# ======================================================
# CONTROLS
# ======================================================
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start"):
        st.session_state.run = True

with col2:
    if st.button("⏹ Stop"):
        st.session_state.run = False

# ======================================================
# PLACEHOLDERS (KEY TO NO-FLICKER UI)
# ======================================================
table_placeholder = st.empty()
chart_placeholder = st.empty()
status_placeholder = st.empty()

# ======================================================
# STREAM LOOP (NO RERUN)
# ======================================================
if st.session_state.run:

    status_placeholder.success("🟢 Live ingestion running...")

    while st.session_state.run:

        try:
            # ===== Generate tx =====
            tx = generate_transaction()

            features = extract_features(tx, st.session_state.txs)
            label, risk = classifier.predict(features)
            drift = drift_monitor.update(risk)

            tx.update({
                "prediction": label,
                "risk": risk,
                "drift": drift,
                "explanation": explain(features, risk)
            })

            # ===== Limit memory =====
            MAX_TX = 300
            st.session_state.txs.append(tx)
            st.session_state.txs = st.session_state.txs[-MAX_TX:]

            # ===== UPDATE TABLE ONLY =====
            table_placeholder.dataframe(
                st.session_state.txs[::-1],
                use_container_width=True
            )

            # ===== UPDATE CHART ONLY =====
            fig = risk_time_series(st.session_state.txs)
            if fig:
                chart_placeholder.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # ===== Drift alert =====
            if drift:
                status_placeholder.warning("⚠️ Drift detected!")

            time.sleep(1)  # smooth streaming speed

        except Exception as e:
            status_placeholder.error(f"Error: {e}")
            break

else:
    status_placeholder.info("Click ▶ Start to begin ingestion")