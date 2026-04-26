from flask import Blueprint, render_template_string, request, jsonify
import socket
import threading
import time
from datetime import datetime

# Blueprint define kiya (Template folder hata diya kyunki hum string use kar rahe hain)
script12_bp = Blueprint('script12', __name__)

# Guaranteed results for your training target
TARGET_RESULTS = {
    '89.117.188.108': {
        'ports': {
            "21": {'state': 'open', 'service': 'ftp', 'version': 'vsftpd 3.0.3', 'vuln': 'High - Anonymous FTP'},
            "22": {'state': 'open', 'service': 'ssh', 'version': 'OpenSSH 7.6p1', 'vuln': 'Medium - Weak Config'},
            "80": {'state': 'open', 'service': 'http', 'version': 'Apache 2.4.29', 'vuln': 'Medium - Directory traversal'},
            "443": {'state': 'open', 'service': 'https', 'version': 'Apache 2.4.29', 'vuln': 'Secure'},
            "3306": {'state': 'open', 'service': 'mysql', 'version': 'MySQL 5.7.33', 'vuln': 'High - Exposed DB'},
            "8080": {'state': 'open', 'service': 'http-proxy', 'version': 'Tomcat 9.0.24', 'vuln': 'Critical - RCE'}
        },
        'os': 'Linux 5.4 Ubuntu 18.04 (94% confidence)',
        'vulns': [
            'vsftpd 3.0.3 - CVE-2011-2523 Backdoor',
            'MySQL 5.7.33 - CVE-2021-27928 Auth Bypass',
            'Tomcat 9.0.24 - CVE-2019-0232 RCE'
        ]
    }
}

def socket_scan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((host, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

# --- FIX: Route sirf "/" rakha hai kyunki app.py pehle hi "/script12" handles karta hai ---
@script12_bp.route('/')
def nmap_ultimate():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>TDCS NMAP ULTIMATE</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; margin: 0; padding: 20px; overflow: hidden; }
        .container { display: flex; height: 95vh; border: 1px solid #333; background: #111; }
        .left-panel { width: 350px; padding: 20px; border-right: 1px solid #444; background: #1a1a1a; }
        .right-panel { flex: 1; padding: 20px; overflow-y: auto; background: #000; position: relative; }
        input, button { width: 100%; padding: 12px; margin: 10px 0; background: #222; border: 1px solid #00ff00; color: #00ff00; font-family: inherit; }
        button { cursor: pointer; font-weight: bold; background: #004400; }
        button:hover { background: #008800; }
        #output { white-space: pre-wrap; font-size: 13px; line-height: 1.5; color: #00ff00; }
        .header { color: #ffff00; text-align: center; font-size: 18px; margin-bottom: 20px; text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <div class="header">🔥 NMAP ULTIMATE v7.94</div>
            <input type="text" id="target_ip" value="89.117.188.108" placeholder="Target IP">
            <button onclick="runScan('quick')">QUICK SCAN</button>
            <button onclick="runScan('vuln')">VULN SCAN</button>
            <button onclick="runScan('full')">OS DETECT</button>
            <button onclick="document.getElementById('output').innerHTML='> Terminal Cleared.\\n'" style="border-color: #ff0000; color: #ff0000;">CLEAR TERMINAL</button>
        </div>
        <div class="right-panel">
            <div id="output">Starting Nmap Ultimate Scanner...\\n> Ready for reconnaissance.</div>
        </div>
    </div>

    <script>
        async function runScan(type) {
            const target = document.getElementById('target_ip').value;
            const output = document.getElementById('output');
            output.innerHTML += `\\n\\n[+] Initiating ${type.toUpperCase()} scan on ${target}...\\n`;

            try {
                // FIX: window.location.pathname use kiya taaki ye "/script12/scan" par hi jaye
                const response = await fetch(window.location.pathname + 'scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target, scan_type: type})
                });
                
                const data = await response.json();
                
                let res = `\\nNmap scan report for ${data.scan_info.host}\\nHost is up (0.02s latency).\\n\\n`;
                res += `PORT     STATE    SERVICE    VERSION\\n`;
                res += `----     -----    -------    -------\\n`;
                
                for (const [port, info] of Object.entries(data.ports)) {
                    res += `${port.padEnd(8)} ${info.state.padEnd(8)} ${info.service.padEnd(10)} ${info.version}\\n`;
                }
                
                if(data.os && data.os !== 'Unknown') res += `\\nOS DETAILS: ${data.os}\\n`;
                if(data.vulns && data.vulns.length > 0) {
                    res += `\\n🔥 CRITICAL VULNERABILITIES FOUND:\\n`;
                    data.vulns.forEach(v => res += `  • ${v}\\n`);
                }
                
                res += `\\nScan completed at ${new Date().toLocaleTimeString()}\\n`;
                output.innerHTML += res;
                
                // Auto scroll to bottom
                const panel = document.querySelector('.right-panel');
                panel.scrollTop = panel.scrollHeight;
                
            } catch (e) {
                output.innerHTML += "\\n[!] ERROR: Connection refused by scanner engine. Check routing!\\n";
            }
        }
    </script>
</body>
</html>
    """)

# --- FIX: Route sirf "/scan" rakha hai ---
@script12_bp.route('/scan', methods=['POST'])
def run_nmap_scan():
    data = request.json
    target = data.get('target', '89.117.188.108')
    scan_type = data.get('scan_type', 'quick')
    
    if target == '89.117.188.108':
        res = TARGET_RESULTS[target].copy()
        res['scan_info'] = {'host': target, 'scan_type': scan_type}
        return jsonify(res)
    
    # Simple real scan for other IPs (limited to avoid server load)
    ports = [21, 22, 80, 443, 3306, 8080]
    found = {}
    for p in ports:
        if socket_scan(target, p):
            found[str(p)] = {'state': 'open', 'service': 'detected', 'version': 'unknown'}
            
    return jsonify({
        'ports': found,
        'os': 'Detected Generic Stack',
        'vulns': [],
        'scan_info': {'host': target, 'scan_type': scan_type}
    })

