import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "leaderboard-lvjdhEed.js")
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print("Full leaderboard JS content:")
print(text)
