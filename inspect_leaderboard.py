import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
p = r"e:\BOUTY ARGON\workspaces\ssrfun_beta_audit\artifacts\leaderboard-lvjdhEed.js"
with open(p, "r", encoding="utf-8") as f:
    text = f.read()

print("Full leaderboard JS content:")
print(text)
