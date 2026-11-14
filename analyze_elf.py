import os
import re, os, json

elf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "program_binary.elf")
with open(elf_path, "rb") as f:
    data = f.read()

# Extract all ASCII/UTF-8 strings of length >= 4
strings = re.findall(b"[\x20-\x7e]{4,}", data)
strings = [s.decode("ascii", errors="ignore") for s in strings]

print(f"Total extracted strings: {len(strings)}")

# Look for anchor errors
errors = [s for s in strings if "Error" in s or "Invalid" in s or "Overflow" in s or "Exceeded" in s or "Mismatch" in s]
print(f"\nSample Error strings ({len(errors)}):")
for s in errors[:25]:
    print(" ", s)

# Look for instruction names / sighashes / rust modules
modules = set()
for s in strings:
    if "src/" in s or "programs/" in s or "::" in s:
        modules.add(s)

print(f"\nSample Rust module / file paths ({len(modules)}):")
for s in sorted(list(modules))[:25]:
    print(" ", s)

# Look for fee / token2022 / transfer_fee keywords
keywords = ["fee", "tax", "transfer", "withheld", "harvest", "basis_points", "reserve", "bonding", "curve", "slippage"]
kw_matches = set()
for s in strings:
    s_lower = s.lower()
    if any(k in s_lower for k in keywords) and len(s) < 80:
        kw_matches.add(s)

print(f"\nSample Domain strings ({len(kw_matches)}):")
for s in sorted(list(kw_matches))[:40]:
    print(" ", s)

# Save all strings to artifact for thorough review
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "elf_strings.txt"), "w", encoding="utf-8") as f:
    for s in strings:
        f.write(s + "\n")
print("\nSaved elf_strings.txt")
