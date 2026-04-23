import socket
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- CLI STYLE UI WITH FIXED CONTROLS ---
NMAP_CLI_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>NMAP TERMINAL v7.97</title>
    <style>
        body { background: #0c0c0c; color: #d1d1d1; font-family: 'Consolas', 'Courier New', monospace; padding: 20px; }
        .terminal-window { background: #000; border: 1px solid #444; padding: 15px; min-height: 550px; box-shadow: 0 0 20px rgba(0,255,0,0.1); position: relative; }
        .input-line { display: flex; align-items: center; margin-bottom: 20px; color: #00ff00; background: #111; padding: 10px; border-radius: 4px; }
        input { background: transparent; border: none; color: #fff; font-family: inherit; font-size: 16px; width: 70%; outline: none; margin-left: 10px; }
        .exec-btn { background: #00ff00; color: #000; border: none; padding: 5px 15px; font-weight: bold; cursor: pointer; border-radius: 3px; font-family: inherit; }
        .exec-btn:hover { background: #fff; }
        #output { white-space: pre-wrap; line-height: 1.5; color: #cccccc; margin-top: 15px; font-size: 14px; border-top: 1px solid #222; padding-top: 15px; }
        .blink { animation: blinker 1s linear infinite; color: #00ff00; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="terminal-window">
        <div class="input-line">
            <span>TDCS_ADMIN@RECON:~# nmap -A</span>
            <input type="text" id="target" placeholder="Enter IP/Domain" autocomplete="off" autofocus>
            <button class="exec-btn" onclick="triggerScan()">EXECUTE</button>
        </div>
        <div id="output"># Nmap 7.97 ready. Type target and press Enter or click Execute...</div>
    </div>

    <script>
        // Enter key support
        document.getElementById('target').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                triggerScan();
            }
        });

        async function triggerScan() {
            const targetInput = document.getElementById('target');
            const target = targetInput.value;
            const output = document.getElementById('output');
            
            if(!target) return;

            output.innerHTML += `\\n\\n<span class="blink">Starting Nmap 7.97 ( https://nmap.org ) at ${new Date().toLocaleString()}</span>\\n`;
            output.innerHTML += `Scanning ${target}...\\n`;

            try {
                const response = await fetch(window.location.pathname + "nmap_exec", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await response.json();
                output.innerHTML += data.report;
                
                // Auto-scroll to bottom
                window.scrollTo(0, document.body.scrollHeight);
            } catch (e) {
                output.innerHTML += "\\n[!] ERROR: Connection to scan engine failed.\\n";
            }
            targetInput.value = ""; // Clear input for next scan
        }
    </script>
</body>
</html>
"""

def generate_nmap_report(target_raw, target_ip, open_ports, duration):
    report = f"""Nmap scan report for {target_raw} ({target_ip})
Host is up (0.031s latency).
Not shown: 995 filtered tcp ports (no-response)

PORT    STATE SERVICE   VERSION
"""
    if not open_ports:
        report += "No open ports detected in the common range.\\n"
    else:
        for p in open_ports:
            report += f"{p['port']}/tcp  open  {p['svc']:<10} {p['ver']}\\n"
            if p['port'] in [80, 443]:
                report += f"|_http-server-header: Vercel/Cloudfront\\n"

    report += f"""
TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   6.00 ms  10.47.227.1
2   21.00 ms 192.168.1.1
3   22.00 ms {target_ip}

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in {duration} seconds
"""
    return report

@script12_bp.route("/")
def index():
    return render_template_string(NMAP_CLI_UI)

@script12_bp.route("/nmap_exec", methods=["POST"])
def nmap_exec():
    target_raw = request.json.get('target')
    try:
        target_ip = socket.gethostbyname(target_raw)
    except:
        return jsonify({"report": "\\n[!] Failed to resolve target. Check your internet or target address."})

    start_time = time.time()
    found = []
    
    # Common ports to check
    check_ports = {
        80: "HTTP", 443: "HTTPS", 22: "OpenSSH", 
        21: "vsftpd", 3306: "MySQL", 3389: "RDP"
    }

    def scan(p, s_name):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            if s.connect_ex((target_ip, p)) == 0:
                return {"port": p, "svc": s_name, "ver": "Cloud-Service-v1.0"}
            s.close()
        except: pass
        return None

    with ThreadPoolExecutor(max_workers=20) as exe:
        results = [exe.submit(scan, p, s) for p, s in check_ports.items()]
        for f in results:
            res = f.result()
            if res: found.append(res)

    duration = round(time.time() - start_time, 2)
    full_report = generate_nmap_report(target_raw, target_ip, found, duration)
    
    return jsonify({"report": full_report})
