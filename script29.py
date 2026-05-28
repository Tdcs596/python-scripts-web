from flask import Blueprint, render_template_string, request, jsonify
import requests

script29_bp = Blueprint('script29', __name__)

# --- GHOST TERMINAL IP LOOKUP UI (FORTIFIEDBYTES EDITION) ---
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
        .box::before { content: '⚡ FORTIFIEDBYTES IP INTEL WIRE ACTIVE'; position: absolute; top: -11px; right: 20px; background: #38bdf8; color: #000; font-size: 11px; padding: 2px 10px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
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
        .error-banner { color: #ef4444; border-color: #7f1d1d !important; background: #450a0a !important; padding: 14px; border-radius: 6px; border: 1px solid; margin-top: 20px; text-align: left;}

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

            <div class="warning">ANTI-LOG PROTOCOL • DIRECT DEEP SCAN PARSING ACTIVATED</div>
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
            consoleStatus.innerHTML = "⏳ Injecting lookup stream on global geo-IP servers...<br>⏳ Extracting ASN matrix, carrier networks, and routing layouts safely...";

            try {
                const res = await fetch('/script29/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ ip: ipInput })
                });

                const data = await res.json();

                if(res.ok && data.status === "success") {
                    consoleStatus.style.display = "none";
                    resultBlock.style.display = "block";

                    document.getElementById('resIp').innerText = data.data.ip || 'N/A';
                    document.getElementById('resIsp').innerText = data.data.isp || 'N/A';
                    document.getElementById('resOrg').innerText = data.data.org || 'N/A';
                    document.getElementById('resAsn').innerText = data.data.asn || 'N/A';
                    document.getElementById('resCountry').innerText = `${data.data.country || 'N/A'} (${data.data.country_code || 'N/A'})`;
                    document.getElementById('resRegion').innerText = data.data.region || 'N/A';
                    document.getElementById('resCity').innerText = data.data.city || 'N/A';
                    document.getElementById('resZip').innerText = data.data.postal || 'N/A';
                    document.getElementById('resTimezone').innerText = data.data.timezone || 'N/A';
                    document.getElementById('resCoords').innerText = `${data.data.lat} / ${data.data.lon}`;
                    
                    document.getElementById('resMapLink').href = `https://www.google.com/maps/search/?api=1&query=${data.data.lat},${data.data.lon}`;
                } else {
                    consoleStatus.className = "error-banner";
                    consoleStatus.innerHTML = `❌ DISCOVERY ERROR: ${data.message}`;
                }
            } catch (e) {
                consoleStatus.className = "error-banner";
                consoleStatus.innerHTML = "❌ EXCEPTION: Node connection lost or response structure unreadable.";
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

@script29_bp.route('/scan', methods=['POST'])
def scan_ip():
    try:
        req_data = request.get_json() or {}
        target_ip = req_data.get('ip', '').strip()

        payload = None
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        # --- LAYER 1: IP-API.COM (PRIMARY SCANNER WITH EXCEPTION CATCH) ---
        try:
            url1 = f"http://ip-api.com/json/{target_ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
            res1 = requests.get(url1, headers=headers, timeout=6)
            if res1.status_code == 200:
                raw_res = res1.json()
                if raw_res.get('status') == 'success':
                    payload = {
                        "ip": raw_res.get('query'),
                        "isp": raw_res.get('isp', 'N/A'),
                        "org": raw_res.get('org', 'N/A'),
                        "asn": raw_res.get('as', 'N/A'),
                        "country": raw_res.get('country', 'N/A'),
                        "country_code": raw_res.get('countryCode', 'N/A'),
                        "region": raw_res.get('regionName', 'N/A'),
                        "city": raw_res.get('city', 'N/A'),
                        "postal": raw_res.get('zip', 'N/A'),
                        "timezone": raw_res.get('timezone', 'N/A'),
                        "lat": raw_res.get('lat', '0.0'),
                        "lon": raw_res.get('lon', '0.0')
                    }
        except Exception:
            pass  # Fail-safe protection triggered, skips to Layer 2

        # --- LAYER 2: IPAPI.CO (BACKUP SCANNER) ---
        if not payload:
            try:
                url2 = f"https://ipapi.co/{target_ip}/json/" if target_ip else "https://ipapi.co/json/"
                res2 = requests.get(url2, headers=headers, timeout=6)
                if res2.status_code == 200:
                    backup_res = res2.json()
                    if "error" not in backup_res:
                        payload = {
                            "ip": backup_res.get('ip', target_ip),
                            "isp": backup_res.get('org', 'Unknown Carrier'),
                            "org": backup_res.get('asn', 'Commercial Node'),
                            "asn": backup_res.get('asn', 'N/A'),
                            "country": backup_res.get('country_name', 'N/A'),
                            "country_code": backup_res.get('country_code', 'N/A'),
                            "region": backup_res.get('region', 'N/A'),
                            "city": backup_res.get('city', 'N/A'),
                            "postal": backup_res.get('postal', 'N/A'),
                            "timezone": backup_res.get('timezone', 'N/A'),
                            "lat": backup_res.get('latitude', '0.0'),
                            "lon": backup_res.get('longitude', '0.0')
                        }
            except Exception:
                pass

        # --- LAYER 3: IP.SEEIP.ORG & GEOPLUGIN (EMERGENCY ULTRA-BYPASS LAYER) ---
        if not payload:
            try:
                # Agar input target_ip blank h, toh pehle server public IP nikalo
                working_ip = target_ip if target_ip else requests.get("https://ip.seeip.org", timeout=4).text.strip()
                url3 = f"http://www.geoplugin.net/json.gp?ip={working_ip}"
                res3 = requests.get(url3, timeout=6)
                if res3.status_code == 200:
                    g_res = res3.json()
                    payload = {
                        "ip": working_ip,
                        "isp": g_res.get('geoplugin_credit', 'Emergency Infrastructure Node'),
                        "org": "Multi-Route Secure Node",
                        "asn": "N/A",
                        "country": g_res.get('geoplugin_countryName', 'N/A'),
                        "country_code": g_res.get('geoplugin_countryCode', 'N/A'),
                        "region": g_res.get('geoplugin_regionName', 'N/A'),
                        "city": g_res.get('geoplugin_city', 'N/A'),
                        "postal": "N/A",
                        "timezone": g_res.get('geoplugin_timezone', 'N/A'),
                        "lat": g_res.get('geoplugin_latitude', '0.0'),
                        "lon": g_res.get('geoplugin_longitude', '0.0')
                    }
            except Exception as e:
                return jsonify({"status": "error", "message": f"All fallback routing nodes are currently rate-limited. Try after 2 minutes. Internal Error: {str(e)}"}), 500

        if payload:
            return jsonify({"status": "success", "data": payload})
        else:
            return jsonify({"status": "error", "message": "Failed to decode response architecture from scanning clusters."}), 400

    except Exception as main_err:
        return jsonify({"status": "error", "message": f"Global core thread fault: {str(main_err)}"}), 500

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script29_bp, url_prefix='/script29')
    app.run(debug=True, port=5001)
