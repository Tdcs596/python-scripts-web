from flask import Blueprint, request, send_file
import os
import subprocess
import shutil
import zipfile
import io

script3_bp = Blueprint('script3', __name__)

# Temporary directories
BASE_DIR = "/tmp/py_converter"
SRC_DIR = os.path.join(BASE_DIR, "src")
DIST_DIR = os.path.join(BASE_DIR, "dist")

def setup_dirs():
    for d in [BASE_DIR, SRC_DIR, DIST_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

@script3_bp.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    error_details = ""
    success = False
    
    if request.method == "POST":
        setup_dirs()
        file = request.files.get("file")
        
        if file and file.filename.endswith(".py"):
            filename = file.filename
            filepath = os.path.join(SRC_DIR, filename)
            file.save(filepath)
            
            try:
                # Running PyInstaller with specific flags for Cloud environments
                # --noconfirm aur --clean zaroori hai purane files hatane ke liye
                process = subprocess.run(
                    ["pyinstaller", "--onefile", "--clean", "--distpath", DIST_DIR, filepath],
                    capture_output=True, text=True, timeout=60
                )
                
                if process.returncode == 0:
                    success = True
                    msg = "✅ Conversion Successful! Binary generated."
                else:
                    msg = "❌ PyInstaller Error (See logs below)"
                    error_details = process.stderr
            except Exception as e:
                msg = f"❌ System Error: {str(e)}"
        else:
            msg = "❌ Please upload a valid .py file."

    return f"""
    <div style="font-family: sans-serif; padding: 20px; background: #f4f4f4;">
        <h2>🛠️ Advanced Py to EXE (Linux Binary)</h2>
        <p><b>Note:</b> Render Linux server hai, toh ye <i>Windows .exe</i> nahi, balki <i>Linux Executable</i> banayega.</p>
        
        <form method="POST" enctype="multipart/form-data" style="background:white; padding:20px; border-radius:10px;">
            <input type="file" name="file" accept=".py" required>
            <button type="submit" style="background:#2ecc71; color:white; border:none; padding:10px 20px; cursor:pointer;">Build Binary</button>
        </form>
        
        <br>
        <div style="background:white; padding:15px; border-radius:10px; border-left: 5px solid {'#2ecc71' if success else '#e74c3c'};">
            <b>Status:</b> {msg}
            {f'<br><br><a href="/script3/download" style="background:#3498db; color:white; padding:10px; text-decoration:none; border-radius:5px;">📥 Download Binary</a>' if success else ""}
        </div>

        {f'<div style="margin-top:20px; background:#333; color:#ff7675; padding:15px; overflow-x:auto;"><b>Logs:</b><pre>{error_details}</pre></div>' if error_details else ""}
        
        <br><a href="/">⬅️ Dashboard</a>
    </div>
    """

@script3_bp.route("/download")
def download():
    files = os.listdir(DIST_DIR)
    if files:
        # Latest file uthayega
        return send_file(os.path.join(DIST_DIR, files[-1]), as_attachment=True)
    return "File not found!"
