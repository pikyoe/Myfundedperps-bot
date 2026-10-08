# MyFundedPerps Evaluation Bot

Risk-first automated trading framework for a MyFundedPerps evaluation account.

## Account profile

- Starting balance: $2,500
- Profit target: $2,725 (+9%)
- MLL floor: $2,425
- Internal emergency stop: $2,440
- Normal risk/trade: $5
- Hard risk/trade ceiling: $7.50
- Internal daily stop: -$15
- Strategy: 1h trend + 15m breakout/retest

## Safety

The bot defaults to sandbox and `MFP_LIVE_TRADING=false`. Set live credentials and explicitly enable live trading only after sandbox validation.

The bot uses only documented MyFundedPerps API endpoints. It does not access browser/internal APIs, use latency arbitrage, HFT, quote stuffing, or platform exploitation.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# fill credentials/account id
pytest -q
python -m mfp_bot.main
```
