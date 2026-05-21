from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json
import urllib.parse

script25_bp = Blueprint('script25', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "breachdirectory.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>BREACH_DIRECTORY_v25</title>
    <style>
        body { background: #07090e; color: #00d2ff; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .box { border: 2px solid #00d2ff; background: #000; padding: 25px; box-shadow: 0 0 25px #00d2ff33; display: inline-block; width: 95%; max-width: 700px; border-radius: 12px; text-align: left; }
        .header { text-align: center; border-bottom: 1px solid #00d2ff; padding-bottom: 15px; margin-bottom: 20px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 10px #00d2ff; }
        .input-group { text-align: center; margin-bottom: 20px; }
        input { width: 75%; padding: 12px; background: #111; border: 1px solid #00d2ff; color: #fff; font-size: 16px; border-radius: 5px; outline: none; text-align: center; }
        button { padding: 12px 30px; background: #00d2ff; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 15px; margin-top: 15px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #status { margin: 15px 0; color: #ffeb3b; text-align: center; display: none; }
        .result-display { margin-top: 25px; background: #05070a; border: 1px solid #1a2333; padding: 15px; border-radius: 8px; display: none; }
        .breach-card { background: #0d131f; border-left: 4px solid #ff3333; padding: 12px; margin-bottom: 12px; border-radius: 4px; }
        .breach-title { color: #ff3333; font-weight: bold; font-size: 16px; margin-bottom: 5px; }
        .breach-meta { color: #aaa; font-size: 13px; }
        .safe-msg { color: #00ff66; text-align: center; font-weight: bold; font-size: 16px; padding: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="header">
            <h2>🔍 BREACH DIRECTORY RECON v25</h2>
            <p style="color: #557099; margin: 5px 0 0 0;">SHIVAM SINGH OMEGA DASHBOARD • INTEL NODE</p>
        </div>

        <div class="input-group">
            <input type="text" id="target_term" placeholder="Enter Email or Username (e.g., target@gmail.com)">
            <br>
            <button onclick="checkBreach()" id="scan_btn">SCAN FOR EXPOSURES</button>
        </div>

        <div id="status">📡 SEARCHING GLOBAL DEEP WEB BREACH REPOSITORIES...</div>
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function checkBreach() {
            const term = document.getElementById('target_term').value.trim();
            const btn = document.getElementById('scan_btn');
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!term) return alert("Bhai, Email ya Username toh daal!");

            btn.disabled = true;
            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script25/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ search_term: term })
                });
                const data = await res.json();
                
                status.style.display = "none";
                btn.disabled = false;

                if(data.status === "error") {
                    resultBox.innerHTML = "<p style='color:red; text-align:center;'>❌ SERVER ERROR: " + data.message + "</p>";
                } else if(data.result && data.result.length > 0) {
                    let html = "<h3 style='color:#fff; margin-top:0;'>⚠️ Pwned! Found in " + data.result.length + " Breaches:</h3>";
                    
                    for(let i = 0; i < data.result.length; i++) {
                        let item = data.result[i];
                        let sources = item.sources ? item.sources.join(', ') : 'Unknown Source';
                        
                        html += '<div class="breach-card">' +
                            '<div class="breach-title">' + sources + '</div>' +
                            '<div class="breach-meta"><strong>Exposed Data:</strong> ' + (item.has_password ? 'Passwords, ' : '') + 'Email/Username</div>' +
                            '<div class="breach-meta" style="color:#ffb700; margin-top:5px;"><strong>SHA-1 Hash:</strong> ' + (item.sha1 || 'N/A') + '</div>' +
                        '</div>';
                    }
                    resultBox.innerHTML = html;
                } else {
                    resultBox.innerHTML = '<div class="safe-msg">💚 Good news! No compromised records found for this target.</div>';
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Cyber Intel Node Connection Failed!";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@script25_bp.route('/')
def index():
    return render_template_string(UI)

@script25_bp.route('/scan', methods=['POST'])
def scan_breach():
    search_term = request.json.get('search_term', '')
    encoded_term = urllib.parse.quote(search_term)
    
    try:
        # Fixed: http.http.client ko badal kar simple http.client kar diya hai
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json",
            'User-Agent': "Mozilla/5.0"
        }

        conn.request("GET", "/?func=auto&term=" + encoded_term, headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        
        if not raw_data:
            return jsonify({"status": "error", "message": f"API returned an empty response. Status Code: {res.status}"})
            
        try:
            parsed_json = json.loads(raw_data)
            if isinstance(parsed_json, dict) and "message" in parsed_json:
                return jsonify({"status": "error", "message": parsed_json["message"]})
                
            return jsonify(parsed_json)
        except json.JSONDecodeError:
            return jsonify({"status": "error", "message": f"Plain text response: {raw_data[:100]}"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
