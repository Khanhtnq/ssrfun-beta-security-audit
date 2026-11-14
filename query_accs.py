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

accs = [
    "5dhEfqb5wLy5yxZwYwZCXNsW2ALYoEbeYBfuR8B3ud88",
    "ASUVTsYaAqdr3T2SfNnuxUoLph3hzWupzx2T1iXyNava",
    "4sUnzREwHoT5pTm3phbzsRJndDCHXM1UYx3MPKnQCeeL",
    "8SB8ii1Gx5e81Q5CnhPe86RDoaYZtJiocmWRv65nNryG",
    "6PSs4N8gCi9mhPMjpEyqeT4r7Jves3vSKUPjtiM5dFQB",
    "2gmVw6fg7kZB4hHmnThGtXUVWSA6hh8tDdFEk8JsZWk3",
    "5c9Z22YXH7jCP8cxb4FRuDg8X116AXwXnq6YKd6XTXo9",
    "5Fckt6eaXRx9xKNiBdNx4xJWB6XEFKzdemTFppgMbGV1",
    "6adZbFYM83jKSK4fjy7QbSCA8vRLCosBh6m8DoFBqDVN"
]

for a in accs:
    res = solana_rpc("getAccountInfo", [a, {"encoding": "jsonParsed"}])
    val = res.get("result", {}).get("value")
    if val:
        owner = val.get("owner")
        space = val.get("space")
        data = val.get("data")
        parsed_type = ""
        if isinstance(data, dict):
            parsed_type = data.get("parsed", {}).get("type", "")
        print(f"{a}: owner={owner}, space={space}, parsed_type={parsed_type}")
    else:
        print(f"{a}: None")
