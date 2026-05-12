from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json
import base64

script11_bp = Blueprint('script11', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "7bab199056msh3df63cfe9c45d9dp1996b2jsn25ec6d748a00"
RAPID_API_HOST = "sendmail-ultimate-email-sender.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>PHANTOM_MAILER_v11</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .container { border: 2px solid #0f0; background: #050505; padding: 30px; box-shadow: 0 0 30px #0f03; display: inline-block; width: 90%; max-width: 700px; border-radius: 10px; text-align: left; }
        .input-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; color: #0f0; font-size: 14px; }
        input, textarea { width: 100%; padding: 10px; background: #111; border: 1px solid #0f0; color: #fff; border-radius: 5px; box-sizing: border-box; font-family: inherit; }
        .attachment-section { border: 1px dashed #555; padding: 10px; margin-top: 10px; }
        button { width: 100%; padding: 15px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 16px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 20px #fff; }
        #status { margin-top: 20px; padding: 10px; display: none; text-align: center; border-radius: 5px; }
        .success { background: #004400; color: #0f0; border: 1px solid #0f0; }
        .error { background: #440000; color: #f00; border: 1px solid #f00; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center;">☣️ PHANTOM_MAILER v11 ☣️</h2>
        <p style="text-align:center; color:#888;">Ultimate Email Sender with Attachment Support</p>
        <hr style="border:0.5px solid #333;">

        <div class="input-group">
            <label>TARGET EMAIL (To):</label>
            <input type="email" id="to_email" placeholder="victim@example.com">
        </div>

        <div class="input-group">
            <label>SENDER NAME/EMAIL (Reply-To):</label>
            <input type="text" id="reply_to" placeholder="support@google.com">
        </div>

        <div class="input-group">
            <label>SUBJECT:</label>
            <input type="text" id="subject" placeholder="Security Alert: Action Required">
        </div>

        <div class="input-group">
            <label>MESSAGE BODY (HTML Supported):</label>
            <textarea id="body" rows="6" placeholder="Bhai, message yahan likho..."></textarea>
        </div>

        <div class="attachment-section">
            <label>ATTACHMENT (Optional):</label>
            <input type="file" id="file_input" onchange="encodeFile()">
            <input type="hidden" id="file_base64">
            <input type="hidden" id="file_name">
            <p id="file_status" style="font-size:10px; color:#888; margin-top:5px;">No file selected</p>
        </div>
        <br>

        <button onclick="sendMail()" id="send_btn">EXECUTE_SENDING</button>
        <div id="status"></div>
    </div>

    <script>
        function encodeFile() {
            const file = document.getElementById('file_input').files[0];
            const reader = new FileReader();
            reader.onloadend = function() {
                document.getElementById('file_base64').value = reader.result.split(',')[1];
                document.getElementById('file_name').value = file.name;
                document.getElementById('file_status').innerText = "File Ready: " + file.name;
            }
            if (file) reader.readAsDataURL(file);
        }

        async function sendMail() {
            const btn = document.getElementById('send_btn');
            const status = document.getElementById('status');
            
            const payload = {
                to: document.getElementById('to_email').value,
                replyTo: document.getElementById('reply_to').value,
                title: document.getElementById('subject').value,
                body: document.getElementById('body').value,
                fileName: document.getElementById('file_name').value,
                fileContent: document.getElementById('file_base64').value
            };

            if(!payload.to || !payload.title) return alert("To and Subject are required!");

            btn.disabled = true;
            btn.innerText = "SENDING_PACKETS...";
            status.style.display = "none";

            try {
                const res = await fetch('/script11/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                status.style.display = "block";
                if(data.success) {
                    status.className = "success";
                    status.innerText = "✅ EMAIL SENT SUCCESSFULLY!";
                } else {
                    status.className = "error";
                    status.innerText = "❌ FAILED: " + data.message;
                }
            } catch (e) {
                status.className = "error";
                status.innerText = "❌ CONNECTION ERROR";
                status.style.display = "block";
            }
            btn.disabled = false;
            btn.innerText = "EXECUTE_SENDING";
        }
    </script>
</body>
</html>
"""

@script11_bp.route('/')
def index():
    return render_template_string(UI)

@script11_bp.route('/send', methods=['POST'])
def send():
    data = request.json
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        
        # Build API Payload
        email_data = {
            "sendTo": data['to'],
            "replyTo": data['replyTo'],
            "isHtml": True,
            "title": data['title'],
            "body": data['body']
        }

        # Agar file hai toh attachment add karo
        if data.get('fileContent'):
            email_data["attachments"] = [
                {
                    "content": data['fileContent'],
                    "filename": data['fileName']
                }
            ]

        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }

        conn.request("POST", "/send-email", json.dumps(email_data), headers)
        res = conn.getresponse()
        res_data = res.read().decode("utf-8")
        
        return jsonify({"success": True, "response": res_data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


