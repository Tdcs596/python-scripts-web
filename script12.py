import nmap
from flask import Blueprint, request, jsonify, render_template_string

script12_bp = Blueprint("script12", __name__)

# --- UI DESIGN ---
NMAP_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA NMAP SCANNER</title>
    <style>
        body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 30px; }
        .scanner-box { border: 2px solid #00ff41; padding: 20px; background: #000; box-shadow: 0 0 15px #00ff4133; max-width: 800px; margin: auto; }
        input, select { background: #111; border: 1px solid #00ff41; color: #fff; padding: 10px; margin: 10px 0; width: 90%; }
        button { background: #00ff41; color: #000; border: none; padding: 15px; width: 93%; font-weight: bold; cursor: pointer; text-transform: uppercase; }
        #results { margin-top: 20px; background: #050505; padding: 15px; border: 1px solid #333; height: 400px; overflow-y: auto; font-size: 13px; color: #00ff41; white-space: pre-wrap; }
        .loading { animation: blink 1s infinite; color: #ff3333; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <div class="scanner-box">
        <h2>[ ADVANCED NETWORK SCANNER ]</h2>
        <p style="color: #888;">Target: IP, Hostname, or Subnet (e.g., 192.168.1.1)</p>
        
        <input type="text" id="target" placeholder="Enter Target IP">
        
        <select id="scan_type">
            <option value="-F">Quick Scan (Fast)</option>
            <option value="-sS -sV">Service & Version Detection</option>
            <option value="-O">OS Fingerprinting</option>
            <option value="-A">Aggressive Scan (Everything)</option>
            <option value="-p 1-65535">Full Port Scan</option>
        </select>
        
        <button onclick="runScan()" id="scanBtn">Execute Scan</button>
        
        <div id="results">System Ready for Reconnaissance...</div>
    </div>

    <script>
        async function runScan() {
            const target = document.getElementById('target').value;
            const args = document.getElementById('scan_type').value;
            const resBox = document.getElementById('results');
            const btn = document.getElementById('scanBtn');

            if(!target) return alert("Target toh daal bhai!");

            btn.disabled = true;
            resBox.innerHTML = "<span class='loading'>[!] SCANNING IN PROGRESS... PLEASE WAIT...</span>";

            try {
                const response = await fetch(window.location.pathname + "scan", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ target: target, arguments: args })
                });
                const data = await response.json();
                
                if(data.error) {
                    resBox.innerText = "ERROR: " + data.error;
                } else {
                    resBox.innerText = data.raw_results;
                }
            } catch (err) {
                resBox.innerText = "Connection Failed. Ensure Nmap is installed on server.";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@script12_bp.route("/")
def index():
    return render_template_string(NMAP_UI)

@script12_bp.route("/scan", methods=["POST"])
def perform_scan():
    data = request.json
    target = data.get('target')
    scan_args = data.get('arguments')

    nm = nmap.PortScanner()
    
    try:
        # Nmap Execute ho raha hai
        nm.scan(hosts=target, arguments=scan_args)
        
        # Result ko readable format mein convert karna
        scan_output = ""
        for host in nm.all_hosts():
            scan_output += f"Host : {host} ({nm[host].hostname()})\n"
            scan_output += f"State : {nm[host].state()}\n"
            
            for proto in nm[host].all_protocols():
                scan_output += f"----------\nProtocol : {proto}\n"
                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    port_data = nm[host][proto][port]
                    scan_output += f"Port : {port}\tState : {port_data['state']}\tService : {port_data['name']}\tVersion : {port_data['version']}\n"
        
        if not scan_output:
            scan_output = "Scan complete. No open ports or hosts found."
            
        return jsonify({"raw_results": scan_output})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
