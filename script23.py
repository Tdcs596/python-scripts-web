from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script23_bp = Blueprint('script23', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "155514abbfmshd5da5b6f34d5791p144617jsn3ac281515eb0"
RAPID_API_HOST = "vehicle-rc-information-v2.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>VAHAN_TRACKER_v23</title>
    <style>
        body { background: #000; color: #00d4ff; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .container { border: 2px solid #00d4ff; background: #050505; padding: 30px; box-shadow: 0 0 25px #00d4ff33; display: inline-block; width: 80%; max-width: 600px; border-radius: 10px; }
        input { width: 70%; padding: 12px; background: #111; border: 1px solid #00d4ff; color: #fff; text-transform: uppercase; font-size: 18px; margin-bottom: 15px; }
        button { padding: 12px 30px; background: #00d4ff; color: #000; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .result-card { margin-top: 25px; text-align: left; border-top: 1px solid #333; padding-top: 15px; display: none; }
        .data-item { margin-bottom: 8px; font-size: 14px; }
        .label { color: #888; text-transform: uppercase; margin-right: 10px; font-size: 12px; }
        .value { color: #fff; font-weight: bold; }
        .loading { color: #ff0; animation: blink 1s infinite; display: none; margin-top: 10px; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚗 VAHAN_RC_TRACKER v23</h2>
        <p>Enter Vehicle Number to fetch Registration Details</p>
        
        <input type="text" id="v_number" placeholder="DL 01 CA 1234" maxlength="12">
        <br>
        <button onclick="fetchRC()">FETCH_INFORMATION</button>
        
        <div id="loader" class="loading">CONNECTING_TO_RTO_DATABASE...</div>

        <div id="result" class="result-card">
            </div>
    </div>

    <script>
        async function fetchRC() {
            const vNum = document.getElementById('v_number').value;
            const loader = document.getElementById('loader');
            const resultBox = document.getElementById('result');

            if(!vNum) return alert("Vehicle number missing!");

            loader.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script23/fetch_rc', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ vehicle_number: vNum })
                });
                const data = await res.json();
                loader.style.display = "none";

                if(data.status === "error") {
                    resultBox.innerHTML = `<div style="color:red; text-align:center;">\${data.message}</div>`;
                } else {
                    resultBox.style.display = "block";
                    // Loop through data to show all details
                    for(let key in data) {
                        if(typeof data[key] !== 'object') {
                            resultBox.innerHTML += `
                                <div class="data-item">
                                    <span class="label">\${key.replace(/_/g, ' ')}:</span>
                                    <span class="value">\${data[key]}</span>
                                </div>
                            `;
                        }
                    }
                }
            } catch (e) {
                loader.style.display = "none";
                alert("Database connection timed out.");
            }
        }
    </script>
</body>
</html>
"""

@script23_bp.route('/')
def index():
    return render_template_string(UI)

@script23_bp.route('/fetch_rc', methods=['POST'])
def fetch_rc():
    v_num = request.json.get('vehicle_number', '').replace(" ", "").upper()
    
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
        data = res.read()
        
        # Parse data and return
        result = json.loads(data.decode("utf-8"))
        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


