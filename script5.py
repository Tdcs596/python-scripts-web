# ────────────────────────────────────────────────────────────────────────
#  script5.py – “Ghost Script5 – Real‑Time Pinger” (enhanced)
#  ────────────────────────────────────────────────────────────────────────
#  • Keeps the original UI and behaviour intact
#  • Adds powerful helper functions (resolve, multi‑ping, port scan, etc.)
#  • All logic stays inside this single file – no external changes needed
#  -------------------------------------------------------------------------

import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import Blueprint, request, jsonify, render_template_string

# ------------------------------------------------------------------
# Blueprint definition – same url_prefix as before
# ------------------------------------------------------------------
script5_bp = Blueprint('script5', __name__, url_prefix='/script5')

# ------------------------------------------------------------------
# UI – unchanged (kept exactly as in the original question)
# ------------------------------------------------------------------
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
    <h2 style="text-align:center;margin-top:0;">GHOST_PRO_PINGER v6.0</h2>
    <div class="stats-bar">
        <div class="stat-item">SENT: <span id="s-sent" class="stat-val">0</span></div>
        <div class="stat-item">RECEIVED: <span id="s-rec" class="stat-val">0</span></div>
        <div class="stat-item">LOST: <span id="s-lost" style="color:red;">0</span></div>
        <div class="stat-item">LOSS %: <span id="s-per" class="stat-val">0%</span></div>
    </div>
    <div style="text-align:center;margin-bottom:15px;">
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

# ------------------------------------------------------------------
# Helper: resolve hostname → IPv4 (first record)
# ------------------------------------------------------------------
def resolve_host(hostname: str) -> str | None:
    """Return the first IPv4 address for *hostname* or None if resolution fails."""
    try:
        infos = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
        return infos[0][4][0]
    except Exception:
        return None

# ------------------------------------------------------------------
# Helper: ping a single host/port, return latency in ms
# ------------------------------------------------------------------
def ping_host(host: str, port: int = 80, timeout: float = 1.5) -> float:
    """Return latency in milliseconds. Raises if host unreachable."""
    ip = resolve_host(host)
    if not ip:
        raise ValueError(f"Unable to resolve {host}")

    start = time.time()
    s = socket.create_connection((ip, port), timeout=timeout)
    latency = round((time.time() - start) * 1000, 2)
    s.close()
    return latency

# ------------------------------------------------------------------
# Blueprint route – UI
# ------------------------------------------------------------------
@script5_bp.route('/')
def script5_home():
    return render_template_string(INTERFACE)

# ------------------------------------------------------------------
# Blueprint route – single ping (used by the UI)
# ------------------------------------------------------------------
@script5_bp.route('/run-single-ping', methods=['POST'])
def run_single_ping():
    data = request.json or {}
    target = data.get('target', '').strip()
    port = int(data.get('port', 80))
    timeout = float(data.get('timeout', 1.5))

    try:
        latency = ping_host(target, port=port, timeout=timeout)
        return jsonify({"status": "success", "latency": latency})
    except Exception:
        return jsonify({"status": "error"}), 500

# ------------------------------------------------------------------
# Blueprint route – multi‑ping (batch)
# ------------------------------------------------------------------
@script5_bp.route('/run-multi-ping', methods=['POST'])
def run_multi_ping():
    """Accepts JSON: {targets: [list], port: int, timeout: float} and returns per‑target result."""
    data = request.json or {}
    targets = data.get('targets', [])
    port = int(data.get('port', 80))
    timeout = float(data.get('timeout', 1.5))

    results = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(ping_host, t, port, timeout): t for t in targets}
        for future in as_completed(futures):
            target = futures[future]
            try:
                latency = future.result()
                results[target] = {"status": "success", "latency": latency}
            except Exception as e:
                results[target] = {"status": "error", "error": str(e)}

    return jsonify(results)

# ------------------------------------------------------------------
# Blueprint route – simple port scanner
# ------------------------------------------------------------------
@script5_bp.route('/scan-port', methods=['POST'])
def scan_port():
    """Return whether a host/port is reachable (open)."""
    data = request.json or {}
    target = data.get('target', '').strip()
    port = int(data.get('port', 80))
    timeout = float(data.get('timeout', 1.5))

    try:
        ping_host(target, port=port, timeout=timeout)
        return jsonify({"status": "open"})
    except Exception:
        return jsonify({"status": "closed"}), 200

# ------------------------------------------------------------------
# Blueprint route – resolve host (useful for debugging)
# ------------------------------------------------------------------
@script5_bp.route('/resolve-host', methods=['POST'])
def resolve_host_route():
    data = request.json or {}
    host = data.get('host', '').strip()
    ip = resolve_host(host)
    if ip:
        return jsonify({"status": "ok", "ip": ip})
    else:
        return jsonify({"status": "error", "message": "Could not resolve"}), 400
