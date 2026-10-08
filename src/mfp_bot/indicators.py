from decimal import Decimal

def ema(values: list[Decimal], period: int) -> Decimal:
    if len(values) < period: raise ValueError("not enough values")
    k = Decimal(2) / Decimal(period + 1)
    e = values[0]
    for x in values[1:]: e = x * k + e * (1-k)
    return e

def atr(highs, lows, closes, period=14):
    if len(closes) < period + 1: raise ValueError("not enough values")
    trs=[]
    for i in range(1,len(closes)):
        trs.append(max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1])))
    return sum(trs[-period:], Decimal(0)) / Decimal(period)
