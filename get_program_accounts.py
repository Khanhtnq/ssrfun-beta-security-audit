import urllib.request, json, ssl

rpc_url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def solana_rpc(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
    req = urllib.request.Request(rpc_url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))

prog_id = "8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9"

# Query all program accounts with dataSlice of 8 bytes (discriminator)
res = solana_rpc("getProgramAccounts", [
    prog_id,
    {
        "encoding": "base64",
        "dataSlice": {"offset": 0, "length": 8}
    }
])

accounts = res.get("result", [])
print(f"Total program accounts owned by {prog_id}: {len(accounts)}")
disc_counts = {}
for a in accounts:
    pk = a.get("pubkey")
    data_b64 = a.get("account", {}).get("data", [""])[0]
    import base64
    disc = base64.b64decode(data_b64).hex()
    disc_counts[disc] = disc_counts.get(disc, 0) + 1

for d, count in sorted(disc_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  Discriminator {d}: {count} accounts")
