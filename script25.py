from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script25_bp = Blueprint('script25', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "cellid-geolocation-api.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>CELL_GEOLOCATION_v25</title>
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
        .debug-console { background: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; font-size: 12px; color: #aaa; overflow-x: auto; margin-top: 15px; text-align: left; }
    </style>
</head>
<body>
    <div class="box">
        <div class="header">
            <h2>🛰️ CELL GEOLOCATION INTEL NODE v25</h2>
            <p style="color: #557099; margin: 5px 0 0 0;">SHIVAM SINGH OMEGA DASHBOARD • RAPIDAPI CORE</p>
        </div>

        <div class="grid-inputs">
            <div class="input-block">
                <label>MCC (Mobile Country Code)</label>
                <input type="number" id="mcc" value="262">
            </div>
            <div class="input-block">
                <label>MNC (Mobile Network Code)</label>
                <input type="number" id="mnc" value="2">
            </div>
            <div class="input-block">
                <label>LAC (Location Area Code)</label>
                <input type="number" id="lac" value="801">
            </div>
            <div class="input-block">
                <label>Cell ID (CID)</label>
                <input type="number" id="cid" value="86355">
            </div>
        </div>

        <div class="btn-container">
            <button onclick="resolveCellTower()">RESOLVE VIA RAPIDAPI</button>
        </div>

        <div id="status">📡 INTERROGATING SECURE CELLID GEOLOCATION GATEWAY...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function resolveCellTower() {
            const mcc = document.getElementById('mcc').value;
            const mnc = document.getElementById('mnc').value;
            const lac = document.getElementById('lac').value;
            const cid = document.getElementById('cid').value;
            
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!mcc || !mnc || !lac || !cid) return alert("Bhai, saare fields bharo!");

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script25/rapid_locate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mcc: mcc, mnc: mnc, lac: lac, cid: cid })
                });
                const data = await res.json();
                status.style.display = "none";

                if (data.status === "error") {
                    resultBox.innerHTML = "<p style='color:red;'>❌ ERROR: " + data.message + "</p>";
                } else if (data.lat || data.latitude || data.location) {
                    // Coordinates Extract karne ke alag alag methods map kiye hain
                    let finalLat = data.lat || data.latitude;
                    let finalLon = data.lon || data.longitude;
                    
                    // Agar API nested response deti hai (e.g., data.location.lat)
                    if (data.location && typeof data.location === 'object') {
                        finalLat = data.location.lat || data.location.latitude;
                        finalLon = data.location.lon || data.location.longitude;
                    }
                    
                    const accuracy = data.accuracy || data.range || 'N/A';
                    
                    resultBox.innerHTML = "<h3 style='color:#fff; margin-top:0;'>📍 Tower Located Successfully!</h3>" +
                        "<p><strong>Latitude:</strong> " + finalLat + "</p>" +
                        "<p><strong>Longitude:</strong> " + finalLon + "</p>" +
                        "<p><strong>Accuracy Radius:</strong> " + accuracy + " meters</p>" +
                        '<a href="https://www.google.com/maps?q=' + finalLat + ',' + finalLon + '" target="_blank" class="map-link">🗺️ OPEN IN GOOGLE MAPS</a>';
                } else {
                    // Agar parameters database mein register nahi hain toh complete dump window khulegi
                    resultBox.innerHTML = "<p style='color:#ffb700; text-align:center;'>⚠️ API Parameter Mismatch or Data Not Found.</p>" +
                        "<div class='debug-console'>" +
                        "<strong>Raw API Server Response:</strong><br><pre>" + JSON.stringify(data, null, 2) + "</pre>" +
                        "</div>";
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Connection to RapidAPI Proxy Node Failed!";
            }
        }
    </script>
</body>
</html>
"""

@script25_bp.route('/')
def index():
    return render_template_string(UI)

@script25_bp.route('/rapid_locate', methods=['POST'])
def rapid_locate():
    req_data = request.json
    mcc = str(req_data.get('mcc'))
    mnc = str(req_data.get('mnc'))
    lac = str(req_data.get('lac'))
    cid = str(req_data.get('cid'))
    
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        
        # Exact API endpoint string format setup
        query_path = f"/query?mcc={mcc}&mnc={mnc}&lac={lac}&cid={cid}"
        
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }
        
        conn.request("GET", query_path, headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        
        if res.status != 200:
            return jsonify({"status": "error", "message": f"RapidAPI Server Error (Status Code: {res.status})"})
            
        try:
            parsed_json = json.loads(raw_data)
            return jsonify(parsed_json)
        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": f"Server sent plain string: {raw_data[:100]}"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
