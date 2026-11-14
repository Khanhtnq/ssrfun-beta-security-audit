import os
import urllib.request, json, ssl, base64

rpc_url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pdata_pk = "2YF7aofgPbNj96pJJh1uzLtCk4H2fUq1FVLxFf9TAwow"

# Fetch in 250KB slices
chunk_size = 250000
total_size = 1772165
full_bytes = bytearray()

print(f"Downloading {total_size} bytes in slices...")
for offset in range(0, total_size, chunk_size):
    length = min(chunk_size, total_size - offset)
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getAccountInfo",
        "params": [
            pdata_pk,
            {"encoding": "base64", "dataSlice": {"offset": offset, "length": length}}
        ]
    }).encode("utf-8")
    req = urllib.request.Request(rpc_url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        b64 = res.get("result", {}).get("value", {}).get("data", [""])[0]
        data = base64.b64decode(b64)
        full_bytes.extend(data)
        print(f"  Offset {offset}: downloaded {len(data)} bytes (total {len(full_bytes)})")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "program_binary.elf"), "wb") as f:
    f.write(full_bytes)

print(f"Saved program_binary.elf ({len(full_bytes)} bytes)")
