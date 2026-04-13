from flask import Flask, request
import script1 as s1   # script1.py import

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Website Analyzer",
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


# 🌐 SCRIPT 1 (WORKING)
@app.route("/script1", methods=["GET", "POST"])
def script1():
    if request.method == "POST":
        url = request.form.get("url")
        result = s1.run(url)

        return f"""
        <h3>Result:</h3>
        <pre>{result}</pre>
        <br><a href="/script1">🔁 Back</a>
        <br><a href="/">🏠 Home</a>
        """

    return """
    <h2>🌐 Website Analyzer</h2>

    <form method="POST">
        <input name="url" placeholder="https://example.com" required>
        <br><br>
        <button>Analyze</button>
    </form>

    <br><a href="/">🏠 Home</a>
    """


# ⚡ SCRIPT 2 (placeholder)
@app.route("/script2")
def script2():
    return "<h2>⚡ Script 2 Coming Soon</h2><br><a href='/'>🏠 Home</a>"


# 🚀 SCRIPT 3 (placeholder)
@app.route("/script3")
def script3():
    return "<h2>🚀 Script 3 Coming Soon</h2><br><a href='/'>🏠 Home</a>"


# 🧠 SCRIPT 4 (placeholder)
@app.route("/script4")
def script4():
    return "<h2>🧠 Script 4 Coming Soon</h2><br><a href='/'>🏠 Home</a>"


# 🔥 RUN
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
