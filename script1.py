import requests

def run(url):
    if not url.startswith("http"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=5)

        headers = response.headers
        status = response.status_code
        length = len(response.text)

        return f"""
URL: {url}
Status Code: {status}
Content Length: {length} bytes

Headers:
{headers}
"""

    except Exception as e:
        return f"Error: {str(e)}"
