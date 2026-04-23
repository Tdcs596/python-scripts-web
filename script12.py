import socket
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- CLI STYLE UI ---
NMAP_CLI_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>NMAP TERMINAL v7.97</title>
    <style>
        body { background: #0c0c0c; color: #d1d1d1; font-family: 'Consolas', 'Courier New', monospace; padding: 20px; }
        .terminal-window { background: #000; border: 1px solid #444; padding: 15px; min-height: 500px; box-shadow: 0 0 20px rgba(0,255,0,0.05); }
        .input-line { display: flex; align-items: center; margin-bottom: 20px; color: #00ff00; }
        input { background: transparent; border: none; color: #fff; font-family: inherit; font-size: 16px; width: 100%; outline: none; margin-left: 10px; }
        #output { white-space: pre-wrap; line-height: 1.4; color: #cccccc; }
        .cursor { display: inline-block; width: 8px; height: 15px; background: #00ff00; animation: blink 1s infinite; vertical-align: middle; }
        @keyframes blink { 50% { opacity: 0; } }
        button { display: none; }
    </style>
</head>
<body>
    <div class="terminal-window">
        <div class="input-line">
            <span>C:\\Users\\TDCS_ADMIN> nmap -A -v</span>
            <input type="text" id="target" placeholder="[IP or Domain]" onkeypress="handleKey(event)">
        </div>
        <div id="output"># Nmap 7.97 scan engine initialized. Enter target and press Enter...</div>
        <span id="cursor-main" class="cursor"></span>
    </div>

    <script>
        async function handleKey(event) {
            if (event.key === 'Enter') {
                const target = document.getElementById('target').value;
                const output = document.getElementById('output');
                if(!target) return;

                document.getElementById('cursor-main').style.display = 'none';
                output.innerHTML += `\\n\\nStarting Nmap 7.97 ( https://nmap.org ) at ${new Date().toLocaleString()}\\n`;
                output.innerHTML += `Initiating Parallel DNS resolution of 1 host...\\n`;
                output.innerHTML += `Initiating SYN Stealth Scan...\\n`;

                try {
                    const response = await fetch(window.location.pathname + "nmap_exec", {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ target: target })
                    });
                    const data = await response.json();
                    output.innerHTML += data.report;
                } catch (e) {
                    output.innerHTML += "\\n[!] FATAL ERROR: nsock_loop error 10022";
                }
                document.getElementById('cursor-main').style.display = 'inline-block';
            }
        }
    </script>
</body>
</html>
"""

def generate_nmap_report(target_raw, target_ip, open_ports, duration):
    curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"""Nmap scan report for {target_raw} ({target_ip})
Host is up (0.031s latency).
Not shown: 988 filtered tcp ports (no-response)
PORT    STATE SERVICE   VERSION
"""
    for p in open_ports:
        report += f"{p['port']}/tcp  open  {p['svc'].lower():<10} {p['ver']}\n"
        if p['port'] == 80 or p['port'] == 443:
            report += f"|_http-server-header: {p['ver']}\n"
            report += f"|_http-title: Site managed by TDCS Infrastructure\n"

    report += f"""
TRACEROUTE (using port 80/tcp)
HOP RTT      ADDRESS
1   6.00 ms  10.47.227.96
2   21.00 ms 192.168.72.131
3   22.00 ms {target_ip}

Nmap done: 1 IP address (1 host up) scanned in {duration} seconds
           Raw packets sent: 1040 | Rcvd: 22
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
        return jsonify({"report": "\n[!] Failed to resolve target."})

    start_time = time.time()
    found = []
    # Major ports and their emulated version for Vercel/Cloud feel
    check_ports = {
        80: "Vercel", 443: "Vercel", 22: "OpenSSH 8.2", 
        21: "vsftpd 3.0.3", 3306: "MySQL 8.0.21"
    }

    def scan(p, v):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.8)
            if s.connect_ex((target_ip, p)) == 0:
                return {"port": p, "svc": socket.getservbyname(p) if p < 1000 else "unknown", "ver": v}
            s.close()
        except: pass
        return None

    with ThreadPoolExecutor(max_workers=20) as exe:
        results = [exe.submit(scan, p, v) for p, v in check_ports.items()]
        for f in results:
            res = f.result()
            if res: found.append(res)

    duration = round(time.time() - start_time, 2)
    full_report = generate_nmap_report(target_raw, target_ip, found, duration)
    
    return jsonify({"report": full_report})
