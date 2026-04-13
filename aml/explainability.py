def explain(features, risk):
    reasons = []
    amount, _, _, _, fanout, entropy, temporal = features

    if entropy > 1.0:
        reasons.append("High flow entropy indicating fund obfuscation")
    if fanout > 2:
        reasons.append("Abnormal fan-out suggesting mixing behavior")
    if temporal > 0.5:
        reasons.append("Rapid transaction velocity (temporal compression)")
    if amount > 3:
        reasons.append("High-value transfer")

    if risk >= 0.6:
        reasons.append("Aggregated risk exceeded illicit threshold")

    return reasons
