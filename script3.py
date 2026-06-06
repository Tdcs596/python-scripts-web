from flask import Blueprint, render_template_string, jsonify, request, redirect
import hashlib
import urllib.parse

script3_bp = Blueprint('script3', __name__)

# Core transactional storage for custom routing paths
SHORTENER_DATABASE = {}

def convert_to_punycode_stream(raw_url):
    """
    Parses incoming structural components to evaluate Internationalized Domain Names (IDN).
    Converts visual homograph strings safely into clear transport punycode notations.
    """
    try:
        parsed = urllib.parse.urlparse(raw_url)
        # Extract hostname boundary (e.g., google.com containing spoofed cyrillic indicators)
        hostname = parsed.hostname
        if hostname:
            puny_host = hostname.encode('idna').decode('ascii')
            # Reconstruct string layout cleanly
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
            padding: 20px;
            height: 100vh;
        }

        #star-canvas {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        .workspace {
            position: relative;
            z-index: 10;
            display: flex;
            width: 100%;
            height: 92vh;
            border: 2px solid #1e293b;
            background: rgba(0, 0, 0, 0.9);
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.15);
        }

        .control-deck {
            width: 420px;
            background: #050b14;
            border-right: 2px solid #1e293b;
            padding: 25px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .deck-title {
            color: #fff;
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .deck-title span { color: #f43f5e; }

        label { 
            font-size: 11px; 
            color: #0284c7; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            display: block; 
            margin-top: 20px; 
            margin-bottom: 6px; 
            font-weight: bold; 
        }

        .short-input { 
            width: 100%; 
            padding: 12px; 
            background: #020408; 
            border: 1px solid #0f355c; 
            color: #fff; 
            font-family: inherit; 
            border-radius: 6px; 
            outline: none; 
            font-size: 13px;
        }
        .short-input:focus { border-color: #38bdf8; }

        .btn-execute { 
            width: 100%; 
            padding: 14px; 
            font-weight: bold; 
            background: #38bdf8; 
            color: #000; 
            border: none; 
            font-family: inherit; 
            cursor: pointer; 
            border-radius: 8px; 
            margin-top: 25px; 
            transition: 0.2s; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
        }
        .btn-execute:hover { background: #fff; box-shadow: 0 0 20px #fff; }

        .terminal-viewport {
            flex: 1;
            background: #010205;
            padding: 25px;
            overflow-y: auto;
        }

        #terminal-output { 
            white-space: pre-wrap; 
            font-size: 13px; 
            line-height: 1.6; 
            color: #e2e8f0; 
        }

        .result-box {
            margin-top: 20px;
            padding: 15px;
            background: #050b14;
            border: 1px solid #1e293b;
            border-radius: 6px;
        }

        .brand-tag { 
            font-size: 10px; 
            color: #475569; 
            text-align: center; 
            letter-spacing: 3px; 
            text-transform: uppercase; 
            border-top: 1px dashed #1e293b; 
            padding-top: 20px; 
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
                <input type="text" id="long_url" class="short-input" placeholder="e.g., https://gооgle.com (with IDN chars)">

                <label for="custom_slug">Custom Routing Token / Alias (Optional)</label>
                <input type="text" id="custom_slug" class="short-input" placeholder="e.g., update-service">

                <button class="btn-execute" onclick="compileShortLink()">⚡ Compress & Analyze Payload</button>
            </div>
            <div class="brand-tag">ROUTING DISTRIBUTION MATRIX</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output">Fortifiedbytes URL dynamic shortener system active.<br>Awaiting outbound target ingestion vectors...</div>
        </div>
    </div>

    <script>
        // Starfield Background Effect Loop
        const canvas = document.getElementById('star-canvas');
        const ctx = canvas.getContext('2d');
        let stars = [];

        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; initStars(); }
        function initStars() {
            stars = [];
            const count = Math.floor((canvas.width * canvas.height) / 4000);
            for (let i = 0; i < count; i++) {
                stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, size: Math.random() * 1.8, alpha: Math.random(), speed: 0.005 + Math.random() * 0.01 });
            }
        }
        function drawStars() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#ffffff';
            stars.forEach(star => { ctx.globalAlpha = Math.abs(Math.sin(star.alpha)); ctx.beginPath(); ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2); ctx.fill(); star.alpha += star.speed; });
            ctx.globalAlpha = 1.0; requestAnimationFrame(drawStars);
        }
        window.addEventListener('resize', resizeCanvas); resizeCanvas(); drawStars();

        // Execution Controller Pipeline
        async function compileShortLink() {
            const destination = document.getElementById('long_url').value.trim();
            const slug = document.getElementById('custom_slug').value.trim();
            const term = document.getElementById('terminal-output');

            if(!destination) {
                alert("Bhai, Destination URL field compile karna mandatory hai!");
                return;
            }

            term.innerHTML += `\n\n[INGEST] Compiling payload destination routing parameters...\n`;

            try {
                const response = await fetch(window.location.pathname + 'shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: destination, alias: slug })
                });
                const data = await response.json();

                if (data.error) {
                    term.innerHTML += `[EXEC_ERR] ${data.error}\n`;
                    return;
                }

                let outputHtml = `\n[SUCCESS] Structural Mapping Matrix Stabilized!\n`;
                outputHtml += `--------------------------------------------------\n`;
                outputHtml += `📥 Input Target Look:   ${destination}\n`;
                outputHtml += `⚙️ IDN Punycode Engine: ${data.punycode_host}\n`;
                outputHtml += `🔗 Parsed Real Target:  ${data.parsed_url}\n`;
                outputHtml += `🚀 Compressed Router:   <a href="${data.short_url}" target="_blank" style="color:#38bdf8; font-weight:bold;">${data.short_url}</a>\n`;
                outputHtml += `--------------------------------------------------\n`;

                term.innerHTML += outputHtml;

                const vp = document.querySelector('.terminal-viewport');
                vp.scrollTop = vp.scrollHeight;

            } catch(e) {
                term.innerHTML += `[ERROR] Ingestion failed over communication channel.\n`;
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
        return jsonify({"error": "Empty destination path parameters specified."}), 400

    # Prefix protocol layers default checks if omitted by user
    if not (raw_url.startswith('http://') or raw_url.startswith('https://')):
        raw_url = 'http://' + raw_url

    # Execute dynamic structural Homograph parsing validation via core IDNA protocols
    reconstructed_url, punycode_host = convert_to_punycode_stream(raw_url)

    # Determine unique structural routing token hash slug
    if alias:
        slug = alias
    else:
        # Generate clean short hash string via MD5 checksum limits
        slug = hashlib.md5(reconstructed_url.encode('utf-8')).hexdigest()[:7]

    # Save tracking reference variables inside temporary local matrix states
    SHORTENER_DATABASE[slug] = reconstructed_url

    # Compile the final local short redirection endpoint address link
    root_url = request.url_root.rstrip('/')
    # Resolves mapping directly to blueprint dynamic redirection route context
    final_short_path = f"{root_url}/script3/go/{slug}"

    return jsonify({
        "status": "synchronized",
        "punycode_host": punycode_host,
        "parsed_url": reconstructed_url,
        "short_url": final_short_path
    }), 200

@script3_bp.route('/go/<slug>')
def dynamic_redirect_gateway(slug):
    """
    Acts as the centralized structural transport handler to route shortened hash tags.
    """
    target_destination = SHORTENER_DATABASE.get(slug)
    if target_destination:
        return redirect(target_destination)
    return "<h3>[404] Fortifiedbytes Core Error: Compressed Routing Link Token Invalid or Expired from Stack Memory.</h3>", 404

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script3_bp, url_prefix='/script3')
    app.run(debug=True, port=5000)
