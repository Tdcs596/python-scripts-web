from flask import Flask

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Script 1",
    "script2": "⚡ Script 2",
    "script3": "🚀 Script 3",
    "script4": "🧠 Script 4"
}

# 🏠 HOME PAGE
@app.route("/")
def home():
    html = "<h2>🔥 Script Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<p><a href="/{key}">{name}</a></p>'

    return html


# 🔥 SCRIPT ROUTES (IMPORTANT FIX)
@app.route("/script1")
def script1():
    return "<h2>🌐 Script 1 Running</h2>"


@app.route("/script2")
def script2():
    return "<h2>⚡ Script 2 Running</h2>"


@app.route("/script3")
def script3():
    return "<h2>🚀 Script 3 Running</h2>"


@app.route("/script4")
def script4():
    return "<h2>🧠 Script 4 Running</h2>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
