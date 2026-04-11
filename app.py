from flask import Flask, request
import subprocess

app = Flask(__name__)

# 🔥 SCRIPT REGISTRY (YAHI SE SAB CONTROL HOGA)
SCRIPTS = {
    "script1": {
        "name": "🌐 Directory Scanner",
        "file": "script1.py",
        "input": "url",
        "placeholder": "https://example.com"
    },
    "script2": {
        "name": "⚡ Script 2",
        "file": "script2.py",
        "input": "text",
        "placeholder": "Enter text"
    },
    "script3": {
        "name": "🚀 Script 3",
        "file": "script3.py",
        "input": "text",
        "placeholder": "Enter input"
    },
    "script4": {
        "name": "🧠 Script 4",
        "file": "script4.py",
        "input": "text",
        "placeholder": "Enter input"
    }
}

# 🏠 HOME PAGE (AUTO MENU)
@app.route("/")
def home():
    menu = "<h2>🔥 Script Control Panel</h2><ul>"

    for key in SCRIPTS:
        menu += f'<li><a href="/run/{key}">{SCRIPTS[key]["name"]}</a></li>'

    menu += "</ul>"
    return menu

# 📥 INPUT PAGE (DYNAMIC)
@app.route("/run/<script_key>")
def run_page(script_key):
    if script_key not in SCRIPTS:
        return "❌ Script not found"

    script = SCRIPTS[script_key]

    return f"""
    <h2>{script['name']}</h2>

    <form action="/execute/{script_key}" method="post">
        Enter Input:<br><br>
        <input type="text" name="user_input" placeholder="{script['placeholder']}" size="40" required>
        <br><br>
        <input type="submit" value="Run">
    </form>

    <br><a href="/">⬅ Back</a>
    """

# ▶️ EXECUTION ENGINE (SAME FOR ALL)
@app.route("/execute/<script_key>", methods=["POST"])
def execute(script_key):
    if script_key not in SCRIPTS:
        return "❌ Script not found"

    script = SCRIPTS[script_key]
    user_input = request.form.get("user_input")

    result = subprocess.run(
        ["python", script["file"], user_input],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    return f"""
    <h3>Result:</h3>
    <pre>{output}</pre>
    <br><br>
    <a href="/run/{script_key}">🔁 Run Again</a><br>
    <a href="/">🏠 Home</a>
    """

app.run(host="0.0.0.0", port=10000)
