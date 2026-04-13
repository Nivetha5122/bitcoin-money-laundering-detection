import pandas as pd
import plotly.graph_objects as go

def risk_time_series(txs):
    if not txs:
        return None

    df = pd.DataFrame(txs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df["risk"],
        mode="lines+markers"
    ))

    fig.add_hline(y=0.6)

    fig.update_layout(
        template="plotly_dark",
        height=400
    )

    return fig