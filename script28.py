from flask import Blueprint, render_template_string, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging

script28_bp = Blueprint('script28', __name__)

# --- SMTP SERVER GATEWAY CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ramakantd809@gmail.com"
SENDER_PASSWORD = "alzrqjaorprdgtex"  # Bhai tumhara verified app password secure hai

# --- CYBER LINK BULK UI ---
SMTP_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S-Mail | Payload Delivery Terminal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #020408; color: #38bdf8; font-family: 'Consolas', 'Courier New', monospace; padding: 30px 15px; text-align: center; }
        .container { display: inline-block; width: 100%; max-width: 800px; text-align: left; }
        .box { border: 2px solid #38bdf8; background: #000; padding: 35px; box-shadow: 0 0 40px rgba(56, 189, 248, 0.15); border-radius: 14px; position: relative; }
        .box::before { content: '🖲️ SMTP DISPATCH PROTOCOL ACTIVE'; position: absolute; top: -11px; right: 20px; background: #38bdf8; color: #000; font-size: 11px; padding: 2px 10px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
        .header { text-align: center; border-bottom: 1px dashed #1e293b; padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #38bdf8; font-size: 24px; letter-spacing: 1px; }
        .subtitle { color: #475569; font-size: 12px; margin-top: 5px; letter-spacing: 2px; text-transform: uppercase; }
        
        label { font-size: 11px; color: #0284c7; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-top: 15px; margin-bottom: 6px; font-weight: bold; }
        input[type="text"], input[type="email"], textarea { width: 100%; padding: 14px; background: #050b14; border: 1px solid #0f355c; color: #fff; border-radius: 6px; outline: none; font-size: 14px; font-family: inherit; transition: 0.3s; }
        textarea { resize: vertical; min-height: 120px; }
        input[type="file"] { width: 100%; background: #050b14; border: 1px dashed #0f355c; color: #cbd5e1; padding: 15px; border-radius: 6px; outline: none; cursor: pointer; }
        
        input:focus, textarea:focus { border-color: #38bdf8; box-shadow: 0 0 10px rgba(56, 189, 248, 0.15); }
        
        button { width: 100%; padding: 16px; background: #38bdf8; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 15px; margin-top: 25px; transition: 0.2s; letter-spacing: 1.5px; text-transform: uppercase; font-family: inherit; }
        button:hover { background: #fff; box-shadow: 0 0 25px #fff; transform: translateY(-1px); }
        
        #console-status { margin-top: 20px; padding: 12px; border-radius: 6px; background: #050505; border: 1px solid #111; font-size: 13px; display: none; text-align: center; font-weight: bold; }
        .success-banner { color: #10b981; border-color: #064e3b !important; background: #022c22 !important; }
        .error-banner { color: #ef4444; border-color: #7f1d1d !important; background: #450a0a !important; }
        .warning { font-size: 11px; color: #334155; margin-top: 25px; text-align: center; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <div class="header">
                <h2>📨 CENTRALIZED SECURE MAIL DISPATCHER</h2>
                <p class="subtitle">SHIVAM SINGH OMEGA DASHBOARD • BINARY ATTACHMENT STREAM v5.0</p>
            </div>

            <form id="mailForm" enctype="multipart/form-data">
                <label for="emailInput">Target Recipient Address (To)</label>
                <input type="email" id="emailInput" name="email" placeholder="enter recipient email ID..." required>

                <label for="subjectInput">Subject Line Protocol</label>
                <input type="text" id="subjectInput" name="subject" placeholder="enter email subject header..." required>

                <label for="messageInput">Email Body (HTML/Plain Text Payload)</label>
                <textarea id="messageInput" name="message" placeholder="Type your core content or raw HTML parameters here..." required></textarea>

                <label for="fileInput">Upload Binary Attachments (Multiple Files Supported)</label>
                <input type="file" id="fileInput" name="files" multiple>

                <button type="button" onclick="fireSmtpPacket()">🚀 Dispatch Secure Packet</button>
            </form>

            <div id="console-status">Establishing transport routing matrices...</div>
            <div class="warning">S-MAIL CORE ENGINE • HARDENED TRANSPORT LAYER SECURITY (TLS) ENABLED</div>
        </div>
    </div>

    <script>
        async function fireSmtpPacket() {
            const form = document.getElementById('mailForm');
            const consoleStatus = document.getElementById('console-status');
            
            const email = document.getElementById('emailInput').value.trim();
            const subject = document.getElementById('subjectInput').value.trim();
            const message = document.getElementById('messageInput').value.trim();

            if(!email || !subject || !message) {
                alert("Bhai, To, Subject aur Message ka text daalna mandatory hai!");
                return;
            }

            consoleStatus.className = "";
            consoleStatus.style.display = "block";
            consoleStatus.style.color = "#eab308";
            consoleStatus.innerText = "⏳ Initializing secure SMTP relay... Streaming packet arrays...";

            const formData = new FormData(form);

            try {
                // FIXED: Direct static routing deployment url for centralized Blueprint module
                const res = await fetch('/script28/dispatch', {
                    method: 'POST',
                    body: formData
                });
                
                const callback = await res.json();

                if(callback.status === "success") {
                    consoleStatus.className = "success-banner";
                    consoleStatus.innerText = `✅ SUCCESS: ${callback.message}`;
                    form.reset();
                } else {
                    consoleStatus.className = "error-banner";
                    consoleStatus.innerText = `❌ CRITICAL ERROR: ${callback.message}`;
                }
            } catch (e) {
                consoleStatus.className = "error-banner";
                consoleStatus.innerText = "❌ EXCEPTION: Internal gateway routing connection timeout.";
            }
        }
    </script>
</body>
</html>
"""

@script28_bp.route('/')
def index():
    return render_template_string(SMTP_UI)

@script28_bp.route('/dispatch', methods=['POST'])
def dispatch_email():
    try:
        recipient = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message_body = request.form.get('message', '').strip()
        uploaded_files = request.files.getlist('files')

        if not recipient or not subject or not message_body:
            return jsonify({"status": "error", "message": "Required parameter extraction failure inside packet processing line."}), 400

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject

        if "<html>" in message_body.lower() or "</div>" in message_body.lower():
            msg.attach(MIMEText(message_body, 'html'))
        else:
            msg.attach(MIMEText(message_body, 'plain'))

        # --- MULTI-ATTACHMENT PROCESSOR STREAM ---
        for file_storage in uploaded_files:
            if file_storage.filename == '':
                continue
            
            file_data = file_storage.read()
            filename = file_storage.filename

            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(attachment)

        # --- SECURE RELAY RUNTIME PIPELINE ---
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()

        return jsonify({"status": "success", "message": f"All packets sent successfully! Delivered payload directly to [{recipient}]."})
    
    except Exception as e:
        logging.error(f"SMTP Gateway Relay Runtime Crash: {e}")
        return jsonify({"status": "error", "message": f"SMTP Gateway execution exception thrown: {str(e)}"}), 500

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script28_bp, url_prefix='/script28')
    app.run(debug=True, port=5000)

