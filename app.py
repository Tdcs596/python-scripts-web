from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>🌐 Directory Scanner</h2>

    <form action="/scan" method="post">
        Enter Website URL:<br><br>
        <input type="text" name="url" placeholder="https://example.com" size="40" required>
        <br><br>
        <input type="submit" value="Scan">
    </form>
    """

@app.route("/scan", methods=["POST"])
def scan():
    url = request.form.get("url")

    if not url:
        return "❌ URL missing"

    try:
        result = subprocess.run(
            ["python", "script1.py", url],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

    except Exception as e:
        output = str(e)

    return f"<h3>Result:</h3><pre>{output}</pre>"

app.run(host="0.0.0.0", port=10000)
