from flask import Flask, request, send_file
import os
import script1 as s1
import script2 as s2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SCRIPTS = {
    "script1": "🌐 Website Analyzer",
    "script2": "⚡ PY to EXE Converter",
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
    """


# 🔥 SCRIPT2 (UPLOAD + CONVERT + DOWNLOAD)
@app.route("/script2", methods=["GET", "POST"])
def script2():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return "❌ No file selected"

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        result = s2.convert(filepath)

        # अगर exe बना
        if result.endswith(".exe") and os.path.exists(result):
            return send_file(result, as_attachment=True)

        return f"<pre>{result}</pre><br><a href='/script2'>Back</a>"

    return """
    <h2>⚡ PY to EXE Converter</h2>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".py" required>
        <br><br>
        <button>Convert</button>
    </form>

    <br><a href="/">🏠 Home</a>
    """


# बाकी placeholder
@app.route("/script3")
def script3():
    return "<h2>🚀 Script 3 Coming Soon</h2><br><a href='/'>Home</a>"

@app.route("/script4")
def script4():
    return "<h2>🧠 Script 4 Coming Soon</h2><br><a href='/'>Home</a>"


# RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
