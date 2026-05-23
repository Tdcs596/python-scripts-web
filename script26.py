from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script26_bp = Blueprint('script26', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "mac-address-lookup3.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>MAC_LOOKUP_v26</title>
    <style>
        body { background: #07090e; color: #00ffcc; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .box { border: 2px solid #00ffcc; background: #000; padding: 25px; box-shadow: 0 0 25px #00ffcc33; display: inline-block; width: 95%; max-width: 650px; border-radius: 12px; text-align: left; }
        .header { text-align: center; border-bottom: 1px solid #00ffcc; padding-bottom: 15px; margin-bottom: 20px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 10px #00ffcc; }
        .input-group { text-align: center; margin-bottom: 20px; }
        input { width: 80%; padding: 12px; background: #111; border: 1px solid #00ffcc; color: #fff; font-size: 16px; border-radius: 5px; outline: none; text-align: center; letter-spacing: 2px; }
        button { padding: 12px 35px; background: #00ffcc; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 15px; margin-top: 15px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #status { margin: 15px 0; color: #ffeb3b; text-align: center; display: none; }
        .result-display { margin-top: 25px; background: #05070a; border: 1px dashed #00ffcc; padding: 15px; border-radius: 8px; display: none; }
        .debug-console { background: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; font-size: 12px; color: #aaa; overflow-x: auto; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="header">
            <h2>🔍 MAC ADDRESS INTELLIGENCE NODE v26</h2>
            <p style="color: #557099; margin: 5px 0 0 0;">SHIVAM SINGH OMEGA DASHBOARD • OUI OVERSIGHT</p>
        </div>

        <div class="input-group">
            <input type="text" id="mac_input" placeholder="00:23:AB:00:00:00 or 0023AB000000" value="0023AB000000">
            <br>
            <button onclick="lookupMacAddress()">RESOLVE VENDOR DATA</button>
        </div>

        <div id="status">📡 QUERYING MAC OUI MANUFACTURER REGISTRIES...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function lookupMacAddress() {
            let mac = document.getElementById('mac_input').value.trim();
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!mac) return alert("Bhai, MAC Address toh daal!");

            // Clean spaces or hyphens just in case
            mac = mac.replace(/[:\\s-]/g, '');

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script26/lookup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mac_address: mac })
                });
                const data = await res.json();
                status.style.display = "none";

                if (data.status === "error") {
                    resultBox.innerHTML = "<p style='color:red;'>❌ ERROR: " + data.message + "</p>";
                } else if (data.companyName || data.company || data.vendor) {
                    // API signature checks
                    const company = data.companyName || data.company || data.vendor;
                    const address = data.companyAddress || data.address || 'Not Provided';
                    const prefix = data.macPrefix || data.oui || 'N/A';
                    
                    resultBox.innerHTML = "<h3 style='color:#fff; margin-top:0;'>✅ Vendor Signature Resolved!</h3>" +
                        "<p><strong>Hardware Company:</strong> <span style='color:#fff; font-weight:bold;'>" + company + "</span></p>" +
                        "<p><strong>OUI Prefix:</strong> " + prefix + "</p>" +
                        "<p><strong>Factory Assignment Address:</strong> " + address + "</p>";
                } else {
                    resultBox.innerHTML = "<p style='color:#ffb700; text-align:center;'>⚠️ Signature signature parsed but no direct mapping found.</p>" +
                        "<div class='debug-console' style='text-align:left;'>" +
                        "<strong>Raw Server Payload Response:</strong><br><pre>" + JSON.stringify(data, null, 2) + "</pre>" +
                        "</div>";
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Connection to RapidAPI Proxy Gateway Failed!";
            }
        }
    </script>
</body>
</html>
"""

@script26_bp.route('/')
def index():
    return render_template_string(UI)

@script26_bp.route('/lookup', methods=['POST'])
def lookup_mac():
    req_data = request.json
    mac_address = str(req_data.get('mac_address', '')).strip()
    
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        
        # Exact request endpoint target formatting string setup
        query_path = f"/{mac_address}"
        
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }
        
        conn.request("GET", query_path, headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        
        if res.status != 200:
            return jsonify({"status": "error", "message": f"RapidAPI Node Error (Status Code: {res.status})"})
            
        try:
            parsed_json = json.loads(raw_data)
            return jsonify(parsed_json)
        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": f"Text payload: {raw_data[:100]}"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

