from flask import Flask
from script1 import script1_bp # Import kiya
# from script2 import script2_bp (Aise hi baki bhi)

app = Flask(__name__)

# Main Dashboard
@app.route("/")
def home():
    return """
    <h1>🔥 Master Dashboard</h1>
    <a href="/script1"><button>Open Analyzer</button></a><br><br>
    <a href="/script2"><button>Open Scraper</button></a>
    """

# Yahan Script ko "Register" kiya
app.register_blueprint(script1_bp, url_prefix='/script1')

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
