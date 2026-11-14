import os
import json, hashlib

# Test account name hash
names = ["Reserve", "reserve", "ReserveAccount", "BondingCurve", "Config", "State", "Global"]
for n in names:
    h = hashlib.sha256(f"account:{n}".encode()).hexdigest()[:16]
    print(f"account:{n} -> {h}")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "sample_tx.json"), "r") as f:
    tx = json.load(f)

meta = tx.get("result", {}).get("meta", {})
log_messages = meta.get("logMessages", [])
print("\nLog messages:")
for l in log_messages:
    print(" ", l)

transaction = tx.get("result", {}).get("transaction", {})
message = transaction.get("message", {})
print("\nInstructions:")
instructions = message.get("instructions", [])
for idx, ix in enumerate(instructions):
    print(f" Ix {idx}: {ix.get('programId')} - data: {ix.get('data')}")
