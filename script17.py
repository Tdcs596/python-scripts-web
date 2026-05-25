from flask import Blueprint, render_template_string, request, jsonify
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging

script17_bp = Blueprint('script17', __name__)

# --- CORE HARDENED CRYPTO ENGINE ---
def get_private_key(password: str, salt: bytes):
    # PBKDF2 Key Derivation Function with SHA256 (Standard Compliance)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def shivam_encrypt(text, pkey):
    try:
        salt = os.urandom(16)
        key = get_private_key(pkey, salt)
        iv = os.urandom(12)  # Recommended IV length for AES-GCM is 12 bytes
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
        tag = encryptor.tag  # CRITICAL FIX: GCM Authentication Tag extracted
        
        # Packing: Salt (16) + IV (12) + Tag (16) + Ciphertext
        packed_payload = salt + iv + tag + ciphertext
        return base64.b64encode(packed_payload).decode('utf-8')
    except Exception as e:
        return f"[!] Encryption Failed: {str(e)}"

def shivam_decrypt(token, pkey):
    try:
        data = base64.b64decode(token.strip())
        if len(data) < 44:  # Salt(16) + IV(12) + Tag(16) = 44 bytes minimum threshold
            return "[!] Error: Payload structure is too short or corrupt!"
            
        salt = data[:16]
        iv = data[16:28]
        tag = data[28:44]
        ciphertext = data[44:]
        
        key = get_private_key(pkey, salt)
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        decrypted_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_bytes.decode('utf-8')
    except Exception:
        return "[!] Error: Invalid Password or Tampered Payload Signature"

# --- CORE COMPACT PREMIUM UI ---
UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S-Encryptor | Shivam Singh Vault</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #030305; color: #ff3333; font-family: 'Consolas', 'Share Tech Mono', monospace; padding: 30px 15px; text-align: center; }
        .main { max-width: 600px; margin: auto; border: 2px solid #ff3333; padding: 30px; background: #000; box-shadow: 0 0 35px rgba(255, 51, 51, 0.25); border-radius: 12px; text-align: left; position: relative; }
        .main::before { content: '⚠️ CRYPTO NODE ACTIVE'; position: absolute; top: -10px; right: 20px; background: #ff3333; color: #000; font-size: 11px; padding: 2px 8px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
        .header { text-align: center; border-bottom: 1px dashed #331111; padding-bottom: 15px; margin-bottom: 20px; }
        h2 { margin: 0; color: #fff; text-shadow: 0 0 15px #ff3333; font-size: 24px; letter-spacing: 1px; }
        .subtitle { color: #555; font-size: 11px; margin-top: 5px; letter-spacing: 2px; }
        
        label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 5px; margin-top: 15px; }
        textarea { width: 100%; background: #07070a; border: 1px solid #441111; color: #fff; padding: 14px; border-radius: 6px; resize: vertical; font-size: 14px; line-height: 1.5; outline: none; font-family: inherit; }
        textarea:focus { border-color: #ff3333; box-shadow: 0 0 10px rgba(255, 51, 51, 0.1); }
        
        .pass-wrapper { position: relative; display: flex; align-items: center; }
        input[type="password"], input[type="text"] { width: 100%; background: #07070a; border: 1px solid #441111; color: #fff; padding: 14px; border-radius: 6px; font-size: 14px; outline: none; font-family: inherit; letter-spacing: 2px; }
        input:focus { border-color: #ff3333; }
        .toggle-btn { position: absolute; right: 12px; background: none; border: none; color: #666; cursor: pointer; font-size: 14px; font-weight: bold; text-transform: uppercase; user-select: none; }
        .toggle-btn:hover { color: #ff3333; }
        
        .utility-row { display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-top: 4px; }
        
        .btns { display: flex; gap: 12px; margin-top: 20px; }
        button.action-btn { flex: 1; padding: 14px; font-weight: bold; cursor: pointer; border: none; text-transform: uppercase; border-radius: 6px; font-size: 14px; letter-spacing: 1px; transition: 0.2s; font-family: inherit; }
        .enc-btn { background: #ff3333; color: #000; }
        .enc-btn:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .dec-btn { background: #09090e; color: #ff3333; border: 1px solid #ff3333; }
        .dec-btn:hover { background: #ff33331a; }
        
        .result-container { margin-top: 25px; background: #040d06; border: 1px solid #113819; padding: 18px; border-radius: 8px; position: relative; }
        .result-label { font-size: 11px; color: #00ff66; text-transform: uppercase; font-weight: bold; letter-spacing: 1px; margin-bottom: 8px; display: block; }
        #result { color: #33ff77; word-break: break-all; font-size: 14px; min-height: 24px; white-space: pre-wrap; }
        
        .output-actions { display: flex; gap: 10px; margin-top: 15px; }
        .sub-btn { padding: 8px 15px; font-size: 12px; background: #111; color: #999; border: 1px solid #333; border-radius: 4px; cursor: pointer; font-family: inherit; text-transform: uppercase; font-weight: bold; transition: 0.2s; }
        .sub-btn:hover { color: #fff; border-color: #666; }
        .swap-btn { color: #38bdf8; border-color: #1e3a8a; }
        .swap-btn:hover { color: #fff; border-color: #38bdf8; background: #38bdf811; }
    </style>
</head>
<body>

    <div class="main">
        <div class="header">
            <h2>☣️ SHIVAM SINGH VAULT CORE ☣️</h2>
            <p class="subtitle">AUTHENTICATED SYMMETRIC ENGINE • AES-GCM 256-BIT PROTOCOL</p>
        </div>
        
        <label for="msg">Data Payload (Text or Encrypted Token)</label>
        <textarea id="msg" rows="5" placeholder="Type your raw secret text to encrypt, or paste an active base64 cryptographic token to decrypt..."></textarea>
        <div class="utility-row">
            <span id="char-count">Length: 0 chars</span>
            <span style="cursor:pointer; color:#888;" onclick="clearInput()">[Clear Input]</span>
        </div>
        
        <label for="key">Master Passphrase Key</label>
        <div class="pass-wrapper">
            <input type="password" id="key" placeholder="Enter security... ">
            <button type="button" class="toggle-btn" id="togglePass" onclick="togglePasswordVisibility()">Show</button>
        </div>
        
        <div class="btns">
            <button class="action-btn enc-btn" onclick="executeCrypto('encrypt')">🔒 Encrypt Block</button>
            <button class="action-btn dec-btn" onclick="executeCrypto('decrypt')">🔑 Decrypt Block</button>
        </div>

        <div class="result-container">
            <span class="result-label">📡 Output Console Terminal</span>
            <div id="result">System waiting for operational handshake execution...</div>
            
            <div class="output-actions">
                <button class="sub-btn" onclick="copyResult()">📋 Copy Output</button>
                <button class="sub-btn swap-btn" onclick="swapOutputToInput()">🔄 Move to Input</button>
            </div>
        </div>
    </div>

    <script>
        // Track char changes live
        document.getElementById('msg').addEventListener('input', function() {
            document.getElementById('char-count').innerText = "Length: " + this.value.length + " chars";
        });

        async function executeCrypto(mode) {
            const text = document.getElementById('msg').value.trim();
            const pass = document.getElementById('key').value;
            const resultDiv = document.getElementById('result');
            
            if(!text || !pass) {
                alert("Bhai, payload aur password dono fields fill karna zaroori hai!");
                return;
            }

            resultDiv.innerText = "⏳ Processing cryptographic sequence... Data integrity processing initialized...";

            try {
                // Generates dynamic matching route configuration path automatically
                const targetPath = window.location.pathname.endsWith('/') ? window.location.pathname + 'process' : window.location.pathname + '/process';
                const res = await fetch(targetPath, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text, pass, mode})
                });
                const data = await res.json();
                resultDiv.innerText = data.output;
            } catch(e) {
                resultDiv.innerText = "[!] Pipeline Exception: Connection to authentication node refused.";
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
        }

        function swapOutputToInput() {
            const outText = document.getElementById('result').innerText;
            if(!outText || outText.startsWith("System waiting") || outText.startsWith("⏳") || outText.startsWith("[!]")) {
                alert("Bhai, pehle console mein koi valid output generate hone do!");
                return;
            }
            document.getElementById('msg').value = outText;
            document.getElementById('char-count').innerText = "Length: " + outText.length + " chars";
        }

        function copyResult() {
            const result = document.getElementById('result').innerText;
            if(result.startsWith("System waiting") || result.startsWith("⏳")) return;
            
            navigator.clipboard.writeText(result).then(() => {
                alert("Payload copied to secure clipboard matrix!");
            });
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
        logging.error(f"Vault standard processing crash error: {e}")
        return jsonify({'output': "[!] Error: Processing subquery exception encountered."})

# Local debugging block wrapper alignment
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script17_bp, url_prefix='/script17')
    app.run(debug=True, port=5000)
