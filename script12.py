import socket
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- UI DESIGN ---
SOCKET_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA NATIVE SCANNER</title>
    <style>
        body { background: #000; color: #00ff41; font-family: 'Courier New', monospace; padding: 30px; text-align: center; }
        .scanner-box { border: 2px solid #00ff41; padding: 20px; background: #050505; display: inline-block; width: 90%; max-width: 600px; box-shadow: 0 0 20px #00ff4133; }
        input { background: #111; border: 1px solid #00ff41; color: #fff; padding: 12px; width: 80%; margin: 10px 0; }
        button { background: #00ff41; color: #000; border: none; padding: 15px; width: 85%; font-weight: bold; cursor: pointer; }
        #results { margin-top: 20px; background: #000; padding: 15px; border: 1px solid #333; height: 300px; overflow-y: auto; text-align: left; font-size: 14px; }
        .open { color: #00ff41; font-weight: bold; }
        .closed { color: #444; }
    </style>
</head>
<body>
    <div class="scanner-box">
        <h2>[ NATIVE PORT SCANNER ]</h2>
        <p style="color: #888;">Render Compatible | No API Required</p>
        <input type="text" id="target" placeholder="Enter IP (e.g. 8.8.8.8)">
        <br>
        <button onclick="runScan()" id="btn">START SCAN</button>
        <div id="results">Waiting for target...</div>
    </div>

    <script>
        async function runScan() {
            const target = document.getElementById('target').value;
            const resBox = document.getElementById('results');
            const btn = document.getElementById('btn');

            if(!target) return alert("Target IP daalo bhai!");

            btn.disabled = true;
            resBox.innerHTML = "Scanning common ports... Please wait...";

            try {
                const response = await fetch(window.location.pathname + "scan", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await response.json();
                
                let output = "<b>Scan Results for " + target + ":</b><br><br>";
                if(data.open_ports.length === 0) {
                    output += "No open ports found in common range.";
                } else {
                    data.open_ports.forEach(p => {
                        output += "<span class='open'>[+] Port " + p + " is OPEN</span><br>";
                    });
                }
                resBox.innerHTML = output;
            } catch (err) {
                resBox.innerText = "Error connecting to server.";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@script12_bp.route("/")
def index():
    return render_template_string(SOCKET_UI)

def check_port(ip, port):
    """Try to connect to a specific port."""
    try:
        # Socket object create kiya
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0) # 1 second wait karega connection ka
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port
        sock.close()
    except:
        pass
    return None

@script12_bp.route("/scan", methods=["POST"])
def scan():
    target = request.json.get('target')
    
    # Common ports jo hum scan karenge
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3306, 3389, 8080]
    
    open_ports = []
    
    # Threading use kar rahe hain taaki scan fast ho
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = [executor.submit(check_port, target, port) for port in common_ports]
        for f in results:
            res = f.result()
            if res:
                open_ports.append(res)
                
    return jsonify({"open_ports": open_ports})
