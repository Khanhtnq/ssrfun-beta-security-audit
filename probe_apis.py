import urllib.request, ssl, json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

endpoints = [
    "https://ssr.fun/api/mainnet/campaign-leaderboard",
    "https://ssr.fun/api/site/claim",
    "https://ssr.fun/api/mainnet/config",
    "https://ssr.fun/api/config",
    "https://ssr.fun/manifest.json",
    "https://ssr.fun/robots.txt",
    "https://ssr.fun/sitemap.xml"
]

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, headers=headers)
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read()
            print(f"{ep} -> {resp.status} ({len(data)} bytes)")
            try:
                j = json.loads(data.decode('utf-8'))
                print("   JSON preview:", str(j)[:200])
            except:
                print("   Text preview:", data[:200])
    except Exception as e:
        print(f"{ep} -> {e}")
