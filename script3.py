from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "dist"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# 🏠 HOME PAGE (FILE UPLOAD UI)
@app.route("/")
def home():
    return """
    <h2>🔥 PY → EXE Converter</h2>

    <form action="/convert" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".py" required>
        <br><br>
        <button type="submit">Convert to EXE</button>
    </form>
    """


# ⚙️ CONVERT ENGINE
@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")

    if not file:
        return "No file uploaded"

    file_id = str(uuid.uuid4())
    py_path = os.path.join(UPLOAD_FOLDER, file_id + ".py")

    file.save(py_path)

    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--distpath", OUTPUT_FOLDER,
            py_path
        ], check=True)

        exe_file = None

        for root, dirs, files in os.walk(OUTPUT_FOLDER):
            for f in files:
                if f.endswith(".exe"):
                    exe_file = os.path.join(root, f)
                    break

        if not exe_file:
            return "EXE not generated"

        return send_file(exe_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
