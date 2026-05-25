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
    <title>ULTIMATE_MAC_CORE_v26</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #030712; color: #38bdf8; font-family: 'Share Tech Mono', monospace; padding: 30px 20px; text-align: center; }
        .container { display: inline-block; width: 100%; max-width: 850px; text-align: left; }
        .box { border: 2px solid #38bdf8; background: #000; padding: 30px; box-shadow: 0 0 40px rgba(56, 189, 248, 0.15); border-radius: 16px; position: relative; }
        .box::before { content: '⚡ OMEGA PROTOCOL ACTIVE'; position: absolute; top: -10px; right: 20px; background: #38bdf8; color: #000; font-size: 11px; padding: 2px 8px; font-weight: bold; border-radius: 4px; }
        .header { text-align: center; border-bottom: 1px dashed #1e293b; padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #38bdf8; font-size: 28px; letter-spacing: 1px; }
        .subtitle { color: #64748b; font-size: 13px; margin-top: 6px; letter-spacing: 2px; }
        .input-group { text-align: center; margin-bottom: 25px; }
        input { width: 85%; padding: 15px; background: #090d16; border: 1px solid #1e40af; color: #fff; font-size: 20px; border-radius: 8px; outline: none; text-align: center; letter-spacing: 4px; box-shadow: inset 0 0 15px rgba(30, 64, 175, 0.2); transition: 0.3s; font-weight: bold; }
        input:focus { border-color: #38bdf8; box-shadow: inset 0 0 20px rgba(56, 189, 248, 0.2), 0 0 20px rgba(56, 189, 248, 0.2); }
        button { padding: 15px 45px; background: #38bdf8; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 15px; margin-top: 15px; transition: 0.3s; letter-spacing: 1px; text-transform: uppercase; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; transform: translateY(-1px); }
        #status { margin: 20px 0; color: #eab308; text-align: center; display: none; font-size: 14px; letter-spacing: 1px; }
        
        /* Advanced Telemetry Layout */
        .result-display { margin-top: 25px; display: none; }
        .grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .card { background: #0b1329; border: 1px solid #1e3a8a; padding: 16px; border-radius: 10px; transition: 0.2s; }
        .card:hover { border-color: #38bdf8; background: #0f1c3f; }
        .card.full { grid-column: span 2; border-color: rgba(56, 189, 248, 0.4); background: #051625; }
        .label { color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; font-weight: bold; }
        .value { color: #fff; font-size: 16px; font-weight: bold; word-break: break-all; }
        .highlight { color: #38bdf8; }
        
        /* Binary Block Array UI */
        .binary-container { display: flex; gap: 6px; justify-content: space-between; margin-top: 10px; flex-wrap: wrap; }
        .binary-block { background: #1e293b; padding: 8px; border-radius: 6px; text-align: center; flex: 1; min-width: 90px; border: 1px solid #334155; }
        .binary-block .byte-title { font-size: 10px; color: #94a3b8; display: block; margin-bottom: 4px; }
        .binary-block .byte-hex { font-size: 14px; color: #38bdf8; font-weight: bold; }
        .binary-block .byte-bin { font-size: 11px; color: #10b981; font-family: monospace; }

        .debug-console { background: #020617; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; font-size: 12px; color: #64748b; overflow-x: auto; margin-top: 25px; font-family: monospace; max-height: 250px; }
        @media(max-width: 650px) { .grid-layout { grid-template-columns: 1fr; } .card.full { grid-column: span 1; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="header">
                <h2>🧬 HARDWARE LAYER CORE INTELLIGENCE</h2>
                <p class="subtitle">SHIVAM SINGH OMEGA DASHBOARD • A TO Z DEEP PACKET MATRIX v3.0</p>
            </div>

            <div class="input-group">
                <input type="text" id="mac_input" placeholder="00:1A:2B:3C:4D:5E" value="001A2B3C4D5E">
                <br>
                <button onclick="lookupMacAddress()">EXECUTE FULL FIELD RECON</button>
            </div>

            <div id="status">📡 OPENING RAW SOCKET CONSOLE & COMPUTING HEX STREAM ANALYSIS...</div>
            
            <div id="result" class="result-display"></div>
        </div>
    </div>

    <script>
        async function lookupMacAddress() {
            let mac = document.getElementById('mac_input').value.trim();
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!mac) return alert("Bhai, bina MAC data ke analysis flow load nahi hoga!");

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
                    resultBox.innerHTML = "<div class='card full' style='border-color:#ef4444; background:#2d1a1a;'><span class='label' style='color:#ef4444;'>CRITICAL PIPELINE ERROR</span><span class='value'>" + data.message + "</span></div>";
                    resultBox.style.display = "block";
                    return;
                }

                // Generates the Live Binary Array blocks HTML safely
                let binaryBlocksHtml = '';
                data.binary_map.forEach(block => {
                    binaryBlocksHtml += `
                        <div class="binary-block">
                            <span class="byte-title">${block.segment}</span>
                            <span class="byte-hex">${block.hex}</span>
                            <span class="byte-bin">${block.bin}</span>
                        </div>
                    `;
                });

                let htmlPayload = `
                    <h3 style="color: #fff; margin-bottom: 12px; font-size: 16px; border-left: 3px solid #38bdf8; padding-left: 8px;">📊 COMPLETE RESOLVED HARDWARE SCHEMATICS:</h3>
                    
                    <div class="grid-layout">
                        <div class="card full">
                            <div class="label">🏢 Confirmed Hardware Manufacturer</div>
                            <div class="value" style="font-size: 19px; color: #38bdf8;">${data.resolved_vendor}</div>
                        </div>
                        
                        <div class="card">
                            <div class="label">📡 Factory OUI Block Prefix</div>
                            <div class="value highlight">${data.oui_prefix}</div>
                        </div>
                        
                        <div class="card">
                            <div class="label">🆔 NIC Serial ID (Device Identifier)</div>
                            <div class="value" style="color: #a855f7;">${data.nic_serial}</div>
                        </div>

                        <div class="card">
                            <div class="label">🎛️ Frame Transmission Protocol</div>
                            <div class="value" style="color: ${data.transmission_type.includes('Unicast') ? '#10b981' : '#f59e0b'}">${data.transmission_type}</div>
                        </div>
                        
                        <div class="card">
                            <div class="label">🌐 Assignment Authority Scope</div>
                            <div class="value">${data.administration_type}</div>
                        </div>
                        
                        <div class="card full">
                            <div class="label">🤖 Architectural Deployment Guess</div>
                            <div class="value" style="color:#60a5fa;">${data.infrastructure_type}</div>
                        </div>

                        <div class="card full">
                            <div class="label">🔢 48-Bit Binary Streams Representation (Hex to Binary)</div>
                            <div class="binary-container">
                                ${binaryBlocksHtml}
                            </div>
                        </div>
                        
                        <div class="card full">
                            <div class="label">📍 Corporate Registration / HQ Base Address</div>
                            <div class="value" style="font-size:13px; font-weight:normal; color:#94a3b8;">${data.vendor_address}</div>
                        </div>
                    </div>
                `;

                if(data.raw_payload) {
                    htmlPayload += `
                        <div class="debug-console">
                            <span style="color:#38bdf8; font-weight:bold;">[RAW_UPSTREAM_DATAFRAME]:</span><br>
                            <pre style="margin-top:8px; white-space: pre-wrap; color: #64748b;">${JSON.stringify(data.raw_payload, null, 2)}</pre>
                        </div>
                    `;
                }

                resultBox.innerHTML = htmlPayload;
                resultBox.style.display = "block";
            } catch (e) {
                status.style.display = "none";
                alert("Interface endpoint timeout exception.");
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
    
    # Standard MAC verification length validation
    if len(mac_address) != 12:
        return jsonify({"status": "error", "message": f"Bhai, MAC Address exactly 12 Hex chars ka hona chahiye (Aapka: {len(mac_address)} chars). Format check karo!"})
        
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
            return jsonify({"status": "error", "message": f"RapidAPI Gateway Error (HTTP Status Code: {res.status})"})
            
        try:
            parsed_json = json.loads(raw_data)
        except json.JSONDecodeError:
            parsed_json = {}

        # Array vs Dictionary protection proxy layer
        if isinstance(parsed_json, list):
            if len(parsed_json) > 0:
                raw_payload_for_debug = {"upstream_array": parsed_json}
                parsed_json = parsed_json[0]
            else:
                parsed_json = {}
        else:
            raw_payload_for_debug = parsed_json

        # --- A TO Z ADVANCED ANALYTICS INTERPRETATION ---
        
        # 1. Vendor mapping extraction
        vendor = parsed_json.get("companyName") or parsed_json.get("company") or parsed_json.get("vendor")
        if not vendor and parsed_json == {}:
            vendor = "Unknown Manufacturer (Not present inside IEEE active tables)"
        elif not vendor:
            vendor = "Custom Modular Hardware Assembly / Private Entity"

        address = parsed_json.get("companyAddress") or parsed_json.get("address") or "No corporate identity registered for this block assignment."
        
        # 2. Advanced Split: OUI vs NIC Breakdown
        oui_prefix = f"{mac_address[0:2]}:{mac_address[2:4]}:{mac_address[4:6]}"
        nic_serial = f"{mac_address[6:8]}:{mac_address[8:10]}:{mac_address[10:12]}"

        # 3. Complete Hex to Binary Decoding Array Construction
        binary_map_list = []
        labels = ["Byte 1 (OUI)", "Byte 2 (OUI)", "Byte 3 (OUI)", "Byte 4 (NIC)", "Byte 5 (NIC)", "Byte 6 (NIC)"]
        
        for i in range(6):
            hex_pair = mac_address[i*2 : (i*2)+2]
            try:
                # Format integer to 8-bit padded binary stream representation
                bin_string = bin(int(hex_pair, 16))[2:].zfill(8)
            except:
                bin_string = "00000000"
            binary_map_list.append({
                "segment": labels[i],
                "hex": hex_pair,
                "bin": bin_string
            })

        # 4. Bitwise Level-2 Telemetry Flags Check
        try:
            first_byte_hex = mac_address[:2]
            first_byte_int = int(first_byte_hex, 16)
            
            # Bit 0 validation: Unicast vs Multicast frame indicator
            transmission = "Unicast (Point-to-Point Node Stream / Individual Dedicated Link)" if not (first_byte_int & 1) else "Multicast (Group Channel Transmission / Network Broadcast Frame)"
            
            # Bit 1 validation: Global Unique vs Software Randomized spoof flag
            administration = "Globally Unique Burned-In Identifier (IEEE Standard Hardcoded)" if not (first_byte_int & 2) else "Locally Administered Virtual Node (Software Random Private MAC / Spoofed Profile)"
        except:
            transmission = "Standard LAN Frame"
            administration = "Generic Field Assignment Parameter"

        # 5. Virtualized Hypervisor Sandbox Profiling Enriched Map
        infra_guess = "Physical Hardware Network Endpoint Device (Laptop, Smartphone, Router Interface)"
        virtual_prefixes = {
            "005056": "VMware ESXi Cloud Virtual Machine Host Node",
            "000C29": "VMware Workstation Guest OS Environment",
            "080027": "Oracle VirtualBox Sandbox Machine Target",
            "00155D": "Microsoft Hyper-V Enterprise Cluster Core",
            "0242AC": "Docker Daemon Internal Container Virtual Network Bridge",
            "525400": "KVM / QEMU Emulator Kernel Sandbox Virtual Core"
        }
        
        # Searching structural prefixes mapping logic
        matched_prefix = mac_address[:6]
        if matched_prefix in virtual_prefixes:
            infra_guess = virtual_prefixes[matched_prefix]

        # Returns the final highly advanced compiled dictionary object package
        return jsonify({
            "status": "success",
            "resolved_vendor": vendor,
            "oui_prefix": oui_prefix,
            "nic_serial": nic_serial,
            "transmission_type": transmission,
            "administration_type": administration,
            "infrastructure_type": infra_guess,
            "vendor_address": address,
            "binary_map": binary_map_list,
            "raw_payload": raw_payload_for_debug
        })
            
    except Exception as pipeline_exception:
        return jsonify({"status": "error", "message": str(pipeline_exception)})

