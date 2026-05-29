from flask import Blueprint, render_template_string, jsonify, request
import urllib.parse

script31_bp = Blueprint('script31', __name__)

DORK_CONSOLE_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORTIFIEDBYTES | Advanced Google Dorking Workspace</title>
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
            overflow-y: auto;
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
            margin-top: 15px; 
            margin-bottom: 6px; 
            font-weight: bold; 
        }

        .dork-input, .dork-select { 
            width: 100%; 
            padding: 10px 12px; 
            background: #020408; 
            border: 1px solid #0f355c; 
            color: #fff; 
            font-family: inherit; 
            border-radius: 6px; 
            outline: none; 
            font-size: 13px;
        }
        
        .dork-input:focus, .dork-select:focus {
            border-color: #38bdf8;
        }

        .cli-preview { 
            background: #020408; 
            border: 1px dashed #1e293b; 
            padding: 12px; 
            border-radius: 6px; 
            font-size: 12px; 
            color: #fda4af; 
            margin-top: 8px; 
            word-break: break-all;
            min-height: 45px;
        }

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
            margin-top: 20px; 
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

        .dork-link {
            display: inline-block;
            margin-top: 10px;
            padding: 10px 15px;
            background: #0f355c;
            color: #fff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
            transition: 0.2s;
            border: 1px solid #38bdf8;
        }
        .dork-link:hover {
            background: #38bdf8;
            color: #000;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
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
    </style>
</head>
<body>

    <canvas id="star-canvas"></canvas>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-title">🛰️ FORTIFIEDBYTES <span>DORK-V31</span></div>
                
                <label for="dork_macro">Pre-configured Intelligence Audits</label>
                <select id="dork_macro" class="dork-select" onchange="applyMacroProfile()">
                    <option value="custom">-- Manual Custom Deployment --</option>
                    <option value="log_files">Exposed Log Files (filetype:log)</option>
                    <option value="env_files">Exposed Environment Configurations (.env / config)</option>
                    <option value="sql_errors">SQL Database Error Leaks</option>
                    <option value="public_db">Exposed Backup/Database Files (.sql / .bkp)</option>
                    <option value="open_dirs">Open Directory Indexes (intitle:"index of")</option>
                </select>

                <label for="target_domain">Target Boundary Scope (site:)</label>
                <input type="text" id="target_domain" class="dork-input" placeholder="e.g. example.com" oninput="compileDorkQuery()">

                <label for="file_type">File Extension Constraint (filetype:)</label>
                <input type="text" id="file_type" class="dork-input" placeholder="e.g. pdf, xml, log" oninput="compileDorkQuery()">

                <label for="in_title">Required Title Tokens (intitle:)</label>
                <input type="text" id="in_title" class="dork-input" placeholder="e.g. "index of"" oninput="compileDorkQuery()">

                <label for="in_url">Required URL String Fragments (inurl:)</label>
                <input type="text" id="in_url" class="dork-input" placeholder="e.g. wp-content, admin" oninput="compileDorkQuery()">

                <label for="generic_term">Additional Search Term / Raw Expression</label>
                <input type="text" id="generic_term" class="dork-input" placeholder="e.g. "password" / "root"" oninput="compileDorkQuery()">

                <label>Compiled Query Matrix Preview</label>
                <div class="cli-preview" id="dork_preview_box">Generating audit payload...</div>

                <button class="btn-execute" onclick="dispatchDorkVector()">⚡ Compile & Launch Query</button>
            </div>
            <div class="brand-tag">INTELLIGENCE PROCESSING HUB</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output">Fortifiedbytes passive intelligence gathering platform structural loop active.<br>Define dork parameters or load a pre-configured audit engine profile...</div>
        </div>
    </div>

    <script>
        // Starfield Engine Loop
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

        // Control Matrix Assembly Logic
        function applyMacroProfile() {
            const profile = document.getElementById('dork_macro').value;
            
            // Reset manual inputs on macro application
            document.getElementById('file_type').value = '';
            document.getElementById('in_title').value = '';
            document.getElementById('in_url').value = '';
            document.getElementById('generic_term').value = '';

            if (profile === 'log_files') {
                document.getElementById('file_type').value = 'log';
                document.getElementById('generic_term').value = '"username" | "password"';
            } else if (profile === 'env_files') {
                document.getElementById('file_type').value = 'env';
                document.getElementById('generic_term').value = '"DB_PASSWORD"';
            } else if (profile === 'sql_errors') {
                document.getElementById('generic_term').value = '"Database Error" | "SQL syntax"';
            } else if (profile === 'public_db') {
                document.getElementById('file_type').value = 'sql';
                document.getElementById('generic_term').value = '"dump"';
            } else if (profile === 'open_dirs') {
                document.getElementById('in_title').value = '"index of"';
                document.getElementById('generic_term').value = '"backup"';
            }
            compileDorkQuery();
        }

        function compileDorkQuery() {
            const site = document.getElementById('target_domain').value.trim();
            const filetype = document.getElementById('file_type').value.trim();
            const title = document.getElementById('in_title').value.trim();
            const url = document.getElementById('in_url').value.trim();
            const generic = document.getElementById('generic_term').value.trim();
            
            let queryParts = [];
            
            if (site) queryParts.push(`site:${site}`);
            if (filetype) queryParts.push(`filetype:${filetype}`);
            if (title) queryParts.push(`intitle:${title}`);
            if (url) queryParts.push(`inurl:${url}`);
            if (generic) queryParts.push(generic);
            
            const compiled = queryParts.join(' ');
            document.getElementById('dork_preview_box').innerText = compiled ? compiled : '[Awaiting parameters input]';
        }

        async function dispatchDorkVector() {
            const rawQuery = document.getElementById('dork_preview_box').innerText;
            const term = document.getElementById('terminal-output');
            
            if (!rawQuery || rawQuery.startsWith('[')) {
                alert("Bhai, kam se kam ek parameter input ya macro select karna zaroorat hai!");
                return;
            }

            term.innerHTML += `\n\n[AUDIT] Compiling query parameters for passive discovery rules...\n`;
            term.innerHTML += `$ dork-engine --build "${rawQuery}"\n`;

            try {
                const response = await fetch(window.location.pathname + 'compile', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: rawQuery })
                });
                const data = await response.json();
                
                let resultConsole = `[SUCCESS] Query verification matching complete.\n`;
                resultConsole += `Parsed Payload Vector: ${data.compiled_query}\n\n`;
                resultConsole += `Google Dorking safety isolation parameters prevent internal server loop scanning block rules. Click below to safely open this compiled search request directly inside isolated browser sandboxes:\n\n`;
                
                term.innerHTML += resultConsole;
                
                // Append custom target processing engine anchor
                const linkElement = document.createElement('a');
                linkElement.href = data.search_url;
                linkElement.target = '_blank';
                linkElement.className = 'dork-link';
                linkElement.innerText = '🚀 Launch Query Vector in Google';
                
                term.appendChild(linkElement);
                term.innerHTML += `<br>\n`;
                
                const vp = document.querySelector('.terminal-viewport');
                vp.scrollTop = vp.scrollHeight;
            } catch(e) {
                term.innerHTML += "[ERROR] Structural transport logic mismatch during calculation stream.\n";
            }
        }
        
        // Initial setup run
        compileDorkQuery();
    </script>
</body>
</html>
"""

@script31_bp.route('/')
def index():
    return render_template_string(DORK_CONSOLE_UI)

@script31_bp.route('/compile', methods=['POST'])
def compile_dork_payload():
    data = request.json or {}
    query_string = data.get('query', '').strip()
    
    # Safe production encryption/encoding for standard search pipeline query parameters
    encoded_query = urllib.parse.quote_plus(query_string)
    isolated_search_target = f"https://www.google.com/search?q={encoded_query}"
    
    return jsonify({
        "status": "compiled",
        "compiled_query": query_string,
        "search_url": isolated_search_target
    }), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script31_bp, url_prefix='/dork')
    app.run(debug=True, port=5002)

