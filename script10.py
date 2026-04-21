from flask import Flask, render_template_string
from script10 import script10_bp

app = Flask(__name__)

# Register blueprint
app.register_blueprint(script10_bp, url_prefix='/script10')

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html><head><title>PENTEST HUB</title>
<style>body{background:#000;color:#0f0;font-family:monospace;padding:50px}
a{display:block;margin:20px;padding:20px;border:2px solid #0f0;color:#0f0;text-decoration:none;font-size:24px}
a:hover{background:#0f0;color:#000}</style></head>
<body>
<h1>🔥 PENTEST TOOLS</h1>
<a href="/script10">💣 SMS BOMBER</a>
<p><b>Check Render Logs for SMS hits!</b></p>
</body></html>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
