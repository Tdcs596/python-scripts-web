from flask import Blueprint, request, send_file
import os
import subprocess
import shutil
import time
import io

# Blueprint for app.py
script3_bp = Blueprint('script3', __name__)

# Temporary folder for conversion
TEMP_DIR = "/tmp/exe_build"

def convert_to_exe(script_name, script_content):
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    
    script_path = os.path.join(TEMP_DIR, script_name)
    
    # 1. Script file write karna
    with open(script_path, "w") as f:
        f.write(script_content)
    
    try:
        # 2. PyInstaller Run karna (Onefile mode)
        # Note: Render Linux hai, toh ye Linux executable banayega. 
        # Agar Windows pe chalana hai toh ise Windows machine pe run karna padta hai.
        subprocess.run([
            "pyinstaller", 
            "--onefile", 
            "--clean",
            "--workpath", os.path.join(TEMP_DIR, "build"),
            "--distpath", os.path.join(TEMP_DIR, "dist"),
            script_path
        ], check=True)
        
        exe_path = os.path.join(TEMP_DIR, "dist", script_name.replace(".py", ""))
        
        if os.path.exists(exe_path):
            return exe_path
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@script3_bp.route("/", methods=["GET", "POST"])
def index():
    msg = ""
    download_link = False
    
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename.endswith(".py"):
            content = file.read().decode("utf-8")
            exe_file = convert_to_exe(file.filename, content)
            
            if exe_file:
                download_link = True
                msg = "✅ Conversion Successful! Download your file below."
            else:
                msg = "❌ Conversion Failed (PyInstaller Error)."
        else:
            msg = "❌ Please upload a valid .py file."

    return f"""
    <div style="font-family: sans-serif; padding: 20px;">
        <h2>🛠️ Python to Executable Converter</h2>
        <p style="color: red;"><b>Note:</b> Render Linux hai, isliye ye Linux Executable banayega.</p>
        
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".py" style="padding:10px;" required>
            <button type="submit" style="padding:10px; background: #e67e22; color:white; border:none; cursor:pointer;">Convert to EXE</button>
        </form>
        
        <br>
        <p>{msg}</p>
        
        {f'<a href="/script3/download" style="padding:10px; background:green; color:white; text-decoration:none;">📥 Download File</a>' if download_link else ""}
        
        <br><br>
        <a href="/">⬅️ Back to Dashboard</a>
    </div>
    """

@script3_bp.route("/download")
def download():
    # Dist folder se file uthana
    files = os.listdir(os.path.join(TEMP_DIR, "dist"))
    if files:
        target = os.path.join(TEMP_DIR, "dist", files[0])
        return send_file(target, as_attachment=True)
    return "File not found."
