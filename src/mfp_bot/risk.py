from dataclasses import dataclass
from decimal import Decimal
from .config import Settings

@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    reason: str

class RiskEngine:
    def __init__(self, settings: Settings): self.s = settings

    def gate(self, equity: Decimal, daily_pnl: Decimal, consecutive_losses: int, open_positions: int, risk: Decimal) -> RiskDecision:
        if equity <= self.s.mll_floor: return RiskDecision(False, "MLL floor reached")
        if equity <= self.s.emergency_equity: return RiskDecision(False, "internal emergency equity stop")
        if daily_pnl <= -self.s.daily_stop: return RiskDecision(False, "internal daily loss stop")
        if consecutive_losses >= 2: return RiskDecision(False, "consecutive-loss cooldown")
        if open_positions >= 1: return RiskDecision(False, "max open positions reached")
        if risk > self.s.max_risk_per_trade: return RiskDecision(False, "risk exceeds hard ceiling")
        return RiskDecision(True, "ok")

    @staticmethod
    def position_size(risk_usd: Decimal, entry: Decimal, stop: Decimal) -> Decimal:
        distance = abs(entry - stop)
        if distance <= 0: raise ValueError("entry and stop must differ")
        return risk_usd / distance
