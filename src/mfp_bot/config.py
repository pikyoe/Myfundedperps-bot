from dataclasses import dataclass
from decimal import Decimal
import os


def D(v: str | float | int) -> Decimal:
    return Decimal(str(v))

@dataclass(frozen=True)
class Settings:
    api_key: str
    account_id: str
    base_url: str
    ws_url: str
    live_trading: bool
    symbols: tuple[str, ...]
    provider: str
    risk_per_trade: Decimal
    max_risk_per_trade: Decimal
    daily_stop: Decimal
    emergency_equity: Decimal
    mll_floor: Decimal
    profit_target: Decimal
    fast_tf: str
    trend_tf: str
    rr: Decimal

    @classmethod
    def from_env(cls):
        return cls(
            api_key=os.getenv("MFP_API_KEY", ""), account_id=os.getenv("MFP_ACCOUNT_ID", ""),
            base_url=os.getenv("MFP_BASE_URL", "https://sandbox.myfundedperpetuals.com").rstrip("/"),
            ws_url=os.getenv("MFP_WS_URL", "wss://api-stream.myfundedperpetuals.com/v1/market-data"),
            live_trading=os.getenv("MFP_LIVE_TRADING", "false").lower() == "true",
            symbols=tuple(x.strip() for x in os.getenv("MFP_SYMBOLS", "BTCUSDT,ETHUSDT").split(",") if x.strip()),
            provider=os.getenv("MFP_PROVIDER", "binance"),
            risk_per_trade=D(os.getenv("MFP_RISK_PER_TRADE_USD", "5")),
            max_risk_per_trade=D(os.getenv("MFP_MAX_RISK_PER_TRADE_USD", "7.5")),
            daily_stop=D(os.getenv("MFP_DAILY_STOP_USD", "15")),
            emergency_equity=D(os.getenv("MFP_EMERGENCY_EQUITY", "2440")),
            mll_floor=D(os.getenv("MFP_MLL_FLOOR", "2425")),
            profit_target=D(os.getenv("MFP_PROFIT_TARGET", "2725")),
            fast_tf=os.getenv("MFP_FAST_TF", "15m"), trend_tf=os.getenv("MFP_TREND_TF", "1h"), rr=D(os.getenv("MFP_RR", "1.8")),
        )
