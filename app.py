from flask import Flask, request

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Script 1",
    "script2": "⚡ Script 2",
    "script3": "🚀 Script 3"
}

@app.route("/")
def home():
    html = "<h2>🔥 Control Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<h3><a href="/open/{key}">{name}</a></h3>'

    return html


@app.route("/open/<key>")
def open_script(key):
    host = request.host_url.strip("/")   # 👈 IMPORTANT FIX

    return f"""
    <script>
        window.location.href = "{host}/{key}";
    </script>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
