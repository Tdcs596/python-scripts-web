import subprocess
import re
from flask import Blueprint, request, jsonify, render_template_string

# Yahan humne Blueprint banaya taaki app.py isse pehchan sake
script5_bp = Blueprint('script5', __name__)

# --- SCRIPT 5 KA DESIGN ---
INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost Script5 - Advanced Pinger</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding-top: 50px; }
        .main-container { border: 2px solid #00ff00; display: inline-block; padding: 30px; background: #000; box-shadow: 0 0 20px #00ff0044; border-radius: 10px; }
        h1 { letter-spacing: 5px; text-shadow: 0 0 10px #0f0; margin: 0; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 250px; outline: none; margin-bottom: 20px; margin-top: 20px; }
        button { background: #0f0; color: #000; border: none; padding: 12px 30px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #0f0; }
        #terminal { background: #111; border: 1px solid #333; color: #888; padding: 15px; width: 500px; height: 250px; margin: 20px auto; text-align: left; overflow-y: auto; font-size: 13px; border-left: 4px solid #0f0; white-space: pre-wrap; }
        .loading { display: none; color: yellow; margin-bottom: 10px; }
    </style>
</head>
<body>
<div class="main-container">
    <h1>SCRIPT5_PINGER</h1>
    <p style="color: #444;">[ Independent Network Diagnostic Tool ]</p>
    <div id="loader" class="loading">>>> PINGING TARGET... PLEASE WAIT...</div>
    <input type="text" id="target" placeholder="Enter IP or Website">
    <br>
    <button onclick="executePing()">RUN PACKET SCAN</button>
    <div id="terminal">[SYSTEM READY] Waiting for input...</div>
</div>

<script>
    async function executePing() {
        const target = document.getElementById('target').value;
        const terminal = document.getElementById('terminal');
        const loader = document.getElementById('loader');
        if(!target) { terminal.innerText = "[!] ERROR: Please enter a target."; return; }
        loader.style.display = "block";
        terminal.innerText = "[#] Initializing packets for: " + target;
        try {
            // Yahan URL prefix /script5/ lagana zaroori hai Blueprint ke liye
            const response = await fetch('/script5/run-ping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target})
            });
            const data = await response.json();
            loader.style.display = "none";
            if(data.status === "success") { terminal.innerText = data.raw; }
            else { terminal.innerText = "[!] FAILED: " + data.message; }
        } catch (e) {
            loader.style.display = "none";
            terminal.innerText = "[!] SYSTEM ERROR: Backend not responding.";
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
    target = data.get('target')
    if not target:
        return jsonify({"status": "error", "message": "No target"}), 400
    try:
        # Linux/Render optimized command
        cmd = ["ping", "-c", "4", "-W", "2", target]
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if process.returncode == 0:
            return jsonify({"status": "success", "raw": process.stdout})
        else:
            return jsonify({"status": "error", "message": "Host Unreachable"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
