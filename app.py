from flask import Flask
from script1 import script1_bp # Import kiya
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
# from script13 import script13_bp
# from script14 import script14_bp
from script15 import script15_bp
from script16 import script16_bp

app = Flask(__name__)

# Main Dashboard
@app.route("/")
def home():
    return """
    <h1>🔥 Master Dashboard</h1>
    <a href="/script1"><button>Open Analyzer</button></a><br><br>
    <a href="/script2"><button>Open Scraper</button></a><br><br>
    <a href="/script3"><button>Open EXE Converter</button></a><br><br>
    <a href="/script4"><button>DDoS Lab</button></a><br><br>
    <a href="/script5"><button>Ping</button></a><br><br>
    <a href="/script6"><button>Video Call</button></a><br><br>
    <a href="/script7"><button>Voipe Call</button></a><br><br>
    <a href="/script8"><button>Phone OSINT</button></a><br><br>
    <a href="/script9"><button>Private call</button></a><br><br>
    <a href="/script10"><button>Cctv Cam</button></a><br><br>
    <a href="/script11"><button>Mail Spoofing</button></a><br><br>
    <a href="/script12"><button>Nmap</button></a><br><br>
    <a href="/script13"><button>ngg</button></a><br><br>
    <a href="/script14"><button>nmmm</button></a><br><br>
    <a href="/script15"><button>Nu Att</button></a><br><br>
    <a href="/script16"><button>Veh</button></a>   
    """

# Yahan Script ko "Register" kiya
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
# app.register_blueprint(script13_bp, url_prefix='/script13')
# app.register_blueprint(script14_bp, url_prefix='/script14')
app.register_blueprint(script15_bp, url_prefix='/script15')
app.register_blueprint(script16_bp, url_prefix='/script16')

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
