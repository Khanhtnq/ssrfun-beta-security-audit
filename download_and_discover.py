import os
import re
import urllib.request
import ssl
from urllib.parse import urljoin

base_dir = os.path.dirname(os.path.abspath(__file__))
artifacts_dir = os.path.join(base_dir, "artifacts")
os.makedirs(artifacts_dir, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        return resp.read()

# 1. Download known JS bundles
js_urls = [
    "https://ssr.fun/assets/beta-CH5hkIN6.js",
    "https://ssr.fun/assets/leaderboard-lvjdhEed.js"
]

downloaded = {}
for u in js_urls:
    fname = os.path.basename(u)
    dest = os.path.join(artifacts_dir, fname)
    print(f"Fetching {u} ...")
    content = fetch(u)
    with open(dest, "wb") as f:
        f.write(content)
    downloaded[fname] = content
    print(f"Saved {fname} ({len(content)} bytes)")

# 2. Check for other chunk references in the JS files
chunk_urls = set()
for fname, content in downloaded.items():
    text = content.decode("utf-8", errors="ignore")
    # Look for assets/*.js or dynamic imports
    matches = re.findall(r'["\'](/assets/[a-zA-Z0-9_\-]+\.js)["\']', text)
    matches += re.findall(r'["\'](assets/[a-zA-Z0-9_\-]+\.js)["\']', text)
    for m in matches:
        full_u = urljoin("https://ssr.fun/", m)
        chunk_urls.add(full_u)

print(f"Discovered {len(chunk_urls)} additional chunks:")
for cu in sorted(chunk_urls):
    print(" ", cu)
    cfname = os.path.basename(cu)
    cdest = os.path.join(artifacts_dir, cfname)
    if not os.path.exists(cdest):
        try:
            ccontent = fetch(cu)
            with open(cdest, "wb") as f:
                f.write(ccontent)
            downloaded[cfname] = ccontent
            print(f"Saved {cfname} ({len(ccontent)} bytes)")
        except Exception as e:
            print(f"Failed to fetch {cu}: {e}")

# 3. Also inspect root.html
with open(os.path.join(artifacts_dir, "root.html"), "r", encoding="utf-8") as f:
    rhtml = f.read()

print(f"\nRoot HTML length: {len(rhtml)}")
scripts_in_root = re.findall(r'src=["\']([^"\']+)["\']', rhtml)
print(f"All src in root.html: {scripts_in_root}")
hrefs_in_root = re.findall(r'href=["\']([^"\']+)["\']', rhtml)
print(f"All href in root.html: {hrefs_in_root}")
