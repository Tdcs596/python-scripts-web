from flask import Blueprint, render_template_string, request, jsonify

script19_bp = Blueprint('script19', __name__)

# --- JARVIS GREEN UI ---
JARVIS_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS v19 | Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; overflow: hidden; }
        .jarvis-circle { 
            width: 200px; height: 200px; border: 5px solid #00ff00; border-radius: 50%; 
            margin: 50px auto; box-shadow: 0 0 50px #00ff00; animation: pulse 2s infinite; 
            display: flex; align-items: center; justify-content: center; font-weight: bold;
        }
        @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
        .terminal { background: #050505; border: 1px solid #00ff00; width: 80%; margin: auto; padding: 20px; height: 150px; overflow-y: auto; text-align: left; font-size: 14px; }
        button { background: #00ff00; color: #000; border: none; padding: 15px 30px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>SYSTEM: JARVIS V19 ACTIVE</h1>
    <div class="jarvis-circle" id="status">IDLE</div>
    
    <div class="terminal" id="log">>> Waiting for command...</div>
    
    <button onclick="startListening()">ACTIVATE MIC</button>

    <script>
        const logBox = document.getElementById('log');
        const status = document.getElementById('status');

        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 0.8; // Deep hacker voice
            window.speechSynthesis.speak(utterance);
        }

        function startListening() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                status.innerText = "LISTENING";
                status.style.boxShadow = "0 0 80px #ff0000";
            };

            recognition.onresult = (event) => {
                const command = event.results[0][0].transcript.toLowerCase();
                logBox.innerHTML += `<br>> User: ${command}`;
                processCommand(command);
            };

            recognition.onerror = () => {
                status.innerText = "ERROR";
            };

            recognition.onend = () => {
                status.innerText = "IDLE";
                status.style.boxShadow = "0 0 50px #00ff00";
            };

            recognition.start();
        }

        function processCommand(cmd) {
            let response = "I am not programmed for this command yet, Shivam Sir.";
            
            if(cmd.includes("hello") || cmd.includes("jarvis")) {
                response = "Hello Shivam Sir. Systems are optimal. How can I help you today?";
            } else if(cmd.includes("time")) {
                response = "The current time is " + new Date().toLocaleTimeString();
            } else if(cmd.includes("who are you")) {
                response = "I am JARVIS, a private AI assistant developed by Shivam Singh.";
            } else if(cmd.includes("status")) {
                response = "All server nodes are active. Script 1 to 18 are fully functional.";
            }

            logBox.innerHTML += `<br><span style="color:white;">>> JARVIS: ${response}</span>`;
            speak(response);
        }
    </script>
</body>
</html>
"""

@script19_bp.route('/')
def index():
    return render_template_string(JARVIS_UI)
