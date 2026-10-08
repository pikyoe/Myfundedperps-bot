import os, json
from dotenv import load_dotenv
from .config import Settings
from .api import MFPClient

def main():
    load_dotenv(); s=Settings.from_env()
    if not s.api_key or not s.account_id: raise SystemExit("MFP_API_KEY and MFP_ACCOUNT_ID are required")
    client=MFPClient(s.base_url,s.api_key)
    account=client.account(s.account_id); policy=client.policy(s.account_id)
    print(json.dumps({"account":account,"policy":policy,"live_trading":s.live_trading}, indent=2, default=str))
    if not s.live_trading: print("DRY RUN: no orders will be submitted")

if __name__ == '__main__': main()
