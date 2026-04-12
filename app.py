from flask import Flask

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Script 1",
    "script2": "⚡ Script 2",
    "script3": "🚀 Script 3",
    "script4": "🧠 Script 4"
}

# 🏠 HOME PAGE (ONLY BUTTONS)
@app.route("/")
def home():
    html = "<h2>🔥 Script Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<p><a href="/run/{key}">{name}</a></p>'

    return html


# ▶️ JUST REDIRECT STYLE ACCESS
@app.route("/run/<key>")
def run_script(key):
    return f"""
    <script>
        window.location.href = "/{key}";
    </script>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
