from flask import Flask, request
import requests

app = Flask(__name__)

# 🏠 HOME PAGE
@app.route("/")
def home():
    return """
    <h2>🌐 Website Analyzer</h2>

    <form method="POST" action="/analyze">
        <input type="text" name="url" placeholder="https://example.com" required>
        <br><br>
        <button>Analyze</button>
    </form>
    """


# 🔍 ANALYZE
@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("url")

    if not url.startswith("http"):
        url = "http://" + url

    try:
        response = requests.get(url, timeout=5)

        headers = response.headers
        status = response.status_code
        length = len(response.text)

        return f"""
        <h3>✅ Analysis Result</h3>

        <p><b>URL:</b> {url}</p>
        <p><b>Status Code:</b> {status}</p>
        <p><b>Content Length:</b> {length} bytes</p>

        <h4>Headers:</h4>
        <pre>{headers}</pre>

        <br><a href="/">🔙 Back</a>
        """

    except Exception as e:
        return f"""
        <h3>❌ Error</h3>
        <p>{str(e)}</p>
        <br><a href="/">🔙 Back</a>
        """


# 🔥 RUN
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10001))
    app.run(host="0.0.0.0", port=port)
