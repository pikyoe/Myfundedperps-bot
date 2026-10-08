from decimal import Decimal
from .risk import RiskEngine

class Executor:
    def __init__(self, client, settings): self.client=client; self.s=settings; self.risk=RiskEngine(settings)
    def execute(self, signal, equity, daily_pnl, consecutive_losses, open_positions, market_id, leverage=2):
        decision=self.risk.gate(equity,daily_pnl,consecutive_losses,open_positions,self.s.risk_per_trade)
        if not decision.allowed: return {"submitted":False,"reason":decision.reason}
        size=self.risk.position_size(self.s.risk_per_trade,signal.entry,signal.stop)
        q=self.client.quote(market_id, signal.side, size)
        data=q.get("data",q)
        if not data.get("fillable",True): return {"submitted":False,"reason":"quote not fillable"}
        payload={"type":"market","account_id":self.s.account_id,"market_id":market_id,"side":signal.side,"size":float(size),"expected_price":float(data.get("mid",signal.entry)),"leverage":leverage,"margin_mode":"cross","take_profit_price":float(signal.target),"stop_loss_price":float(signal.stop),"client_order_id":f"trend-{market_id.replace('|','-')}-{signal.side}"}
        if not self.s.live_trading: return {"submitted":False,"dry_run":True,"payload":payload,"quote":data}
        return {"submitted":True,"response":self.client.order(payload),"quote":data}
