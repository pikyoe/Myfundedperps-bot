import uuid, httpx

class MFPClient:
    def __init__(self, base_url, api_key):
        self.base=base_url.rstrip('/'); self.headers={"Authorization":f"Bearer {api_key}"}
    def _get(self,path,**params):
        with httpx.Client(timeout=10) as c:
            r=c.get(self.base+path,headers=self.headers,params=params); r.raise_for_status(); return r.json()
    def _post(self,path,payload):
        h={**self.headers,"Content-Type":"application/json","Idempotency-Key":str(uuid.uuid4())}
        with httpx.Client(timeout=10) as c:
            r=c.post(self.base+path,headers=h,json=payload); r.raise_for_status(); return r.json()
    def accounts(self): return self._get('/v1/accounts')
    def account(self, account_id): return self._get(f'/v1/accounts/{account_id}')
    def policy(self, account_id): return self._get(f'/v1/accounts/{account_id}/trading-policy')
    def markets(self): return self._get('/v1/markets')
    def quote(self, market_id, side, size): return self._get(f'/v1/markets/{market_id.replace("|","%7C")}/quote', side=side, size=str(size))
    def order(self, payload): return self._post('/v1/orders',payload)
