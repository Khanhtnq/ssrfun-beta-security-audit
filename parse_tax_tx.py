import os
import json

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "collect_trade_tax_tx.json"), "r") as f:
    tx = json.load(f)

meta = tx.get("result", {}).get("meta", {})
transaction = tx.get("result", {}).get("transaction", {})
message = transaction.get("message", {})

print("=== Transaction Overview ===")
print("Slot:", tx.get("result", {}).get("slot"))
print("Err:", meta.get("err"))
print("Fee:", meta.get("fee"))

print("\n=== Account Keys ===")
for idx, acc in enumerate(message.get("accountKeys", [])):
    if isinstance(acc, dict):
        print(f" {idx}: {acc.get('pubkey')} (signer={acc.get('signer')}, writable={acc.get('writable')})")
    else:
        print(f" {idx}: {acc}")

print("\n=== Instructions ===")
for idx, ix in enumerate(message.get("instructions", [])):
    print(f"Ix {idx}: prog={ix.get('programId')}, progIndex={ix.get('programIdIndex')}, data={ix.get('data')}, accounts={ix.get('accounts')}")

print("\n=== Inner Instructions ===")
for inner in meta.get("innerInstructions", []):
    print(f"Inner index {inner.get('index')}:")
    for sub_ix in inner.get("instructions", []):
        parsed = sub_ix.get("parsed")
        prog = sub_ix.get("program") or sub_ix.get("programId")
        print(f"  prog={prog}, parsed={parsed}")

print("\n=== Pre/Post Token Balances ===")
pre_b = meta.get("preTokenBalances", [])
post_b = meta.get("postTokenBalances", [])
for p in pre_b:
    print("Pre:", p.get("accountIndex"), p.get("mint"), p.get("owner"), p.get("uiTokenAmount"))
for p in post_b:
    print("Post:", p.get("accountIndex"), p.get("mint"), p.get("owner"), p.get("uiTokenAmount"))

print("\n=== Log Messages ===")
for l in meta.get("logMessages", []):
    print(" ", l)
