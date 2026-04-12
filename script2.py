import requests
import time

def run(user_input):
    url = user_input

    if not url.startswith("http"):
        url = "https://" + url

    try:
        start = time.time()
        res = requests.get(url, timeout=10)
        end = time.time()

        headers = dict(res.headers)

        output = f"""
🔍 WEBSITE SCAN RESULT

URL: {url}
STATUS: {res.status_code}
RESPONSE TIME: {round(end-start, 2)} sec

SERVER: {headers.get('Server')}
CONTENT-TYPE: {headers.get('Content-Type')}

FULL HEADERS:
{headers}
"""
        return output

    except Exception as e:
        return f"ERROR: {str(e)}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(run(sys.argv[1]))
