import urllib.request, json, ssl

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

pdata_pk = "2YF7aofgPbNj96pJJh1uzLtCk4H2fUq1FVLxFf9TAwow"
res = solana_rpc("getAccountInfo", [pdata_pk, {"encoding": "base64", "dataSlice": {"offset": 0, "length": 128}}])
val = res.get("result", {}).get("value")
print("Lamports:", val.get("lamports"))
print("Space:", val.get("space"))
