import os, re

with open("artifacts/root.html", "r", encoding="utf-8") as f:
    text = f.read()

print("root.html length:", len(text))
print("root.html preview:")
print(text[:1000])

# Find any links, preload, modulepreload, etc.
preloads = re.findall(r'<link[^>]+(?:href|src)=["\']([^"\']+)["\']', text)
print("\nLinks in root.html:")
for p in preloads:
    print(" ", p)
