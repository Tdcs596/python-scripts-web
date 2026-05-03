from flask import Blueprint, render_template_string, request, send_file
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

# --- GREEN HACKER UI ---
GREEN_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>S-Vault | Secure Unlock</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .box { max-width: 500px; margin: 50px auto; border: 1px solid #00ff00; padding: 30px; background: #050505; box-shadow: 0 0 20px #00ff00; display: grid; grid-template-columns: 1fr; grid-gap: 10px; }
        input { width: 100%; background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 12px; margin: 10px 0; outline: none; }
        .btn-row { display: flex; gap: 10px; margin-top: 20px; }
        button { flex: 1; padding: 15px; background: transparent; border: 1px solid #00ff00; color: #00ff00; font-weight: bold; cursor: pointer; }
        button:hover { background: #00ff00; color: #000; }
        .warning { font-size: 10px; color: #555; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="box">
        <h2>[ FILE VAULT RECOVERY ]</h2>
        <form action="/script18/process" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="password" name="password" placeholder="ENTER MASTER PASSWORD" required>
            <div class="btn-row">
                <button type="submit" name="mode" value="encrypt">LOCK FILE</button>
                <button type="submit" name="mode" value="decrypt" style="border-width: 2px;">UNLOCK FILE</button>
            </div>
        </form>
        <div class="warning">S-VAULT V18.2 | AES-256 BINARY SYMMETRIC</div>
    </div>
</body>
</html>
"""

@script18_bp.route('/')
def index():
    return render_template_string(GREEN_UI)

@script18_bp.route('/process', methods=['POST'])
def process():
    try:
        f = request.files['file']
        pw = request.form['password']
        mode = request.form['mode']
        
        # Binary reading is crucial here
        raw_data = f.read()

        if mode == 'encrypt':
            # Encryption logic (Binary safe)
            salt = os.urandom(16)
            iv = os.urandom(16)
            key = get_secure_key(pw, salt)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            secure_payload = encryptor.update(raw_data) + encryptor.finalize()
            
            # Pack everything: Salt(16) + IV(16) + Data
            final_binary = salt + iv + secure_payload
            out_name = f.filename + ".shivam"
            
        else:
            # Decryption logic (Strict Slicing)
            if len(raw_data) < 32:
                return "<h3>[!] ERROR: File too small or not a Vault file!</h3>"
            
            salt = raw_data[:16]
            iv = raw_data[16:32]
            ciphertext = raw_data[32:]
            
            key = get_secure_key(pw, salt)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            
            try:
                final_binary = decryptor.update(ciphertext) + decryptor.finalize()
                out_name = f.filename.replace(".shivam", "")
            except:
                return "<h3>[!] ACCESS DENIED: Password galat hai ya file corrupt hai!</h3>"

        return send_file(
            io.BytesIO(final_binary),
            as_attachment=True,
            download_name=out_name,
            mimetype='application/octet-stream'
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return f"<h3>[!] SYSTEM ERROR: {str(e)}</h3>"

if __name__ == '__main__':
    script18_bp.run(debug=True)
