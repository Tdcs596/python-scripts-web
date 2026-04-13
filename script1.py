import sys
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def run(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    
    return f"""
    File received: {filename}
    Saved at: {path}
    """

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No file given")
    else:
        print(run(sys.argv[1]))
