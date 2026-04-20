import time
import re
import requests
from flask import Blueprint, request, jsonify, render_template_string

# Create the blueprint
script16_bp = Blueprint("script16", __name__)

# --- THE "VEHICLE GHOST" UI ---
VEHICLE_GHOST_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>INDIAN VEHICLE GHOST SCANNER</title>
    <style>
        body { 
            background: #0a0f14; 
            color: #00ff88; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0;
        }
        
        .scanner-box {
            background: #111820;
            border: 2px solid #00ff88;
            padding: 40px;
            width: 500px;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.15);
            border-radius: 8px;
        }

        h2 { 
            color: #fff; 
            text-align: center; 
            margin-bottom: 30px; 
            text-transform: uppercase; 
            letter-spacing: 2px;
            border-bottom: 1px solid #333;
            padding-bottom: 15px;
        }

        .input-group { position: relative; margin-bottom: 25px; }
        
        input { 
            width: 100%; 
            background: #05080a; 
            border: 1px solid #00ff88; 
            color: #fff; 
            padding: 15px; 
            font-size: 20px; 
            text-align: center; 
            letter-spacing: 3px;
            font-weight: bold;
            outline: none;
        }
        
        input:focus { box-shadow: 0 0 15px rgba(0, 255, 136, 0.4); }

        button { 
            width: 100%; 
            background: #00ff88; 
            color: #000; 
            border: none; 
            padding: 15px; 
            font-weight: bold; 
            cursor: pointer; 
            text-transform: uppercase; 
            font-size: 16px;
            transition: 0.3s;
        }
        
        button:hover { background: #fff; box-shadow: 0 0 20px #00ff88; }

        /* RESULTS CARD */
        #result-card {
            display: none;
            margin-top: 30px;
            border: 1px dashed #444;
            padding: 20px;
            background: #05080a;
        }

        .data-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            border-bottom: 1px solid #222;
            padding-bottom: 5px;
        }

        .label { color: #888; font-size: 14px; }
        .value { color: #00ff88; font-weight: bold; font-family: monospace; font-size: 16px; text-align: right; }
        .value.error { color: #ff3333; }
        
        .loading {
            text-align: center;
            margin-top: 20px;
            display: none;
            color: #00ff88;
            font-size: 14px;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.5; }
            50% { opacity: 1; }
            100% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="scanner-box">
        <h2>🚗 VEHICLE GHOST SCANNER</h2>
        
        <div class="input-group">
            <input type="text" id="vehicleNum" placeholder="ENTER NUMBER (e.g., MH02AB1234)" value="">
        </div>
        
        <button onclick="scanVehicle()" id="btn">SCAN DATABASE</button>

        <div class="loading" id="loading">
            [CONNECTING TO PARIVAHAN API...]<br>
            DECRYPTING OWNER DETAILS...
        </div>

        <div id="result-card">
            <div class="data-row"><span class="label">VEHICLE NO:</span> <span class="value" id="v-no"></span></div>
            <div class="data-row"><span class="label">OWNER NAME:</span> <span class="value" id="v-owner"></span></div>
            <div class="data-row"><span class="label">MOBILE NO:</span> <span class="value" id="v-mobile"></span></div>
            <div class="data-row"><span class="label">ADDRESS:</span> <span class="value" id="v-addr"></span></div>
            <div class="data-row"><span class="label">FUEL TYPE:</span> <span class="value" id="v-fuel"></span></div>
            <div class="data-row"><span class="label">CLASS:</span> <span class="value" id="v-class"></span></div>
            <div class="data-row"><span class="label">INSURANCE:</span> <span class="value" id="v-ins"></span></div>
        </div>
    </div>

    <script>
        async function scanVehicle() {
            const num = document.getElementById('vehicleNum').value.trim().toUpperCase();
            const btn = document.getElementById('btn');
            const loading = document.getElementById('loading');
            const resultCard = document.getElementById('result-card');
            
            if (num.length < 5) { alert("Enter a valid vehicle number!"); return; }

            // Reset UI
            btn.disabled = true;
            btn.innerText = "SCANNING...";
            resultCard.style.display = 'none';
            loading.style.display = 'block';

            try {
                const response = await fetch(window.location.pathname + "/ghost", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ vehicle: num })
                });

                const data = await response.json();

                if (data.status === "success") {
                    // Populate Data
                    document.getElementById('v-no').innerText = data.vehicle_no;
                    document.getElementById('v-owner').innerText = data.owner_name || "N/A";
                    document.getElementById('v-mobile').innerText = data.mobile || "N/A";
                    document.getElementById('v-addr').innerText = data.address || "N/A";
                    document.getElementById('v-fuel').innerText = data.fuel_type || "N/A";
                    document.getElementById('v-class').innerText = data.vehicle_class || "N/A";
                    document.getElementById('v-ins').innerText = data.insurance || "N/A";

                    // Show Result
                    resultCard.style.display = 'block';
                    
                    // Close after 15 seconds
                    setTimeout(() => { window.close(); }, 15000);

                } else {
                    loading.innerText = "⚠️ ERROR: " + data.message;
                    setTimeout(() => { 
                        btn.disabled = false; 
                        btn.innerText = "SCAN DATABASE";
                    }, 2000);
                }

            } catch (err) {
                loading.innerText = "🔴 CONNECTION LOST TO API";
                btn.disabled = false;
                btn.innerText = "SCAN DATABASE";
            }
        }
    </script>
</body>
</html>
"""

@script16_bp.route("/")
def index():
    return render_template_string(VEHICLE_GHOST_UI)

@script16_bp.route("/ghost", methods=["POST"])
def handle_ghost():
    data = request.get_json()
    raw_vehicle = data['vehicle']
    
    # Clean the number (remove spaces, ensure uppercase)
    clean_vehicle = re.sub(r'\s+', '', raw_vehicle).upper()
    
    # Basic Validation: Must start with 2 letters (State) + numbers
    if not re.match(r'^[A-Z]{2}\d{1,2}[A-Z]{0,2}\d{4}$', clean_vehicle):
        return jsonify({"status": "error", "message": "Invalid Format. Use: MH02AB1234"}), 400

    try:
        result = query_parivahan(clean_vehicle)
        if result:
            return jsonify({"status": "success", **result})
        else:
            return jsonify({"status": "error", "message": "Vehicle Not Found or Data Locked"}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def query_parivahan(vehicle_no):
    """
    Queries the Parivahan Sewa API (Public Endpoint).
    Note: This uses a direct GET request to the RTO database.
    """
    
    # The official endpoint for vehicle details
    url = "https://parivahan.gov.in/parivahan5.0/apis/v2/search"
    
    # Headers to mimic a real browser (Chrome on Android usually)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://parivahan.gov.in'
    }

    # The payload for the search API
    payload = {
        "key": vehicle_no,
        "type": "VEHICLE"
    }

    try:
        # Send request (Timeout 5 seconds)
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        
        if response.status_code == 200:
            api_data = response.json()
            
            # Parse the complex JSON structure returned by Parivahan
            # The actual data is nested deep inside 'data' -> 'details'
            
            details = api_data.get('data', {}).get('details', [])
            
            if not details:
                return None

            # Extract specific fields (Note: Keys might vary slightly, this covers standard response)
            owner_info = details[0]
            
            # Fallback logic for missing data
            owner_name = owner_info.get('name', 'N/A')
            mobile = owner_info.get('mobile', 'N/A')
            address = owner_info.get('address', 'N/A')
            fuel = owner_info.get('fuelType', 'N/A')
            v_class = owner_info.get('vehicleClass', 'N/A')
            
            # Insurance usually in a separate section or nested, trying to find it
            insurance = "Check RTO for details" 
            
            return {
                "vehicle_no": vehicle_no,
                "owner_name": owner_name,
                "mobile": mobile,
                "address": address,
                "fuel_type": fuel,
                "vehicle_class": v_class,
                "insurance": insurance
            }
            
        else:
            return None

    except requests.exceptions.Timeout:
        raise Exception("API Timeout (Server too slow)")
    except Exception as e:
        raise Exception(str(e))

# --- RUN SCRIPT ---
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script16_bp)
    
    print("🚗 Starting Vehicle Ghost Scanner...")
    print("Open: http://127.0.0.1:5007")
    
    app.run(debug=True, port=5007)
