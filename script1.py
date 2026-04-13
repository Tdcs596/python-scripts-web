from flask import Flask, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🏠 HOME PAGE (UI)
@app.route("/")
def home():
    return """
    <h2>🚀 Python File Upload Tool</h2>

    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".py" required>
        <br><br>
        <button type="submit">Upload File</button>
    </form>
    """


# 📤 FILE UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return "<h3>❌ No file selected</h3>"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return f"""
    <h3>✅ File Uploaded Successfully</h3>
    <p>Filename: {file.filename}</p>
    <p>Saved to server</p>
    """


# 🔥 RUN (IMPORTANT)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10001))  # different port from app.py
    app.run(host="0.0.0.0", port=port)
