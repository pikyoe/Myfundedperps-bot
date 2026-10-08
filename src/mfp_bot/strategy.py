from dataclasses import dataclass
from decimal import Decimal
from .indicators import ema, atr

@dataclass(frozen=True)
class Signal:
    side: str
    entry: Decimal
    stop: Decimal
    target: Decimal
    reason: str

class TrendBreakoutStrategy:
    def __init__(self, rr=Decimal("1.8")): self.rr=rr

    def evaluate(self, candles_1h, candles_15m):
        if len(candles_1h) < 200 or len(candles_15m) < 30: return None
        c1=[x[4] for x in candles_1h]; c15=[x[4] for x in candles_15m]
        e50,e200=ema(c1,50),ema(c1,200)
        highs=[x[2] for x in candles_15m]; lows=[x[3] for x in candles_15m]
        a=atr(highs,lows,c15,14); last=c15[-1]
        resistance=max(highs[-21:-1]); support=min(lows[-21:-1])
        if e50 > e200 and last > resistance:
            stop=min(support, last-a); return Signal("buy",last,stop,last+(last-stop)*self.rr,"1h bullish trend + 15m breakout")
        if e50 < e200 and last < support:
            stop=max(resistance, last+a); return Signal("sell",last,stop,last-(stop-last)*self.rr,"1h bearish trend + 15m breakdown")
        return None
