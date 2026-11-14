import json

with open(r"e:\BOUTY ARGON\workspaces\ssrfun_beta_audit\artifacts\sample_tx.json", "r") as f:
    tx = json.load(f)

message = tx.get("result", {}).get("transaction", {}).get("message", {})
instructions = message.get("instructions", [])

print("AccrueFees accounts in sample_tx:")
for idx, acc in enumerate(instructions[0].get("accounts", [])):
    print(f"  Account {idx}: {acc}")
