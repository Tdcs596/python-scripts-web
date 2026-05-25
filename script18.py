from flask import Blueprint, render_template_string, request, send_file, jsonify
import io
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging

script18_bp = Blueprint('script18', __name__)

def get_secure_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# --- ADVANCED MATRIX HACKER UI ---
GREEN_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>S-Vault | Secure File Crypt</title>
    <style>
        body { background: #020402; color: #00ff66; font-family: 'Consolas', 'Courier New', monospace; text-align: center; padding: 30px 15px; }
        .box { max-width: 600px; margin: 40px auto; border: 2px solid #00ff66; padding: 35px; background: #000; box-shadow: 0 0 30px rgba(0, 255, 102, 0.2); border-radius: 12px; position: relative; text-align: left; }
        .box::before { content: '🔒 AES-GCM HARDENED'; position: absolute; top: -11px; right: 20px; background: #00ff66; color: #000; font-size: 11px; padding: 2px 10px; font-weight: bold; border-radius: 4px; letter-spacing: 1px; }
        h2 { text-align: center; margin-top: 0; color: #fff; text-shadow: 0 0 15px #00ff66; font-size: 24px; letter-spacing: 1px; margin-bottom: 25px; }
        
        label { font-size: 11px; color: #00aa44; text-transform: uppercase; letter-spacing: 1.5px; display: block; margin-top: 15px; margin-bottom: 5px; font-weight: bold; }
        input[type="file"] { width: 100%; background: #050a05; border: 1px dashed #00ff66; color: #fff; padding: 15px; border-radius: 6px; outline: none; cursor: pointer; }
        input[type="password"] { width: 100%; background: #050a05; border: 1px solid #005522; color: #fff; padding: 14px; margin-bottom: 5px; outline: none; border-radius: 6px; font-size: 15px; letter-spacing: 3px; font-weight: bold; }
        input[type="password"]:focus { border-color: #00ff66; box-shadow: 0 0 10px rgba(0, 255, 102, 0.1); }
        
        .btn-row { display: flex; gap: 15px; margin-top: 25px; }
        button { flex: 1; padding: 15px; background: transparent; border: 1px solid #00ff66; color: #00ff66; font-weight: bold; cursor: pointer; border-radius: 6px; text-transform: uppercase; font-size: 14px; letter-spacing: 1px; transition: 0.2s; font-family: inherit; }
        button:hover { background: #00ff66; color: #000; box-shadow: 0 0 15px #00ff66; transform: translateY(-1px); }
        .dec-btn { border-width: 2px; border-color: #00ffaa; color: #00ffaa; }
        
        #status-console { margin-top: 20px; padding: 12px; border-radius: 6px; background: #050505; border: 1px solid #222; font-size: 13px; display: none; text-align: center; }
        .error-msg { color: #ff3333; border-color: #551111; background: #140505; }
        .success-msg { color: #33ff77; border-color: #115522; background: #051408; }
        .warning { font-size: 11px; color: #444; margin-top: 20px; text-align: center; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>[ SHIVAM SINGH BINARY FILE VAULT ]</h2>
        
        <form id="vaultForm">
            <label for="fileInput">Target Binary Payload File</label>
            <input type="file" id="fileInput" name="file" required>
            
            <label for="passInput">Master Key Passphrase</label>
            <input type="password" id="passInput" name="password" placeholder="ENTER SYMMETRIC PASSWORD..." required>
            
            <div class="btn-row">
                <button type="button" onclick="submitVault('encrypt')">🔒 Lock File</button>
                <button type="button" class="dec-btn" onclick="submitVault('decrypt')">🔑 Unlock File</button>
            </div>
        </form>
        
        <div id="status-console">Console operational standby...</div>
        
        <div class="warning">S-VAULT ENGINE v18.2 • MILITARY GRAD AES-256 GCM INTEGRITY</div>
    </div>

    <script>
        async function submitVault(mode) {
            const fileInput = document.getElementById('fileInput');
            const passInput = document.getElementById('passInput');
            const consoleBox = document.getElementById('status-console');
            
            if(!fileInput.files[0] || !passInput.value) {
                alert("Bhai, file aur password dono fill karna zaroori hai!");
                return;
            }

            consoleBox.className = "";
            consoleBox.style.display = "block";
            consoleBox.style.color = "#eab308";
            consoleBox.innerText = "⏳ Cryptographic streaming initialized... Processing file buffers...";

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('password', passInput.value);
            formData.append('mode', mode);

            try {
                // Generates endpoint handling sub-path configuration dynamically
                const targetPath = window.location.pathname.endsWith('/') ? window.location.pathname + 'process' : window.location.pathname + '/process';
                const response = await fetch(targetPath, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.message || "Cryptographic authentication failed.");
                }

                // Check if it's returning a file download blob
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    const data = await response.json();
                    if(data.status === "error") throw new Error(data.message);
                }

                // Trigger direct payload binary blob download stream download trigger
                const blob = await response.blob();
                const disposition = response.headers.get('Content-Disposition');
                let filename = mode === 'encrypt' ? fileInput.files[0].name + ".shivam" : fileInput.files[0].name.replace(".shivam", "");
                
                if (disposition && disposition.indexOf('filename=') !== -1) {
                    filename = disposition.split('filename=')[1].replaceAll('"', '');
                }

                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();

                consoleBox.className = "success-msg";
                consoleBox.innerText = `✅ Process Complete! File safely ${mode === 'encrypt' ? 'locked' : 'unlocked'} and downloaded.`;
            } catch (error) {
                consoleBox.className = "error-msg";
                consoleBox.innerText = `❌ [!] ACCESS DENIED: ${error.message}`;
            }
        }
    </script>
</body>
</html>
"""

@script18_bp.route('/')
def index():
    return render_template_string(GREEN_UI)

@script18_bp.route('/process', methods=['POST'])
def process():
    try:
        if 'file' not in request.files or 'password' not in request.form or 'mode' not in request.form:
            return jsonify({"status": "error", "message": "Missing parameters inside extraction stream"}), 400
            
        f = request.files['file']
        pw = request.form['password']
        mode = request.form['mode']
        
        raw_data = f.read()
        if len(raw_data) == 0:
            return jsonify({"status": "error", "message": "Bhai, file khali hai (0 bytes)!"}), 400

        if mode == 'encrypt':
            salt = os.urandom(16)
            iv = os.urandom(12)  # Recommended 12 bytes IV block structure for AES-GCM
            key = get_secure_key(pw, salt)
            
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            
            secure_payload = encryptor.update(raw_data) + encryptor.finalize()
            tag = encryptor.tag  # CRITICAL STRUCTURAL FIX: Extracting GCM tag
            
            # Pack Everything: Salt(16) + IV(12) + Tag(16) + Encrypted Byte Stream Data
            final_binary = salt + iv + tag + secure_payload
            out_name = f.filename + ".shivam"
            
        else:
            # Slicing validation: Minimum threshold = Salt(16) + IV(12) + Tag(16) = 44 Bytes
            if len(raw_data) < 44:
                return jsonify({"status": "error", "message": "File size too short! Definitively not a secure Shivam Vault (.shivam) file."}), 400
            
            salt = raw_data[:16]
            iv = raw_data[16:28]
            tag = raw_data[28:44]
            ciphertext = raw_data[44:]
            
            key = get_secure_key(pw, salt)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            try:
                final_binary = decryptor.update(ciphertext) + decryptor.finalize()
                out_name = f.filename.replace(".shivam", "")
            except Exception:
                return jsonify({"status": "error", "message": "Incorrect Password or Tampered Payload Block Schema."}), 400

        return send_file(
            io.BytesIO(final_binary),
            as_attachment=True,
            download_name=out_name,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        logging.error(f"Global file pipeline exception: {e}")
        return jsonify({"status": "error", "message": f"System processing error: {str(e)}"}), 500

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script18_bp, url_prefix='/script18')
    app.run(debug=True, port=5000)
