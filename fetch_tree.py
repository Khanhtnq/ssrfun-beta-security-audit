import os, sys, re, urllib.request, ssl
from urllib.parse import urljoin

base_dir = r"e:\BOUTY ARGON\workspaces\ssrfun_beta_audit\artifacts"
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

queue = [
    "https://ssr.fun/assets/modulepreload-polyfill-Dezn_h7o.js",
    "https://ssr.fun/assets/core-DNPvxTZ8.js"
]

visited = set()

while queue:
    u = queue.pop(0)
    if u in visited:
        continue
    visited.add(u)
    fname = os.path.basename(u)
    dest = os.path.join(base_dir, fname)
    print(f"Fetching {u} ...")
    try:
        content = fetch(u)
        with open(dest, "wb") as f:
            f.write(content)
        print(f"Saved {fname} ({len(content)} bytes)")
        
        # Check for more imports
        text = content.decode("utf-8", errors="ignore")
        imports = re.findall(r'from\s*["\'](\./[^"\']+)["\']', text)
        imports += re.findall(r'import\s*["\'](\./[^"\']+)["\']', text)
        imports += re.findall(r'import\([^)]*["\'](\./[^"\']+)["\']', text)
        for imp in imports:
            clean = imp.replace("./", "")
            next_url = urljoin("https://ssr.fun/assets/", clean)
            if next_url not in visited and next_url not in queue:
                queue.append(next_url)
    except Exception as e:
        print(f"Failed {u}: {e}")

print("Done fetching queue.")
