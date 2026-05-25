from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script26_bp = Blueprint('script26', __name__)

# --- CONFIGURATION CHANNEL ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "mac-address-lookup3.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>MAC_DEEP_INTELLIGENCE_v26</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #05070c; color: #00ffcc; font-family: 'Share Tech Mono', monospace; padding: 30px 20px; text-align: center; }
        .box { border: 2px solid #00ffcc; background: #000; padding: 30px; box-shadow: 0 0 35px #00ffcc22; display: inline-block; width: 95%; max-width: 750px; border-radius: 16px; text-align: left; position: relative; overflow: hidden; }
        .box::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #00ffcc, #0055ff); }
        .header { text-align: center; border-bottom: 1px solid #113333; padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #00ffcc; font-size: 26px; letter-spacing: 1px; }
        .subtitle { color: #557099; font-size: 13px; margin-top: 6px; letter-spacing: 2px; }
        .input-group { text-align: center; margin-bottom: 25px; }
        input { width: 85%; padding: 14px; background: #0a0f1d; border: 1px solid #0055ff; color: #fff; font-size: 18px; border-radius: 8px; outline: none; text-align: center; letter-spacing: 3px; box-shadow: inset 0 0 10px #0055ff11; transition: 0.3s; }
        input:focus { border-color: #00ffcc; box-shadow: inset 0 0 15px #00ffcc22, 0 0 15px #00ffcc22; }
        button { padding: 14px 40px; background: #00ffcc; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 15px; margin-top: 15px; transition: 0.3s; letter-spacing: 1px; }
        button:hover { background: #fff; box-shadow: 0 0 20px #fff; transform: translateY(-1px); }
        #status { margin: 20px 0; color: #ffeb3b; text-align: center; display: none; font-size: 14px; animation: blink 1.5s infinite; }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        
        /* Advanced Info UI Matrix */
        .result-display { margin-top: 25px; display: none; }
        .grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .card { background: #09111c; border: 1px solid #112a47; padding: 15px; border-radius: 8px; }
        .card.full { grid-column: span 2; border-color: #00ffcc44; background: #041619; }
        .label { color: #557099; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
        .value { color: #fff; font-size: 15px; font-weight: bold; }
        .highlight { color: #00ffcc; }
        .debug-console { background: #05070a; border: 1px solid #222; padding: 15px; border-radius: 8px; font-size: 12px; color: #888; overflow-x: auto; margin-top: 20px; font-family: monospace; }
        
        @media(max-width: 600px) { .grid-layout { grid-template-columns: 1fr; } .card.full { grid-column: span 1; } }
    </style>
</head>
<body>
    <div class="box">
        <div class="header">
            <h2>🔍 MAC LAYER DEEP INTELLIGENCE NODE</h2>
            <p class="subtitle">SHIVAM SINGH OMEGA DASHBOARD • METRIC TELEMETRY v2.0</p>
        </div>

        <div class="input-group">
            <input type="text" id="mac_input" placeholder="00:23:AB:00:00:00" value="0023AB000000">
            <br>
            <button onclick="lookupMacAddress()">EXTRACT LAYER-2 METRICS</button>
        </div>

        <div id="status">📡 INTERROGATING GLOBAL REGISTRIES & PARSING HEX STREAM...</div>
        
        <div id="result" class="result-display"></div>
    </div>

    <script>
        async function lookupMacAddress() {
            let mac = document.getElementById('mac_input').value.trim();
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!mac) return alert("Bhai, MAC Address bina execution workflow kaise test karein!");

            // Alphanumeric format cleanup stripping spaces or separators
            let cleanMac = mac.replace(/[:\\s-]/g, '');

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script26/lookup', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mac_address: cleanMac })
                });
                const data = await res.json();
                status.style.display = "none";

                if (data.status === "error") {
                    resultBox.innerHTML = "<div class='card full' style='border-color:red;'><span class='label' style='color:red;'>EXECUTION ERROR</span><span class='value'>" + data.message + "</span></div>";
                    resultBox.style.display = "block";
                    return;
                }

                // Building the Premium Information Dashboard Blocks
                let htmlPayload = `
                    <h3 style="color: #fff; margin-bottom: 10px; font-size: 16px;">📊 RECONNAISSANCE ANALYSIS PACKET:</h3>
                    <div class="grid-layout">
                        <div class="card full">
                            <div class="label">🏢 Primary Hardware Vendor / Manufacturer</div>
                            <div class="value" style="font-size: 18px; color: #00ffcc;">${data.resolved_vendor}</div>
                        </div>
                        <div class="card">
                            <div class="label">📡 OUI Registry Prefix</div>
                            <div class="value highlight">${data.oui_prefix}</div>
                        </div>
                        <div class="card">
                            <div class="label">🎛️ Transmission Mode</div>
                            <div class="value" style="color: ${data.transmission_type.includes('Unicast') ? '#00ffcc' : '#ffeb3b'}">${data.transmission_type}</div>
                        </div>
                        <div class="card">
                            <div class="label">🌐 Assignment Administration</div>
                            <div class="value">${data.administration_type}</div>
                        </div>
                        <div class="card">
                            <div class="label">🤖 Infrastructure Guess</div>
                            <div class="value" style="color:#60a5fa;">${data.infrastructure_type}</div>
                        </div>
                        <div class="card full">
                            <div class="label">📍 Corporate Registry Address</div>
                            <div class="value" style="font-size:13px; font-weight:normal; color:#cbd5e1;">${data.vendor_address}</div>
                        </div>
                    </div>
                `;

                // Attaching the full structural data stream backup logs for diagnostics view
                if(data.raw_payload) {
                    htmlPayload += `
                        <div class="debug-console">
                            <span style="color:#00ffcc; font-weight:bold;">[DEBUG_CONSOLE_LOGS]:</span><br>
                            <pre style="margin-top:5px; white-space: pre-wrap;">${JSON.stringify(data.raw_payload, null, 2)}</pre>
                        </div>
                    `;
                }

                resultBox.innerHTML = htmlPayload;
                resultBox.style.display = "block";
            } catch (e) {
                status.style.display = "none";
                alert("Internal backend routing error or exception timeout.");
            }
        }
    </script>
</body>
</html>
"""

@script26_bp.route('/')
def index():
    return render_template_string(UI)

@script26_bp.route('/lookup', methods=['POST'])
def lookup_mac():
    req_data = request.json or {}
    mac_address = str(req_data.get('mac_address', '')).strip().upper()
    
    if len(mac_address) < 6:
        return jsonify({"status": "error", "message": "Bhai, kam se kam shuruati 6 hex characters (OUI) toh enter karo!"})
        
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        query_path = f"/{mac_address}"
        
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }
        
        conn.request("GET", query_path, headers=headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        conn.close()

        if res.status != 200:
            return jsonify({"status": "error", "message": f"RapidAPI Gateway Server Error (Status: {res.status})"})
            
        try:
            parsed_json = json.loads(raw_data)
        except json.JSONDecodeError:
            parsed_json = {}

        # --- CRITICAL BUG FIX LAYER (Shivam Spec) ---
        # Agar API direct elements list array bhejti hai, toh pehle list validation wrap verify karke index 0 select karenge
        if isinstance(parsed_json, list):
            if len(parsed_json) > 0:
                raw_payload_for_debug = {"api_array_response": parsed_json}
                parsed_json = parsed_json[0]
            else:
                parsed_json = {}
        else:
            raw_payload_for_debug = parsed_json

        # --- ADVANCED DATAFRAME EXTRACTOR ---
        vendor = parsed_json.get("companyName") or parsed_json.get("company") or parsed_json.get("vendor")
        if not vendor and parsed_json == {}:
            vendor = "Unknown Manufacturer (Not listed in IEEE Global Registry)"
        elif not vendor:
            vendor = "Generic Assembly / Private Node"

        address = parsed_json.get("companyAddress") or parsed_json.get("address") or "Not registered in local block database schema."
        prefix = parsed_json.get("macPrefix") or parsed_json.get("oui") or mac_address[:6]

        # --- HIGH-LEVEL BITWISE TELEMETRY ENCODING ---
        # Pehle byte (First 2 hex characters) ko process karke standard flags compute karte hain
        try:
            first_byte_hex = mac_address[:2]
            first_byte_int = int(first_byte_hex, 16)
            
            # Checking Least Significant Bit (Bit 0): 0 = Unicast, 1 = Multicast
            transmission = "Unicast (Single Device / Dedicated Stream)" if not (first_byte_int & 1) else "Multicast (Group Network/Broadcast Frame)"
            
            # Checking Universal vs Local Bit (Bit 1): 0 = Global (IEEE Hardcoded), 1 = Local (Randomized/Spoofed)
            administration = "Globally Unique (Factory Burned-In Address)" if not (first_byte_int & 2) else "Locally Administered (Software Spoofed / Random Private MAC)"
        except:
            transmission = "Standard Ethernet Transmission Node"
            administration = "Unspecified Protocol Architecture"

        # --- ENVIRONMENT & VIRTUAL SANDBOX FINGERPRINTING ---
        infra_guess = "Physical Hardware Node (Endpoint Terminal/Mobile/Router Interface)"
        virtual_prefixes = {
            "005056": "VMware ESXi Server Node",
            "000C29": "VMware Workstation System Instance",
            "080027": "Oracle VirtualBox Sandbox Machine",
            "00155D": "Microsoft Hyper-V Engine Cluster",
            "0242AC": "Docker Daemon Container Containerized Overlay Bridge",
            "525400": "KVM / QEMU Emulator Kernel Interface"
        }
        
        for virt_pfx, name in virtual_prefixes.items():
            if mac_address.startswith(virt_pfx):
                infra_guess = name
                break

        # Response payload assembly pipeline
        return jsonify({
            "status": "success",
            "resolved_vendor": vendor,
            "oui_prefix": prefix,
            "transmission_type": transmission,
            "administration_type": administration,
            "infrastructure_type": infra_guess,
            "vendor_address": address,
            "raw_payload": raw_payload_for_debug
        })
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

