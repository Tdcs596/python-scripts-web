from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

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
        label { display: block; margin-bottom: 5px; color: #0f0; font-size: 14px; margin-top: 15px; }
        input, textarea { width: 100%; padding: 10px; background: #111; border: 1px solid #0f0; color: #fff; border-radius: 5px; box-sizing: border-box; }
        .file-box { border: 1px dashed #555; padding: 15px; margin-top: 15px; text-align: center; }
        button { width: 100%; padding: 15px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; margin-top: 20px; border-radius: 5px; }
        #status { margin-top: 20px; padding: 10px; display: none; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center;">☣️ PHANTOM MAIL SPOOFER ☣️</h2>
        
        <label>TO (Victim Email):</label>
        <input type="email" id="to_email" placeholder="target@gmail.com">

        <label>REPLY-TO (Spoofed Sender):</label>
        <input type="text" id="reply_to" placeholder="billing@netflix.com">

        <label>SUBJECT:</label>
        <input type="text" id="subject" placeholder="Account Suspension Alert">

        <label>MESSAGE:</label>
        <textarea id="body" rows="5" placeholder="Write HTML or Plain text here..."></textarea>

        <div class="file-box">
            <label style="margin-top:0;">📎 ATTACH FILE (PDF/JPG/PNG):</label>
            <input type="file" id="file_input">
            <p id="file_info" style="font-size:11px; color:#888;"></p>
        </div>

        <button onclick="sendMail()" id="send_btn">EXECUTE SEND</button>
        <div id="status"></div>
    </div>

    <script>
        // File ko Base64 mein convert karne ka function
        const toBase64 = file => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = error => reject(error);
        });

        async function sendMail() {
            const btn = document.getElementById('send_btn');
            const status = document.getElementById('status');
            const file = document.getElementById('file_input').files[0];
            
            btn.disabled = true;
            btn.innerText = "UPLOADING & SENDING...";

            let fileData = null;
            let fileName = null;

            if (file) {
                fileData = await toBase64(file);
                fileName = file.name;
            }

            const payload = {
                to: document.getElementById('to_email').value,
                replyTo: document.getElementById('reply_to').value,
                title: document.getElementById('subject').value,
                body: document.getElementById('body').value,
                att_name: fileName,
                att_content: fileData
            };

            try {
                const res = await fetch('/script11/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                
                status.style.display = "block";
                if(result.success) {
                    status.innerHTML = "<span style='color:#0f0;'>✅ SENT: " + result.response + "</span>";
                } else {
                    status.innerHTML = "<span style='color:#f00;'>❌ FAILED: " + result.message + "</span>";
                }
            } catch (e) {
                alert("Connection Error!");
            }
            btn.disabled = false;
            btn.innerText = "EXECUTE SEND";
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
        
        email_payload = {
            "sendTo": data['to'],
            "replyTo": data['replyTo'],
            "isHtml": True,
            "title": data['title'],
            "body": data['body']
        }

        # Agar attachment payload mein hai toh add karein
        if data.get('att_content'):
            email_payload["attachments"] = [
                {
                    "content": data['att_content'],
                    "filename": data['att_name']
                }
            ]

        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }

        conn.request("POST", "/send-email", json.dumps(email_payload), headers)
        res = conn.getresponse()
        resp_data = res.read().decode("utf-8")
        
        return jsonify({"success": True, "response": resp_data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
