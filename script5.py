import socket
import time
from flask import Blueprint, request, jsonify, render_template_string

script5_bp = Blueprint('script5', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost Script5 - Continuous Pinger</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .terminal-window { border: 2px solid #0f0; background: #050505; width: 95%; max-width: 700px; display: inline-block; padding: 15px; box-shadow: 0 0 20px #0f04; text-align: left; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 250px; outline: none; }
        .controls { margin-bottom: 20px; text-align: center; }
        button { padding: 10px 20px; font-weight: bold; cursor: pointer; border: none; margin: 5px; }
        .start-btn { background: #0f0; color: #000; }
        .stop-btn { background: #f00; color: #fff; display: none; }
        #output { height: 400px; overflow-y: auto; font-size: 13px; color: #0f0; line-height: 1.4; border-top: 1px solid #333; padding-top: 10px; margin-top: 10px; }
        .lost { color: #ff4444; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #0f0; }
    </style>
</head>
<body>
    <div class="terminal-window">
        <div class="controls">
            <h2 style="color: #0f0; margin-top: 0;">GHOST_CONTINUOUS_PINGER</h2>
            <input type="text" id="target" placeholder="Enter IP or Domain (8.8.8.8)">
            <button class="start-btn" id="startBtn" onclick="togglePing(true)">START PING</button>
            <button class="stop-btn" id="stopBtn" onclick="togglePing(false)">STOP PING</button>
        </div>
        <div id="output">Ready...</div>
    </div>

<script>
    let pingInterval;
    let isPinging = false;

    async function sendPing() {
        const target = document.getElementById('target').value;
        const output = document.getElementById('output');
        
        try {
            const res = await fetch('/script5/run-single-ping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target})
            });
            const data = await res.json();
            
            const line = document.createElement('div');
            if(data.status === "success") {
                line.innerHTML = `Reply from ${target}: time=${data.latency}ms status=200`;
            } else {
                line.innerHTML = `<span class="lost">Request timed out. (Packet Lost)</span>`;
            }
            
            output.appendChild(line);
            output.scrollTop = output.scrollHeight;
        } catch (e) {
            console.error("Ping Error");
        }
    }

    function togglePing(start) {
        const target = document.getElementById('target').value;
        if(!target && start) return alert("Enter Target!");

        isPinging = start;
        document.getElementById('startBtn').style.display = start ? 'none' : 'inline-block';
        document.getElementById('stopBtn').style.display = start ? 'inline-block' : 'none';

        if(start) {
            document.getElementById('output').innerHTML = `[!] Starting Continuous Ping for ${target}...<br>`;
            // Har 1000ms (1 second) mein ping bhejega
            pingInterval = setInterval(sendPing, 1000);
        } else {
            clearInterval(pingInterval);
            document.getElementById('output').innerHTML += `<br>[!] Ping Stopped.`;
        }
    }
</script>
</body>
</html>
"""

@script5_bp.route('/')
def script5_home():
    return render_template_string(INTERFACE)

@script5_bp.route('/run-single-ping', methods=['POST'])
def run_single_ping():
    data = request.json
    target = data.get('target', '').strip()
    
    try:
        start = time.time()
        # TCP Ping check
        s = socket.create_connection((target, 80), timeout=1.5)
        latency = round((time.time() - start) * 1000, 2)
        s.close()
        return jsonify({"status": "success", "latency": latency})
    except:
        return jsonify({"status": "error", "message": "Lost"}), 500
