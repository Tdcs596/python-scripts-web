import socket
import threading
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- ULTIMATE CYBER UI ---
XTREME_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA X-TREME RECON</title>
    <style>
        body { background: #020202; color: #00ff41; font-family: 'Courier New', monospace; margin: 0; padding: 20px; overflow-x: hidden; }
        .header { border-bottom: 2px solid #00ff41; padding-bottom: 10px; margin-bottom: 20px; text-shadow: 0 0 10px #00ff41; }
        .main-grid { display: grid; grid-template-columns: 350px 1fr; gap: 20px; }
        .sidebar { background: #050505; border: 1px solid #00ff41; padding: 20px; height: fit-content; }
        .terminal { background: #000; border: 1px solid #333; padding: 15px; height: 500px; overflow-y: auto; font-size: 13px; box-shadow: inset 0 0 20px #00ff4111; }
        
        input { background: #111; border: 1px solid #00ff41; color: #fff; padding: 12px; width: 90%; margin-bottom: 10px; outline: none; }
        button { background: #00ff41; color: #000; border: none; padding: 12px; width: 98%; font-weight: bold; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 20px #fff; }
        
        .result-card { border-left: 3px solid #00ff41; background: #0a0a0a; margin-bottom: 10px; padding: 10px; animation: slideIn 0.3s ease; }
        .vuln-high { border-left: 3px solid #ff003c; background: #1a0005; }
        .tag { font-size: 10px; padding: 2px 6px; border-radius: 2px; margin-right: 5px; text-transform: uppercase; }
        .tag-vuln { background: #ff003c; color: #fff; }
        .tag-safe { background: #008800; color: #fff; }
        
        @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        .blink { animation: blinker 1s linear infinite; color: #ff003c; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="header">
        <h2>CORE_SYSTEM: OMEGA X-TREME v4.0 (RECONNAISSANCE ENGINE)</h2>
    </div>

    <div class="main-grid">
        <div class="sidebar">
            <h3>TARGET INJECTION</h3>
            <input type="text" id="target" placeholder="IP or DOMAIN">
            <button onclick="startDeepRecon()" id="execBtn">Launch Deep Recon</button>
            
            <div id="intel-box" style="margin-top:20px; font-size:12px; border-top:1px solid #222; padding-top:10px;">
                <p>> INTEL_STATUS: <span id="status-text">AWAITING_INPUT</span></p>
                <div id="geo-data"></div>
            </div>
        </div>

        <div class="terminal" id="terminal">
            <div style="color:#555;">> [SYSTEM] Engine Initialized...<br>> [SYSTEM] Ready for Target Packet Injection...</div>
        </div>
    </div>

    <script>
        async function startDeepRecon() {
            const target = document.getElementById('target').value;
            const term = document.getElementById('terminal');
            const btn = document.getElementById('execBtn');
            const geo = document.getElementById('geo-data');
            
            if(!target) return alert("Bhai, target daalo!");

            btn.disabled = true;
            btn.innerText = "RECON IN PROGRESS...";
            term.innerHTML = "<p class='blink'>> [!] INITIATING DEEP SCAN ON " + target + "...</p>";

            try {
                const response = await fetch(window.location.pathname + "deep_recon", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await response.json();

                if(data.error) {
                    term.innerHTML += `<p style="color:red;">> [ERROR] ${data.error}</p>`;
                } else {
                    // Update Intel
                    geo.innerHTML = `<p style="color:#888;"><b>ISP:</b> ${data.intel.isp}<br><b>LOC:</b> ${data.intel.city}, ${data.intel.country}<br><b>ORG:</b> ${data.intel.org}</p>`;
                    
                    let html = `<p style="color:#00ff41;">> [SUCCESS] RECON COMPLETED IN ${data.duration}s</p>`;
                    data.scan_results.forEach(p => {
                        let isVuln = p.risk !== "SAFE";
                        html += `
                            <div class="result-card ${isVuln ? 'vuln-high' : ''}">
                                <b>PORT ${p.port} (${p.service})</b> 
                                ${isVuln ? '<span class="tag tag-vuln">RISK DETECTED</span>' : '<span class="tag tag-safe">STABLE</span>'}<br>
                                <span style="color:#888; font-size:11px;">BANNER: ${p.banner}</span><br>
                                <span style="color:${isVuln ? '#ff003c' : '#00ff41'}; font-size:11px;">ADVISORY: ${p.advisory}</span>
                            </div>`;
                    });
                    term.innerHTML = html;
                }
            } catch (e) {
                term.innerHTML += "<p style="color:red;">> [FATAL] CONNECTION_REFUSED</p>";
            }
            btn.disabled = false;
            btn.innerText = "Launch Deep Recon";
        }
    </script>
</body>
</html>
"""

# Advanced Vulnerability Knowledge Base
VULN_INTEL = {
    21: {"service": "FTP", "advisory": "Potential for Anonymous login / Brute Force."},
    22: {"service": "SSH", "advisory": "Ensure Key-based Auth. Check for outdated OpenSSH versions."},
    23: {"service": "TELNET", "advisory": "CRITICAL: Plaintext protocol. Sniffing risk is 100%."},
    25: {"service": "SMTP", "advisory": "Check for Open Relay vulnerabilities."},
    53: {"service": "DNS", "advisory": "Zone Transfer (AXFR) might be possible."},
    80: {"service": "HTTP", "advisory": "Exposed Web Server. Run Directory Brute-Force."},
    110: {"service": "POP3", "advisory": "Email credentials might be sent in plaintext."},
    443: {"service": "HTTPS", "advisory": "SSL/TLS Secured. Check for Heartbleed/Expired certs."},
    445: {"service": "SMB", "advisory": "HIGH RISK: Potential EternalBlue/SambaCry vulnerability."},
    3306: {"service": "MySQL", "advisory": "Database exposed. Check for default 'root' without password."},
    3389: {"service": "RDP", "advisory": "High Risk: BlueKeep or brute-force attack vectors."},
    8080: {"service": "HTTP-ALT", "advisory": "Commonly used for unhardened Admin Panels."}
}

def grab_service_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1.2)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner if banner else "No banner (Silent Service)"
    except:
        return "Unknown Service Response"

def deep_scan_worker(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((ip, port))
        if result == 0:
            banner = grab_service_banner(ip, port)
            intel = VULN_INTEL.get(port, {"service": "Unknown", "advisory": "No specific advisory for this port."})
            risk_level = "HIGH" if port in [21, 23, 445, 3306, 3389] else "SAFE"
            return {
                "port": port,
                "service": intel["service"],
                "banner": banner,
                "advisory": intel["advisory"],
                "risk": risk_level
            }
        sock.close()
    except:
        pass
    return None

@script12_bp.route("/")
def index():
    return render_template_string(XTREME_UI)

@script12_bp.route("/deep_recon", methods=["POST"])
def deep_recon():
    target_input = request.json.get('target')
    try:
        target_ip = socket.gethostbyname(target_input)
        # Geo-Intel Integration
        geo_res = requests.get(f"http://ip-api.com/json/{target_ip}", timeout=3).json()
    except:
        return jsonify({"error": "Host Resolution Failed. Target might be offline."})

    start_time = time.time()
    results = []
    scan_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 1433, 3306, 3389, 8080, 8443]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(deep_scan_worker, target_ip, p) for p in scan_ports]
        for f in futures:
            res = f.result()
            if res:
                results.append(res)

    return jsonify({
        "scan_results": results,
        "duration": round(time.time() - start_time, 2),
        "intel": {
            "isp": geo_res.get('isp', 'Unknown'),
            "city": geo_res.get('city', 'Unknown'),
            "country": geo_res.get('country', 'Unknown'),
            "org": geo_res.get('org', 'Unknown')
        }
    })

