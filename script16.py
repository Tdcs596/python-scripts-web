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
        .box { border: 2px solid #00ffcc; background: #000; padding: 25px; box-shadow: 0 0 20px #00ffcc44; display: inline-block; width: 90%; max-width: 650px; border-radius: 15px; }
        h2 { text-shadow: 0 0 10px #00ffcc; margin-bottom: 20px; }
        input { width: 80%; padding: 15px; background: #111; border: 1px solid #00ffcc; color: #fff; font-size: 20px; text-transform: uppercase; text-align: center; border-radius: 8px; outline: none; margin-bottom: 20px; }
        button { width: 85%; padding: 15px; background: #00ffcc; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 16px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #status { margin-top: 20px; color: #ffeb3b; font-weight: bold; display: none; }
        .result-display { margin-top: 25px; text-align: left; background: #050505; border: 1px solid #333; padding: 15px; border-radius: 8px; display: none; max-height: 400px; overflow-y: auto; }
        .row { border-bottom: 1px solid #1a1a1a; padding: 8px 0; display: flex; justify-content: space-between; }
        .label { color: #888; font-size: 12px; text-transform: uppercase; }
        .val { color: #fff; font-weight: bold; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🏎️ VAHAN RC SCANNER v16</h2>
        <p style="color: #666;">Enter Vehicle Number (e.g. PB65AM0008)</p>
        
        <input type="text" id="v_num" placeholder="CH 01 AB 1234">
        <br>
        <button onclick="scanVehicle()" id="scan_btn">FETCH RC DETAILS</button>
        
        <div id="status">📡 CONNECTING TO RTO DATABASE...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function scanVehicle() {
            const vNum = document.getElementById('v_num').value.replace(/\s+/g, '').toUpperCase();
            const btn = document.getElementById('scan_btn');
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!vNum) return alert("Bhai, number toh daal!");

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

                if(data.status === "error" || data.message === "You have exceeded the rate limit per second for your plan") {
                    resultBox.innerHTML = "<p style='color:red; text-align:center;'>❌ ERROR: API Limit Crossed or Invalid Number</p>";
                } else {
                    let html = "";
                    for(let key in data) {
                        if(typeof data[key] !== 'object' && data[key] !== null) {
                            html += `<div class="row">
                                <span class="label">\${key.replace(/_/g, ' ')}</span>
                                <span class="val">\${data[key]}</span>
                            </div>`;
                        }
                    }
                    resultBox.innerHTML = html || "<p style='color:red;'>No data found for this number.</p>";
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
        
        # Rate limit check
        if res.status == 429:
            return jsonify({"status": "error", "message": "Limit Exceeded"})
            
        data = res.read()
        return jsonify(json.loads(data.decode("utf-8")))

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

