from flask import Flask, request
import subprocess

app = Flask(__name__)

# 🔥 SCRIPT REGISTRY
SCRIPTS = {
    "script1": {
        "name": "🌐 Script 1",
        "file": "script1.py"
    },
    "script2": {
        "name": "⚡ Script 2",
        "file": "script2.py"
    },
    "script3": {
        "name": "🚀 Script 3",
        "file": "script3.py"
    },
    "script4": {
        "name": "🧠 Script 4",
        "file": "script4.py"
    }
}

# 🏠 HOME PAGE
@app.route("/")
def home():
    html = "<h2>🔥 Script Control Panel</h2><ul>"

    for key, val in SCRIPTS.items():
        html += f'<li><a href="/run/{key}">{val["name"]}</a></li>'

    html += "</ul>"
    return html


# 📥 RUN PAGE
@app.route("/run/<script_key>")
def run_page(script_key):
    if script_key not in SCRIPTS:
        return "❌ Script not found"

    script = SCRIPTS[script_key]

    return f"""
    <h2>{script['name']}</h2>

    <form action="/execute/{script_key}" method="post">
        <input type="text" name="user_input" placeholder="Enter input (optional)" size="40">
        <br><br>
        <button type="submit">Run Script</button>
    </form>

    <br><a href="/">⬅ Back</a>
    """


# ▶️ EXECUTION ENGINE
@app.route("/execute/<script_key>", methods=["POST"])
def execute(script_key):
    if script_key not in SCRIPTS:
        return "❌ Script not found"

    script = SCRIPTS[script_key]
    user_input = request.form.get("user_input", "")

    try:
        result = subprocess.run(
            ["python3", script["file"], user_input],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout + result.stderr

        return f"""
        <h3>📌 Output</h3>
        <pre>{output}</pre>

        <br><a href="/run/{script_key}">🔁 Run Again</a>
        <br><a href="/">🏠 Home</a>
        """

    except Exception as e:
        return f"<pre>Error: {str(e)}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
