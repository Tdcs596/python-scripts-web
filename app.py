from flask import Flask

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Script 1 - URL Scanner",
    "script2": "⚡ Script 2 - IP Tool",
    "script3": "🚀 Script 3 - File Tool"
}

# 🏠 DASHBOARD ONLY
@app.route("/")
def home():
    html = "<h2>🔥 Control Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<h3><a href="/open/{key}">{name}</a></h3>'

    return html


# 🔥 DIRECT OPEN (NO LOGIC)
@app.route("/open/<key>")
def open_script(key):
    return f"""
    <script>
        window.location.href = "http://127.0.0.1:10000/{key}";
    </script>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
