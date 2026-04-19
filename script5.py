import socket
import time
from flask import Blueprint, request, jsonify, render_template_string

script5_bp = Blueprint('script5', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost Script5 - Real-Time Pinger</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }
        .terminal-window { border: 2px solid #0f0; background: #050505; width: 95%; max-width: 800px; display: inline-block; padding: 15px; box-shadow: 0 0 20px #0f04; text-align: left; }
        .stats-bar { display: flex; justify-content: space-around; background: #111; padding: 10px; border: 1px solid #333; margin-bottom: 15px; font-weight: bold; }
        .stat-item { color: #fff; }
        .stat-val { color: #0f0; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 250px; outline: none; }
        button { padding: 10px 20px; font-weight: bold; cursor: pointer; border: none; margin: 5px; }
        .start-btn { background: #0f0; color: #000; }
        .stop-btn { background: #f00; color: #fff; display: none; }
        #output { height: 350px; overflow-y: auto; font-size: 13px; color: #0f0; border-top: 1px solid #333; padding-top: 10px; }
        .lost-msg { color: #ff4444; font-weight: bold; }
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #0f0; }
    </style>
</head>
<body>
    <div class="terminal-window">
        <h2 style="text-align:center; margin-top:0;">GHOST_PRO_PINGER v6.0</h2>
        
        <div class="stats-bar">
            <div class="stat-item">SENT: <span id="s-sent" class="stat-val">0</span></div>
            <div class="stat-item">RECEIVED: <span id="s-rec" class="stat-val">0</span></div>
            <div class="stat-item">LOST: <span id="s-lost" style="color:red;">0</span></div>
            <div class="stat-item">LOSS %: <span id="s-per" class="stat-val">0%</span></div>
        </div>

        <div style="text-align:center; margin-bottom:15px;">
            <input type="text" id="target" placeholder="Enter IP or Domain (8.8.8.8)">
            <button class="start-btn" id="startBtn" onclick="togglePing(true)">START PING</button>
            <button class="stop-btn" id="stopBtn" onclick="togglePing(false)">STOP PING</button>
        </div>

        <div id="output">System Ready... Waiting for target.</div>
    </div>

<script>
    let pingInterval;
    let sent = 0, received = 0, lost = 0;

    function updateStats() {
        document.getElementById('s-sent').innerText = sent;
        document.getElementById('s-rec').innerText = received;
        document.getElementById('s-lost').innerText = lost;
        let per = sent > 0 ? Math.round((lost / sent) * 100) : 0;
        document.getElementById('s-per').innerText = per + "%";
    }

    async function sendPing() {
        const target = document.getElementById('target').value;
        const output = document.getElementById('output');
        sent++;
        
        try {
            const res = await fetch('/script5/run-single-ping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target})
            });
            const data = await res.json();
            
            const line = document.createElement('div');
            if(data.status === "success") {
                received++;
                line.innerHTML = `Reply from ${target}: time=${data.latency}ms status=OK`;
            } else {
                lost++;
                line.innerHTML = `<span class="lost-msg">Request timed out.</span>`;
            }
            output.appendChild(line);
        } catch (e) {
            lost++;
        }
        updateStats();
        output.scrollTop = output.scrollHeight;
    }

    function togglePing(start) {
        const target = document.getElementById('target').value;
        if(!target && start) return alert("Bhai target toh daal!");

        if(start) {
            sent = 0; received = 0; lost = 0;
            updateStats();
            document.getElementById('output').innerHTML = `[!] Pinging ${target}...<br>`;
            document.getElementById('startBtn').style.display = 'none';
            document.getElementById('stopBtn').style.display = 'inline-block';
            pingInterval = setInterval(sendPing, 1000);
        } else {
            clearInterval(pingInterval);
            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
            document.getElementById('output').innerHTML += `<br>[!] Scan Stopped. Summary updated above.`;
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
        # TCP connection attempt on port 80
        s = socket.create_connection((target, 80), timeout=1.5)
        latency = round((time.time() - start) * 1000, 2)
        s.close()
        return jsonify({"status": "success", "latency": latency})
    except:
        return jsonify({"status": "error"}), 500
