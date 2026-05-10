from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script23_bp = Blueprint('script23', __name__)

# --- CONFIGURATION ---
# Tera RapidAPI Credentials
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
        h2 { margin-top: 0; color: #fff; text-shadow: 0 0 10px #00d4ff; }
        input { width: 80%; padding: 12px; background: #111; border: 1px solid #00d4ff; color: #fff; text-transform: uppercase; font-size: 18px; margin-bottom: 15px; border-radius: 5px; outline: none; }
        button { padding: 12px 30px; background: #00d4ff; color: #000; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; border-radius: 5px; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .result-card { margin-top: 25px; text-align: left; border-top: 1px solid #333; padding-top: 15px; display: none; }
        .data-item { margin-bottom: 8px; font-size: 14px; border-bottom: 1px solid #111; padding-bottom: 5px; }
        .label { color: #888; text-transform: uppercase; margin-right: 10px; font-size: 11px; }
        .value { color: #fff; font-weight: bold; }
        .loading { color: #ff0; animation: blink 1s infinite; display: none; margin-top: 10px; font-weight: bold; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚗 VAHAN_RC_TRACKER v23</h2>
        <p>Shivm Singh Omega Dashboard - RTO Node</p>
        
        <input type="text" id="v_number" placeholder="MH 01 AB 1234" maxlength="12">
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

            if(!vNum) return alert("Bhai, gaadi ka number toh daal!");

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

                if(data.status === "error" || !data || data.message) {
                    resultBox.innerHTML = '<div style="color:red; text-align:center;">Vehicle Not Found or API Limit Exceeded</div>';
                    resultBox.style.display = "block";
                } else {
                    resultBox.style.display = "block";
                    
                    let htmlContent = "";
                    // Pure data object ko loop karke details nikal rahe hain
                    for(let key in data) {
                        // Agar value object nahi hai, tabhi display karein
                        if(typeof data[key] !== 'object' && data[key] !== null) {
                            let cleanKey = key.replace(/_/g, ' ').toUpperCase();
                            htmlContent += '<div class="data-item">' +
                                '<span class="label">' + cleanKey + ':</span>' +
                                '<span class="value">' + data[key] + '</span>' +
                            '</div>';
                        }
                    }
                    resultBox.innerHTML = htmlContent || '<div style="color:red;">No specific details available.</div>';
                }
            } catch (e) {
                loader.style.display = "none";
                alert("Error: Server se connection nahi ho paya.");
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
    # User input ko clean karna (Spaces hatana aur Uppercase banana)
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
        
        # JSON response ko parse karke bhejna
        result = json.loads(data.decode("utf-8"))
        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

