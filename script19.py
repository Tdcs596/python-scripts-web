from flask import Blueprint, render_template_string

script19_bp = Blueprint('script19', __name__)

# --- ELITE HACKER HUD UI ---
JARVIS_ELITE_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS ELITE | Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Consolas', monospace; text-align: center; margin: 0; overflow: hidden; }
        
        /* THE HUD BOX */
        .hud-frame { border: 2px solid #00ff00; height: 90vh; margin: 20px; position: relative; background: radial-gradient(circle, #001a00 0%, #000 100%); }
        
        /* ROTATING REACTOR */
        .reactor-container { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }
        .ring { border: 2px solid #00ff00; border-radius: 50%; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 20px #00ff00; }
        .r1 { width: 180px; height: 180px; border-style: dashed; animation: spin 10s linear infinite; }
        .r2 { width: 140px; height: 140px; border-style: double; animation: spin-rev 5s linear infinite; }
        .core-text { color: #fff; font-weight: bold; font-size: 14px; text-shadow: 0 0 10px #00ff00; }

        @keyframes spin { from { transform: translate(-50%, -50%) rotate(0deg); } to { transform: translate(-50%, -50%) rotate(360deg); } }
        @keyframes spin-rev { from { transform: translate(-50%, -50%) rotate(360deg); } to { transform: translate(-50%, -50%) rotate(0deg); } }

        /* DATA BOXES */
        .data-panel { position: absolute; border: 1px solid #004400; padding: 10px; font-size: 12px; text-align: left; background: rgba(0,0,0,0.8); }
        .top-left { top: 20px; left: 20px; width: 200px; }
        .bottom-right { bottom: 20px; right: 20px; width: 250px; }
        
        #console { color: #00ff00; height: 100px; overflow: hidden; margin-top: 10px; }
        .pulse-mic { position: absolute; bottom: 50px; left: 50%; transform: translateX(-50%); 
                     background: #00ff00; color: #000; padding: 15px 40px; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="hud-frame">
        <div class="data-panel top-left">
            <div>SYSTEM: ONLINE</div>
            <div>USER: SHIVAM SINGH</div>
            <div id="clock"></div>
            <div id="console">>> Initializing neural links...</div>
        </div>

        <div class="reactor-container">
            <div class="ring r1"></div>
            <div class="ring r2"></div>
            <div class="core-text" id="status">JARVIS</div>
        </div>

        <div class="data-panel bottom-right">
            <div>VULNERABILITY: 0%</div>
            <div>ENCRYPTION: AES-256 ACTIVE</div>
            <div style="color: #666; font-size: 10px;">Commands: "Open Google", "Time", "Search [X]", "System Status"</div>
        </div>

        <button class="pulse-mic" onclick="initJarvis()">INITIALIZE VOICE CONTROL</button>
    </div>

    <script>
        const statusText = document.getElementById('status');
        const consoleLog = document.getElementById('console');

        // Real-time Clock
        setInterval(() => { document.getElementById('clock').innerText = "TIME: " + new Date().toLocaleTimeString(); }, 1000);

        function speak(text) {
            const utter = new SpeechSynthesisUtterance(text);
            utter.rate = 1.1; utter.pitch = 0.8;
            window.speechSynthesis.speak(utter);
        }

        function initJarvis() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = true; // Ye Jarvis ko "always listening" mode mein dalega
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                statusText.innerText = "LISTENING";
                consoleLog.innerHTML += "<br>> Voice Engine Started...";
                speak("System initialized. I am online and ready, Shivam Sir.");
            };

            recognition.onresult = (event) => {
                const current = event.resultIndex;
                const transcript = event.results[current][0].transcript.toLowerCase();
                processEliteCommand(transcript);
            };

            recognition.start();
        }

        function processEliteCommand(cmd) {
            consoleLog.innerHTML = "> detected: " + cmd;
            let response = "";

            if (cmd.includes("hello") || cmd.includes("jarvis")) {
                response = "At your service, Shivam Sir.";
            } 
            else if (cmd.includes("time")) {
                response = "The current time is " + new Date().toLocaleTimeString();
            }
            else if (cmd.includes("open google")) {
                response = "Opening Google Mainframe.";
                window.open("https://www.google.com", "_blank");
            }
            else if (cmd.includes("search for")) {
                let query = cmd.split("search for")[1];
                response = "Searching the global database for " + query;
                window.open("https://www.google.com/search?q=" + query, "_blank");
            }
            else if (cmd.includes("system status")) {
                response = "All modules from Script 1 to 18 are fully operational. Encryption levels optimal.";
            }
            else if (cmd.includes("who is shivam")) {
                response = "Shivam Singh is the architect of the Omega Dashboard and my creator.";
            }

            if(response !== "") {
                speak(response);
                consoleLog.innerHTML += "<br>> Jarvis: " + response;
            }
        }
    </script>
</body>
</html>
"""

@script19_bp.route('/')
def index():
    return render_template_string(JARVIS_ELITE_UI)

