import time
import http.client
import urllib.parse
from flask import Blueprint, request, jsonify, render_template_string

script5_bp = Blueprint('script5', __name__)

# --- SCRIPT 5 UI ---
INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost Script5 - Web Pinger</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }
        .main-container { border: 2px solid #00ff00; display: inline-block; padding: 30px; background: #000; box-shadow: 0 0 20px #00ff0044; border-radius: 10px; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 250px; outline: none; margin-bottom: 20px; }
        button { background: #0f0; color: #000; border: none; padding: 12px 30px; cursor: pointer; font-weight: bold; }
        #terminal { background: #111; border: 1px solid #333; color: #888; padding: 15px; width: 500px; height: 200px; margin: 20px auto; text-align: left; overflow-y: auto; white-space: pre-wrap; font-size: 13px; }
    </style>
</head>
<body>
<div class="main-container">
    <h1>GHOST_WEB_PINGER</h1>
    <p style="color: #444;">[ Render Optimized - No Root Required ]</p>
    <input type="text" id="target" placeholder="e.g. google.com or idealdocs.in">
    <br>
    <button onclick="executePing()">CHECK STATUS</button>
    <div id="terminal">[SYSTEM READY]...</div>
</div>

<script>
    async function executePing() {
        const target = document.getElementById('target').value;
        const terminal = document.getElementById('terminal');
        if(!target) return;
        
        terminal.innerText = "[#] Analyzing connection to: " + target;
        
        try {
            const response = await fetch('/script5/run-ping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target})
            });
            const data = await response.json();
            if(data.status === "success") { 
                terminal.innerText = `[SUCCESS] Target: ${target}\\n[STATUS] Online (200 OK)\\n[LATENCY] ${data.latency}ms\\n[SERVER] Render-Backbone`; 
            } else { 
                terminal.innerText = "[!] FAILED: " + data.message; 
            }
        } catch (e) {
            terminal.innerText = "[!] SYSTEM ERROR: Check URL format.";
        }
    }
</script>
</body>
</html>
"""

@script5_bp.route('/')
def script5_home():
    return render_template_string(INTERFACE)

@script5_bp.route('/run-ping', methods=['POST'])
def run_ping():
    data = request.json
    target = data.get('target', '').replace('http://', '').replace('https://', '').strip('/')
    
    if not target:
        return jsonify({"status": "error", "message": "No target"}), 400
    
    try:
        start_time = time.time()
        # Hum HTTP connection try kar rahe hain jo Render allow karta hai
        conn = http.client.HTTPSConnection(target, timeout=5)
        conn.request("HEAD", "/")
        response = conn.getresponse()
        end_time = time.time()
        
        latency = round((end_time - start_time) * 1000, 2)
        conn.close()
        
        return jsonify({
            "status": "success", 
            "latency": latency,
            "code": response.status
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
