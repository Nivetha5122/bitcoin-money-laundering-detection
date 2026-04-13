class AMLClassifier:
    def predict(self, features):
        amount, _, _, _, fanout, entropy, temporal = features

        risk = 0.0
        if entropy > 1.0: risk += 0.3
        if fanout > 2: risk += 0.25
        if temporal > 0.5: risk += 0.25
        if amount > 3: risk += 0.2

        risk = min(risk, 1.0)
        label = "ILLICIT" if risk >= 0.6 else "LICIT"
        return label, round(risk, 3)
