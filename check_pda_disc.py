import hashlib

# Check Discriminators of the PDAs
import urllib.request, json, ssl, base64

rpc_url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def solana_rpc(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    req = urllib.request.Request(rpc_url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

accounts = {
    "GlobalConfig": "5dhEfqb5wLy5yxZwYwZCXNsW2ALYoEbeYBfuR8B3ud88",
    "Reserve_93": "FFPxPj1BaAPD8WuYpvnpReyUCYJZqA2pQxXH94yW7MVb",
    "PDA_74": "6PSs4N8gCi9mhPMjpEyqeT4r7Jves3vSKUPjtiM5dFQB",
    "PDA_76": "2gmVw6fg7kZB4hHmnThGtXUVWSA6hh8tDdFEk8JsZWk3"
}

for name, pubkey in accounts.items():
    res = solana_rpc("getAccountInfo", [pubkey, {"encoding": "base64"}])
    data_b64 = res.get("result", {}).get("value", {}).get("data", [""])[0]
    data = base64.b64decode(data_b64)
    disc = data[:8].hex()
    print(f"{name} ({pubkey}): len={len(data)}, disc={disc}")
    
    # Check candidate names for discriminator
    for c in ["global", "config", "global_config", "reserve", "user", "fee", "checkpoint", "epoch", "vault", "holder", "reward", "trader"]:
        sh = hashlib.sha256(f"account:{c}".encode()).hexdigest()[:16]
        if sh == disc:
            print(f"  -> MATCHED account name: {c}")
        # Capitalized
        sh_cap = hashlib.sha256(f"account:{c.title()}".encode()).hexdigest()[:16]
        if sh_cap == disc:
            print(f"  -> MATCHED account name: {c.title()}")
        # CamelCase
        cc = "".join(x.title() for x in c.split("_"))
        sh_cc = hashlib.sha256(f"account:{cc}".encode()).hexdigest()[:16]
        if sh_cc == disc:
            print(f"  -> MATCHED account name: {cc}")
