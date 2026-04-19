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
body { background:#000;color:#0f0;font-family:'Courier New',monospace;padding:20px; }
.terminal-window{border:2px solid #0f0;background:#050505;width:95%;max-width:800px;display:inline-block;padding:15px;
box-shadow:0 0 20px #0f04;text-align:left;}
.stats-bar{display:flex;justify-content:space-around;background:#111;padding:10px;border:1px solid #333;margin-bottom:15px;font-weight:bold;}
.stat-item{color:#fff;}
.stat-val{color:#0f0;}
input{background:#000;border:1px solid #0f0;color:#0f0;padding:10px;width:250px;outline:none;}
button{padding:10px 20px;font-weight:bold;cursor:pointer;border:none;margin:5px;}
.start-btn{background:#0f0;color:#000;}
.stop-btn{background:#f00;color:#fff;display:none;}
#output{height:350px;overflow-y:auto;font-size:13px;color:#0f0;border-top:1px solid #333;padding-top:10px;}
.lost-msg{color:#ff4444;font-weight:bold;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-thumb{background:#0f0;}
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
<input type="text" id="port" placeholder="Port (80)" style="width:100px;">
<input type="text" id="timeout" placeholder="Timeout (1.5)" style="width:80px;">
<button class="start-btn" id="startBtn" onclick="togglePing(true)">START PING</button>
<button class="stop-btn" id="stopBtn" onclick="togglePing(false)">STOP PING</button>
</div>

<div style="text-align:center;margin-bottom:15px;">
<input type="text" id="targets" placeholder="Targets (comma separated)">
<button onclick="sendMultiPing()">PING ALL</button>
</div>

<div style="text-align:center;margin-bottom:15px;">
<input type="text" id="scan-target" placeholder="Host to scan">
<input type="text" id="scan-start" placeholder="Start (1)" style="width:80px;">
<input type="text" id="scan-end" placeholder="End (1024)" style="width:80px;">
<button onclick="scanPorts()">SCAN PORTS</button>
</div>

<div id="output">System Ready... Waiting for target.</div>
</div>

<script>
let pingInterval; let sent=0, received=0, lost=0;
function updateStats(){document.getElementById('s-sent').innerText=sent;
document.getElementById('s-rec').innerText=received;
document.getElementById('s-lost').innerText=lost;
let per=sent>0?Math.round((lost/sent)*100):0;document.getElementById('s-per').innerText=per+"%";}
async function sendPing(){let target=document.getElementById('target').value;
let port=document.getElementById('port').value||80;
let timeout=document.getElementById('timeout').value||1.5;sent++;
try{let res=await fetch('/script5/run-single-ping',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target,port,timeout})});
let data=await res.json();let line=document.createElement('div');
if(data.status==="success"){received++;line.innerHTML=`Reply from ${target}: time=${data.latency}ms status=OK`;}
else{lost++;line.innerHTML=`<span class="lost-msg">Request timed out.</span>`;}document.getElementById('output').appendChild(line);}catch(e){lost++;}updateStats();document.getElementById('output').scrollTop=document.getElementById('output').scrollHeight;}
function togglePing(start){let target=document.getElementById('target').value;if(!target&&start)return alert("Bhai target toh daal!");
if(start){sent=0;received=0;lost=0;updateStats();document.getElementById('output').innerHTML=`[!] Pinging ${target}...<br>`;document.getElementById('startBtn').style.display='none';
document.getElementById('stopBtn').style.display='inline-block';pingInterval=setInterval(sendPing,1000);}else{clearInterval(pingInterval);document.getElementById('startBtn').style.display='inline-block';
document.getElementById('stopBtn').style.display='none';document.getElementById('output').innerHTML+='<br>[!] Scan Stopped. Summary updated above.';}
}
async function sendMultiPing(){let list=document.getElementById('targets').value.split(',').map(x=>x.trim()).filter(Boolean);
if(list.length===0)return alert("Enter at least one target");
let port=document.getElementById('port').value||80;
let timeout=document.getElementById('timeout').value||1.5;
let output=document.getElementById('output');output.innerHTML='[!] Pinging multiple targets...<br>';
let res=await fetch('/script5/run-multi-ping',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({targets:list,port,timeout})});
let data=await res.json();for(let t of list){let line=document.createElement('div');if(data[t].status==="success"){line.innerHTML=`Reply from ${t}: time=${data[t].latency}ms`;}else{line.innerHTML=`<span class="lost-msg">Ping failed for ${t}.</span>`;}output.appendChild(line);}
}
async function scanPorts(){let host=document.getElementById('scan-target').value;
let start=document.getElementById('scan-start').value||1;
let end=document.getElementById('scan-end').value||1024;
if(!host)return alert("Enter host to scan");
let output=document.getElementById('output');output.innerHTML='[!] Scanning ports on '+host+'...<br>';
let res=await fetch('/script5/scan-host',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target:host,start_port:start,end_port:end,timeout:1.5})});
let data=await res.json();if(data.status==='ok'){output.innerHTML+=`Open ports on ${host}: ${data.open_ports.join(', ')}<br>`;}else{output.innerHTML+='No open ports found.<br>';}
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
# Helper: test a single port – used by the scanner
# ------------------------------------------------------------------
def test_port(host: str, port: int, timeout: float = 1.5) -> bool:
    """Return True if the TCP port is open (connection succeeds)."""
    ip = resolve_host(host)
    if not ip:
        return False
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
        sock.close()
        return True
    except Exception:
        return False

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

    with ThreadPoolExecutor(max_workers=20) as executor:
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
@script5_bp.route('/scan-host', methods=['POST'])
def scan_host():
    """Return a list of open ports for a host."""
    data = request.json or {}
    target = data.get('target', '').strip()
    start_port = int(data.get('start_port', 1))
    end_port = int(data.get('end_port', 1024))
    timeout = float(data.get('timeout', 1.5))

    if not target:
        return jsonify({"status": "error", "message": "No target provided"}), 400

    open_ports = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(test_port, target, p, timeout): p for p in range(start_port, end_port + 1)}
        for future in as_completed(futures):
            port = futures[future]
            if future.result():
                open_ports.append(port)

    return jsonify({"status": "ok", "open_ports": open_ports})

# ------------------------------------------------------------------
# Blueprint route – port scanner for a single port (used by /scan-port)
# ------------------------------------------------------------------
@script5_bp.route('/scan-port', methods=['POST'])
def scan_port():
    """Return whether a host/port is reachable (open)."""
    data = request.json or {}
    target = data.get('target', '').strip()
    port = int(data.get('port', 80))
    timeout = float(data.get('timeout', 1.5))

    if test_port(target, port, timeout):
        return jsonify({"status": "open"})
    else:
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
