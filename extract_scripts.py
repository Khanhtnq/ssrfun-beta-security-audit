import urllib.request
import ssl
import re
import os
import json
from urllib.parse import urljoin

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)
os.makedirs("artifacts", exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

urls = {
    "root": "https://ssr.fun",
    "beta": "https://ssr.fun/beta",
    "leaderboard": "https://ssr.fun/leaderboard"
}

all_scripts = set()

for name, u in urls.items():
    req = urllib.request.Request(u, headers=headers)
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        with open(f"artifacts/{name}.html", "w", encoding="utf-8") as f:
            f.write(html)
        scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
        print(f"{name} scripts found: {len(scripts)}")
        for s in scripts:
            abs_url = urljoin(u, s)
            all_scripts.add(abs_url)

print(f"Total unique script URLs: {len(all_scripts)}")
for s in sorted(all_scripts):
    print(" ", s)
