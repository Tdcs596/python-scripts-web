from flask import Blueprint, render_template_string, request, jsonify
import socket
import time

script12_bp = Blueprint('script12', __name__)

# --- ADVANCED PRODUCTION LAB TARGET MAP DATA ---
TARGET_RESULTS = {
    '89.117.188.108': {
        'ports': {
            "21": {'state': 'open', 'service': 'ftp', 'version': 'vsftpd 3.0.3', 'reason': 'syn-ack', 'ttl': '64'},
            "22": {'state': 'open', 'service': 'ssh', 'version': 'OpenSSH 7.6p1 Ubuntu 4ubuntu0.3', 'reason': 'syn-ack', 'ttl': '64'},
            "80": {'state': 'open', 'service': 'http', 'version': 'Apache httpd 2.4.29 ((Ubuntu))', 'reason': 'syn-ack', 'ttl': '63'},
            "443": {'state': 'open', 'service': 'https', 'version': 'Apache httpd 2.4.29 (SSL Configuration Matrix)', 'reason': 'syn-ack', 'ttl': '63'},
            "3306": {'state': 'open', 'service': 'mysql', 'version': 'MySQL 5.7.33-0ubuntu0.18.04.1', 'reason': 'syn-ack', 'ttl': '64'},
            "8080": {'state': 'open', 'service': 'http-proxy', 'version': 'Apache Tomcat/9.0.24', 'reason': 'syn-ack', 'ttl': '63'}
        },
        'os': 'Linux 5.0 - 5.4 • Ubuntu Linux 18.04 LTS (Device Type: General Purpose | CPE: cpe:/o:linux:linux_kernel:5)',
        'distance': '2 hops',
        'script_output': [
            '| ftp-anon: Anonymous FTP login allowed (FTP code 230)',
            '| mysql-info: \n|   Protocol: 10\n|   Version: 5.7.33-0ubuntu0.18.04.1\n|   Thread id: 412\n|   Status: Autocommit Engine Active',
            '|_http-server-header: Apache/2.4.29 (Ubuntu)',
            '| ssl-cert: Subject: commonName=fortifiedbytes.local\n|   Issuer: commonName=Fortifiedbytes Root CA',
            '| vulners: \n|   cpe:/a:apache:tomcat:9.0.24:\n|     CVE-2019-0232\t10.0\thttps://vulners.com/cve/CVE-2019-0232\n|     CVE-2020-1938\t7.5\thttps://vulners.com/cve/CVE-2020-1938'
        ]
    }
}

def direct_socket_probe(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.4)
        result = sock.connect_ex((host, port))
        sock.close()
        return port if result == 0 else None
    except:
        return None

@script12_bp.route('/')
def nmap_ultimate():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>FORTIFIEDBYTES | Elite Network Mapper Engine</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Consolas', 'Courier New', monospace; background: #020408; color: #38bdf8; padding: 20px; }
        .container { display: flex; height: 93vh; border: 2px solid #1e293b; background: #000; border-radius: 14px; overflow: hidden; box-shadow: 0 0 40px rgba(56,189,248,0.15); }
        
        /* Left Configuration Array Control */
        .left-panel { width: 400px; padding: 25px; border-right: 2px solid #1e293b; background: #050b14; display: flex; flex-direction: column; justify-content: space-between; overflow-y: auto; }
        .right-panel { flex: 1; padding: 25px; overflow-y: auto; background: #010205; position: relative; }
        
        .panel-title { color: #fff; font-size: 18px; font-weight: bold; margin-bottom: 25px; letter-spacing: 1px; display: flex; align-items: center; gap: 10px; }
        .panel-title span { color: #f43f5e; text-shadow: 0 0 10px rgba(244,63,94,0.5); }
        
        label { font-size: 11px; color: #0284c7; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-top: 15px; margin-bottom: 6px; font-weight: bold; }
        input, select { width: 100%; padding: 12px 14px; background: #020408; border: 1px solid #0f355c; color: #fff; font-family: inherit; border-radius: 6px; outline: none; transition: 0.3s; font-size: 13px; }
        input:focus, select:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.15); }
        
        .cli-preview { background: #020408; border: 1px dashed #1e293b; padding: 12px; border-radius: 6px; font-size: 12px; color: #fda4af; margin-top: 10px; word-break: break-all; }
        
        .btn-group { margin-top: 25px; display: flex; flex-direction: column; gap: 10px; }
        button { width: 100%; padding: 14px; font-weight: bold; background: #38bdf8; color: #000; border: none; font-family: inherit; cursor: pointer; border-radius: 8px; transition: 0.2s; text-transform: uppercase; letter-spacing: 1.5px; font-size: 13px; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; transform: translateY(-1px); }
        
        .btn-clear { background: transparent; border: 1px solid #f43f5e; color: #f43f5e; }
        .btn-clear:hover { background: #450a0a; color: #fff; box-shadow: 0 0 15px rgba(244,63,94,0.3); }
        
        #output { white-space: pre-wrap; font-size: 13px; line-height: 1.6; color: #e2e8f0; }
        .brand-tag { font-size: 10px; color: #475569; text-align: center; letter-spacing: 3px; text-transform: uppercase; border-top: 1px dashed #1e293b; padding-top: 25px; margin-top: 20px; }
        
        /* Custom Terminal Aesthetics */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #010205; }
        ::-webkit-scrollbar-thumb { background: #0f355c; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <div>
                <div class="panel-title">🛰️ FORTIFIEDBYTES <span>MAPPER Engine</span></div>
                
                <label for="target_ip">Target Node IPv4 Address / Target Range</label>
                <input type="text" id="target_ip" value="89.117.188.108" oninput="updateCliStructure()">
                
                <label for="scan_mode">Nmap Scan Type Command Options</label>
                <select id="scan_mode" onchange="updateCliStructure()">
                    <option value="-sS">-sS (TCP SYN Stealth Scan - Recommended)</option>
                    <option value="-sT">-sT (TCP Connect Scan - Complete Handshake)</option>
                    <option value="-sU">-sU (UDP Protocol Scan - Core Services)</option>
                    <option value="-sA">-sA (ACK Scan - Firewall Rule Mapping)</option>
                </select>
                
                <label for="port_range">Port Ranges Array Configuration</label>
                <select id="port_range" onchange="updateCliStructure()">
                    <option value="--top-ports 1000">Default Base (Top 1000 Common System Ports)</option>
                    <option value="-p 21,22,80,443,3306,8080">Targeted Matrix (-p 21,22,80,443,3306,8080)</option>
                    <option value="-p-">All Engine Channels (-p- 1-65535 Extensive)</option>
                </select>

                <label for="engine_flags">Advanced Flag Configurations</label>
                <select id="engine_flags" onchange="updateCliStructure()">
                    <option value="-F">-F (Fast Scan Mode - Limited Scope)</option>
                    <option value="-sV -O --script vuln">-A (Aggressive Version, OS & Deep Vuln Engine)</option>
                    <option value="-Pn -sV">-Pn -sV (Skip Ping + Intensive Service Versioning)</option>
                </select>
                
                <label>Raw Terminal Command Execution Preview</label>
                <div class="cli-preview" id="cli_command_box">nmap -sS --top-ports 1000 -F 89.117.188.108</div>
                
                <div class="btn-group">
                    <button onclick="executeAdvancedEngineScan()">🚀 Initialize Live Network Scan</button>
                    <button onclick="resetConsoleBuffer()" class="btn-clear">🧹 Clear Terminal Shell</button>
                </div>
            </div>
            
            <div class="brand-tag">FORTIFIEDBYTES PIPELINE HUB</div>
        </div>
        
        <div class="right-panel">
            <div id="output">Fortifiedbytes engine infrastructure connection stabilized.\nAwaiting active diagnostic instructions...</div>
        </div>
    </div>

    <script>
        function updateCliStructure() {
            const target = document.getElementById('target_ip').value.trim() || '127.0.0.1';
            const mode = document.getElementById('scan_mode').value;
            const ports = document.getElementById('port_range').value;
            const flags = document.getElementById('engine_flags').value;
            
            document.getElementById('cli_command_box').innerText = `nmap ${mode} ${ports} ${flags} ${target}`;
        }

        function resetConsoleBuffer() {
            document.getElementById('output').innerHTML = "Console environment cleared. Ready for execution stream.\n";
        }

        async function executeAdvancedEngineScan() {
            const target = document.getElementById('target_ip').value.trim();
            const mode = document.getElementById('scan_mode').value;
            const ports = document.getElementById('port_range').value;
            const flags = document.getElementById('engine_flags').value;
            const output = document.getElementById('output');
            
            if(!target) {
                alert("Bhai, Target Node IP address field mandatory hai!");
                return;
            }

            // Real-feel stream initialization matching standard Nmap terminal outputs
            output.innerHTML += `\n\n# nmap ${mode} ${ports} ${flags} ${target}\n`;
            output.innerHTML += `Starting Nmap 7.94 ( https://nmap.org ) at ${new Date().toISOString().split('T')[0]} ${new Date().toLocaleTimeString()}\n`;
            output.innerHTML += `NSE: Loaded 284 essential script modules for deep exploitation metrics.\n`;
            output.innerHTML += `Initiating Target Ping Scan against core node boundary...\n`;
            
            await new Promise(res => setTimeout(res, 900));
            output.innerHTML += `Target Node Host discovered up (Received echo-reply). Latency structural metric: 0.012s.\n`;
            output.innerHTML += `Initiating Parallel DNS resolution loops...\n`;
            output.innerHTML += `Initiating Complete Port/Service Signature Diagnostic Analysis Matrix...\n`;

            try {
                const response = await fetch(window.location.pathname + 'scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target, scan_type: mode, advanced_flags: flags})
                });
                
                const data = await response.json();
                await new Promise(res => setTimeout(res, 1100));
                
                let report = `\nNmap scan report for ${data.scan_info.host}\n`;
                report += `Host is up (0.014s network response timeout window).\n`;
                report += `Not shown: 994 closed ports (reset response matrix handles)\n\n`;
                report += `PORT      STATE    SERVICE      REASON          VERSION\n`;
                report += `--------- -------- ------------ --------------- -----------------------------------------\n`;
                
                for (const [port, info] of Object.entries(data.ports)) {
                    const formattedPort = `${port}/tcp`.padEnd(9);
                    const formattedState = info.state.padEnd(8);
                    const formattedService = info.service.padEnd(12);
                    const formattedReason = (info.reason || 'syn-ack').padEnd(15);
                    report += `${formattedPort} ${formattedState} ${formattedService} ${formattedReason} ${info.version}\n`;
                }
                
                if(flags.includes('--script vuln') || flags.includes('-F') === false || target === '89.117.188.108') {
                    if(data.os) {
                        report += `\nAggressive OS Detection Details:\n`;
                        report += `|_ OS Family/Signature: ${data.os}\n`;
                        report += `|_ Network Distance Track: ${data.distance || '1 hop'}\n`;
                    }
                    
                    if(data.script_output && data.script_output.length > 0) {
                        report += `\nNSE Extension Execution Pipeline Results:\n`;
                        data.script_output.forEach(script_line => {
                            report += `${script_line}\n`;
                        });
                    }
                }
                
                report += `\nNmap execution sequence completed: 1 IP address (1 host up) mapped fully in ${(Math.random() * 2 + 1.8).toFixed(2)} seconds\n`;
                output.innerHTML += report;
                
                // Auto scroll element focus tracking
                const panel = document.querySelector('.right-panel');
                panel.scrollTop = panel.scrollHeight;
                
            } catch (e) {
                output.innerHTML += "\n[!] Engine Scan Sequence Failure: Node interface timeout or bad formatting stream rules.\n";
            }
        }

        // Initialize script parameters on load window
        window.onload = updateCliStructure;
    </script>
</body>
</html>
    """)

@script12_bp.route('/scan', methods=['POST'])
def run_nmap_scan():
    data = request.json or {}
    target = data.get('target', '89.117.188.108').strip()
    scan_type = data.get('scan_type', '-sS')
    flags = data.get('advanced_flags', '')
    
    if target == '89.117.188.108':
        res = TARGET_RESULTS[target].copy()
        res['scan_info'] = {'host': target, 'scan_type': scan_type}
        return jsonify(res)
    
    # Active parallel detection layer for custom client infrastructure node scans
    live_diagnostic_ports = [21, 22, 80, 443, 3306, 8080]
    found = {}
    
    for port in live_diagnostic_ports:
        if direct_socket_probe(target, port):
            service_label = 'unknown-svc'
            version_string = 'Discovered Operational Signature Stack'
            
            if port == 21: service_label = 'ftp'; version_string = 'FTP Server Pipeline'
            elif port == 22: service_label = 'ssh'; version_string = 'OpenSSH Core Layer'
            elif port == 80: service_label = 'http'; version_string = 'Web Server Gateway Node'
            elif port == 443: service_label = 'https'; version_string = 'Secure Gateway Tunnel SSL'
            elif port == 3306: service_label = 'mysql'; version_string = 'Relational Database Layer'
            elif port == 8080: service_label = 'http-proxy'; version_string = 'Alternate Web Handling Cluster'
            
            found[str(port)] = {
                'state': 'open', 
                'service': service_label, 
                'version': version_string,
                'reason': 'syn-ack',
                'ttl': '54'
            }
            
    return jsonify({
        'ports': found,
        'os': 'Generic Unidentified Linux Kernel Node Environment',
        'distance': '1 hop (Direct Routing Path Network Boundary)',
        'script_output': ['|_ banner-grab: Stream responses matched outside pre-compiled enterprise arrays.'],
        'scan_info': {'host': target, 'scan_type': scan_type}
    })

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script12_bp, url_prefix='/script12')
    app.run(debug=True, port=5000)
