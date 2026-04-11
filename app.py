from flask import Flask, request
import subprocess

app = Flask(__name__)

# 🏠 Home Page
@app.route("/")
def home():
    return """
    <h2>🔥 Script Control Panel</h2>

    <ul>
        <li><a href="/script1">Run Directory Scanner</a></li>
        <li><a href="#">Script 2 (Coming Soon)</a></li>
    </ul>
    """

# 📥 Script1 Page
@app.route("/script1")
def script1_page():
    return """
    <h2>🌐 Directory Scanner</h2>

    <form action="/run-script1" method="post">
        Enter Website URL:<br><br>
        <input type="text" name="url" placeholder="https://example.com" size="40" required>
        <br><br>
        <input type="submit" value="Scan">
    </form>

    <br><a href="/">⬅ Back</a>
    """

# ▶️ Run Script1
@app.route("/run-script1", methods=["POST"])
def run_script1():
    url = request.form.get("url")

    if not url:
        return "❌ URL missing"

    result = subprocess.run(
        ["python", "script1.py", url],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    return f"""
    <h3>Result:</h3>
    <pre>{output}</pre>
    <br><br>
    <a href="/script1">🔁 Run Again</a><br>
    <a href="/">🏠 Home</a>
    """

app.run(host="0.0.0.0", port=10000)
