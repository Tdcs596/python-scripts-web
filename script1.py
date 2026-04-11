import sys
import requests

# Input URL from website
url = sys.argv[1]

# Directory list (yahi main logic hai)
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
