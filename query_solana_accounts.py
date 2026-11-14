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

accounts = [
    ("Reserve 93", "FFPxPj1BaAPD8WuYpvnpReyUCYJZqA2pQxXH94yW7MVb"),
    ("Mint 93", "8NF4joMpjNmnSZNmZh5nxFnp5YGbvtUUiAWFzVdo54W5"),
    ("Reserve 94", "A3tRdnc1s7fiwvkmVwm6s7wAmF3fML56Pz7QdhpbHJvX"),
    ("Mint 94", "D8zqKJ7vThhKRA9eVjgyWXN9zbktE9RKr4aSYGmjNks5"),
    ("Reserve 95", "B2Es46k6AGUDKaf9VdDvSverf9MDFC8wx7CTM9vWiJZr"),
    ("Mint 95", "AWB8Dw56EVj7ExfYQkP81MyFumDvNS3Nfkmx6us3nzJL")
]

for label, pubkey in accounts:
    res = solana_rpc("getAccountInfo", [pubkey, {"encoding": "jsonParsed"}])
    val = res.get("result", {}).get("value")
    if val:
        owner = val.get("owner")
        lamports = val.get("lamports")
        data = val.get("data")
        print(f"=== {label} ({pubkey}) ===")
        print(f"  Owner: {owner}")
        print(f"  Lamports: {lamports}")
        if isinstance(data, dict):
            print(f"  Parsed program: {data.get('program')}")
            print(f"  Parsed space: {data.get('space')}")
            parsed_info = data.get("parsed", {}).get("info", {})
            print(f"  Mint info: decimals={parsed_info.get('decimals')}, supply={parsed_info.get('supply')}")
            extensions = parsed_info.get("extensions")
            if extensions:
                print(f"  Extensions: {json.dumps(extensions, indent=4)}")
        else:
            print(f"  Raw data len: {len(data) if data else 0}")
    else:
        print(f"=== {label} ({pubkey}) === NOT FOUND or EMPTY")
