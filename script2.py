import os
import subprocess

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "dist"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert(filepath):
    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--distpath", OUTPUT_FOLDER,
            filepath
        ], check=True)

        # find exe
        for file in os.listdir(OUTPUT_FOLDER):
            if file.endswith(".exe"):
                return os.path.join(OUTPUT_FOLDER, file)

        return "❌ EXE not generated"

    except Exception as e:
        return f"❌ Error: {str(e)}"
