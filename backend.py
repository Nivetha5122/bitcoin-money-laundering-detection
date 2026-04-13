import asyncio
import json
from fastapi import FastAPI, WebSocket

from simulator.transaction_generator import generate_transaction
from aml.feature_extractor import extract_features
from aml.classifier import AMLClassifier
from aml.drift_detector import DriftMonitor
from aml.explainability import explain

app = FastAPI()

classifier = AMLClassifier()
drift_monitor = DriftMonitor()
tx_history = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("✅ WebSocket connected")

    try:
        while True:
            tx = generate_transaction()

            features = extract_features(tx, tx_history)
            label, risk = classifier.predict(features)
            drift = drift_monitor.update(risk)

            tx.update({
                "prediction": label,
                "risk": risk,
                "drift": drift,
                "explanation": explain(features, risk)
            })

            tx_history.append(tx)
            tx_history[:] = tx_history[-300:]

            await ws.send_text(json.dumps(tx, default=str))

            await asyncio.sleep(3)

    except Exception as e:
        print("❌ Error:", e)