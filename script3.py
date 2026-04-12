from flask import Flask, request, send_file
import os
import uuid
import subprocess

app = Flask(__name__)

UPLOAD = "uploads"
DIST = "dist"

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(DIST, exist_ok=True)


@app.route("/")
def home():
    return """
    <h2>PY → EXE Converter</h2>
    <form method="POST" action="/convert" enctype="multipart/form-data">
        <input type="file" name="file" accept=".py" required>
        <button>Convert</button>
    </form>
    """


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]

    uid = str(uuid.uuid4())
    py_path = os.path.join(UPLOAD, uid + ".py")

    file.save(py_path)

    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--distpath", DIST,
            py_path
        ], check=True)

        exe_file = None

        for root, dirs, files in os.walk(DIST):
            for f in files:
                if f.endswith(".exe"):
                    exe_file = os.path.join(root, f)
                    break

        if not exe_file:
            return "EXE not found"

        return send_file(exe_file, as_attachment=True)

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
