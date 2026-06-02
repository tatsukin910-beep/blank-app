import random
from config import TRIGGER_WORDS, MAX_LOOPS, COMPLETION_THRESHOLD

class CognitiveOS:
    def __init__(self, stress=0.3):
        self.stress = stress
        self.completion = 0.0
        self.loops = 0

    def process(self, event: str):
        self.completion = 0.0
        self.loops = 0
        logs = []

        while self.completion < COMPLETION_THRESHOLD:
            self.loops += 1
            risk = self._calc_risk(event)

            if risk < 0.3:
                self.completion += 0.3
            elif risk > 0.6:
                self.completion *= 0.5

            logs.append({
                "loop": self.loops,
                "risk": round(risk, 3),
                "completion": round(self.completion, 3)
            })

            if risk > 0.85 or self.loops >= MAX_LOOPS:
                return "⚠️ EMERGENCY → 今は決めない", logs

        return "✅ OK → ソフト判断で進む", logs

    def _calc_risk(self, event: str) -> float:
        base = 0.65 if any(x in event for x in TRIGGER_WORDS) else 0.3
        risk = base * (1 + self.stress * 0.6)
        risk *= (1 + self.loops * 0.1)
        return min(1.0, risk + random.uniform(-0.05, 0.05))