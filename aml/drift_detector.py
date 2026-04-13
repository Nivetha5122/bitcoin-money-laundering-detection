from river.drift import ADWIN

class DriftMonitor:
    def __init__(self):
        self.detector = ADWIN()

    def update(self, risk_score: float):
        self.detector.update(risk_score)
        return self.detector.drift_detected
