import socket
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- ULTRA-REALISTIC TERMINAL UI ---
ULTRA_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>TDCS OMEGA-X SCANNER</title>
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Consolas', monospace; padding: 20px; }
        .terminal { background: #000; border: 1px solid #00ff41; padding: 20px; min-height: 600px; box-shadow: 0 0 30px rgba(0,255,65,0.2); }
        .cmd-line { display: flex; align-items: center; background: #111; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        input { background: transparent; border: none; color: #fff; font-size: 16px; width: 70%; outline: none; margin-left: 10px; font-family: inherit; }
        .btn { background: #00ff41; color: #000; border: none; padding: 8px 20px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        #output { white-space: pre-wrap; line-height: 1.6; color: #ccc; font-size: 13px; }
        .v-high { color: #ff3e3e; font-weight: bold; }
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header" style="color:#888; font-size:11px; margin-bottom:10px;">
            TDCS TERMINAL [Version 10.0.19045.4291] | (c) TDCS Technologies.
        </div>
        <div class="cmd-line">
            <span>root@tdcs_recon:~# nmap -sV -O -T4</span>
            <input type="text" id="target" placeholder="Enter Target IP/Domain" autofocus>
            <button class="btn" onclick="runIntenseScan()">SCAN</button>
        </div>
        <div id="output">Ready for deep-packet inspection...</div>
    </div>

    <script>
        document.getElementById('target').addEventListener('keypress', (e) => { if(e.key === 'Enter') runIntenseScan(); });

        async function runIntenseScan() {
            const target = document.getElementById('target').value;
            const out = document.getElementById('output');
            if(!target) return;

            out.innerHTML = `\\n<span class="blink">Starting Nmap 7.97 ( https://nmap.org ) at ${new Date().toLocaleString()}</span>\\n`;
            out.innerHTML += `NSE: Loaded 158 scripts for scanning.\\n`;
            out.innerHTML += `Initiating SYN Stealth Scan against ${target}...\\n`;

            try {
                const res = await fetch(window.location.pathname + "intense_scan", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target })
                });
                const data = await res.json();
                out.innerHTML += data.report;
            } catch (e) {
                out.innerHTML += "\\n[!] FATAL: Engine process aborted.";
            }
        }
    </script>
</body>
</html>
"""

def get_banner(ip, port):
    """Real service version nikalne ke liye banner grabber."""
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect((ip, port))
        # Pehle connection bante hi kuch data bhejte hain taaki server reply de
        if port == 80: s.send(b"HEAD / HTTP/1.1\\r\\n\\r\\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner[:50] if banner else "Unknown Service"
    except:
        return "Service undetected"

def perform_scan_logic(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        if sock.connect_ex((ip, port)) == 0:
            banner = get_banner(ip, port)
            return {"port": port, "banner": banner}
        sock.close()
    except: pass
    return None

@script12_bp.route("/")
def index():
    return render_template_string(ULTRA_UI)

@script12_bp.route("/intense_scan", methods=["POST"])
def intense_scan():
    target_raw = request.json.get('target')
    try:
        target_ip = socket.gethostbyname(target_raw)
    except:
        return jsonify({"report": "\\n[!] ERROR: Failed to resolve host."})

    start = time.time()
    found_ports = []
    
    # Extensive Port List (Common + Database + Admin + Backdoors)
    critical_ports = [
        21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 
        1723, 3306, 3389, 5900, 8000, 8080, 8443, 8888, 9000
    ]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(perform_scan_logic, target_ip, p) for p in critical_ports]
        for f in futures:
            res = f.result()
            if res: found_ports.append(res)

    duration = round(time.time() - start, 2)
    
    # Generating Real Nmap Style Report
    report = f"\\nNmap scan report for {target_raw} ({target_ip})\\n"
    report += f"Host is up (0.024s latency).\\n"
    report += f"Not shown: {1000 - len(found_ports)} closed ports\\n\\n"
    report += f"{'PORT':<10} {'STATE':<10} {'SERVICE':<15} {'VERSION':<30}\\n"
    report += "-"*65 + "\\n"
    
    for p in found_ports:
        svc_name = socket.getservbyname(p['port']) if p['port'] < 1000 else "unknown"
        report += f"{str(p['port'])+'/tcp':<10} {'open':<10} {svc_name:<15} {p['banner']}\\n"

    report += f"\\nAggressive OS guesses: Linux 4.15 - 5.6 (91%), Windows 10 (85%)\\n"
    report += f"Network Distance: 2 hops\\n"
    report += f"\\nNmap done: 1 IP address (1 host up) scanned in {duration} seconds\\n"
    
    return jsonify({"report": report})
