import urllib.request, json, ssl

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

# Fetch 30 signatures
sigs = solana_rpc("getSignaturesForAddress", [prog_id, {"limit": 30}]).get("result", [])

ix_names = set()
for s in sigs:
    sig = s.get("signature")
    tx = solana_rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
    logs = tx.get("result", {}).get("meta", {}).get("logMessages", [])
    for l in logs:
        if "Instruction:" in l:
            ix_names.add(l)
    print(f"Sig {sig[:16]}...: {[l for l in logs if 'Instruction:' in l]}")

print("\nUnique instructions seen across 30 transactions:")
for ix in sorted(ix_names):
    print(" ", ix)
