import hashlib

alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
base_count = len(alphabet)

def b58decode(s):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * alphabet.index(char)
        multi = multi * base_count
    h = hex(decoded)[2:]
    if len(h) % 2 != 0:
        h = '0' + h
    return bytes.fromhex(h)

data_b58 = "Pu5LkBQB5vV"
data_bytes = b58decode(data_b58)
data_hex = data_bytes.hex()
print("AccrueFees data hex:", data_hex)

def anchor_sighash(name):
    return hashlib.sha256(f"global:{name}".encode()).digest()[:8]

candidates = [
    "accrue_fees",
    "accrue_fee",
    "accrue",
    "mint_to",
    "crank_fees",
    "distribute_fees"
]

for c in candidates:
    sh = anchor_sighash(c).hex()
    print(f"global:{c} -> {sh} (matches={sh == data_hex})")
