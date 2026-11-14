import hashlib

# Pure python base58 decode
alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
base_count = len(alphabet)

def b58decode(s):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count
    
    # Convert to hex bytes
    h = hex(decoded)[2:]
    if len(h) % 2 != 0:
        h = '0' + h
    return bytes.fromhex(h)

data_b58 = "adJtZW9Rxnq"
data_bytes = b58decode(data_b58)
data_hex = data_bytes.hex()
print("CollectTradeTax data hex:", data_hex)

def anchor_sighash(name):
    return hashlib.sha256(f"global:{name}".encode()).digest()[:8]

candidates = [
    "collect_trade_tax",
    "collect_tax",
    "collect_trade_fees",
    "accrue_fees",
    "create_reserve",
    "buy",
    "sell",
    "swap",
    "initialize"
]

for c in candidates:
    sh = anchor_sighash(c).hex()
    print(f"global:{c} -> {sh} (matches={sh == data_hex})")
