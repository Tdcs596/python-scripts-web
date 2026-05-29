from flask import Blueprint, render_template_string, request, jsonify
import socket
import time

script12_bp = Blueprint('script12', __name__)

# Training/Simulated environments endpoints mapping
TARGET_RESULTS = {
    '89.117.188.108': {
        'ports': {
            "21": {'state': 'open', 'service': 'ftp', 'version': 'vsftpd 3.0.3'},
            "22": {'state': 'open', 'service': 'ssh', 'version': 'OpenSSH 7.6p1 Ubuntu 4ubuntu0.3'},
            "80": {'state': 'open', 'service': 'http', 'version': 'Apache httpd 2.4.29 ((Ubuntu))'},
            "443": {'state': 'open', 'service': 'https', 'version': 'Apache httpd 2.4.29'},
            "3306": {'state': 'open', 'service': 'mysql', 'version': 'MySQL 5.7.33-0ubuntu0.18.04.1'},
            "8080": {'state': 'open', 'service': 'http-proxy', 'version': 'Apache Tomcat/9.0.24'}
        },
        'os': 'Linux 5.4 • Ubuntu 18.04 LTS (Aggressive OS guessing: 94% confidence)',
        'script_output': [
            '| ftp-anon: Anonymous FTP login allowed (FTP code 230)',
            '| mysql-info: Protocol: 10, Version: 5.7.33, Thread id: 412, Capabilities: 63487',
            '|_http-server-header: Apache/2.4.29 (Ubuntu)',
            '| vulners: \n|   cpe:/a:apache:tomcat:9.0.24:\n|     CVE-2019-0232\t10.0\thttps://vulners.com/cve/CVE-2019-0232'
        ]
    }
}

def socket_scan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
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
    <title>FORTIFIEDBYTES | Network Mapper Engine</title>
    <style>
        body { font-family: 'Consolas', 'Courier New', monospace; background: #030712; color: #38bdf8; margin: 0; padding: 20px; }
        .container { display: flex; height: 92vh; border: 1px solid #1e293b; background: #000; border-radius: 12px; overflow: hidden; box-shadow: 0 0 30px rgba(56,189,248,0.1); }
        .left-panel { width: 360px; padding: 25px; border-right: 1px solid #1e293b; background: #090d16; display: flex; flex-direction: column; justify-content: space-between; }
        .right-panel { flex: 1; padding: 25px; overflow-y: auto; background: #02040a; position: relative; }
        
        .panel-title { color: #fff; font-size: 16px; font-weight: bold; margin-bottom: 20px; letter-spacing: 1px; display: flex; align-items: center; gap: 8px; }
        .panel-title span { color: #f43f5e; }
        
        label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 1px; display: block; margin-top: 15px; margin-bottom: 5px; }
        input, select { width: 100%; padding: 12px; background: #030712; border: 1px solid #1e293b; color: #fff; font-family: inherit; border-radius: 6px; box-sizing: border-box; outline: none; }
        input:focus { border-color: #38bdf8; }
        
        .btn-group { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
        button { width: 100%; padding: 12px; font-weight: bold; background: #38bdf8; color: #000; border: none; font-family: inherit; cursor: pointer; border-radius: 6px; transition: 0.2s; text-transform: uppercase; letter-spacing: 1px; }
        button:hover { background: #fff; box-shadow: 0 0 15px rgba(255,255,255,0.2); }
        
        .btn-clear { background: transparent; border: 1px solid #f43f5e; color: #f43f5e; }
        .btn-clear:hover { background: #450a0a; color: #fff; }
        
        #output { white-space: pre-wrap; font-size: 13px; line-height: 1.6; color: #e2e8f0; }
        .brand-tag { font-size: 10px; color: #475569; text-align: center; letter-spacing: 2px; text-transform: uppercase; border-top: 1px dashed #1e293b; padding-top: 15px; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #02040a; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <div>
                <div class="panel-title">🛰️ FORTIFIEDBYTES <span>MAPPER</span></div>
                
                <label for="target_ip">Target Specification (IPv4 / Hostname)</label>
                <input type="text" id="target_ip" value="89.117.188.108" placeholder="e.g. 192.168.1.1">
                
                <label for="scan_mode">Scan Technique Profile</label>
                <select id="scan_mode">
                    <option value="syn">-sS (TCP SYN Stealth Scan)</option>
                    <option value="connect">-sT (TCP Connect Scan)</option>
                    <option value="version">-sV (Service Version Detection)</option>
                    <option value="os">-O (Enable OS Detection)</option>
                </select>
                
                <div class="btn-group">
                    <button onclick="triggerEngineScan()">⚡ Execute Command Scan</button>
                    <button onclick="clearDisplayTerminal()" class="btn-clear">🧹 Reset Console</button>
                </div>
            </div>
            
            <div class="brand-tag">FORTIFIEDBYTES PIPELINE SYSTEM</div>
        </div>
        
        <div class="right-panel">
            <div id="output">Fortifiedbytes network mapper sub-grid system operational.\nAwaiting target definition parameters...</div>
        </div>
    </div>

    <script>
        function clearDisplayTerminal() {
            document.getElementById('output').innerHTML = "Console buffer reset.\n";
        }

        async function triggerEngineScan() {
            const target = document.getElementById('target_ip').value.trim();
            const mode = document.getElementById('scan_mode').value;
            const output = document.getElementById('output');
            
            if(!target) {
                alert("Please define a target address node.");
                return;
            }

            // Real-time terminal output formatting simulation
            output.innerHTML += `\n\n# nmap -v -A -p- ${target}\n`;
            output.innerHTML += `Starting Nmap 7.94 ( https://nmap.org ) at ${new Date().toISOString().split('T')[0]} ${new Date().toLocaleTimeString()}\n`;
            output.innerHTML += `NSE: Loaded 156 scripts for scanning.\n`;
            output.innerHTML += `Initiating ARP Ping Scan at ${new Date().toLocaleTimeString()}\n`;
            output.innerHTML += `Scanning ${target} [1 port]\n`;
            
            // Artificial delay implementation to replicate real routing stream checkouts
            await new Promise(resolve => setTimeout(resolve, 1200));
            
            output.innerHTML += `Completed ARP Ping Scan at ${new Date().toLocaleTimeString()}, 1 hosts up\n`;
            output.innerHTML += `Initiating Parallel DNS resolution of 1 IP address.\n`;
            output.innerHTML += `Initiating Connect Scan against network grid...\n`;

            try {
                const response = await fetch(window.location.pathname + 'scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target, scan_type: mode})
                });
                
                const data = await response.json();
                await new Promise(resolve => setTimeout(resolve, 800));
                
                let res = `\nNmap scan report for ${data.scan_info.host}\n`;
                res += `Host is up (0.012s latency).\n\n`;
                res += `PORT      STATE    SERVICE      VERSION\n`;
                res += `--------- -------- ------------ -----------------------------------------\n`;
                
                for (const [port, info] of Object.entries(data.ports)) {
                    const formattedPort = `${port}/tcp`.padEnd(9);
                    const formattedState = info.state.padEnd(8);
                    const formattedService = info.service.padEnd(12);
                    res += `${formattedPort} ${formattedState} ${formattedService} ${info.version}\n`;
                }
                
                if(mode === 'os' || mode === 'version' || target === '89.117.188.108') {
                    if(data.os) {
                        res += `\nDevice type: general purpose\n`;
                        res += `Running: ${data.os}\n`;
                    }
                }

                if((mode === 'version' || mode === 'syn') && data.script_output && data.script_output.length > 0) {
                    res += `\nHost script results:\n`;
                    data.script_output.forEach(script => {
                        res += `${script}\n`;
                    });
                }
                
                res += `\nNmap done: 1 IP address (1 host up) scanned in ${(Math.random() * 3 + 2).toFixed(2)} seconds\n`;
                output.innerHTML += res;
                
                const panel = document.querySelector('.right-panel');
                panel.scrollTop = panel.scrollHeight;
                
            } catch (e) {
                output.innerHTML += "\n[!] Engine Stream Fault: Pipeline connection refused or target network out of boundaries.\n";
            }
        }
    </script>
</body>
</html>
    """)

@script12_bp.route('/scan', methods=['POST'])
def run_nmap_scan():
    data = request.json or {}
    target = data.get('target', '89.117.188.108').strip()
    scan_type = data.get('scan_type', 'syn')
    
    if target == '89.117.188.108':
        res = TARGET_RESULTS[target].copy()
        res['scan_info'] = {'host': target, 'scan_type': scan_type}
        return jsonify(res)
    
    # Simple real network diagnostics check over specific public routing boundaries
    standard_ports = [21, 22, 80, 443, 3306, 8080]
    found = {}
    for p in standard_ports:
        if socket_scan(target, p):
            service_lbl = 'unknown'
            if p == 80: service_lbl = 'http'
            elif p == 443: service_lbl = 'https'
            elif p == 22: service_lbl = 'ssh'
            found[str(p)] = {'state': 'open', 'service': service_lbl, 'version': 'Production Stack Detection'}
            
    return jsonify({
        'ports': found,
        'os': 'Generic Linux Kernel Infrastructure Stack',
        'script_output': ['|_ network-range-check: Node confirmed outside standard dashboard loop'],
        'scan_info': {'host': target, 'scan_type': scan_type}
    })

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script12_bp, url_prefix='/script12')
    app.run(debug=True, port=5000)
