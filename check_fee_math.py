import os
import re

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "elf_strings.txt"), "r", encoding="utf-8") as f:
    lines = f.readlines()

print("Strings related to fee math:")
for line in lines:
    line = line.strip()
    if any(k in line.lower() for k in ["fee_math", "transferfee", "basis_points", "10000", "rounding", "ceiling", "withheld"]):
        if len(line) < 120:
            print(" ", line)
