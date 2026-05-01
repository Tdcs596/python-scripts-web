from flask import Blueprint, render_template_string

script19_bp = Blueprint('script19', __name__)

OMEGA_X_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA X-TREME | Shivam Singh</title>
    <style>
        :root { --neon: #00ff00; --glow: #00ff0055; }
        body { background: #000; color: var(--neon); font-family: 'Segoe UI', 'Consolas', monospace; margin: 0; overflow: hidden; }
        
        /* THE SCI-FI GRID BACKGROUND */
        body::before {
            content: ''; position: absolute; width: 200%; height: 200%;
            background-image: linear-gradient(var(--glow) 1px, transparent 1px), linear-gradient(90deg, var(--glow) 1px, transparent 1px);
            background-size: 50px 50px; transform: perspective(500px) rotateX(60deg);
            bottom: -50%; left: -50%; z-index: -1; animation: moveGrid 10s linear infinite;
        }
        @keyframes moveGrid { from { transform: perspective(500px) rotateX(60deg) translateY(0); } to { transform: perspective(500px) rotateX(60deg) translateY(50px); } }

        /* HOLOGRAPHIC CONTAINER */
        .hologram { height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: space-around; padding: 20px; box-sizing: border-box; }
        
        /* ADVANCED REACTOR CORE */
        .core-wrap { position: relative; width: 250px; height: 250px; }
        .ring { position: absolute; border: 2px solid var(--neon); border-radius: 50%; top: 50%; left: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 20px var(--neon); }
        .r1 { width: 240px; height: 240px; border-style: dotted; animation: spin 20s linear infinite; }
        .r2 { width: 200px; height: 200px; border-style: dashed; animation: spin-rev 10s linear infinite; }
        .r3 { width: 160px; height: 160px; border-width: 4px; animation: pulse 2s ease-in-out infinite; }
        
        @keyframes spin { from { transform: translate(-50%, -50%) rotate(0deg); } to { transform: translate(-50%, -50%) rotate(360deg); } }
        @keyframes spin-rev { from { transform: translate(-50%, -50%) rotate(360deg); } to { transform: translate(-50%, -50%) rotate(0deg); } }
        @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; } 50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; } }

        /* DATA PANELS */
        .panel { position: absolute; border-left: 5px solid var(--neon); background: rgba(0,255,0,0.05); padding: 15px; width: 250px; backdrop-filter: blur(5px); }
        .top-left { top: 20px; left: 20px; }
        .bottom-right { bottom: 20px; right: 20px; }
        
        #cmd-display { font-size: 1.5rem; text-shadow: 0 0 10px var(--neon); color: #fff; height: 40px; }
        .visualizer { display: flex; gap: 5px; height: 30px; align-items: flex-end; }
        .bar { width: 4px; background: var(--neon); animation: dance 1s infinite alternate; }
        @keyframes dance { from { height: 5px; } to { height: 30px; } }

        .scan-line { position: absolute; width: 100%; height: 2px; background: var(--neon); top: 0; box-shadow: 0 0 15px var(--neon); animation: scan 4s linear infinite; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body>
    <div class="scan-line"></div>
    <div class="hologram">
        <div class="panel top-left">
            <div>BIOMETRIC: SHIVAM_SINGH</div>
            <div>STATUS: <span id="sys-status">SECURE</span></div>
            <div id="clock">00:00:00</div>
            <div class="visualizer" id="viz"></div>
        </div>

        <div class="core-wrap" onclick="initOmega()">
            <div class="ring r1"></div>
            <div class="ring r2"></div>
            <div class="ring r3"></div>
            <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-weight:bold; letter-spacing:3px;">OMEGA-X</div>
        </div>

        <div id="cmd-display">TAP CORE TO INITIALIZE</div>

        <div class="panel bottom-right">
            <div>CORE: V19.9-ULTRA</div>
            <div>LOC: MIRA_BHAYANDAR</div>
            <div style="font-size: 10px; color: #666; margin-top: 10px;">Say: "Analyze System", "Search [X]", "Security Protocol"</div>
        </div>
    </div>

    <script>
        const cmdDisplay = document.getElementById('cmd-display');
        const clock = document.getElementById('clock');
        const viz = document.getElementById('viz');

        // Create Bars for Visualizer
        for(let i=0; i<15; i++) {
            let bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.animationDelay = (i * 0.1) + 's';
            viz.appendChild(bar);
        }

        setInterval(() => { clock.innerText = new Date().toLocaleTimeString(); }, 1000);

        function speak(text) {
            const utter = new SpeechSynthesisUtterance(text);
            utter.pitch = 0.7; utter.rate = 1.0;
            window.speechSynthesis.speak(utter);
        }

        function initOmega() {
            const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
            const rec = new SpeechRecognition();
            rec.lang = 'en-US';
            rec.continuous = true;

            rec.onstart = () => {
                cmdDisplay.innerText = "LISTENING_FOR_COMMANDS";
                speak("Neural link established. Omega X-Treme is at your service, Shivam Sir.");
            };

            rec.onresult = (event) => {
                const transcript = event.results[event.results.length - 1][0].transcript.toLowerCase();
                cmdDisplay.innerText = transcript.toUpperCase();
                handleAction(transcript);
            };

            rec.onend = () => rec.start();
            rec.start();
        }

        function handleAction(cmd) {
            let reply = "";
            if (cmd.includes("hello")) reply = "Greetings Sir. Systems are running at peak performance.";
            else if (cmd.includes("analyze system")) reply = "Scanning Scripts 1 to 18. All modules are clean. No intrusion detected.";
            else if (cmd.includes("security protocol")) reply = "Executing Black-Hat protection. Rotating AES-256 keys now.";
            else if (cmd.includes("search for")) {
                let q = cmd.split("search for")[1];
                reply = "Scanning global data for " + q;
                window.open("https://google.com/search?q=" + q);
            }
            else if (cmd.includes("open youtube")) { reply = "Opening Media Interface."; window.open("https://youtube.com"); }
            else if (cmd.includes("time")) reply = "The system clock shows " + new Date().toLocaleTimeString();

            if(reply) speak(reply);
        }
    </script>
</body>
</html>
"""

@script19_bp.route('/')
def index():
    return render_template_string(OMEGA_X_UI)

