import math
from datetime import datetime

def extract_features(tx, history):
    amount = tx["amount"]
    fee = tx["fee"]
    inputs = tx["inputs"]
    outputs = len(tx["receivers"])

    fanout = outputs / max(inputs, 1)
    fee_ratio = fee / (amount + 1e-6)

    # Intent Flow Entropy
    probs = [1 / outputs] * outputs
    entropy = -sum(p * math.log(p) for p in probs)

    # Temporal Compression
    if history:
        t1 = datetime.fromisoformat(history[-1]["timestamp"])
        t2 = datetime.fromisoformat(tx["timestamp"])
        delta = max((t2 - t1).total_seconds(), 1e-3)
    else:
        delta = 1.0

    temporal_compression = 1 / delta

    return [
        amount,
        fee_ratio,
        inputs,
        outputs,
        fanout,
        entropy,
        temporal_compression
    ]
