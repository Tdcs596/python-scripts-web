from flask import Flask, request, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return """
    <h2>📂 Upload Python File</h2>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <br><br>
        <button>Upload</button>
    </form>
    """

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    return f"<h3>File uploaded: {file.filename}</h3><p>EXE conversion NOT supported on Render</p>"

if __name__ == "__main__":
    app.run(port=5001)
