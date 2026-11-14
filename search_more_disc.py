import hashlib

targets = {
    "PDA_74": "6b591e426c26219c",
    "PDA_76": "c1c6d31d0b62c3e5"
}

words = [
    "user", "holder", "account", "trader", "maker", "owner", "participant", "buyer", "seller",
    "fee", "reward", "tax", "share", "dividend", "yield", "distribution", "snapshot", "epoch", "period",
    "accrual", "claim", "checkpoint", "record", "state", "tracker", "info", "data", "ledger",
    "reserve_user", "user_reserve", "fee_recipient", "tax_recipient", "trade", "volume"
]

all_candidates = set()
for w1 in words:
    all_candidates.add(w1)
    all_candidates.add(w1.title())
    all_candidates.add(f"User{w1.title()}")
    all_candidates.add(f"Reserve{w1.title()}")
    for w2 in words:
        all_candidates.add(f"{w1}_{w2}")
        all_candidates.add(f"{w1.title()}{w2.title()}")
        for w3 in ["state", "info", "record", "account", "data"]:
            all_candidates.add(f"{w1.title()}{w2.title()}{w3.title()}")

for c in all_candidates:
    sh = hashlib.sha256(f"account:{c}".encode()).hexdigest()[:16]
    for t_name, t_disc in targets.items():
        if sh == t_disc:
            print(f"MATCH for {t_name}: {c} -> {sh}")
