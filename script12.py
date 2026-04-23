import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- ADVANCED UI (THE MATRIX STYLE) ---
ADV_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA PRO SCANNER v2.0</title>
    <style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .container { border: 2px solid #00ff41; background: rgba(0, 20, 0, 0.9); padding: 30px; display: inline-block; width: 95%; max-width: 800px; box-shadow: 0 0 30px #00ff4166; border-radius: 5px; }
        .input-group { margin: 15px 0; display: flex; justify-content: center; gap: 10px; }
        input { background: #000; border: 1px solid #00ff41; color: #00ff41; padding: 12px; font-size: 16px; width: 60%; outline: none; }
        button { background: #00ff41; color: #000; border: none; padding: 12px 25px; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        
        #console { background: #050505; border: 1px solid #333; height: 400px; overflow-y: auto; text-align: left; padding: 15px; font-size: 13px; margin-top: 20px; line-height: 1.6; }
        .status-bar { display: flex; justify-content: space-between; font-size: 12px; color: #888; border-bottom: 1px solid #222; padding-bottom: 10px; }
        .entry { margin-bottom: 5px; border-left: 2px solid #00ff41; padding-left: 10px; }
        .open { color: #fff; background: #008800; padding: 2px 5px; font-weight: bold; }
        .meta { color: #888; font-style: italic; }
        .loader { color: #ff0000; animation: pulse 1s infinite; }
        @keyframes pulse { 50% { opacity: 0.3; } }
    </style>
</head>
<body>
    <div class="container">
        <h2>[ OMEGA PRO: ADVANCED RECON ENGINE ]</h2>
        <div class="status-bar">
            <span>STATION: RENDER_CLOUD_v3</span>
            <span>ENGINE: NATIVE_SOCKET_V2</span>
        </div>
        
        <div class="input-group">
            <input type="text" id="target" placeholder="TARGET IP / DOMAIN (e.g., google.com)">
            <button onclick="startDeepScan()" id="scanBtn">LAUNCH DEEP SCAN</button>
        </div>

        <div id="console">SYSTEM READY_...<br>> Awaiting Target Injection...</div>
    </div>

    <script>
        async function startDeepScan() {
            const target = document.getElementById('target').value;
            const consoleBox = document.getElementById('console');
            const btn = document.getElementById('scanBtn');

            if(!target) return alert("Target missing, Commander!");

            btn.disabled = true;
            consoleBox.innerHTML = "<span class='loader'>> [!] SCANNING INITIATED... ESTABLISHING SOCKET CONNECTIONS...</span><br>";

            try {
                const response = await fetch(window.location.pathname + "scan", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await response.json();
                
                let results = "> <b>SCAN REPORT FOR: " + target + "</b><br>";
                results += "> <b>TIME ELAPSED:</b> " + data.duration + "s<br>";
                results += "> ------------------------------------------------<br>";

                if(data.open_ports.length === 0) {
                    results += "> <span style='color:red;'>[!] NO EXPOSED VULNERABILITIES FOUND IN COMMON RANGE.</span>";
                } else {
                    data.open_ports.forEach(p => {
                        results += "<div class='entry'>> PORT <span class='open'>" + p.port + "</span> is OPEN <span class='meta'>| SERVICE: " + p.service + "</span></div>";
                    });
                }
                consoleBox.innerHTML = results;
            } catch (err) {
                consoleBox.innerHTML = "> ERROR: SERVER_CON_LOST";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

# Common Service Mapping
PORT_MAP = {
    21: "FTP", 22: "SSH (Secure Shell)", 23: "Telnet", 25: "SMTP (Mail)",
    53: "DNS", 80: "HTTP (Web)", 110: "POP3", 135: "RPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS (Secure Web)", 445: "SMB (Direct-over-IP)",
    1433: "MSSQL", 3306: "MySQL", 3389: "RDP (Remote Desktop)", 
    5432: "PostgreSQL", 8080: "HTTP-Proxy/Alt", 8888: "Web-Interface"
}

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8) # Fast timeout for Render speed
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = PORT_MAP.get(port, "Unknown Service")
            return {"port": port, "service": service}
        sock.close()
    except:
        pass
    return None

@script12_bp.route("/")
def index():
    return render_template_string(ADV_UI)

@script12_bp.route("/scan", methods=["POST"])
def deep_scan():
    import time
    target_raw = request.json.get('target')
    
    # DNS Resolution (Agar victim domain name daale toh use IP mein badlo)
    try:
        target = socket.gethostbyname(target_raw)
    except:
        return jsonify({"error": "Invalid Domain or IP"})

    start_time = time.time()
    open_ports = []
    
    # 50 Ports scan karenge (Advanced list)
    ports_to_scan = sorted(list(PORT_MAP.keys()) + [20, 81, 444, 1025, 2049, 3000, 5000, 5900, 6379, 27017])

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, target, p) for p in ports_to_scan]
        for f in futures:
            res = f.result()
            if res:
                open_ports.append(res)
    
    duration = round(time.time() - start_time, 2)
    return jsonify({"open_ports": open_ports, "duration": duration})

