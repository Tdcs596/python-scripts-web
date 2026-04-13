from flask import Flask
import subprocess

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Script 1",
    "script2": "⚡ Script 2",
    "script3": "🚀 Script 3",
    "script4": "🧠 Script 4"
}

@app.route("/")
def home():
    html = "<h2>🔥 Script Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<p><a href="/{key}">{name}</a></p>'

    return html


# 🔥 SCRIPT RUNNER
@app.route("/script1")
def script1():
    result = subprocess.run(
        ["python3", "script1.py"],
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout + result.stderr}</pre>"


@app.route("/script2")
def script2():
    result = subprocess.run(
        ["python3", "script2.py"],
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout + result.stderr}</pre>"


@app.route("/script3")
def script3():
    result = subprocess.run(
        ["python3", "script3.py"],
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout + result.stderr}</pre>"


@app.route("/script4")
def script4():
    result = subprocess.run(
        ["python3", "script4.py"],
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout + result.stderr}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
