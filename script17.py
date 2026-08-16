from flask import Blueprint, render_template_string, request, jsonify
import base64
import os
import hashlib
import hmac
import logging

script17_bp = Blueprint('script17', __name__)

# --- PROPRIETARY ADVANCED ENTROPIC CIPHER ENGINE (NON-STANDARD CUSTOM PROTOCOL) ---
# Designed exclusively for the Omega Vault Architecture. Combines a rolling dynamic
# XOR matrix, cryptographic confusion substitution, dynamic salt layering, and HMAC integrity binding.

def _derive_custom_key(passphrase: str, salt: bytes, length: int) -> bytes:
    """Derives a custom pseudo-random byte stream using multi-pass SHA-384 folding."""
    key_material = passphrase.encode('utf-8') + salt
    derived = bytearray()
    counter = 0
    while len(derived) < length:
        h = hashlib.sha384(key_material + counter.to_bytes(4, 'big')).digest()
        derived.extend(h)
        counter += 1
    return bytes(derived[:length])

def shivam_encrypt(text, pkey):
    try:
        # Generate cryptographically secure random salt and initialization vector
        salt = os.urandom(24)
        iv = os.urandom(24)
        
        raw_data = text.encode('utf-8')
        data_len = len(raw_data)
        
        # Derive two distinct keys for stream transformation and integrity
        encryption_key = _derive_custom_key(pkey, salt, data_len + 32)
        
        # Apply custom multi-layer non-standard diffusion (Rolling XOR with positional index shift)
        obfuscated = bytearray(data_len)
        for i in range(data_len):
            key_byte = encryption_key[i] ^ iv[i % len(iv)]
            # Custom confusion matrix operation
            shifted_byte = ((raw_data[i] + (i % 251) + (salt[i % len(salt)])) ^ key_byte) & 0xFF
            obfuscated[i] = shifted_byte
            
        # Generate cryptographic HMAC-SHA256 integrity signature over salt + iv + obfuscated payload
        mac_key = _derive_custom_key(pkey, salt + b"MAC_DOMAIN", 32)
        signature = hmac.new(mac_key, salt + iv + bytes(obfuscated), hashlib.sha256).digest()
        
        # Final packing: Salt (24) + IV (24) + HMAC Tag (32) + Obfuscated Payload
        packed_payload = salt + iv + signature + bytes(obfuscated)
        return base64.urlsafe_b64encode(packed_payload).decode('utf-8')
    except Exception as e:
        return f"[!] Custom Encryption Protocol Exception: {str(e)}"

def shivam_decrypt(token, pkey):
    try:
        cleaned_token = token.strip().encode('utf-8')
        # Padding safety correction for URL-safe base64
        padding_needed = 4 - (len(cleaned_token) % 4)
        if padding_needed < 4:
            cleaned_token += b'=' * padding_needed
            
        data = base64.urlsafe_b64decode(cleaned_token)
        
        # Minimum structure check: Salt(24) + IV(24) + HMAC(32) = 80 bytes minimum
        if len(data) < 80:
            return "[!] Error: Payload structure is corrupt, truncated, or invalid!"
            
        salt = data[:24]
        iv = data[24:48]
        received_signature = data[48:80]
        obfuscated = data[80:]
        data_len = len(obfuscated)
        
        # Verify HMAC signature first (Constant-time check to prevent timing attacks)
        mac_key = _derive_custom_key(pkey, salt + b"MAC_DOMAIN", 32)
        expected_signature = hmac.new(mac_key, salt + iv + obfuscated, hashlib.sha256).digest()
        
        if not hmac.compare_digest(received_signature, expected_signature):
            return "[!] Security Alert: Cryptographic Signature Verification Failed! Incorrect Passphrase or Tampered Token."
            
        # Derive decryption stream key
        encryption_key = _derive_custom_key(pkey, salt, data_len + 32)
        
        # Reverse the custom diffusion and transformation steps
        original_bytes = bytearray(data_len)
        for i in range(data_len):
            key_byte = encryption_key[i] ^ iv[i % len(iv)]
            intermediate = (obfuscated[i] ^ key_byte) & 0xFF
            original_byte = ((intermediate - (i % 251) - (salt[i % len(salt)])) % 256) & 0xFF
            original_bytes[i] = original_byte
            
        return original_bytes.decode('utf-8')
    except Exception:
        return "[!] Error: Decryption sequence aborted. Invalid Master Passphrase or Malformed Data Stream."

# --- CORE PREMIUM ULTIMATE CYBERPUNK UI ---
UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Omega Vault | Ultimate Custom Cryptographic Node</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #020205;
            --bg-card: #08080f;
            --accent-red: #ff2a5f;
            --accent-glow: rgba(255, 42, 95, 0.35);
            --accent-cyan: #00f0ff;
            --text-main: #f0f0f5;
            --text-muted: #8888a0;
            --border-color: #221c35;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: var(--bg-primary); 
            color: var(--text-main); 
            font-family: 'Share Tech Mono', monospace; 
            padding: 40px 20px; 
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 42, 95, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 240, 255, 0.05) 0%, transparent 40%);
        }
        .main { 
            max-width: 680px; 
            width: 100%;
            border: 1px solid var(--border-color); 
            padding: 35px; 
            background: var(--bg-card); 
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.8), 0 0 25px var(--accent-glow); 
            border-radius: 16px; 
            position: relative; 
            backdrop-filter: blur(10px);
        }
        .main::before { 
            content: '🛡️ OMEGA CUSTOM CIPHER ENGINE v3.5'; 
            position: absolute; 
            top: -12px; 
            left: 30px; 
            background: var(--accent-red); 
            color: #000; 
            font-family: 'Orbitron', sans-serif;
            font-size: 10px; 
            padding: 3px 12px; 
            font-weight: 800; 
            border-radius: 4px; 
            letter-spacing: 1.5px; 
            box-shadow: 0 0 10px var(--accent-red);
        }
        .header { text-align: center; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; margin-bottom: 25px; }
        h2 { margin: 0; color: #fff; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 20px var(--accent-red); font-size: 22px; letter-spacing: 2px; }
        .subtitle { color: var(--text-muted); font-size: 11px; margin-top: 8px; letter-spacing: 2px; text-transform: uppercase; }
        
        .control-panel-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px; }
        .mode-selector { background: #0c0c16; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; cursor: pointer; text-align: center; font-family: 'Orbitron', sans-serif; font-size: 12px; color: var(--text-muted); transition: 0.3s; letter-spacing: 1px; }
        .mode-selector.active { border-color: var(--accent-red); color: #fff; background: rgba(255, 42, 95, 0.08); box-shadow: 0 0 15px rgba(255, 42, 95, 0.2); }
        
        label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-bottom: 6px; margin-top: 18px; font-family: 'Orbitron', sans-serif; }
        
        .textarea-wrapper, .pass-wrapper { position: relative; }
        textarea { width: 100%; background: #040408; border: 1px solid var(--border-color); color: #fff; padding: 14px; border-radius: 8px; resize: vertical; font-size: 13px; line-height: 1.6; outline: none; font-family: inherit; min-height: 120px; transition: 0.3s; }
        textarea:focus, input:focus { border-color: var(--accent-cyan); box-shadow: 0 0 15px rgba(0, 240, 255, 0.15); }
        
        input[type="password"], input[type="text"] { width: 100%; background: #040408; border: 1px solid var(--border-color); color: #fff; padding: 14px 45px 14px 14px; border-radius: 8px; font-size: 14px; outline: none; font-family: inherit; letter-spacing: 3px; transition: 0.3s; }
        
        .toggle-btn { position: absolute; right: 14px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: 'Orbitron', sans-serif; }
        .toggle-btn:hover { color: var(--accent-cyan); }
        
        .utility-row { display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); margin-top: 6px; }
        .clear-link { cursor: pointer; transition: 0.2s; }
        .clear-link:hover { color: var(--accent-red); }
        
        .action-container { margin-top: 25px; }
        button.action-btn { width: 100%; padding: 16px; font-weight: 800; cursor: pointer; border: none; text-transform: uppercase; border-radius: 8px; font-size: 14px; letter-spacing: 2px; transition: 0.3s; font-family: 'Orbitron', sans-serif; background: linear-gradient(135deg, var(--accent-red), #ff5e7e); color: #fff; box-shadow: 0 0 20px var(--accent-glow); }
        button.action-btn:hover { transform: translateY(-2px); box-shadow: 0 0 30px var(--accent-red); background: linear-gradient(135deg, #ff4070, var(--accent-red)); }
        button.action-btn:active { transform: translateY(0); }
        
        .result-container { margin-top: 30px; background: #050b08; border: 1px solid #103522; padding: 20px; border-radius: 10px; position: relative; }
        .result-label { font-size: 11px; color: #00ff88; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 10px; display: block; font-family: 'Orbitron', sans-serif; }
        #result { color: #55ffaa; word-break: break-all; font-size: 13px; min-height: 28px; white-space: pre-wrap; line-height: 1.5; }
        
        .output-actions { display: flex; gap: 10px; margin-top: 18px; }
        .sub-btn { flex: 1; padding: 10px 15px; font-size: 11px; background: #0c0c16; color: var(--text-muted); border: 1px solid var(--border-color); border-radius: 6px; cursor: pointer; font-family: 'Orbitron', sans-serif; text-transform: uppercase; font-weight: 600; letter-spacing: 1px; transition: 0.3s; }
        .sub-btn:hover { color: #fff; border-color: var(--accent-cyan); background: rgba(0, 240, 255, 0.05); }
        .swap-btn { color: var(--accent-cyan); border-color: rgba(0, 240, 255, 0.3); }
        
        .toast { position: fixed; bottom: 30px; right: 30px; background: #0c0c16; border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 12px 24px; border-radius: 6px; font-family: 'Orbitron', sans-serif; font-size: 12px; letter-spacing: 1px; box-shadow: 0 0 20px rgba(0, 240, 255, 0.3); display: none; z-index: 1000; animation: fadeInOut 2.5s ease; }
        @keyframes fadeInOut { 0% { opacity: 0; transform: translateY(20px); } 15% { opacity: 1; transform: translateY(0); } 85% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(20px); } }
    </style>
</head>
<body>

    <div class="main">
        <div class="header">
            <h2>☣️ OMEGA SECURE VAULT ☣️</h2>
            <p class="subtitle">Proprietary Non-Standard Entropic Cipher Protocol</p>
        </div>
        
        <div class="control-panel-grid">
            <div class="mode-selector active" id="modeEncBtn" onclick="setMode('encrypt')">🔒 Lock Payload</div>
            <div class="mode-selector" id="modeDecBtn" onclick="setMode('decrypt')">🔑 Unlock Payload</div>
        </div>
        
        <label for="msg" id="inputLabel">Source Data Payload</label>
        <div class="textarea-wrapper">
            <textarea id="msg" placeholder="Enter plaintext to secure or paste custom cryptographic token..."></textarea>
        </div>
        <div class="utility-row">
            <span id="char-count">Length: 0 chars</span>
            <span class="clear-link" onclick="clearInput()">[Clear Workspace]</span>
        </div>
        
        <label for="key">Master Security Passphrase</label>
        <div class="pass-wrapper">
            <input type="password" id="key" placeholder="Enter high-entropy master key...">
            <button type="button" class="toggle-btn" id="togglePass" onclick="togglePasswordVisibility()">Show</button>
        </div>
        
        <div class="action-container">
            <button class="action-btn" id="executeBtn" onclick="executeCrypto()">Initialize Encryption Sequence</button>
        </div>

        <div class="result-container">
            <span class="result-label" id="outputLabel">📡 Secure Terminal Output</span>
            <div id="result">System ready. Waiting for cryptographic handshake...</div>
            
            <div class="output-actions">
                <button class="sub-btn" onclick="copyResult()">📋 Copy Payload</button>
                <button class="sub-btn swap-btn" onclick="swapOutputToInput()">🔄 Route to Input</button>
            </div>
        </div>
    </div>

    <div class="toast" id="toastNotification">Notification Message</div>

    <script>
        let currentMode = 'encrypt';

        function setMode(mode) {
            currentMode = mode;
            const encBtn = document.getElementById('modeEncBtn');
            const decBtn = document.getElementById('modeDecBtn');
            const execBtn = document.getElementById('executeBtn');
            const inputLabel = document.getElementById('inputLabel');
            
            if (mode === 'encrypt') {
                encBtn.classList.add('active');
                decBtn.classList.remove('active');
                execBtn.innerText = 'Initialize Encryption Sequence';
                inputLabel.innerText = 'Source Plaintext Payload';
                showToast("Mode Switched: Encryption Active");
            } else {
                decBtn.classList.add('active');
                encBtn.classList.remove('active');
                execBtn.innerText = 'Initialize Decryption Sequence';
                inputLabel.innerText = 'Encrypted Cipher Token';
                showToast("Mode Switched: Decryption Active");
            }
        }

        document.getElementById('msg').addEventListener('input', function() {
            document.getElementById('char-count').innerText = "Length: " + this.value.length + " chars";
        });

        async function executeCrypto() {
            const text = document.getElementById('msg').value.trim();
            const pass = document.getElementById('key').value;
            const resultDiv = document.getElementById('result');
            
            if(!text || !pass) {
                showToast("Error: Both payload and passphrase are required!");
                return;
            }

            resultDiv.innerText = "⏳ Executing proprietary entropic transformation matrix...";

            try {
                const targetPath = window.location.pathname.endsWith('/') ? window.location.pathname + 'process' : window.location.pathname + '/process';
                const res = await fetch(targetPath, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text, pass, mode: currentMode})
                });
                const data = await res.json();
                resultDiv.innerText = data.output;
                showToast("Cryptographic execution complete.");
            } catch(e) {
                resultDiv.innerText = "[!] Pipeline Failure: Communication breakdown with server node.";
                showToast("Error: Connection failure.");
            }
        }

        function togglePasswordVisibility() {
            const passInput = document.getElementById('key');
            const toggleBtn = document.getElementById('togglePass');
            if (passInput.type === 'password') {
                passInput.type = 'text';
                toggleBtn.innerText = 'Hide';
            } else {
                passInput.type = 'password';
                toggleBtn.innerText = 'Show';
            }
        }

        function clearInput() {
            document.getElementById('msg').value = '';
            document.getElementById('char-count').innerText = "Length: 0 chars";
            showToast("Workspace cleared.");
        }

        function swapOutputToInput() {
            const outText = document.getElementById('result').innerText;
            if(!outText || outText.startsWith("System ready") || outText.startsWith("⏳") || outText.startsWith("[!]")) {
                showToast("No valid output available to route.");
                return;
            }
            document.getElementById('msg').value = outText;
            document.getElementById('char-count').innerText = "Length: " + outText.length + " chars";
            
            // Automatically flip mode for convenience
            if(currentMode === 'encrypt') {
                setMode('decrypt');
            } else {
                setMode('encrypt');
            }
            showToast("Output routed to input workspace.");
        }

        function copyResult() {
            const result = document.getElementById('result').innerText;
            if(result.startsWith("System ready") || result.startsWith("⏳")) return;
            
            navigator.clipboard.writeText(result).then(() => {
                showToast("Payload copied to secure buffer!");
            });
        }

        function showToast(message) {
            const toast = document.getElementById('toastNotification');
            toast.innerText = message;
            toast.style.display = 'block';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 2500);
        }
    </script>
</body>
</html>
"""

@script17_bp.route('/')
def index():
    return render_template_string(UI)

@script17_bp.route('/process', methods=['POST'])
def process():
    try:
        data = request.json or {}
        mode = data.get('mode')
        text = data.get('text', '')
        pkey = data.get('pass', '')
        
        if mode == 'encrypt':
            output = shivam_encrypt(text, pkey)
        else:
            output = shivam_decrypt(text, pkey)
            
        return jsonify({'output': output})
    except Exception as e:
        logging.error(f"Omega Vault processing error: {e}")
        return jsonify({'output': "[!] Error: Critical exception encountered during core pipeline processing."})

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script17_bp, url_prefix='/script17')
    app.run(debug=True, port=5000)
