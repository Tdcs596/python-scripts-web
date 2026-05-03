from flask import Blueprint, render_template_string, request, jsonify
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging
import asyncio

script17_bp = Blueprint('script17', __name__)

# --- CORE LOGIC (SHIVAM SINGH PRIVATE) ---
def get_private_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def shivam_encrypt(text, pkey):
    salt = os.urandom(16)
    key = get_private_key(pkey, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    token = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(salt + iv + token).decode('utf-8')

def shivam_decrypt(token, pkey):
    try:
        data = base64.b64decode(token)
        salt, iv, secret = data[:16], data[16:32], data[32:]
        key = get_private_key(pkey, salt)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return (decryptor.update(secret) + decryptor.finalize()).decode('utf-8')
    except:
        return "[!] Error: Invalid Password or Corrupt Payload"

# --- CUSTOM UI ---
UI = """
<!DOCTYPE html>
<html>
<head>
    <title>S-Encryptor | Shivam Singh</title>
    <style>
        body { background: #050505; color: #ff0000; font-family: 'Consolas', monospace; text-align: center; padding: 20px; }
        .main { max-width: 500px; margin: auto; border: 2px solid #ff0000; padding: 30px; background: #000; box-shadow: 0 0 30px #ff000055; border-radius: 10px; display: grid; grid-template-columns: 1fr; grid-gap: 10px; }
        textarea, input { width: 100%; background: #111; border: 1px solid #ff0000; color: #fff; padding: 12px; margin: 10px 0; border-radius: 5px; }
        .btns { display: flex; gap: 10px; justify-content: center; }
        button { flex: 1; padding: 15px; font-weight: bold; cursor: pointer; border: none; text-transform: uppercase; }
        .enc-btn { background: #ff0000; color: #000; }
        .dec-btn { background: #222; color: #ff0000; border: 1px solid #ff0000; }
        #result { margin-top: 20px; color: #00ff00; word-break: break-all; border-top: 1px solid #333; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="main">
        <h2 style="margin-top:0;">☣️ SHIVAM SINGH VAULT ☣️</h2>
        <p style="font-size:10px; color:#666;">OFFLINE SYMMETRIC ENCRYPTION ENGINE</p>
        
        <textarea id="msg" rows="4" placeholder="Enter Message..."></textarea>
        <input type="password" id="key" placeholder="Enter Master Password">
        
        <div class="btns">
            <button class="enc-btn" onclick="run('encrypt')">Encrypt</button>
            <button class="dec-btn" onclick="run('decrypt')">Decrypt</button>
        </div>

        <div id="result">Waiting for input...</div>
    </div>

    <script>
        async function run(mode) {
            const text = document.getElementById('msg').value;
            const pass = document.getElementById('key').value;
            if(!text || !pass) return alert("Fill all fields!");

            const res = await fetch(window.location.pathname + 'process', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, pass, mode})
            });
            const data = await res.json();
            document.getElementById('result').innerText = data.output;
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
        data = request.json
        mode, text, pkey = data.get('mode'), data.get('text'), data.get('pass')
        output = shivam_encrypt(text, pkey) if mode == 'encrypt' else shivam_decrypt(text, pkey)
        return jsonify({'output': output})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'output': "[!] Error: Invalid Password or Corrupt Payload"})

if __name__ == '__main__':
    script17_bp.run(debug=True)
