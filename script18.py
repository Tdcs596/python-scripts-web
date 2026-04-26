from flask import Blueprint, render_template_string, request, send_file
import io
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Blueprint Definition
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

# --- GREEN HACKER MATRIX UI ---
HACKER_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>S-Vault | File Locker</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .vault-container { 
            max-width: 550px; margin: 50px auto; border: 1px solid #00ff00; 
            padding: 40px; background: rgba(0, 15, 0, 0.95); box-shadow: 0 0 25px #00ff0066; 
        }
        h1 { font-size: 20px; letter-spacing: 4px; text-shadow: 0 0 10px #00ff00; }
        .upload-area { border: 1px dashed #00ff00; padding: 30px; margin: 20px 0; transition: 0.3s; }
        .upload-area:hover { background: #001a00; }
        input[type="file"] { color: #00ff00; }
        input[type="password"] { 
            width: 85%; background: #000; border: 1px solid #00ff00; color: #00ff00; 
            padding: 15px; margin-bottom: 25px; text-align: center; outline: none; font-size: 16px;
        }
        .btn-box { display: flex; gap: 15px; justify-content: center; }
        button { 
            flex: 1; padding: 15px; font-weight: bold; cursor: pointer; 
            border: 1px solid #00ff00; background: transparent; color: #00ff00; text-transform: uppercase;
        }
        button:hover { background: #00ff00; color: #000; box-shadow: 0 0 15px #00ff00; }
        .footer { margin-top: 30px; font-size: 10px; color: #004400; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="vault-container">
        <h1>[ SHIVAM-SINGH-VAULT-v18 ]</h1>
        <p style="font-size: 11px;">SECURE FILE SYSTEM : AES-256-BIT</p>
        
        <form action="/script18/process" method="post" enctype="multipart/form-data">
            <div class="upload-area">
                <input type="file" name="file" required>
            </div>
            
            <input type="password" name="password" placeholder="ENTER ACCESS_KEY" required>
            
            <div class="btn-box">
                <button type="submit" name="mode" value="encrypt">LOCK FILE</button>
                <button type="submit" name="mode" value="decrypt">UNLOCK FILE</button>
            </div>
        </form>
        
        <div class="footer">SYSTEM STATUS: READY | ENCRYPTION: ACTIVE</div>
    </div>
</body>
</html>
"""

@script18_bp.route('/')
def index():
    return render_template_string(HACKER_UI)

@script18_bp.route('/process', methods=['POST'])
def process():
    try:
        f = request.files['file']
        pw = request.form['password']
        mode = request.form['mode']
        raw_data = f.read()

        if mode == 'encrypt':
            salt = os.urandom(16)
            iv = os.urandom(16)
            key = get_secure_key(pw, salt)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            secure_data = encryptor.update(raw_data) + encryptor.finalize()
            final_out = salt + iv + secure_data
            out_name = f.filename + ".shivam"
        else:
            salt, iv, payload = raw_data[:16], raw_data[16:32], raw_data[32:]
            key = get_secure_key(pw, salt)
            cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            final_out = decryptor.update(payload) + decryptor.finalize()
            out_name = f.filename.replace(".shivam", "")

        return send_file(io.BytesIO(final_out), as_attachment=True, download_name=out_name)
    except Exception as e:
        return f"<h3>[!] CRITICAL ERROR: {str(e)}</h3>"

