from flask import Blueprint, render_template_string, jsonify, request
import subprocess
import shlex

script30_bp = Blueprint('script30', __name__)

# Allowed safe base commands matrix to prevent arbitrary OS command injection
ALLOWED_ADB_COMMANDS = {
    'devices': 'adb devices',
    'logcat': 'adb logcat -d -v time',
    'getprop': 'adb shell getprop ro.product.model',
    'battery': 'adb shell dumpsys battery',
    'features': 'adb shell pm list features',
    'packages': 'adb shell pm list packages -3',
    'uptime': 'adb shell uptime'
}

ADB_CONSOLE_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FORTIFIEDBYTES | Real-Time ADB Control Gateway</title>
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
            width: 380px;
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

        .adb-select, .adb-input { 
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
        
        .adb-input:focus {
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
                <div class="deck-title">🛰️ FORTIFIEDBYTES <span>ADB-CORE</span></div>
                
                <label for="adb_macro">Pre-configured Macro Commands</label>
                <select id="adb_macro" class="adb-select" onchange="applyMacro()">
                    <option value="devices">adb devices (Enumerate Targets)</option>
                    <option value="logcat">adb logcat (Diagnostic Stream)</option>
                    <option value="getprop">adb shell getprop (Model Info)</option>
                    <option value="battery">adb shell dumpsys battery (Power Stats)</option>
                    <option value="features">adb shell pm list features</option>
                    <option value="packages">adb shell pm list packages (3rd Party)</option>
                    <option value="uptime">adb shell uptime</option>
                    <option value="custom">-- Execute Custom Arguments --</option>
                </select>

                <label for="custom_args">Custom ADB Sub-Arguments / Shell parameters</label>
                <input type="text" id="custom_args" class="adb-input" placeholder="e.g. shell getprop" disabled oninput="updatePreview()">

                <label>Raw Process Execution Preview</label>
                <div class="cli-preview" id="adb_preview_box">adb devices</div>

                <button class="btn-execute" onclick="runAdbCommand()">⚡ Dispatch ADB Process</button>
            </div>
            <div class="brand-tag">PRODUCTION HARDWARE HUB</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output">Fortifiedbytes real ADB communication pipeline online.<br>Ready to execute backend shell commands against targets...</div>
        </div>
    </div>

    <script>
        // Starfield background loop
        const canvas = document.getElementById('star-canvas');
        const ctx = canvas.getContext('2d');
        let stars = [];

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initStars();
        }
        function initStars() {
            stars = [];
            const count = Math.floor((canvas.width * canvas.height) / 4000);
            for (let i = 0; i < count; i++) {
                stars.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    size: Math.random() * 1.8,
                    alpha: Math.random(),
                    speed: 0.005 + Math.random() * 0.01
                });
            }
        }
        function drawStars() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#ffffff';
            stars.forEach(star => {
                ctx.globalAlpha = Math.abs(Math.sin(star.alpha));
                ctx.beginPath();
                ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
                ctx.fill();
                star.alpha += star.speed;
            });
            ctx.globalAlpha = 1.0;
            requestAnimationFrame(drawStars);
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();
        drawStars();

        // Control logic
        function applyMacro() {
            const macro = document.getElementById('adb_macro').value;
            const customInput = document.getElementById('custom_args');
            
            if (macro === 'custom') {
                customInput.disabled = false;
                customInput.value = '';
                customInput.focus();
            } else {
                customInput.disabled = true;
                customInput.value = '';
            }
            updatePreview();
        }

        function updatePreview() {
            const macro = document.getElementById('adb_macro').value;
            const customArgs = document.getElementById('custom_args').value.trim();
            const preview = document.getElementById('adb_preview_box');

            if (macro === 'custom') {
                preview.innerText = customArgs ? `adb ${customArgs}` : 'adb [arguments]';
            } else {
                const mapping = {
                    'devices': 'adb devices',
                    'logcat': 'adb logcat -d -v time',
                    'getprop': 'adb shell getprop ro.product.model',
                    'battery': 'adb shell dumpsys battery',
                    'features': 'adb shell pm list features',
                    'packages': 'adb shell pm list packages -3',
                    'uptime': 'adb shell uptime'
                };
                preview.innerText = mapping[macro] || 'adb devices';
            }
        }

        async function runAdbCommand() {
            const macro = document.getElementById('adb_macro').value;
            const customArgs = document.getElementById('custom_args').value.trim();
            const term = document.getElementById('terminal-output');
            
            const fullCommandString = document.getElementById('adb_preview_box').innerText;
            term.innerHTML += `\n\n$ ${fullCommandString}\n[PROCESS] Calling Android Debug Bridge runtime sub-process...\n`;

            try {
                const response = await fetch(window.location.pathname + 'run', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mode: macro, custom: customArgs })
                });
                const data = await response.json();
                
                term.innerHTML += data.output;
                
                const vp = document.querySelector('.terminal-viewport');
                vp.scrollTop = vp.scrollHeight;
            } catch(e) {
                term.innerHTML += "[ERROR] Subprocess transport pipeline failed to respond.\n";
            }
        }
    </script>
</body>
</html>
"""

@script30_bp.route('/')
def index():
    return render_template_string(ADB_CONSOLE_UI)

@script30_bp.route('/run', methods=['POST'])
def execute_adb_subprocess():
    data = request.json or {}
    mode = data.get('mode', 'devices')
    custom_args = data.get('custom', '').strip()
    
    # Process building string
    if mode == 'custom':
        if not custom_args:
            return jsonify({"output": "Error: Custom arguments string empty.\n"}), 200
        
        # Enforce strict parsing validation: Only execute adb context binaries
        args_parsed = shlex.split(custom_args)
        if args_parsed and args_parsed[0].lower() == 'adb':
            # Remove redundant 'adb' token if included by user since it is appended automatically
            args_parsed.pop(0)
            
        full_command = ['adb'] + args_parsed
    else:
        # Revert back to verified pre-configured commands matrix
        command_line = ALLOWED_ADB_COMMANDS.get(mode, 'adb devices')
        full_command = shlex.split(command_line)

    try:
        # Spawning real execution stream safely via subprocess shell=False mechanism
        result = subprocess.run(
            full_command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            timeout=8.0
        )
        
        output_buffer = ""
        if result.stdout:
            output_buffer += result.stdout
        if result.stderr:
            output_buffer += f"[STDERR_LOG]\n{result.stderr}"
        if not output_buffer:
            output_buffer = "Command completed with no standard descriptor output stream.\n"
            
        return jsonify({"output": output_buffer}), 200

    except subprocess.TimeoutExpired:
        return jsonify({"output": "[TIMEOUT] Process execution exceeded safety windows. Check if daemon is active or stuck.\n"}), 200
    except FileNotFoundError:
        return jsonify({"output": "[EXEC_ERR] 'adb' runtime binary could not be located on host system PATH parameters.\n"}), 200
    except Exception as e:
        return jsonify({"output": f"[SYSTEM_ERR] Unhandled exception occurred: {str(e)}\n"}), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script30_bp, url_prefix='/adb')
    app.run(debug=True, port=5001)

