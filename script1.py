from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>🌐 Script 1 - URL Scanner</h2>

    <form method="POST" action="/run">
        <input name="url" placeholder="Enter URL" required>
        <button>Scan</button>
    </form>
    """


@app.route("/run", methods=["POST"])
def run():
    url = request.form.get("url")
    return f"""
    <h3>Scanning Result</h3>
    <p>URL: {url}</p>
    """


if __name__ == "__main__":
    app.run(port=5001)
