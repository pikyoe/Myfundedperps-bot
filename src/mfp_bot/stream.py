import asyncio, json, websockets

class MarketStream:
    def __init__(self, url, symbols, provider): self.url=url; self.symbols=symbols; self.provider=provider
    async def events(self):
        backoff=1
        while True:
            try:
                async with websockets.connect(self.url, ping_interval=20, ping_timeout=20, max_size=2**20) as ws:
                    reqs=[{"op":"sub","id":1,"channel":"candles","payload":{"symbols":list(self.symbols),"providers":[self.provider],"intervals":["15m","1h"],"historyLimit":200}}]
                    await ws.send(json.dumps(reqs[0])); backoff=1
                    async for raw in ws:
                        frame=json.loads(raw)
                        for event in frame.get("events",[]): yield event
            except Exception:
                await asyncio.sleep(backoff); backoff=min(backoff*2,30)
