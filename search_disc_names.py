import hashlib

targets = {
    "GlobalConfig": "cf5bfa1c98b3d7d1",
    "PDA_74": "6b591e426c26219c",
    "PDA_76": "c1c6d31d0b62c3e5"
}

words = [
    "global", "config", "state", "protocol", "settings", "root",
    "user", "position", "holder", "account", "balance", "participant", "investor", "member",
    "fee", "checkpoint", "epoch", "distribution", "pool", "vault", "tax", "stats", "yield",
    "reserve", "entry", "history", "lock", "escrow", "curve", "bonding", "mint"
]

all_candidates = set()
for w1 in words:
    all_candidates.add(w1)
    all_candidates.add(w1.title())
    all_candidates.add(w1.upper())
    for w2 in words:
        all_candidates.add(f"{w1}_{w2}")
        all_candidates.add(f"{w1.title()}{w2.title()}")
        all_candidates.add(f"{w1}{w2.title()}")

for c in all_candidates:
    sh = hashlib.sha256(f"account:{c}".encode()).hexdigest()[:16]
    for t_name, t_disc in targets.items():
        if sh == t_disc:
            print(f"MATCH for {t_name}: {c} -> {sh}")
