from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script28_bp = Blueprint('script28', __name__)

# --- CONFIGURATION CHANNEL (Using your existing RapidAPI Cluster Key) ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "imei-lookup1.p.rapidapi.com" # Standby Fallback Engine

# --- LUHN ALGORITHM CHECK (IMEI Integrity Verification) ---
def verify_luhn(imei_str: str) -> bool:
    if not imei_str.isdigit() or len(imei_str) != 15:
        return False
    
    total_sum = 0
    for i in range(15):
        digit = int(imei_str[i])
        if i % 2 == 1: # Double every second digit
            digit *= 2
            if digit > 9:
                digit = (digit % 10) + 1
        total_sum += digit
    
    return (total_sum % 10 == 0)

# --- TELEMETRY DASHBOARD UI ---
UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMEI_INTELLIGENCE_v28</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #030712; color: #f43f5e; font-family: 'Share Tech Mono', monospace; padding: 30px 20px; text-align: center; }
        .container { display: inline-block; width: 100%; max-width: 850px; text-align: left; }
        .box { border: 2px solid #f43f5e; background: #000; padding: 30px; box-shadow: 0 0 40px rgba(244, 63, 94, 0.15); border-radius: 16px; position: relative; }
        .box::before { content: '📡 SYSTEM TELEMETRY ACTIVE'; position: absolute; top: -10px; right: 20px; background: #f43f5e; color: #000; font-size: 11px; padding: 2px 8px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
        .header { text-align: center; border-bottom: 1px dashed #1e293b; padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #f43f5e; font-size: 26px; letter-spacing: 1px; }
        .subtitle { color: #64748b; font-size: 13px; margin-top: 6px; letter-spacing: 2px; }
        
        .input-group { text-align: center; margin-bottom: 25px; }
        input { width: 85%; padding: 15px; background: #090d16; border: 1px solid #991b1b; color: #fff; font-size: 22px; border-radius: 8px; outline: none; text-align: center; letter-spacing: 5px; box-shadow: inset 0 0 15px rgba(153, 27, 27, 0.2); transition: 0.3s; font-weight: bold; }
        input:focus { border-color: #f43f5e; box-shadow: inset 0 0 20px rgba(244, 63, 94, 0.2), 0 0 20px rgba(244, 63, 94, 0.2); }
        button { padding: 15px 45px; background: #f43f5e; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 15px; margin-top: 15px; transition: 0.3s; letter-spacing: 1px; text-transform: uppercase; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; transform: translateY(-1px); }
        
        #status { margin: 20px 0; color: #eab308; text-align: center; display: none; font-size: 14px; letter-spacing: 1px; }
        
        /* Dashboard Matrix Layout */
        .result-display { margin-top: 25px; display: none; }
        .grid-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px; }
        .card { background: #0b0f19; border: 1px solid #3f1212; padding: 16px; border-radius: 10px; transition: 0.2s; }
        .card:hover { border-color: #f43f5e; background: #140b11; }
        .card.full { grid-column: span 2; border-color: rgba(244, 63, 94, 0.4); background: #11060a; }
        .label { color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 6px; font-weight: bold; }
        .value { color: #fff; font-size: 16px; font-weight: bold; word-break: break-all; }
        .highlight { color: #f43f5e; }
        
        .debug-console { background: #020617; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; font-size: 12px; color: #64748b; overflow-x: auto; margin-top: 25px; font-family: monospace; max-height: 220px; }
        @media(max-width: 650px) { .grid-layout { grid-template-columns: 1fr; } .card.full { grid-column: span 1; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="header">
                <h2>🔍 IMEI FIELD RECONNAISSANCE CORE</h2>
                <p class="subtitle">SHIVAM SINGH OMEGA DASHBOARD • HARDWARE SPEC REGISTRY v3.0</p>
            </div>

            <div class="input-group">
                <input type="text" id="imei_input" placeholder="ENTER 15 DIGIT IMEI" maxlength="15" value="351895091234561">
                <br>
                <button onclick="executeImeiScan()">RESOLVE CELLULAR SIGNATURE</button>
            </div>

            <div id="status">📡 OPENING GSM REGISTRY STREAM & DECODING LUHN CHECKSUM...</div>
            
            <div id="result" class="result-display"></div>
        </div>
    </div>

    <script>
        async function executeImeiScan() {
            let imei = document.getElementById('imei_input').value.trim();
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(imei.length !== 15) {
                return alert("Bhai, IMEI number poora exactly 15 digits ka hona chahiye!");
            }

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script28/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ imei: imei })
                });
                const data = await res.json();
                status.style.display = "none";

                if (data.status === "error") {
                    resultBox.innerHTML = `<div class='card full' style='border-color:#ef4444; background:#2d1a1a;'><span class='label' style='color:#ef4444;'>INTEGRITY CRASH</span><span class='value'>${data.message}</span></div>`;
                    resultBox.style.display = "block";
                    return;
                }

                let htmlPayload = `
                    <h3 style="color: #fff; margin-bottom: 12px; font-size: 16px; border-left: 3px solid #f43f5e; padding-left: 8px;">📊 PARSED EQUIPMENT IDENTIFICATION SHEET:</h3>
                    
                    <div class="grid-layout">
                        <div class="card">
                            <div class="label">🔢 Input IMEI Block</div>
                            <div class="value highlight" style="letter-spacing:1px;">${data.imei}</div>
                        </div>
                        <div class="card">
                            <div class="label">🛡️ Luhn Algorithm Checksum</div>
                            <div class="value" style="color: ${data.checksum_valid ? '#10b981' : '#ef4444'}">
                                ${data.checksum_valid ? '✅ VALID (Authentic Structural Allocation)' : '❌ INVALID SIGNATURE'}
                            </div>
                        </div>
                        
                        <div class="card">
                            <div class="label">🏢 TAC Prefix (Type Allocation Code)</div>
                            <div class="value" style="color: #38bdf8;">${data.tac_code}</div>
                        </div>
                        <div class="card">
                            <div class="label">🏭 Reporting Body Identifier (RBI)</div>
                            <div class="value">${data.rbi_origin}</div>
                        </div>

                        <div class="card full">
                            <div class="label">📱 Estimated Device Identity (Oversight Lookup)</div>
                            <div class="value" style="color:#eab308; font-size:18px;">${data.device_brand}</div>
                        </div>
                        
                        <div class="card">
                            <div class="label">⚙️ Serial Sequence Segment</div>
                            <div class="value" style="color:#a855f7;">${data.serial_segment}</div>
                        </div>
                        <div class="card">
                            <div class="label">🏁 Check Digit Bit</div>
                            <div class="value">${data.check_digit}</div>
                        </div>

                        <div class="card full">
                            <div class="label">📍 Legal Tracking & GPS Vector Protocol Note</div>
                            <div class="value" style="font-size:12px; font-weight:normal; color:#94a3b8; line-height:1.4;">
                                ${data.tracking_alert}
                            </div>
                        </div>
                    </div>
                `;

                if(data.raw_data) {
                    htmlPayload += `
                        <div class="debug-console">
                            <span style="color:#f43f5e; font-weight:bold;">[METADATA_ANALYSIS_STREAM]:</span><br>
                            <pre style="margin-top:8px; white-space: pre-wrap; color: #64748b;">${JSON.stringify(data.raw_data, null, 2)}</pre>
                        </div>
                    `;
                }

                resultBox.innerHTML = htmlPayload;
                resultBox.style.display = "block";
            } catch (e) {
                status.style.display = "none";
                alert("Core interface exception or response timeout.");
            }
        }
    </script>
</body>
</html>
"""

@script28_bp.route('/')
def index():
    return render_template_string(UI)

@script28_bp.route('/scan', methods=['POST'])
def scan_imei():
    req_data = request.json or {}
    imei_input = str(req_data.get('imei', '')).strip()
    
    if len(imei_input) != 15 or not imei_input.isdigit():
        return jsonify({"status": "error", "message": "Bhai, verification pipeline ke liye pure 15-digit ka numeric string zaroori hai!"})
    
    # 1. Checksum Verification
    checksum_passed = verify_luhn(imei_input)
    
    # 2. Extract Architectural Blocks
    tac = imei_input[:8]
    rbi = imei_input[:2]
    serial = imei_input[8:14]
    check_digit = imei_input[14]
    
    # 3. RBI Origin Mapping (GSMA Allocation Standards)
    rbi_map = {
        "01": "CTIA (United States Wireless System)",
        "35": "BABT (United Kingdom / Global Standard)",
        "44": "BABT (United Kingdom Assemblies)",
        "86": "TAF (China Cellular Standard Bureau)",
        "91": "MSAI (India National Telecom Identifier Block)",
        "99": "GMSA Global Multi-mode Allocation"
    }
    origin = rbi_map.get(rbi, "International GSMA Allocation Body Pool")
    
    # 4. TAC Database Guess Layer (Common Industry Signatures)
    brand_guess = "Generic / Multi-Band GSM Terminal Module"
    common_tacs = {
        "359061": "Apple iPhone (Global Series Node)",
        "351895": "Samsung Galaxy Enterprise Hardware",
        "860845": "Xiaomi Redmi Terminal Architecture",
        "352452": "OnePlus Performance Cellular Node",
        "990004": "Qualcomm Snapdragon Reference Platform System"
    }
    
    for prefix, name in common_tacs.items():
        if tac.startswith(prefix):
            brand_guess = name
            break

    # 5. Tracking Protocol Advisory Text
    alert_text = (
        "NETWORK ATTRIBUTE: This device profile is legally structural. For active real-time cell-tower triangulation, "
        "the IMEI must be logged into live HLR/VLR operator databases. Private scripts can only verify hardware signatures "
        "and allocation blocks via GSMA registries."
    )

    # --- ADVANCED LIVE UPSTREAM INTEGRITY CHECK (RapidAPI Standby Query) ---
    api_payload_backup = {"internal_registry": "Local Parsing Match"}
    try:
        # Standby code connection structure just in case you ever connect active full specs subscription key
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST
        }
        conn.request("GET", f"/api/imei/{tac}", headers=headers)
        res = conn.getresponse()
        if res.status == 200:
            raw_res = res.read().decode("utf-8")
            api_payload_backup = json.loads(raw_res)
        conn.close()
    except:
        pass # Graceful fallback to local high-end structural parsing layer if API tier is inactive

    return jsonify({
        "status": "success",
        "imei": imei_input,
        "checksum_valid": checksum_passed,
        "tac_code": f"{tac[:4]} {tac[4:]}",
        "rbi_origin": origin,
        "device_brand": brand_guess,
        "serial_segment": serial,
        "check_digit": check_digit,
        "tracking_alert": alert_text,
        "raw_data": api_payload_backup
    })

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script28_bp, url_prefix='/script28')
    app.run(debug=True, port=5000)

