import streamlit as st

def show_header():
    with st.sidebar:
        st.image(
            "assets/bitcoin.gif",
            use_container_width=True
        )
        st.markdown(
            """
            <div style="text-align:center; font-size:14px;">
            <b>Bitcoin AML Analytics</b><br>
            Intent-Flow • Drift-Aware
            </div>
            """,
            unsafe_allow_html=True
        )
        st.divider()
