import os, sys

# Set utf-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

artifacts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")

for fname in os.listdir(artifacts_dir):
    p = os.path.join(artifacts_dir, fname)
    if os.path.isfile(p):
        print(f"=== {fname} ({os.path.getsize(p)} bytes) ===")
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if len(content) < 8000:
                print(content)
            else:
                print(content[:3000])
                print("\n... [TRUNCATED] ...\n")
                print(content[-2000:])
        print("\n" + "="*50 + "\n")
