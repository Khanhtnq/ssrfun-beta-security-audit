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

prog_id = "8hTW7fHwn8t8hcgTVeyAhHMiCTHGUP3783NWUTBBFwH9"
res = solana_rpc("getAccountInfo", [prog_id, {"encoding": "base64"}])
data_b64 = res.get("result", {}).get("value", {}).get("data", [""])[0]
data = base64.b64decode(data_b64)
print("Program account data len:", len(data))
print("Raw hex:", data.hex())

# Convert 32 bytes starting at offset 4 to base58 pubkey
alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58encode(b):
    n = int.from_bytes(b, "big")
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(alphabet[r])
    for byte in b:
        if byte == 0:
            res.append(alphabet[0])
        else:
            break
    return "".join(reversed(res))

prog_data_pk = b58encode(data[4:36])
print("ProgramData Pubkey:", prog_data_pk)
