from flask import Blueprint, render_template_string, jsonify, request
from PIL import Image
import io
import base64

script32_bp = Blueprint('script32', __name__)

STEGANO_PREMIUM_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORTIFIEDBYTES | Steganography Quantum Matrix</title>
    <style>
        /* --- RESET & PREMIUM CSS VARIABLES --- */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-color: #030712;
            --panel-bg: rgba(9, 17, 35, 0.75);
            --border-glow: #1e293b;
            --neon-blue: #0ea5e9;
            --neon-emerald: #10b981;
            --neon-rose: #f43f5e;
            --text-main: #f3f4f6;
            --text-dark: #64748b;
        }

        body { 
            background: var(--bg-color); 
            color: var(--text-main); 
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Consolas', monospace; 
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            overflow-x: hidden;
        }

        /* --- BACKGROUND PARTICLE LOOP --- */
        #star-canvas {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
            pointer-events: none;
        }

        /* --- THE MASTER WORKSPACE PANEL --- */
        .workspace {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: row;
            width: 100%;
            max-width: 1250px;
            height: 88vh;
            min-height: 650px;
            border: 1px solid rgba(14, 165, 233, 0.2);
            background: var(--panel-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 40px rgba(14, 165, 233, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* --- LEFT SIDEBAR: CONFIGURATION DECK --- */
        .control-deck {
            width: 42%;
            min-width: 380px;
            background: rgba(4, 9, 20, 0.9);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            padding: 35px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow-y: auto;
        }

        .deck-header {
            border-bottom: 1px dashed rgba(14, 165, 233, 0.3);
            padding-bottom: 20px;
            margin-bottom: 10px;
        }

        .deck-title {
            color: #fff;
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .deck-title span { 
            color: var(--neon-rose); 
            text-shadow: 0 0 15px rgba(244, 63, 94, 0.6); 
        }

        /* --- INTERACTIVE TABS --- */
        .tabs {
            display: flex;
            gap: 12px;
            margin-top: 20px;
        }

        .tab-btn {
            flex: 1;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: var(--text-dark);
            padding: 12px;
            cursor: pointer;
            border-radius: 10px;
            font-family: inherit;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }

        .tab-btn:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }

        .tab-btn.active {
            border-color: var(--neon-blue);
            color: var(--neon-blue);
            background: rgba(14, 165, 233, 0.08);
            box-shadow: inset 0 0 12px rgba(14, 165, 233, 0.15);
        }

        label { 
            font-size: 11px; 
            color: var(--neon-blue); 
            text-transform: uppercase; 
            letter-spacing: 1.5px; 
            display: block; 
            margin-top: 25px; 
            margin-bottom: 10px; 
            font-weight: 700; 
        }

        /* --- PREMIUM FILE & TEXT INPUTS --- */
        .stego-input-file {
            width: 100%;
            padding: 14px;
            background: #02040a;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #fff;
            border-radius: 12px;
            outline: none;
            font-size: 13px;
            cursor: pointer;
            transition: 0.3s;
        }
        .stego-input-file:hover {
            border-color: rgba(14, 165, 233, 0.4);
        }

        .input-container {
            position: relative;
        }

        .stego-textarea { 
            width: 100%; 
            padding: 16px; 
            background: #02040a; 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            color: #fff; 
            font-family: 'Consolas', monospace; 
            border-radius: 12px; 
            outline: none; 
            font-size: 13px;
            resize: none; 
            height: 110px;
            transition: all 0.3s;
        }
        
        .stego-textarea:focus { 
            border-color: var(--neon-blue); 
            box-shadow: 0 0 15px rgba(14, 165, 233, 0.15);
        }

        .char-counter {
            position: absolute;
            bottom: 10px;
            right: 15px;
            font-size: 11px;
            color: var(--text-dark);
        }

        /* --- ACTION TRIGGER BUTTON --- */
        .btn-execute { 
            width: 100%; 
            padding: 16px; 
            font-weight: 700; 
            background: var(--neon-blue); 
            color: #000; 
            border: none; 
            font-family: inherit; 
            cursor: pointer; 
            border-radius: 12px; 
            margin-top: 25px; 
            transition: all 0.3s ease; 
            text-transform: uppercase; 
            letter-spacing: 1.5px; 
            font-size: 14px;
        }
        .btn-execute:hover { 
            background: #fff; 
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }

        /* --- RIGHT PANEL: LIVE VIEWPORT & LOGS --- */
        .terminal-viewport {
            flex: 1;
            background: rgba(2, 4, 10, 0.95);
            padding: 35px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }

        #terminal-output { 
            white-space: pre-wrap; 
            font-size: 13px; 
            line-height: 1.8; 
            color: #cbd5e1; 
            font-family: 'Consolas', 'Courier New', monospace;
            word-break: break-all;
        }

        /* --- DOWNLOAD BUTTON INTERACTIVE CARD --- */
        .download-wrapper {
            margin-top: 20px;
            padding: 20px;
            background: rgba(16, 185, 129, 0.04);
            border: 1px dashed rgba(16, 185, 129, 0.3);
            border-radius: 14px;
            text-align: center;
            animation: fadeIn 0.4s ease forwards;
        }

        .download-link {
            display: inline-flex;
            align-items: center;
            padding: 12px 24px;
            background: var(--neon-emerald);
            color: #020408;
            text-decoration: none;
            font-weight: 700;
            border-radius: 10px;
            transition: 0.3s;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .download-link:hover { 
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.4); 
            background: #fff; 
        }

        .brand-tag { 
            font-size: 10px; 
            color: var(--text-dark); 
            text-align: center; 
            letter-spacing: 4px; 
            text-transform: uppercase; 
            border-top: 1px dashed rgba(255, 255, 255, 0.08); 
            padding-top: 20px; 
            margin-top: 25px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- MEDIA QUERIES FOR ULTIMATE RESPONSIVENESS --- */
        @media (max-width: 950px) {
            body { padding: 10px; }
            .workspace {
                flex-direction: column;
                height: auto;
                min-height: calc(100vh - 20px);
                border-radius: 16px;
            }
            .control-deck { 
                width: 100%; 
                min-width: 100%; 
                border-right: none; 
                border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
                padding: 25px; 
            }
            .terminal-viewport { 
                min-height: 400px; 
                padding: 25px; 
            }
        }

        @media (max-width: 480px) {
            .control-deck { padding: 20px; }
            .terminal-viewport { padding: 20px; }
            .deck-title { font-size: 17px; }
            .tab-btn { padding: 10px; font-size: 11px; }
        }
    </style>
</head>
<body>

    <canvas id="star-canvas"></canvas>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-header">
                    <div class="deck-title">🛰️ FORTIFIEDBYTES <span>STEGO-v32</span></div>
                    
                    <div class="tabs">
                        <button id="tab-hide" class="tab-btn active" onclick="switchMode('hide')">EMBED DATA</button>
                        <button id="tab-extract" class="tab-btn" onclick="switchMode('extract')">EXTRACT DATA</button>
                    </div>
                </div>

                <label for="image_file">Upload Cover Matrix Image (PNG Preferred)</label>
                <input type="file" id="image_file" class="stego-input-file" accept="image/*" required>

                <div id="hide-fields-container">
                    <label for="secret_data">Secret Payload Content String</label>
                    <div class="input-container">
                        <textarea id="secret_data" class="stego-textarea" placeholder="Type or paste confidential data strings..." oninput="updateCharCount()"></textarea>
                        <div class="char-counter" id="char-counter-text">0 characters</div>
                    </div>
                </div>

                <button class="btn-execute" id="exec-btn" onclick="processStegoVector()">⚡ Launch Encode Vector</button>
            </div>
            <div class="brand-tag">QUANTUM ENCRYPTION MODULATOR</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output"><span style="color:var(--neon-blue);">[SYSTEM STATUS]</span> Quantum processing matrix initialized successfully.<br>Load high-density configurations or swap modes to start bit streams...</div>
        </div>
    </div>

    <script>
        // --- PREMIUM FLOATING NETWORK BACKGROUND ---
        const canvas = document.getElementById('star-canvas');
        const ctx = canvas.getContext('2d');
        let stars = [];

        function resizeCanvas() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; initStars(); }
        function initStars() {
            stars = [];
            const count = Math.floor((canvas.width * canvas.height) / 4000);
            for (let i = 0; i < count; i++) {
                stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height, size: Math.random() * 1.8, alpha: Math.random(), speed: 0.005 + Math.random() * 0.008 });
            }
        }
        function drawStars() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.fillStyle = '#38bdf8';
            stars.forEach(star => { ctx.globalAlpha = Math.abs(Math.sin(star.alpha)); ctx.beginPath(); ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2); ctx.fill(); star.alpha += star.speed; });
            ctx.globalAlpha = 1.0; requestAnimationFrame(drawStars);
        }
        window.addEventListener('resize', resizeCanvas); resizeCanvas(); drawStars();

        // --- CORE UI ANIMATION CONTROLLERS ---
        let currentMode = 'hide';
        function switchMode(mode) {
            currentMode = mode;
            document.getElementById('tab-hide').classList.toggle('active', mode === 'hide');
            document.getElementById('tab-extract').classList.toggle('active', mode === 'extract');
            document.getElementById('hide-fields-container').style.display = mode === 'hide' ? 'block' : 'none';
            
            const btn = document.getElementById('exec-btn');
            if (mode === 'hide') {
                btn.innerText = '⚡ Launch Encode Vector';
                btn.style.background = 'var(--neon-blue)';
            } else {
                btn.innerText = '🔍 Scan & Extract Payload';
                btn.style.background = 'var(--neon-emerald)';
            }
        }

        function updateCharCount() {
            const count = document.getElementById('secret_data').value.length;
            document.getElementById('char-counter-text').innerText = `${count} characters`;
        }

        // --- ASYNC DATA FLUSH ENGINE HANDSHAKE ---
        async function processStegoVector() {
            const fileInput = document.getElementById('image_file');
            const secretData = document.getElementById('secret_data').value.trim();
            const term = document.getElementById('terminal-output');

            if (fileInput.files.length === 0) {
                alert("Bhai, Pehle processing ke liye image file upload karo!");
                return;
            }

            if (currentMode === 'hide' && !secretData) {
                alert("Bhai, Embedded message framework khali nahi chhod sakte!");
                return;
            }

            const file = fileInput.files[0];
            const reader = new FileReader();

            term.innerHTML += `\n\n<span style="color:#eab308;">[JOB START]</span> Ingesting raw byte configurations into asynchronous storage...`;

            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                const endpoint = currentMode === 'hide' ? '/hide' : '/extract';
                
                const payload = { image: base64Image };
                if (currentMode === 'hide') payload.data = secretData;

                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(currentPath + endpoint, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    const resData = await response.json();

                    if (resData.error) {
                        term.innerHTML += `\n<span style="color:var(--neon-rose);">[RUNTIME_ERROR]</span> Execution blocked: ${resData.error}\n`;
                        return;
                    }

                    if (currentMode === 'hide') {
                        term.innerHTML += `\n\n<span style="color:var(--neon-emerald);">[SUCCESS]</span> Bitwise operations injection process stable.\n`;
                        term.innerHTML += `-------------------------------------------------------------\n`;
                        term.innerHTML += `📦 Structural Bytes Embedded : ${secretData.length} Chars\n`;
                        term.innerHTML += `🖼️ Transmitted Quality Alpha : 100% Intact\n`;
                        term.innerHTML += `-------------------------------------------------------------\n`;
                        
                        // Clean older cards and rebuild modern downloader module
                        const oldWrapper = document.querySelector('.download-wrapper');
                        if (oldWrapper) oldWrapper.remove();

                        const wrap = document.createElement('div');
                        wrap.className = 'download-wrapper';
                        wrap.innerHTML = `<p style="color:#a7f3d0; margin-bottom:12px; font-size:12px;">PROCESSED STEGO BUFFER COMPREHENSION COMPLETE</p>`;
                        
                        const dl = document.createElement('a');
                        dl.href = "data:image/png;base64," + resData.result_image;
                        dl.download = "fortified_stego_output.png";
                        dl.className = "download-link";
                        dl.innerText = "📥 Download Stego Asset";
                        
                        wrap.appendChild(dl);
                        term.appendChild(wrap);
                    } else {
                        term.innerHTML += `\n\n<span style="color:var(--neon-emerald);">[SUCCESS]</span> Matrix scan stream complete!\n`;
                        term.innerHTML += `-------------------------------------------------------------\n`;
                        term.innerHTML += `🔓 Extracted Content Payload:\n\n`;
                        term.innerHTML += `<span style="color:var(--neon-emerald); font-weight:800; font-size:15px; background:rgba(16, 185, 129, 0.08); padding:10px; border-radius:8px; display:block; border:1px solid rgba(16, 185, 129, 0.2);">${resData.extracted_data}</span>\n`;
                        term.innerHTML += `-------------------------------------------------------------\n`;
                    }

                    const vp = document.querySelector('.terminal-viewport');
                    vp.scrollTop = vp.scrollHeight;

                } catch(err) {
                    term.innerHTML += `\n<span style="color:var(--neon-rose);">[CRITICAL_FAULT]</span> Request interface connection dropped.\n`;
                }
            };

            reader.readAsDataURL(file);
        }
    </script>
</body>
</html>
"""

@script32_bp.route('/')
def index():
    return render_template_string(STEGANO_PREMIUM_UI)

@script32_bp.route('/hide', methods=['POST'])
def hide_data_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    secret_text = data.get('data', '')

    if not image_b64 or not secret_text:
        return jsonify({"error": "Missing essential payload stream variables."}), 400

    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Unique identification sequence anchor
        secret_text += "##END##"
        binary_secret = ''.join([format(ord(char), '08b') for char in secret_text])
        
        pixels = image.load()
        data_index = 0
        data_len = len(binary_secret)

        width, height = image.size
        for y in range(height):
            for x in range(width):
                if data_index >= data_len:
                    break
                
                r, g, b = pixels[x, y]
                if data_index < data_len:
                    r = (r & ~1) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < data_len:
                    g = (g & ~1) | int(binary_secret[data_index])
                    data_index += 1
                if data_index < data_len:
                    b = (b & ~1) | int(binary_secret[data_index])
                    data_index += 1
                    
                pixels[x, y] = (r, g, b)

        if data_index < data_len:
            return jsonify({"error": "Selected image canvas resolution is too tiny for this text packet size."}), 200

        output_buffer = io.BytesIO()
        image.save(output_buffer, format="PNG")
        encoded_result = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return jsonify({"result_image": encoded_result}), 200

    except Exception as e:
        return jsonify({"error": f"Internal matrix transformation logic broke: {str(e)}"}), 200

@script32_bp.route('/extract', methods=['POST'])
def extract_data_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')

    if not image_b64:
        return jsonify({"error": "Target sequence tracking index point missing."}), 400

    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        pixels = image.load()
        binary_buffer = ""
        extracted_chars = []
        
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_buffer += str(r & 1)
                binary_buffer += str(g & 1)
                binary_buffer += str(b & 1)

        for i in range(0, len(binary_buffer), 8):
            byte = binary_buffer[i:i+8]
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            extracted_chars.append(char)
            
            current_stream = "".join(extracted_chars)
            if "##END##" in current_stream:
                final_data = current_stream.split("##END##")[0]
                return jsonify({"extracted_data": final_data}), 200

        return jsonify({"error": "No verified Fortifiedbytes transmission data blocks found inside this target asset."}), 200

    except Exception as e:
        return jsonify({"error": f"Extraction framework execution failed: {str(e)}"}), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script32_bp, url_prefix='/stego')
    app.run(debug=True, port=5000)

