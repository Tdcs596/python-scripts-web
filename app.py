from flask import Flask, render_template_string
import os

# Import Blueprints
from script1 import script1_bp
from script2 import script2_bp
from script3 import script3_bp
from script4 import script4_bp
from script5 import script5_bp
from script6 import script6_bp
from script7 import script7_bp
from script8 import script8_bp
from script9 import script9_bp
from script10 import script10_bp
from script11 import script11_bp
from script12 import script12_bp
from script15 import script15_bp
from script16 import script16_bp
from script17 import script17_bp

app = Flask(__name__)
# Ye line ensure karegi ki /script17 aur /script17/ dono chalein
app.url_map.strict_slashes = False

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Shivam Singh - Master Dashboard</title>
        <style>
            body { background: #050505; color: #ff0000; font-family: 'Consolas', monospace; text-align: center; padding: 50px; }
            .btn { background: #111; border: 1px solid #ff0000; color: #ff0000; padding: 15px; width: 250px; 
                   margin: 10px; cursor: pointer; font-weight: bold; transition: 0.3s; border-radius: 5px; }
            .btn:hover { background: #ff0000; color: #000; box-shadow: 0 0 20px #ff0000; }
            h1 { color: #fff; text-shadow: 0 0 10px #ff0000; letter-spacing: 2px; }
            .sub { color: #666; margin-bottom: 30px; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>💀 SHIVAM SINGH OMEGA DASHBOARD 💀</h1>
        <p class="sub">PRIVATE CYBERSECURITY & UTILITY PANEL</p>
        <div style="display: flex; flex-wrap: wrap; justify-content: center;">
            <a href="/script1/"><button class="btn">Open Analyzer</button></a>
            <a href="/script2/"><button class="btn">Open Scraper</button></a>
            <a href="/script3/"><button class="btn">Open EXE Converter</button></a>
            <a href="/script4/"><button class="btn">DDoS Lab</button></a>
            <a href="/script5/"><button class="btn">Ping Tool</button></a>
            <a href="/script6/"><button class="btn">Video Call</button></a>
            <a href="/script7/"><button class="btn">VoIP Call</button></a>
            <a href="/script8/"><button class="btn">Phone OSINT</button></a>
            <a href="/script9/"><button class="btn">Private Call</button></a>
            <a href="/script10/"><button class="btn">CCTV Cam / SMS Flooder</button></a>
            <a href="/script11/"><button class="btn">Mail Spoofing</button></a>
            <a href="/script12/"><button class="btn">Nmap Scanner</button></a>
            <a href="/script15/"><button class="btn">Nu Attack</button></a>
            <a href="/script16/"><button class="btn">Vehicle Info</button></a>
            <a href="/script17/"><button class="btn">SHIVAM VAULT (ENCRYPTION)</button></a>
        </div>
    </body>
    </html>
    """

# --- BLUEPRINT REGISTRATION ---
app.register_blueprint(script1_bp, url_prefix='/script1')
app.register_blueprint(script2_bp, url_prefix='/script2')
app.register_blueprint(script3_bp, url_prefix='/script3')
app.register_blueprint(script4_bp, url_prefix='/script4')
app.register_blueprint(script5_bp, url_prefix='/script5')
app.register_blueprint(script6_bp, url_prefix='/script6')
app.register_blueprint(script7_bp, url_prefix='/script7')
app.register_blueprint(script8_bp, url_prefix='/script8')
app.register_blueprint(script9_bp, url_prefix='/script9')
app.register_blueprint(script10_bp, url_prefix='/script10')
app.register_blueprint(script11_bp, url_prefix='/script11')
app.register_blueprint(script12_bp, url_prefix='/script12')
app.register_blueprint(script15_bp, url_prefix='/script15')
app.register_blueprint(script16_bp, url_prefix='/script16')
app.register_blueprint(script17_bp, url_prefix='/script17')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
