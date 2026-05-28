from flask import Blueprint, render_template_string, request, jsonify

script29_bp = Blueprint('script29', __name__)

# --- GHOST TERMINAL IP LOOKUP UI (FORTIFIEDBYTES V2 ULTRA-ENGINE) ---
LOOKUP_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost IP Tracker | Fortifiedbytes Intel Node</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #020408; color: #38bdf8; font-family: 'Consolas', 'Courier New', monospace; padding: 30px 15px; text-align: center; }
        .container { display: inline-block; width: 100%; max-width: 850px; text-align: left; }
        .box { border: 2px solid #38bdf8; background: #000; padding: 35px; box-shadow: 0 0 40px rgba(56, 189, 248, 0.15); border-radius: 14px; position: relative; }
        .box::before { content: '⚡ FORTIFIEDBYTES IP INTEL EDGE TUNNEL ACTIVE'; position: absolute; top: -11px; right: 20px; background: #38bdf8; color: #000; font-size: 11px; padding: 2px 10px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
        .header { text-align: center; border-bottom: 1px dashed #1e293b; padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #38bdf8; font-size: 24px; letter-spacing: 1px; }
        .subtitle { color: #475569; font-size: 12px; margin-top: 5px; letter-spacing: 2px; text-transform: uppercase; }
        
        label { font-size: 11px; color: #0284c7; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-top: 15px; margin-bottom: 6px; font-weight: bold; }
        .input-group { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 14px; background: #050b14; border: 1px solid #0f355c; color: #fff; border-radius: 6px; outline: none; font-size: 14px; font-family: inherit; transition: 0.3s; }
        input:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.15); }
        
        button { padding: 14px 28px; background: #38bdf8; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 6px; font-size: 14px; transition: 0.2s; letter-spacing: 1px; text-transform: uppercase; font-family: inherit; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; transform: translateY(-1px); }
        
        #console-status { margin-top: 20px; padding: 14px; border-radius: 6px; background: #050505; border: 1px solid #111; font-size: 13px; display: none; text-align: left; line-height: 1.6; }
        .error-banner { color: #ef4444; border-color: #7f1d1d !important; background: #450a0a !important; padding: 14px; border-radius: 6px; border: 1px solid; margin-top: 20px; text-align: left; font-size: 13px; }

        /* Result Grid Style */
        .result-container { margin-top: 25px; display: none; animation: fadeIn 0.5s ease; }
        .result-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 15px; }
        .result-card { background: #040814; border: 1px solid #0f2440; padding: 15px; border-radius: 8px; }
        .card-label { font-size: 10px; color: #475569; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
        .card-value { font-size: 14px; color: #fff; font-weight: bold; word-break: break-all; }
        .highlight { color: #f43f5e; }
        .highlight-green { color: #10b981; }
        
        .map-btn { display: inline-block; width: 100%; text-align: center; padding: 12px; background: #1e1b4b; border: 1px solid #3730a3; color: #818cf8; font-weight: bold; border-radius: 6px; text-decoration: none; margin-top: 20px; transition: 0.3s; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
        .map-btn:hover { background: #3730a3; color: #fff; box-shadow: 0 0 15px rgba(99, 102, 241, 0.4); }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .warning { font-size: 11px; color: #334155; margin-top: 25px; text-align: center; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="header">
                <h2>🛰️ GHOST ADVANCED IP TRACKER BLOCK</h2>
                <p class="subtitle">FORTIFIEDBYTES OMEGA DASHBOARD • SCRIPT29 SYSTEM</p>
            </div>

            <form id="lookupForm" onsubmit="event.preventDefault(); executeIpScan();">
                <label for="ipInput">Target IPv4 / IPv6 Address</label>
                <div class="input-group">
                    <input type="text" id="ipInput" placeholder="e.g., 8.8.8.8, 103.241.x.x (Blank chhodoge toh khud ki IP trace hogi)" autocomplete="off">
                    <button type="submit" id="submitBtn">🚀 Scan IP Network</button>
                </div>
            </form>

            <div id="console-status">System primed. Awaiting targets...</div>

            <div class="result-container" id="resultBlock">
                <div class="result-grid">
                    <div class="result-card" style="grid-column: span 2; border-color: #38bdf8;">
                        <div class="card-label">Target IP Node</div>
                        <div class="card-value highlight-green" id="resIp" style="font-size: 18px;">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">ISP Network Owner</div>
                        <div class="card-value" id="resIsp">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Organization / Business</div>
                        <div class="card-value" id="resOrg">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Autonomous System (ASN)</div>
                        <div class="card-value highlight" id="resAsn">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Country Code</div>
                        <div class="card-value" id="resCountry">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">State / Region</div>
                        <div class="card-value" id="resRegion">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">City Zone</div>
                        <div class="card-value" id="resCity">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Postal / Zip Code</div>
                        <div class="card-value" id="resZip">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Timezone Sector</div>
                        <div class="card-value" id="resTimezone">-</div>
                    </div>
                    <div class="result-card">
                        <div class="card-label">Geo Matrix (Lat / Long)</div>
                        <div class="card-value" id="resCoords">-</div>
                    </div>
                </div>

                <a href="#" id="resMapLink" target="_blank" class="map-btn">📍 Open Coordinates Target on Google Maps</a>
            </div>

            <div class="warning">ANTI-LOG PROTOCOL • DIRECT RESIDENTIAL BROWSER SOCKET TUNNELING</div>
        </div>
    </div>

    <script>
        async function executeIpScan() {
            const ipInput = document.getElementById('ipInput').value.trim();
            const consoleStatus = document.getElementById('console-status');
            const resultBlock = document.getElementById('resultBlock');
            const submitBtn = document.getElementById('submitBtn');

            submitBtn.disabled = true;
            resultBlock.style.display = "none";
            consoleStatus.className = "";
            consoleStatus.style.display = "block";
            consoleStatus.style.color = "#eab308";
            consoleStatus.innerHTML = "⏳ Establishing direct browser socket tunnel...<br>⏳ Bypassing cloud datacenter firewalls...<br>⏳ Streaming real-time carrier nodes & ASN matrix data...";

            try {
                // LAYER 1: Hit premium ipwho.is client-side endpoint (No cloud blocks)
                const targetUrl = `https://ipwho.is/${ipInput}`;
                const res = await fetch(targetUrl);
                const data = await res.json();

                if(data.success === true) {
                    consoleStatus.style.display = "none";
                    resultBlock.style.display = "block";

                    document.getElementById('resIp').innerText = data.ip || 'N/A';
                    document.getElementById('resIsp').innerText = data.isp || 'N/A';
                    document.getElementById('resOrg').innerText = data.org || 'N/A';
                    document.getElementById('resAsn').innerText = data.asn || 'N/A';
                    document.getElementById('resCountry').innerText = `${data.country || 'N/A'} (${data.country_code || 'N/A'})`;
                    document.getElementById('resRegion').innerText = data.region || 'N/A';
                    document.getElementById('resCity').innerText = data.city || 'N/A';
                    document.getElementById('resZip').innerText = data.postal || 'N/A';
                    document.getElementById('resTimezone').innerText = `${data.timezone || 'N/A'} (${data.timezone_gmt || ''})`;
                    document.getElementById('resCoords').innerText = `${data.latitude} / ${data.longitude}`;
                    
                    document.getElementById('resMapLink').href = `https://www.google.com/maps?q=${data.latitude},${data.longitude}`;
                    return;
                } else {
                    throw new Error(data.message || "Invalid target configuration.");
                }
            } catch (e) {
                // LAYER 2: Emergency Fail-safe Fallback directly inside the client browser
                try {
                    const fallbackUrl = `https://ipapi.co/${ipInput ? ipInput + '/' : ''}json/`;
                    const resBackup = await fetch(fallbackUrl);
                    const dataBackup = await resBackup.json();
                    
                    if(!dataBackup.error) {
                        consoleStatus.style.display = "none";
                        resultBlock.style.display = "block";

                        document.getElementById('resIp').innerText = dataBackup.ip || 'N/A';
                        document.getElementById('resIsp').innerText = dataBackup.org || 'N/A';
                        document.getElementById('resOrg').innerText = dataBackup.asn || 'N/A';
                        document.getElementById('resAsn').innerText = dataBackup.asn || 'N/A';
                        document.getElementById('resCountry').innerText = `${dataBackup.country_name || 'N/A'} (${dataBackup.country_code || 'N/A'})`;
                        document.getElementById('resRegion').innerText = dataBackup.region || 'N/A';
                        document.getElementById('resCity').innerText = dataBackup.city || 'N/A';
                        document.getElementById('resZip').innerText = dataBackup.postal || 'N/A';
                        document.getElementById('resTimezone').innerText = dataBackup.timezone || 'N/A';
                        document.getElementById('resCoords').innerText = `${dataBackup.latitude} / ${dataBackup.longitude}`;
                        
                        document.getElementById('resMapLink').href = `https://www.google.com/maps?q=${dataBackup.latitude},${dataBackup.longitude}`;
                        return;
                    }
                } catch(backupErr) {}

                consoleStatus.className = "error-banner";
                consoleStatus.innerHTML = `❌ DISCOVERY ERROR: Both secure network streams were rate-limited or target IP structure is faulty.`;
            } finally {
                submitBtn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@script29_bp.route('/')
def index():
    return render_template_string(LOOKUP_UI)

# Keeping the endpoint active as a standard blueprint template format
@script29_bp.route('/scan', methods=['POST'])
def scan_ip():
    return jsonify({"status": "error", "message": "Deprecated server route. UI safely shifted to Client-Side Edge Tunnel."}), 400

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script29_bp, url_prefix='/script29')
    app.run(debug=True, port=5001)

