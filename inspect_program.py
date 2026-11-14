import os
import urllib.request, json, ssl, base64

rpc_url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def solana_rpc(method, params):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }).encode("utf-8")
    req = urllib.request.Request(rpc_url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

prog_id = "8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9"

# 1. Inspect Program Account Info
info = solana_rpc("getAccountInfo", [prog_id, {"encoding": "base64"}])
print("Program Account Info:", info.get("result", {}).get("value", {}).get("owner"))

# 2. Get recent signatures for the program
sigs = solana_rpc("getSignaturesForAddress", [prog_id, {"limit": 10}])
sig_list = sigs.get("result", [])
print(f"Recent signatures for program ({len(sig_list)}):")
for s in sig_list[:5]:
    print("  Signature:", s.get("signature"), "err:", s.get("err"), "slot:", s.get("slot"), "memo:", s.get("memo"))

# 3. Fetch one recent transaction to inspect instructions and accounts
if sig_list:
    sample_sig = sig_list[0].get("signature")
    print(f"\nFetching tx: {sample_sig}")
    tx = solana_rpc("getTransaction", [sample_sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "sample_tx.json"), "w", encoding="utf-8") as f:
        json.dump(tx, f, indent=2)
    print("Saved sample_tx.json")
    
    # Also inspect reserve account raw data
    res_info = solana_rpc("getAccountInfo", ["FFPxPj1BaAPD8WuYpvnpReyUCYJZqA2pQxXH94yW7MVb", {"encoding": "base64"}])
    raw_b64 = res_info.get("result", {}).get("value", {}).get("data", [""])[0]
    raw_bytes = base64.b64decode(raw_b64)
    print(f"Reserve raw data len: {len(raw_bytes)}")
    print("First 32 bytes hex:", raw_bytes[:32].hex())
    print("Discriminator:", raw_bytes[:8].hex())
