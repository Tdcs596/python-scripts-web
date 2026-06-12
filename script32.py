from flask import Blueprint, render_template_string, jsonify, request
import urllib.parse

# Blueprint registered as 'script32'
script32_bp = Blueprint('script32', __name__)

WHATSAPP_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORTIFIEDBYTES | WhatsApp Dispatch Gateway</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            background: #020408; 
            color: #10b981; 
            font-family: 'Consolas', 'Courier New', monospace; 
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 15px;
            overflow-x: hidden;
        }

        #star-canvas {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        .workspace {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: row;
            width: 100%;
            max-width: 1100px;
            height: 85vh;
            min-height: 580px;
            border: 2px solid #14532d;
            background: rgba(4, 16, 10, 0.85);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(16, 185, 129, 0.12);
            transition: all 0.3s ease-in-out;
        }

        .control-deck {
            width: 40%;
            min-width: 360px;
            background: rgba(5, 20, 13, 0.95);
            border-right: 2px solid #14532d;
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .deck-title {
            color: #fff;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            border-bottom: 1px dashed #14532d;
            padding-bottom: 15px;
        }
        .deck-title span { color: #10b981; text-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }

        label { 
            font-size: 11px; 
            color: #059669; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            display: block; 
            margin-top: 20px; 
            margin-bottom: 8px; 
            font-weight: bold; 
        }

        .bot-input, .bot-textarea { 
            width: 100%; 
            padding: 14px; 
            background: #020408; 
            border: 1px solid #14532d; 
            color: #fff; 
            font-family: inherit; 
            border-radius: 8px; 
            outline: none; 
            font-size: 13px;
            transition: all 0.2s;
        }
        .bot-textarea {
            resize: none;
            height: 120px;
        }
        .bot-input:focus, .bot-textarea:focus { 
            border-color: #10b981; 
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
        }

        .btn-execute { 
            width: 100%; 
            padding: 15px; 
            font-weight: bold; 
            background: #10b981; 
            color: #000; 
            border: none; 
            font-family: inherit; 
            cursor: pointer; 
            border-radius: 8px; 
            margin-top: 20px; 
            transition: all 0.25s ease; 
            text-transform: uppercase; 
            letter-spacing: 1.5px; 
        }
        .btn-execute:hover { 
            background: #fff; 
            box-shadow: 0 0 25px #fff;
            transform: translateY(-1px);
        }

        .terminal-viewport {
            flex: 1;
            background: rgba(1, 5, 2, 0.9);
            padding: 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }

        #terminal-output { 
            white-space: pre-wrap; 
            font-size: 13px; 
            line-height: 1.7; 
            color: #e2e8f0; 
            word-break: break-all;
        }

        .brand-tag { 
            font-size: 10px; 
            color: #334155; 
            text-align: center; 
            letter-spacing: 3px; 
            text-transform: uppercase; 
            border-top: 1px dashed #14532d; 
            padding-top: 20px; 
            margin-top: 20px;
        }

        /* --- RESPONSIVE ADJUSTMENTS --- */
        @media (max-width: 868px) {
            body { padding: 10px; }
            .workspace {
                flex-direction: column;
                height: auto;
                min-height: calc(100vh - 20px);
            }
            .control-deck {
                width: 100%;
                min-width: 100%;
                border-right: none;
                border-bottom: 2px solid #14532d;
                padding: 20px;
            }
            .terminal-viewport {
                width: 100%;
                padding: 20px;
                min-height: 350px;
            }
        }
    </style>
</head>
<body>

    <canvas id="star-canvas"></canvas>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-title">🛰️ FORTIFIEDBYTES <span>WP-BOT</span></div>
                
                <label for="phone_number">Target Phone Number (With Country Code)</label>
                <input type="text" id="phone_number" class="bot-input" placeholder="e.g., 919876543210" required>

                <label for="bot_message">Message Payload Text</label>
                <textarea id="bot_message" class="bot-textarea" placeholder="Type your automated message here..." required></textarea>

                <button class="btn-execute" onclick="dispatchWhatsappPayload()">⚡ Trigger Bot Vector</button>
            </div>
            <div class="brand-tag">WHATSAPP AUTOMATION CORE</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output">Fortifiedbytes WhatsApp bot runtime pipeline initialized.<br>Awaiting target phone routing variables...</div>
        </div>
    </div>

    <script>
        // Matrix Canvas Background
        const canvas = document.getElementById('star-canvas');
        const ctx = canvas.getContext('2d');
        let stars = [];

        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; initStars(); }
        function initStars() {
            stars = [];
            const count = Math.floor((canvas.width * canvas.height) / 4500);
            for (let i = 0; i < count; i++) {
                stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, size: Math.random() * 1.6, alpha: Math.random(), speed: 0.006 + Math.random() * 0.01 });
            }
        }
        function drawStars() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#10b981';
            stars.forEach(star => { ctx.globalAlpha = Math.abs(Math.sin(star.alpha)); ctx.beginPath(); ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2); ctx.fill(); star.alpha += star.speed; });
            ctx.globalAlpha = 1.0; requestAnimationFrame(drawStars);
        }
        window.addEventListener('resize', resizeCanvas); resizeCanvas(); drawStars();

        // Dispatch Action Controller
        async function dispatchWhatsappPayload() {
            const number = document.getElementById('phone_number').value.trim();
            const msg = document.getElementById('bot_message').value.trim();
            const term = document.getElementById('terminal-output');

            if(!number || !msg) {
                alert("Bhai, Target Number aur Message dono field bharna mandatory hai!");
                return;
            }

            term.innerHTML += `\n\n[INGEST] Packaging string layers for destination target: +${number}...`;

            try {
                const currentPath = window.location.pathname.replace(/\/$/, "");
                const response = await fetch(currentPath + '/send', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ phone: number, message: msg })
                });
                const data = await response.json();

                if (data.error) {
                    term.innerHTML += `\n[EXEC_ERR] ${data.error}\n`;
                    return;
                }

                let outputHtml = `\n\n[SUCCESS] Bot Messaging Routing Synchronized!\n`;
                outputHtml += `-------------------------------------------------------------\n`;
                outputHtml += `📱 Destination Target: +${data.target_phone}\n`;
                outputHtml += `💬 Message Payload:    "${data.payload_msg}"\n\n`;
                outputHtml += `🚀 Launch Protocol:   <a href="${data.api_url}" target="_blank" style="color:#fff; background:#10b981; padding: 5px 10px; border-radius: 4px; font-weight:bold; text-decoration:none;">Open Web WhatsApp Trigger</a>\n`;
                outputHtml += `-------------------------------------------------------------\n`;

                term.innerHTML += outputHtml;

                const vp = document.querySelector('.terminal-viewport');
                vp.scrollTop = vp.scrollHeight;

            } catch(e) {
                term.innerHTML += `\n[ERROR] Network sync handshake failed.\n`;
            }
        }
    </script>
</body>
</html>
"""

@script32_bp.route('/')
def render_panel():
    return render_template_string(WHATSAPP_UI)

@script32_bp.route('/send', methods=['POST'])
def process_bot_request():
    data = request.json or {}
    phone = data.get('phone', '').strip().replace('+', '').replace(' ', '')
    message = data.get('message', '').strip()

    if not phone or not message:
        return jsonify({"error": "Target number or payload content is missing."}), 400

    # URL safe encryption/encoding for WhatsApp message format strings
    encoded_message = urllib.parse.quote(message)
    
    # Official Universal WA Gateway Link Protocol
    whatsapp_api_gateway = f"https://api.whatsapp.com/send?phone={phone}&text={encoded_message}"

    # NOTE: Professional Production API setups integrate Twilio/Meta Business SDK right here:
    # Example: client.messages.create(body=message, from_='whatsapp:+14155238886', to=f'whatsapp:+{phone}')

    return jsonify({
        "status": "packet_built",
        "target_phone": phone,
        "payload_msg": message,
        "api_url": whatsapp_api_gateway
    }), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script32_bp, url_prefix='/bot')
    app.run(debug=True, port=5000)
