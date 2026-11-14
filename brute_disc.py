import hashlib

targets = {
    "22f692fa870f4022": "22f692fa870f4022 (343 accs)",
    "6b591e426c26219c": "6b591e426c26219c (88 accs)",
    "c1c6d31d0b62c3e5": "c1c6d31d0b62c3e5 (87 accs)",
    "5c91a66f0b2626f7": "5c91a66f0b2626f7 (27 accs)",
    "f3b0f4829fdc0f74": "f3b0f4829fdc0f74 (15 accs)",
    "129971fd1fa12940": "129971fd1fa12940 (12 accs)",
    "04cbb54974a8a8ff": "04cbb54974a8a8ff (12 accs)",
    "6978d05be59425fa": "6978d05be59425fa (7 accs)",
    "cfd849462c1ce954": "cfd849462c1ce954 (5 accs)",
    "f23abc015ce690cf": "f23abc015ce690cf (4 accs)",
    "d27a70a569844763": "d27a70a569844763 (1 acc)"
}

# Load dictionary words or common anchor account terms
terms = [
    "user", "holder", "trader", "maker", "order", "fill", "position", "account",
    "fee", "fees", "tax", "trade", "swap", "volume", "checkpoint", "epoch", "period", "round",
    "reserve", "pool", "vault", "bonding", "curve", "curve_state", "mint", "token", "quote", "base",
    "campaign", "leaderboard", "reward", "rewards", "claim", "stake", "staker", "lock", "vesting",
    "dividend", "distribution", "share", "shares", "history", "referral", "referrer", "ref", "affiliate",
    "admin", "operator", "authority", "treasury", "fee_recipient", "whitelist", "metadata",
    "snapshot", "accumulator", "harvest", "withheld", "global", "state", "config", "protocol",
    "registry", "manifest", "market", "market_state", "pair", "amm", "pair_state", "router",
    "tax_accumulator", "fee_accumulator", "reserve_account", "user_account", "user_position",
    "fee_tier", "fee_distribution", "campaign_user", "campaign_entry"
]

found = {}

def check(name):
    # Try account:Name, account:name, account:snake_case, account:PascalCase
    variants = [
        name,
        name.lower(),
        name.title(),
        "".join(x.title() for x in name.split("_")),
        "".join(x.lower() for x in name.split("_"))
    ]
    for v in set(variants):
        sh = hashlib.sha256(f"account:{v}".encode()).hexdigest()[:16]
        if sh in targets and sh not in found:
            found[sh] = v
            print(f"FOUND MATCH! {targets[sh]} -> account:{v}")

for t in terms:
    check(t)
    for t2 in terms:
        check(f"{t}_{t2}")
        check(f"{t}{t2.title()}")

print(f"\nTotal identified so far: {len(found)} / {len(targets)}")
