from flask import Flask
import subprocess

app = Flask(__name__)

def run_script(file):
    result = subprocess.run(["python", file], capture_output=True, text=True)
    return result.stdout + result.stderr

@app.route("/")
def home():
    return """
    <h2>Script Control Panel</h2>
    <a href='/s1'>Run Script 1</a><br><br>
    <a href='/s2'>Run Script 2</a>
    """

@app.route("/s1")
def s1():
    output = run_script("script1.py")
    return f"<pre>{output}</pre>"

@app.route("/s2")
def s2():
    output = run_script("script2.py")
    return f"<pre>{output}</pre>"

app.run(host="0.0.0.0", port=10000)
