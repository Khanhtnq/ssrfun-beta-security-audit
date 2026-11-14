import hashlib

targets = {
    "22f692fa870f4022": "343 accs",
    "6b591e426c26219c": "88 accs",
    "c1c6d31d0b62c3e5": "87 accs",
    "5c91a66f0b2626f7": "27 accs",
    "f3b0f4829fdc0f74": "15 accs",
    "129971fd1fa12940": "12 accs",
    "04cbb54974a8a8ff": "12 accs",
    "6978d05be59425fa": "7 accs",
    "f23abc015ce690cf": "4 accs",
    "d27a70a569844763": "1 acc"
}

prefixes = [
    "Reserve", "Protocol", "User", "Holder", "Creator", "Trader", "Trade", "Fee", "Tax",
    "Yield", "Reward", "Epoch", "Checkpoint", "Distribution", "Harvest", "Withheld",
    "Bonding", "Curve", "Token", "Mint", "Vault", "Pool", "Campaign", "Leaderboard",
    "Referral", "Referrer", "Affiliate", "Admin", "Authority", "Global", "System",
    "Share", "Stake", "Balance", "Position", "Account", "Metadata", "Registry", "Listing"
]

suffixes = [
    "Account", "State", "Config", "Data", "Info", "Record", "Tracker", "Ledger",
    "Tax", "Fee", "Fees", "Reward", "Rewards", "Yield", "Share", "Shares",
    "Holding", "Holdings", "Position", "Positions", "Balance", "Balances",
    "History", "Checkpoint", "Checkpoints", "Epoch", "Epochs", "Distribution",
    "Vault", "Pool", "Curve", "Mint", "Token", "User", "Creator", "Trader",
    "Entry", "Entries", "Leaderboard", "Campaign", "Participant", "Member", "Summary"
]

found = {}
for p in prefixes:
    for s in suffixes:
        for sep in ["", "_"]:
            candidate = f"{p}{sep}{s}"
            for c in [candidate, candidate.lower(), candidate.upper()]:
                sh = hashlib.sha256(f"account:{c}".encode()).hexdigest()[:16]
                if sh in targets and sh not in found:
                    found[sh] = (c, targets[sh])
                    print(f"MATCH: {sh} ({targets[sh]}) -> account:{c}")

# Also try 3-word combinations
for p in ["Reserve", "User", "Protocol", "Trade"]:
    for m in ["Fee", "Tax", "Yield", "Reward", "Share", "Epoch"]:
        for s in ["Account", "State", "Tracker", "Record", "Info", "Distribution", "Checkpoint", "Entry"]:
            for sep in ["", "_"]:
                candidate = f"{p}{sep}{m}{sep}{s}"
                for c in [candidate, candidate.lower()]:
                    sh = hashlib.sha256(f"account:{c}".encode()).hexdigest()[:16]
                    if sh in targets and sh not in found:
                        found[sh] = (c, targets[sh])
                        print(f"MATCH 3-word: {sh} ({targets[sh]}) -> account:{c}")
