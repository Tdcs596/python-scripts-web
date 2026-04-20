import requests
from flask import Blueprint, request, jsonify, render_template_string

script11_bp = Blueprint("script11", __name__)

# --- Hacker UI ---
SPOOF_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>GHOST-MAIL ZERO</title>
    <style>
        body { background: #000; color: #00ffcc; font-family: 'Courier New', monospace; text-align: center; padding: 40px; }
        .box { border: 1px solid #00ffcc; padding: 25px; display: inline-block; background: #0a0a0a; box-shadow: 0 0 20px #00ffcc44; width: 400px; border-radius: 10px; }
        input, textarea { background: #000; border: 1px solid #333; color: #00ffcc; padding: 12px; width: 90%; margin: 8px 0; outline: none; }
        button { background: #00ffcc; color: #000; border: none; padding: 15px; width: 96%; cursor: pointer; font-weight: bold; margin-top: 15px; }
        #status { margin-top: 15px; font-size: 11px; color: #555; }
    </style>
</head>
<body>
    <div class="box">
        <h2>[ GHOST-MAIL ZERO ]</h2>
        <p style="font-size: 10px;">NO SETUP REQUIRED - DIRECT DEPLOY</p>
        <input type="text" id="from_name" placeholder="FAKE SENDER NAME">
        <input type="email" id="from_email" placeholder="FAKE EMAIL (e.g. info@apple.com)">
        <input type="email" id="to_email" placeholder="TARGET EMAIL">
        <input type="text" id="subject" placeholder="SUBJECT">
        <textarea id="msg" placeholder="MESSAGE..." rows="5"></textarea>
        <button id="sendBtn" onclick="sendMail()">EXECUTE BYPASS</button>
        <div id="status">SYSTEM READY_</div>
    </div>

    <script>
        async function sendMail() {
            const btn = document.getElementById('sendBtn');
            const status = document.getElementById('status');
            
            const payload = {
                from_name: document.getElementById('from_name').value,
                from_email: document.getElementById('from_email').value,
                to_email: document.getElementById('to_email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('msg').value
            };

            btn.disabled = true;
            status.innerText = "ROUTING THROUGH PUBLIC RELAY...";
            
            try {
                const res = await fetch(window.location.pathname + "/send", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                status.innerText = data.message || data.error;
            } catch (e) {
                status.innerText = "RELAY_CONNECTION_ERROR";
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@script11_bp.route("/")
def index():
    return render_template_string(SPOOF_UI)

@script11_bp.route("/send", methods=["POST"])
def handle_send():
    data = request.get_json()
    
    # Using a Public Form-to-Email Relay (Zero Setup)
    # Yeh service bina kisi login ke email forward karti hai
    try:
        response = requests.post("https://formspree.io/f/mqakpney", json={
            "Sender": f"{data['from_name']} <{data['from_email']}>",
            "To": data['to_email'],
            "Subject": data['subject'],
            "Message": data['message']
        }, headers={"Accept": "application/json"})

        if response.status_code == 200:
            return jsonify({"message": "SUCCESS: Email Dispatched via Relay"})
        else:
            return jsonify({"error": "RELAY_REJECTED: Check target email"}), 400
            
    except Exception as e:
        return jsonify({"error": f"SYSTEM_ERR: {str(e)}"}), 500

