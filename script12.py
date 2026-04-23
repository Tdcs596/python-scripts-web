import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- HACKER CONSOLE UI ---
ULTIMATE_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA X-TREME RECON</title>
    <style>
        body { background: #020202; color: #00ff41; font-family: 'Courier New', monospace; padding: 20px; }
        .terminal { border: 2px solid #00ff41; background: #000; padding: 20px; box-shadow: 0 0 25px #00ff4133; max-width: 900px; margin: auto; }
        .header { border-bottom: 1px solid #00ff41; margin-bottom: 15px; padding-bottom: 10px; font-weight: bold; }
        input { background: #111; border: 1px solid #00ff41; color: #fff; padding: 12px; width: 70%; margin-right: 10px; outline: none; }
        button { background: #00ff41; color: #000; border: none; padding: 12px 25px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #output { margin-top: 20px; background: #050505; border: 1px solid #222; height: 450px; overflow-y: auto; padding: 15px; font-size: 13px; line-height: 1.5; }
        .port-entry { border-left: 2px solid #00ff41; padding-left: 10px; margin-bottom: 10px; }
        .vulnerable { color: #ff3333; font-weight: bold; }
        .secure { color: #00ff41; }
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">OMEGA SYSTEM v5.0 | ADVANCED RECONNAISSANCE ENGINE</div>
        <div style="margin-bottom: 20px;">
            <input type="text" id="target" placeholder="TARGET_IP / DOMAIN (e.g. google.com)">
            <button onclick="startScan()" id="btn">ENGINE_START</button>
        </div>
        <div id="output">> SYSTEM_READY: Awaiting Target Injection...</div>
    </div>

    <script>
        async function startScan() {
            const target = document.getElementById('target').value;
            const output = document.getElementById('output');
            const btn = document.getElementById('btn');

            if(!target) return alert("Target missing!");

            btn.disabled = true;
            output.innerHTML = "<span class='blink'>> [!] INITIALIZING DEEP RECONNAISSANCE... DATA PACKETS DISPATCHED...</span><br>";

            try {
                const response = await fetch(window.location.pathname + "scan", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await response.json();
                
                let report = `> SCAN COMPLETED FOR: ${target}\\n`;
                report += `> ELAPSED TIME: ${data.duration}s\\n`;
                report += `> --------------------------------------------------\\n`;

                if(data.results.length === 0) {
                    report += "> [!] ALERT: No common ports found open on this target.";
                } else {
                    data.results.forEach(p => {
                        let riskClass = p.risk === "HIGH" ? "vulnerable" : "secure";
                        report += `<div class='port-entry'>[+] PORT: ${p.port} | SERVICE: ${p.service}\\n`;
                        report += `    STATUS: <span class='${riskClass}'>${p.status}</span>\\n`;
                        report += `    ADVISORY: ${p.info}</div>`;
                    });
                }
                output.innerHTML = report;
            } catch (err) {
                output.innerText = "> ERROR: SERVER_HANDSHAKE_FAILED";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

# Advanced Feature Set: Port mapping + Advisory + Risk Analysis
INTEL_DB = {
    21: {"svc": "FTP", "risk": "HIGH", "info": "Risk of Anonymous Login. Plaintext protocol."},
    22: {"svc": "SSH", "risk": "MED", "info": "Secure Shell. Check for brute-force attempts."},
    23: {"svc": "Telnet", "risk": "HIGH", "info": "CRITICAL: Insecure. Sniffing risk is 100%."},
    25: {"svc": "SMTP", "risk": "MED", "info": "Mail server. Check for open relay issues."},
    53: {"svc": "DNS", "risk": "LOW", "info": "Domain Name System. Possible Zone Transfer."},
    80: {"svc": "HTTP", "risk": "MED", "info": "Web Server. Check for directory listing."},
    110: {"svc": "POP3", "risk": "MED", "info": "Mail protocol. Plaintext auth possible."},
    443: {"svc": "HTTPS", "risk": "LOW", "info": "Secure Web. Check SSL/TLS certificate."},
    445: {"svc": "SMB", "risk": "HIGH", "info": "Vulnerable to EternalBlue / SMBGhost."},
    3306: {"svc": "MySQL", "risk": "HIGH", "info": "Database exposed. Check root password."},
    3389: {"svc": "RDP", "risk": "HIGH", "info": "Remote Desktop. BlueKeep vulnerability risk."},
    8080: {"svc": "HTTP-Proxy", "risk": "MED", "info": "Secondary Web Port. Often unhardened."}
}

def scan_worker(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((ip, port))
        if result == 0:
            intel = INTEL_DB.get(port, {"svc": "Unknown", "risk": "MED", "info": "No info available."})
            return {
                "port": port,
                "service": intel["svc"],
                "status": "OPEN",
                "risk": intel["risk"],
                "info": intel["info"]
            }
        sock.close()
    except:
        pass
    return None

@script12_bp.route("/")
def index():
    return render_template_string(ULTIMATE_UI)

@script12_bp.route("/scan", methods=["POST"])
def perform_scan():
    target_raw = request.json.get('target')
    try:
        target_ip = socket.gethostbyname(target_raw)
    except:
        return jsonify({"error": "Host resolution failed"}), 400

    start = time.time()
    found = []
    # All major ports
    ports_to_check = [21, 22, 23, 25, 53, 80, 110, 443, 445, 3306, 3389, 8080]

    with ThreadPoolExecutor(max_workers=40) as executor:
        results = [executor.submit(scan_worker, target_ip, p) for p in ports_to_check]
        for f in results:
            res = f.result()
            if res:
                found.append(res)

    duration = round(time.time() - start, 2)
    return jsonify({"results": found, "duration": duration})
