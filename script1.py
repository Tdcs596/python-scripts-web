from flask import Blueprint, request

# Blueprint define kiya
script1_bp = Blueprint('script1', __name__)

def run_logic(url):
    # Tera purana logic yahan rahega
    import requests
    try:
        res = requests.get(url, timeout=5)
        return f"Status: {res.status_code} | Size: {len(res.text)} bytes"
    except Exception as e:
        return str(e)

@script1_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        result = run_logic(url)
    
    # Iska apna alag HTML interface
    return f"""
    <h2>🌐 Website Analyzer (Script 1)</h2>
    <form method="POST">
        <input name="url" placeholder="https://example.com" required>
        <button type="submit">Analyze</button>
    </form>
    <br><pre>{result}</pre>
    <br><a href="/">Back to Main Dashboard</a>
    """
