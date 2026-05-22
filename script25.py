from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json
import urllib.parse

script25_bp = Blueprint('script25', __name__)

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>CELL_RESOLVER_NO_API</title>
    <style>
        body { background: #06090e; color: #00ffcc; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .box { border: 2px solid #00ffcc; background: #000; padding: 25px; box-shadow: 0 0 25px #00ffcc33; display: inline-block; width: 95%; max-width: 650px; border-radius: 12px; text-align: left; }
        .header { text-align: center; border-bottom: 1px solid #00ffcc; padding-bottom: 15px; margin-bottom: 20px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 10px #00ffcc; }
        .grid-inputs { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .input-block { display: flex; flex-direction: column; }
        label { font-size: 13px; color: #557099; margin-bottom: 5px; }
        input { padding: 10px; background: #111; border: 1px solid #00ffcc; color: #fff; font-size: 15px; border-radius: 5px; outline: none; }
        .btn-container { text-align: center; }
        button { padding: 12px 35px; background: #00ffcc; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 15px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #status { margin: 15px 0; color: #ffeb3b; text-align: center; display: none; }
        .result-display { margin-top: 25px; background: #05070a; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; display: none; }
        .map-link { display: inline-block; margin-top: 10px; background: #ffb700; color: #000; padding: 8px 15px; border-radius: 4px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <div class="header">
            <h2>📡 PUBLIC CELL RESOLVER v25 (Bina API Key)</h2>
            <p style="color: #557099; margin: 5px 0 0 0;">SHIVAM SINGH OMEGA DASHBOARD • OPEN SOURCE INTEL</p>
        </div>

        <div class="grid-inputs">
            <div class="input-block">
                <label>MCC (Country Code - e.g., 404)</label>
                <input type="number" id="mcc" value="404">
            </div>
            <div class="input-block">
                <label>MNC (Network Code - e.g., 45)</label>
                <input type="number" id="mnc" value="45">
            </div>
            <div class="input-block">
                <label>LAC (Location Area Code)</label>
                <input type="number" id="lac" placeholder="e.g., 901">
            </div>
            <div class="input-block">
                <label>Cell ID (CID)</label>
                <input type="number" id="cid" placeholder="e.g., 4321">
            </div>
        </div>

        <div class="btn-container">
            <button onclick="locateCellTower()">SCRAPE & RESOLVE LOCATION</button>
        </div>

        <div id="status">📡 PARSING OPEN CELL REGISTRY WITHOUT KEYS...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function locateCellTower() {
            const mcc = document.getElementById('mcc').value;
            const mnc = document.getElementById('mnc').value;
            const lac = document.getElementById('lac').value;
            const cid = document.getElementById('cid').value;
            
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!mcc || !mnc || !lac || !cid) return alert("Bhai, sab bharo pehle!");

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script25/free_locate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mcc: mcc, mnc: mnc, lac: lac, cid: cid })
                });
                const data = await res.json();
                status.style.display = "none";

                if(data.status === "error") {
                    resultBox.innerHTML = "<p style='color:red;'>❌ ERROR: " + data.message + "</p>";
                } else if(data.status === "success") {
                    resultBox.innerHTML = "<h3 style='color:#fff; margin-top:0;'>📍 Location Scraping Successful!</h3>" +
                        "<p><strong>Latitude:</strong> " + data.lat + "</p>" +
                        "<p><strong>Longitude:</strong> " + data.lon + "</p>" +
                        "<p><strong>Radio Type:</strong> GSM / LTE Mode</p>" +
                        '<a href="https://www.google.com/maps?q=' + data.lat + ',' + data.lon + '" target="_blank" class="map-link">🗺️ VIEW ON GOOGLE MAPS</a>';
                } else {
                    resultBox.innerHTML = "<p style='color:#ffb700;'>Data not found for this tower signature in open source pool.</p>";
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Local Scraper Node Offline!";
            }
        }
    </script>
</body>
</html>
"""

@script25_bp.route('/')
def index():
    return render_template_string(UI)

@script25_bp.route('/free_locate', methods=['POST'])
def free_locate():
    req_data = request.json
    mcc = str(req_data.get('mcc'))
    mnc = str(req_data.get('mnc'))
    lac = str(req_data.get('lac'))
    cid = str(req_data.get('cid'))
    
    try:
        # Open source database gateway call without personal credentials
        conn = http.client.HTTPSConnection("opencellid.org")
        
        # Public payload endpoint binding
        query_path = f"/ajax/searchCell.php?mcc={mcc}&mnc={mnc}&lac={lac}&cellid={cid}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        conn.request("GET", query_path, headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        
        if res.status != 200 or not raw_data:
            return jsonify({"status": "error", "message": f"Server Refused Connection (Status: {res.status})"})
            
        parsed = json.loads(raw_data)
        
        # Check if the platform found the row coordinates
        if parsed and "lat" in parsed and float(parsed["lat"]) != 0:
            return jsonify({
                "status": "success",
                "lat": parsed["lat"],
                "lon": parsed["lon"]
            })
        else:
            return jsonify({"status": "not_found"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
