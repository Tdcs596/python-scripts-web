from flask import Blueprint, render_template_string, jsonify, request, redirect
import hashlib
import urllib.parse

# Blueprint registered as 'script3'
script3_bp = Blueprint('script3', __name__)

# Global runtime transactional grid memory
SHORTENER_DATABASE = {}

def convert_to_punycode_stream(raw_url):
    """
    Parses structural domain parameters to evaluate Internationalized Domain Names (IDN).
    Safely translates lookalike characters into clear ascii punycode (xn--).
    """
    try:
        parsed = urllib.parse.urlparse(raw_url)
        hostname = parsed.hostname
        if hostname:
            puny_host = hostname.encode('idna').decode('ascii')
            reconstructed_netloc = puny_host
            if parsed.port:
                reconstructed_netloc += f":{parsed.port}"
                
            parsed = parsed._replace(netloc=reconstructed_netloc)
            return urllib.parse.urlunparse(parsed), puny_host
    except Exception:
        pass
    return raw_url, "Standard Resolution Vector"

SHORTENER_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORTIFIEDBYTES | Elite Shortener & IDN Compiler</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            background: #020408; 
            color: #38bdf8; 
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
            border: 2px solid #1e293b;
            background: rgba(4, 7, 16, 0.85);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.12);
            transition: all 0.3s ease-in-out;
        }

        .control-deck {
            width: 40%;
            min-width: 360px;
            background: rgba(5, 11, 20, 0.95);
            border-right: 2px solid #1e293b;
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
            border-bottom: 1px dashed #1e293b;
            padding-bottom: 15px;
        }
        .deck-title span { color: #f43f5e; text-shadow: 0 0 10px rgba(244, 63, 94, 0.5); }

        label { 
            font-size: 11px; 
            color: #0284c7; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            display: block; 
            margin-top: 25px; 
            margin-bottom: 8px; 
            font-weight: bold; 
        }

        .short-input { 
            width: 100%; 
            padding: 14px; 
            background: #020408; 
            border: 1px solid #0f355c; 
            color: #fff; 
            font-family: inherit; 
            border-radius: 8px; 
            outline: none; 
            font-size: 13px;
            transition: all 0.2s;
        }
        .short-input:focus { 
            border-color: #38bdf8; 
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
        }

        .btn-execute { 
            width: 100%; 
            padding: 15px; 
            font-weight: bold; 
            background: #38bdf8; 
            color: #000; 
            border: none; 
            font-family: inherit; 
            cursor: pointer; 
            border-radius: 8px; 
            margin-top: 30px; 
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
            background: rgba(1, 2, 5, 0.9);
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
            color: #475569; 
            text-align: center; 
            letter-spacing: 3px; 
            text-transform: uppercase; 
            border-top: 1px dashed #1e293b; 
            padding-top: 20px; 
            margin-top: 20px;
        }

        /* --- MEDIA QUERIES FOR ULTIMATE RESPONSIVENESS --- */
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
                border-bottom: 2px solid #1e293b;
                padding: 20px;
            }
            .terminal-viewport {
                width: 100%;
                padding: 20px;
                min-height: 350px;
            }
            .btn-execute { margin-top: 20px; }
        }

        @media (max-width: 480px) {
            .deck-title { font-size: 15px; }
            #terminal-output { font-size: 12px; }
            .control-deck { padding: 15px; }
            .terminal-viewport { padding: 15px; }
        }
    </style>
</head>
<body>

    <canvas id="star-canvas"></canvas>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-title">🛰️ FORTIFIEDBYTES <span>SHORT-ENG</span></div>
                
                <label for="long_url">Target Redirection Destination URL</label>
                <input type="url" id="long_url" class="short-input" placeholder="e.g., https://gооgle.com" required>

                <label for="custom_slug">Custom Routing Token / Alias (Optional)</label>
                <input type="text" id="custom_slug" class="short-input" placeholder="e.g., update-logs">

                <button class="btn-execute" onclick="compileShortLink()">⚡ Compress & Analyze Payload</button>
            </div>
            <div class="brand-tag">ROUTING DISTRIBUTION MATRIX</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output">Fortifiedbytes link converter environment initialized.<br>Awaiting outbound target tracking tokens...</div>
        </div>
    </div>

    <script>
        // Background Particle Space Loop
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
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#ffffff';
            stars.forEach(star => { ctx.globalAlpha = Math.abs(Math.sin(star.alpha)); ctx.beginPath(); ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2); ctx.fill(); star.alpha += star.speed; });
            ctx.globalAlpha = 1.0; requestAnimationFrame(drawStars);
        }
        window.addEventListener('resize', resizeCanvas); resizeCanvas(); drawStars();

        // Shortener Dispatch Request Handler
        async function compileShortLink() {
            const destination = document.getElementById('long_url').value.trim();
            const slug = document.getElementById('custom_slug').value.trim();
            const term = document.getElementById('terminal-output');

            if(!destination) {
                alert("Bhai, Target Destination URL compile karna mandatory hai!");
                return;
            }

            term.innerHTML += `\n\n[INGEST] Cleaning data packages and analyzing string formatting...`;

            try {
                // Fixed relative blueprint handshake invocation path
                const currentPath = window.location.pathname.replace(/\/$/, "");
                const response = await fetch(currentPath + '/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: destination, alias: slug })
                });
                const data = await response.json();

                if (data.error) {
                    term.innerHTML += `\n[EXEC_ERR] ${data.error}\n`;
                    return;
                }

                let outputHtml = `\n\n[SUCCESS] Structural Matrix Sync Complete!\n`;
                outputHtml += `-------------------------------------------------------------\n`;
                outputHtml += `📥 Ingestion Target:  ${destination}\n`;
                outputHtml += `🛡️ IDN Spec Target:   ${data.punycode_host}\n`;
                outputHtml += `🔗 Parsed Domain:     ${data.parsed_url}\n\n`;
                outputHtml += `🚀 Super Short Link:  <a href="${data.short_url}" target="_blank" style="color:#10b981; font-weight:bold; text-decoration:underline;">${data.short_url}</a>\n`;
                outputHtml += `-------------------------------------------------------------\n`;

                term.innerHTML += outputHtml;

                const vp = document.querySelector('.terminal-viewport');
                vp.scrollTop = vp.scrollHeight;

            } catch(e) {
                term.innerHTML += `\n[ERROR] Network sync handshake interface dropped.\n`;
            }
        }
    </script>
</body>
</html>
"""

@script3_bp.route('/')
def render_shortener_panel():
    return render_template_string(SHORTENER_UI)

@script3_bp.route('/shorten', methods=['POST'])
def process_shortener_request():
    data = request.json or {}
    raw_url = data.get('url', '').strip()
    alias = data.get('alias', '').strip()

    if not raw_url:
        return jsonify({"error": "Parameters input field missing destination path."}), 400

    # Format protocol schemes cleanly
    if not (raw_url.startswith('http://') or raw_url.startswith('https://')):
        raw_url = 'http://' + raw_url

    # Convert Homograph unicodes into safe Punycode notations (xn--)
    reconstructed_url, punycode_host = convert_to_punycode_stream(raw_url)

    # Shorten the routing tokens mapping
    if alias:
        slug = alias
    else:
        slug = hashlib.md5(reconstructed_url.encode('utf-8')).hexdigest()[:6]

    # Save mapping straight to transactional standard memory states
    SHORTENER_DATABASE[slug] = reconstructed_url

    # Strict structural formatting validation for proxies like Render.com
    # Parses host domain string with exact clean slashes
    host_base = request.host_url.rstrip('/')
    blueprint_prefix = request.blueprint.strip('/')
    
    # Generated Super Short Link structure matching your requested style perfectly
    final_short_path = f"{host_base}/{blueprint_prefix}/s/{slug}"

    return jsonify({
        "status": "synchronized",
        "punycode_host": punycode_host,
        "parsed_url": reconstructed_url,
        "short_url": final_short_path
    }), 200

@script3_bp.route('/s/<slug>')
def dynamic_redirect_gateway(slug):
    """
    Centralized high-performance link route matching distribution gateway.
    """
    target_destination = SHORTENER_DATABASE.get(slug)
    if target_destination:
        return redirect(target_destination)
    return "<h3>[404] Fortifiedbytes Core Error: Link token missing or state record expired from stack memory.</h3>", 404

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script3_bp, url_prefix='/script3')
    app.run(debug=True, port=5000)
