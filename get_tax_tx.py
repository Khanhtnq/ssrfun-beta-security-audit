import urllib.request, json, ssl, time

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

time.sleep(1)
sig = "5XeqCkt9Wm6aYjq1Gq2j6jYjTf6tL7B2nEvW9X5T7o2Kqg9p9g2r7vT5w2Kqg9p9g2r7vT5w" # or first sig
# Let's get sig from earlier: 2VWvC33xWVYfqDsz...
# Wait, let's find the exact sigs from the earlier output:
# Sig 2VWvC33xWVYfqDsz
sig = "2VWvC33xWVYfqDsz"
# Let's list signatures again with limit 5 and grab index 5
sigs = solana_rpc("getSignaturesForAddress", ["8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9", {"limit": 10}])
sig_list = sigs.get("result", [])
for s in sig_list:
    sig_str = s.get("signature")
    print("Checking sig:", sig_str)
    time.sleep(0.5)
    tx = solana_rpc("getTransaction", [sig_str, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    logs = tx.get("result", {}).get("meta", {}).get("logMessages", [])
    if any("CollectTradeTax" in l for l in logs):
        print(f"FOUND CollectTradeTax tx: {sig_str}")
        with open(r"e:\BOUTY ARGON\workspaces\ssrfun_beta_audit\artifacts\collect_trade_tax_tx.json", "w", encoding="utf-8") as f:
            json.dump(tx, f, indent=2)
        break
