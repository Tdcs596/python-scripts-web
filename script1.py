import sys
import requests

# Debug (optional)
print("ARGS:", sys.argv)

# Check input
if len(sys.argv) < 2:
    print("❌ No URL provided")
    exit()

url = sys.argv[1]

paths = [
    "admin",
    "login",
    "dashboard",
    "uploads",
    "images",
    "backup",
    "config",
    ".git",
    "api"
]

print("Scanning:", url)
print("-" * 30)

for path in paths:
    full_url = url.rstrip("/") + "/" + path
    try:
        res = requests.get(full_url, timeout=5)

        if res.status_code == 200:
            print(f"[FOUND] {full_url}")

        elif res.status_code == 403:
            print(f"[FORBIDDEN] {full_url}")

    except:
        print(f"[ERROR] {full_url}")
