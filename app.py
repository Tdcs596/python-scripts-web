from flask import Flask, render_template_string
import os

# Blueprints Import Karein
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
from script18 import script18_bp # <-- Naya Script Import
from script19 import script19_bp
from script20 import script20_bp

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Shivam Singh Dashboard</title>
        <style>
            body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 40px; }
            .btn { background: transparent; border: 1px solid #00ff00; color: #00ff00; padding: 15px; width: 260px; 
                   margin: 10px; cursor: pointer; font-weight: bold; transition: 0.3s; }
            .btn:hover { background: #00ff00; color: #000; box-shadow: 0 0 15px #00ff00; }
            h1 { text-shadow: 0 0 10px #00ff00; }
        </style>
    </head>
    <body>
        <h1>[ SHIVAM SINGH OMEGA DASHBOARD ]</h1>
        <div style="display: flex; flex-wrap: wrap; justify-content: center;">
            <a href="/script1/"><button class="btn">Open Analyzer</button></a>
            <a href="/script2/"><button class="btn">Open Scraper</button></a>
            <a href="/script3/"><button class="btn">EXE Converter</button></a>
            <a href="/script4/"><button class="btn">DDoS Lab</button></a>
            <a href="/script5/"><button class="btn">Ping Tool</button></a>
            <a href="/script6/"><button class="btn">Video Call</button></a>
            <a href="/script7/"><button class="btn">VoIP Call</button></a>
            <a href="/script8/"><button class="btn">Phone OSINT</button></a>
            <a href="/script9/"><button class="btn">Private Call</button></a>
            <a href="/script10/"><button class="btn">Spy Cam</button></a>
            <a href="/script11/"><button class="btn">Mail Spoofing</button></a>
            <a href="/script12/"><button class="btn">Nmap Scanner</button></a>
            <a href="/script15/"><button class="btn">Nu Attack</button></a>
            <a href="/script16/"><button class="btn">Vehicle Info</button></a>
            <a href="/script17/"><button class="btn">Message Vault</button></a>
            <a href="/script18/"><button class="btn" style="border-width: 2px;">FILE VAULT (PRIVATE)</button></a>
            <a href="/script19/"><button class="btn">Jarvis</button></a>
            <a href="/script20/"><button class="btn">Jarvis</button></a>
        </div>
    </body>
    </html>
    """

# Blueprints Register Karein
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
app.register_blueprint(script18_bp, url_prefix='/script18') # <-- Naya Register
app.register_blueprint(script19_bp, url_prefix='/script19')
app.register_blueprint(script20_bp, url_prefix='/script20')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
