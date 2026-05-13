from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script24_bp = Blueprint('script24', __name__)

# --- CONFIGURATION ---
RAPID_API_KEY = "155514abbfmshd5da5b6f34d5791p144617jsn3ac281515eb0"
RAPID_API_HOST = "anonmyous-mail-sender.p.rapidapi.com"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>GHOST_MAILER_v24</title>
    <style>
        body { background: #000; color: #ff0055; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .container { border: 2px solid #ff0055; background: #050505; padding: 30px; box-shadow: 0 0 30px #ff005533; display: inline-block; width: 90%; max-width: 700px; border-radius: 10px; text-align: left; }
        label { display: block; margin-bottom: 5px; color: #ff0055; font-size: 14px; margin-top: 15px; }
        input, textarea { width: 100%; padding: 12px; background: #111; border: 1px solid #ff0055; color: #fff; border-radius: 5px; box-sizing: border-box; outline: none; }
        .file-section { border: 1px dashed #444; padding: 15px; margin-top: 20px; text-align: center; background: #0a0a0a; }
        button { width: 100%; padding: 15px; background: #ff0055; color: #fff; border: none; font-weight: bold; cursor: pointer; margin-top: 20px; border-radius: 5px; font-size: 16px; transition: 0.3s; }
        button:hover { background: #fff; color: #000; box-shadow: 0 0 20px #fff; }
        #status { margin-top: 20px; padding: 10px; display: none; text-align: center; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align:center;">🕵️ ANONYMOUS GHOST MAILER v24</h2>
        <p style="text-align:center; color:#666; font-size:12px;">Identity: HIDDEN | Status: ENCRYPTED</p>
        <hr style="border:0.5px solid #222;">

        <label>TARGET EMAIL (To):</label>
        <input type="email" id="to_email" placeholder="victim@gmail.com">

        <label>SUBJECT:</label>
        <input type="text" id="subject" placeholder="Confidential Message">

        <label>MESSAGE BODY (Text):</label>
        <textarea id="body" rows="6" placeholder="Apna secret message yahan likho..."></textarea>

        <div class="file-section">
            <label style="margin-top:0;">📎 ATTACH FILE (Images/PDF/Docs):</label>
            <input type="file" id="file_input">
            <p id="file_msg" style="font-size:10px; color:#888; margin-top:10px;">File will be converted to Base64 automatically</p>
        </div>

        <button onclick="sendGhostMail()" id="send_btn">EXECUTE ANONYMOUS SEND</button>
        <div id="status"></div>
    </div>

    <script>
        // File ko base64 mein badalne ka modern tareeka
        const getBase64 = file => new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = error => reject(error);
        });

        async function sendGhostMail() {
            const btn = document.getElementById('send_btn');
            const status = document.getElementById('status');
            const file = document.getElementById('file_input').files[0];

            const to = document.getElementById('to_email').value;
            const subject = document.getElementById('subject').value;
            const body = document.getElementById('body').value;

            if(!to || !subject || !body) return alert("Bhai, Details toh bharo!");

            btn.disabled = true;
            btn.innerText = "ENCRYPTING & SENDING...";
            status.style.display = "none";

            let fileContent = null;
            if (file) {
                fileContent = await getBase64(file);
            }

            const payload = {
                to: to,
                subject: subject,
                text: body,
                attachment: fileContent
            };

            try {
                const res = await fetch('/script24/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const result = await res.json();
                
                status.style.display = "block";
                if(result.success) {
                    status.style.color = "#0f0";
                    status.innerText = "✅ GHOST MAIL DELIVERED!";
                } else {
                    status.style.color = "#f00";
                    status.innerText = "❌ FAILED: " + result.message;
                }
            } catch (e) {
                alert("Server Connection Error!");
            }
            btn.disabled = false;
            btn.innerText = "EXECUTE ANONYMOUS SEND";
        }
    </script>
</body>
</html>
"""

@script24_bp.route('/')
def index():
    return render_template_string(UI)

@script24_bp.route('/send', methods=['POST'])
def send_mail():
    data = request.json
    try:
        conn = http.client.HTTPSConnection(RAPID_API_HOST)
        
        # API expects specific fields
        mail_payload = {
            "to": data['to'],
            "subject": data['subject'],
            "text": data['text']
        }

        # Agar attachment hai toh payload mein inject karo
        # Note: Kuch APIs mein key 'file' ya 'attachment' hoti hai
        if data.get('attachment'):
            mail_payload["attachment"] = data['attachment']

        headers = {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': RAPID_API_HOST,
            'Content-Type': "application/json"
        }

        conn.request("POST", "/send", json.dumps(mail_payload), headers)
        res = conn.getresponse()
        resp_data = res.read().decode("utf-8")
        
        return jsonify({"success": True, "response": resp_data})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

