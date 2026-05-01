from flask import Blueprint, render_template_string

script19_bp = Blueprint('script19', __name__)

GHOST_AI_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA-X GHOST | SHIVAM SINGH</title>
    <style>
        :root { --main-color: #00ff00; --bg-color: #000800; --accent: #ff0000; }
        body { background: var(--bg-color); color: var(--main-color); font-family: 'Share Tech Mono', monospace; margin: 0; overflow: hidden; }
        
        /* GHOST LAYER BACKGROUND */
        #ghost-canvas { position: absolute; top: 0; left: 0; z-index: -1; filter: blur(2px); opacity: 0.3; }

        .hud-wrapper { height: 100vh; display: flex; flex-direction: column; justify-content: space-between; padding: 20px; box-sizing: border-box; border: 1px solid #003300; }
        
        /* NEURAL CORE ANIMATION */
        .core-container { position: relative; width: 300px; height: 300px; margin: auto; display: flex; align-items: center; justify-content: center; }
        .neural-ring { position: absolute; border-radius: 50%; border: 2px solid var(--main-color); box-shadow: 0 0 30px var(--main-color); }
        .ring-1 { width: 280px; height: 280px; border-style: dashed; animation: rotate 15s linear infinite; }
        .ring-2 { width: 220px; height: 220px; border-style: double; animation: rotate-rev 8s linear infinite; }
        .ring-3 { width: 160px; height: 160px; border-width: 5px; animation: pulse 1s infinite; }

        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotate-rev { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
        @keyframes pulse { 0%, 100% { box-shadow: 0 0 20px var(--main-color); } 50% { box-shadow: 0 0 60px var(--main-color); } }

        /* DATA LOGS & SPECTRUM */
        .log-panel { width: 300px; background: rgba(0,20,0,0.8); border: 1px solid var(--main-color); padding: 10px; font-size: 11px; max-height: 200px; overflow: hidden; }
        #live-transcript { font-size: 1.8rem; text-align: center; color: #fff; text-shadow: 0 0 15px var(--main-color); margin-bottom: 20px; min-height: 40px; }
        .visualizer { display: flex; gap: 3px; height: 50px; align-items: center; justify-content: center; }
        .bar { width: 5px; height: 10px; background: var(--main-color); animation: ghost-wave 0.5s infinite alternate; }

        @keyframes ghost-wave { from { height: 5px; opacity: 0.5; } to { height: 40px; opacity: 1; } }
        .btn-ghost { background: transparent; border: 1px solid var(--main-color); color: var(--main-color); padding: 15px 40px; cursor: pointer; font-weight: bold; letter-spacing: 5px; transition: 0.3s; }
        .btn-ghost:hover { background: var(--main-color); color: #000; box-shadow: 0 0 50px var(--main-color); }
    </style>
</head>
<body>
    <canvas id="ghost-canvas"></canvas>
    
    <div class="hud-wrapper">
        <div style="display: flex; justify-content: space-between; font-size: 12px;">
            <div>LOCATION: MIRA_BHAYANDAR // IND</div>
            <div id="sys-timer">STABLE</div>
            <div>UID: SHIVAM_GHOST_99</div>
        </div>

        <div class="core-container">
            <div class="neural-ring ring-1"></div>
            <div class="neural-ring ring-2"></div>
            <div class="neural-ring ring-3"></div>
            <div style="z-index: 10; font-size: 20px; font-weight: bold;">GHOST</div>
        </div>

        <div id="live-transcript">SYSTEM: ENCRYPTED</div>

        <div class="visualizer" id="spectrum"></div>

        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
            <div class="log-panel" id="log-box">>> Ghost Node Initialized...</div>
            <button class="btn-ghost" onclick="igniteGhost()">ENGAGE LINK</button>
            <div class="log-panel" style="text-align: right;">
                ACTIVE SCRIPTS: 1-18<br>
                AUTH: SHIVAM SINGH<br>
                LEVEL: SOVEREIGN
            </div>
        </div>
    </div>

    <script>
        const transcriptDiv = document.getElementById('live-transcript');
        const logBox = document.getElementById('log-box');
        const spectrum = document.getElementById('spectrum');

        // Create bars
        for(let i=0; i<20; i++) { spectrum.innerHTML += `<div class="bar" style="animation-delay: ${i*0.05}s"></div>`; }

        function ghostSpeak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            // GHOST VOICE: Deep, slow, and robotic
            utter.pitch = 0.05; 
            utter.rate = 0.85;
            utter.volume = 1;
            synth.speak(utter);
        }

        function igniteGhost() {
            const SpeechRec = window.webkitSpeechRecognition || window.SpeechRecognition;
            const rec = new SpeechRec();
            rec.lang = 'en-US';
            rec.continuous = true;

            rec.onstart = () => {
                transcriptDiv.innerText = "LISTENING...";
                logBox.innerHTML += "<br>>> Neural Link: SUCCESS";
                ghostSpeak("Ghost protocol initiated. I am watching, Shivam Sir.");
            };

            rec.onresult = (e) => {
                const cmd = e.results[e.results.length - 1][0].transcript.toLowerCase();
                transcriptDiv.innerText = cmd.toUpperCase();
                processGhostCommand(cmd);
            };

            rec.onend = () => rec.start(); // Eternal Loop
            rec.start();
        }

        function processGhostCommand(cmd) {
            let res = "";
            if(cmd.includes("status")) res = "Nodes are secure. No trace detected on the network.";
            else if(cmd.includes("search for")) {
                let q = cmd.split("search for")[1];
                res = "Scraping dark-web for " + q;
                window.open(`https://www.google.com/search?q=${q}`);
            }
            else if(cmd.includes("open youtube")) { res = "Accessing media mainframe."; window.open("https://youtube.com"); }
            else if(cmd.includes("who am i")) res = "You are the Architect, Shivam Singh.";
            else if(cmd.includes("ghost exit")) { res = "Fading into the void."; location.reload(); }
            
            if(res) {
                logBox.innerHTML += `<br>> ${res}`;
                ghostSpeak(res);
            }
        }

        // Ghost Background Effect
        const c = document.getElementById('ghost-canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const chars = "01";
        const drops = Array(Math.floor(c.width/20)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0, 8, 0, 0.05)";
            ctx.fillRect(0,0,c.width,c.height);
            ctx.fillStyle = "#0f0";
            drops.forEach((y, i) => {
                const text = chars[Math.floor(Math.random()*chars.length)];
                ctx.fillText(text, i*20, y*20);
                if(y*20 > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 50);
    </script>
</body>
</html>
"""

@script19_bp.route('/')
def index():
    return render_template_string(GHOST_AI_UI)
