from flask import Blueprint, render_template_string, request, send_file
import io
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

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

# --- ADVANCED UI ---
FILE_VAULT_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Universal Vault | Shivam Singh</title>
    <style>
        body { background: #000; color: #ff0000; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .container { max-width: 550px; margin: auto; border: 2px solid #ff0000; padding: 30px; background: #0a0a0a; box-shadow: 0 0 25px #ff000044; border-radius: 12px; }
        .file-input { background: #111; border: 2px dashed #444; color: #888; padding: 30px; width: 90%; margin: 20px 0; cursor: pointer; transition: 0.3s; }
        .file-input:hover { border-color: #ff0000; color: #fff; }
        input[type="password"] { width: 85%; background: #000; border: 1px solid #ff0000; color: #fff; padding: 15px; margin-bottom: 20px; font-size: 16px; text-align: center; }
        .action-btns { display: flex; gap: 15px; justify-content: center; }
        button { flex: 1; padding: 18px; font-weight: bold; cursor: pointer; border: none; font-size: 14px; letter-spacing: 1px; }
        .lock-btn { background: #ff0000; color: #000; }
        .unlock-btn { background: #000; color: #ff0000; border: 1px solid #ff0000; }
        .status { margin-top: 20px; font-size: 11px; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="letter-spacing: 3px;">☣️ SHIVAM UNIVERSAL LOCKER ☣️</h2>
        <p style="color: #666; font-size: 12px;">ENCRYPT ANY FILE TYPE (NO SIZE LIMIT ON LOCAL)</p>
        
        <form action="/script18/handle" method="post" enctype="multipart/form-data">
            <input type="file" name="file" class="file-input" required>
            <input type="password" name="password" placeholder="ENTER PRIVATE KEY" required>
            
            <div class="action-btns">
                <button type="submit" name="op" value="lock" class="lock-btn">LOCK FILE</button>
                <button type="submit" name="op" value="unlock" class="unlock-btn">UNLOCK FILE</button>
            </div>
        </form>
        
        <div class="status">
            * Files are processed in memory and never stored on server.
        </div>
    </div>
</body>
</html>
"""

@script18_bp.route('/')
def index():
    return render_template_string(FILE_VAULT_UI)

@script18_bp.route('/handle', methods=['POST'])
def handle():
    f = request.files['file']
    pw = request.form['password']
    op = request.form['op']
    
    raw_data = f.read()
    
    if op == 'lock':
        # Universal Encryption
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = get_secure_key(pw, salt)
        
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        secure_data = encryptor.update(raw_data) + encryptor.finalize()
        
        # Package: Salt + IV + Encrypted Bytes
        processed_data = salt + iv + secure_data
        out_name = f.filename + ".shivam"
    else:
        # Universal Decryption
        try:
            salt = raw_data[:16]
            iv = raw_data[16:32]
            payload = raw_data[32:]
            key = get_secure_key(pw, salt)
            
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            processed_data = decryptor.update(payload) + decryptor.finalize()
            out_name = f.filename.replace(".shivam", "")
        except:
            return "<h3>[!] ERROR: Galat Key ya File Corrupt hai!</h3>"

    return send_file(
        io.BytesIO(processed_data),
        as_attachment=True,
        download_name=out_name,
        mimetype='application/octet-stream'
    )
