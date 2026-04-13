from flask import Flask, request
import script1 as s1
import script2 as s2

app = Flask(__name__)

SCRIPTS = {
    "script1": "🌐 Website Analyzer",
    "script2": "🕷 Website Scraper",
    "script3": "🚀 Script 3",
    "script4": "🧠 Script 4"
}

# 🏠 HOME
@app.route("/")
def home():
    html = "<h2>🔥 Script Dashboard</h2><br>"

    for key, name in SCRIPTS.items():
        html += f'<p><a href="/{key}">{name}</a></p>'

    return html


# ✅ SCRIPT1 (UNCHANGED)
@app.route("/script1", methods=["GET", "POST"])
def script1():
    if request.method == "POST":
        url = request.form.get("url")
        result = s1.run(url)

        return f"<pre>{result}</pre><br><a href='/script1'>Back</a>"

    return """
    <h2>🌐 Website Analyzer</h2>
    <form method="POST">
        <input name="url" placeholder="https://example.com" required>
        <br><br>
        <button>Analyze</button>
    </form>
    """


# 🔥 SCRIPT2 (SCRAPER)
@app.route("/script2", methods=["GET", "POST"])
def script2():
    if request.method == "POST":
        url = request.form.get("url")
        result = s2.scrape(url)

        return f"<pre>{result}</pre><br><a href='/script2'>Back</a>"

    return """
    <h2>🕷 Website Scraper</h2>
    <form method="POST">
        <input name="url" placeholder="https://example.com" required>
        <br><br>
        <button>Scrape</button>
    </form>
    """


# placeholders
@app.route("/script3")
def script3():
    return "<h2>🚀 Script 3 Coming Soon</h2>"

@app.route("/script4")
def script4():
    return "<h2>🧠 Script 4 Coming Soon</h2>"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
