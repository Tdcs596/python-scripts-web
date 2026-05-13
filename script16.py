from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script16_bp = Blueprint('script16', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "vehicle-rc-information-v2.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>VAHAN_RC_SCANNER_v16</title>
    <style>
        body { background: #0a0a0a; color: #00ffcc; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .box { border: 2px solid #00ffcc; background: #000; padding: 25px; box-shadow: 0 0 20px #00ffcc44; display: inline-block; width: 95%; max-width: 650px; border-radius: 15px; }
        input { width: 80%; padding: 15px; background: #111; border: 1px solid #00ffcc; color: #fff; font-size: 20px; text-transform: uppercase; text-align: center; border-radius: 8px; margin-bottom: 20px; outline: none; }
        button { width: 85%; padding: 15px; background: #00ffcc; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 16px; }
        .result-display { margin-top: 25px; text-align: left; background: #050505; border: 1px solid #333; padding: 15px; border-radius: 8px; display: none; }
        .row { border-bottom: 1px solid #1a1a1a; padding: 10px 0; display: flex; justify-content: space-between; align-items: center; }
        .label { color: #00ffcc; font-size: 11px; text-transform: uppercase; opacity: 0.7; }
        .val { color: #fff; font-weight: bold; font-size: 14px; text-align: right; word-break: break-all; width: 60%; }
        #status { margin: 15px 0; color: #ffeb3b; display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🏎️ VAHAN RC SCANNER v16</h2>
        <input type="text" id="v_num" placeholder="PB65AM0008">
        <br>
        <button onclick="scanVehicle()" id="scan_btn">FETCH RC DETAILS</button>
        <div id="status">📡 SCANNING RTO DATABASE...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function scanVehicle() {
            const vNum = document.getElementById('v_num').value.replace(/\s+/g, '').toUpperCase();
            const btn = document.getElementById('scan_btn');
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!vNum) return alert("Bhai, number daalo!");

            btn.disabled = true;
            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script16/fetch', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ vehicle_number: vNum })
                });
                const data = await res.json();
                status.style.display = "none";
                btn.disabled = false;

                let rData = data.result || data.data || data;
                
                if (data.status === "error" || data.message) {
                    resultBox.innerHTML = "<p style='color:red; text-align:center;'>❌ ERROR: " + (data.message || "Failed") + "</p>";
                } else {
                    let html = "";
                    for (let key in rData) {
                        if (typeof rData[key] !== 'object' && rData[key] !== null && rData[key] !== "") {
                            let cleanKey = key.replace(/_/g, ' ');
                            html += '<div class="row">' +
                                '<span class="label">' + cleanKey + '</span>' +
                                '<span class="val">' + rData[key] + '</span>' +
                            '</div>';
                        }
                    }
                    resultBox.innerHTML = html || "<p style='color:red;'>No data found.</p>";
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Connection Failed!";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@script16_bp.route('/')
def index():
    return render_template_string(UI)

@script16_bp.route('/fetch', methods=['POST'])
def fetch_rc():
    v_num = request.json.get('vehicle_number', '')
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        payload = json.dumps({"vehicle_number": v_num})
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }
        conn.request("POST", "/", payload, headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        return jsonify(json.loads(raw_data))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
