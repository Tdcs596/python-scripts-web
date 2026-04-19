import socket
import time
from flask import Blueprint, request, jsonify, render_template_string

script5_bp = Blueprint('script5', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost Script5 - TCP Pinger</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .main-container { border: 2px solid #00ff00; display: inline-block; padding: 20px; background: #000; width: 90%; max-width: 600px; box-shadow: 0 0 20px #0f03; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 60%; margin-bottom: 10px; outline: none; }
        button { background: #0f0; color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        #terminal { background: #000; border: 1px solid #333; color: #0f0; padding: 15px; height: 300px; margin-top: 20px; text-align: left; overflow-y: auto; font-size: 12px; white-space: pre-wrap; border-left: 3px solid #0f0; }
        .stat-line { color: yellow; }
    </style>
</head>
<body>
<div class="main-container">
    <h2>GHOST_TCP_PINGER v5.0</h2>
    <input type="text" id="target" placeholder="Enter IP or Domain (e.g. 8.8.8.8)">
    <button onclick="startAdvancedPing()">START PING</button>
    <div id="terminal">[SYSTEM READY]... Enter Target to scan packets.</div>
</div>

<script>
    async function startAdvancedPing() {
        const target = document.getElementById('target').value;
        const terminal = document.getElementById('terminal');
        if(!target) return;
        
        terminal.innerText = `[#] Pinging ${target} with 4 packets (TCP_SCAN)...\\n`;
        
        try {
            const response = await fetch('/script5/run-ping', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: target})
            });
            const data = await response.json();
            
            if(data.status === "success") {
                let output = "";
                data.results.forEach(res => {
                    output += `Reply from ${target}: bytes=32 time=${res}ms\\n`;
                });
                output += `\\n--- ${target} ping statistics ---\\n`;
                output += `Packets: Sent = 4, Received = ${data.received}, Lost = ${4 - data.received}\\n`;
                output += `Approximate round trip times in milli-seconds:\\n`;
                output += `Minimum = ${data.min}ms, Maximum = ${data.max}ms, Average = ${data.avg}ms`;
                terminal.innerText = output;
            } else {
                terminal.innerText = "[!] FAILED: " + data.message;
            }
        } catch (e) {
            terminal.innerText = "[!] ERROR: Check network or IP.";
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
    target = data.get('target', '').strip()
    port = 80 # Standard Web Port for TCP Ping
    
    results = []
    received = 0
    
    for _ in range(4):
        try:
            start = time.time()
            # Socket connection jo har server allow karta hai
            s = socket.create_connection((target, port), timeout=2)
            end = time.time()
            s.close()
            
            ms = round((end - start) * 1000, 2)
            results.append(ms)
            received += 1
        except Exception:
            pass # Packet Lost
            
    if results:
        return jsonify({
            "status": "success",
            "results": results,
            "received": received,
            "min": min(results),
            "max": max(results),
            "avg": round(sum(results)/len(results), 2)
        })
    else:
        return jsonify({"status": "error", "message": "Host Unreachable or Packets Lost 100%"}), 500
