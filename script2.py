from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "dist"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return """
    <h2>🔥 PY → EXE Converter</h2>
    <form method="POST" action="/convert" enctype="multipart/form-data">
        <input type="file" name="file" accept=".py" required>
        <button>Convert & Download EXE</button>
    </form>
    """


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    file_id = str(uuid.uuid4())
    py_path = os.path.join(UPLOAD_FOLDER, file_id + ".py")

    file.save(py_path)

    try:
        # build exe
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--distpath", OUTPUT_FOLDER,
            py_path
        ], check=True)

        exe_name = os.path.splitext(os.path.basename(py_path))[0] + ".exe"

        # find generated exe
        exe_path = None
        for root, dirs, files in os.walk(OUTPUT_FOLDER):
            for f in files:
                if f.endswith(".exe"):
                    exe_path = os.path.join(root, f)
                    break

        if not exe_path:
            return "EXE not found"

        # 👉 DIRECT DOWNLOAD
        return send_file(exe_path, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
