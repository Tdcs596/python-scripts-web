from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# --- SHIVAM SINGH PRIVATE PIN REMOTE SPY ---
REMOTE_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Private Spy - Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow: hidden; }
        .header { position: fixed; top: 10px; width: 100%; color: #ff0000; font-weight: bold; z-index: 10; font-size: 14px; text-shadow: 0 0 5px #000; }
        
        /* Setup Boxes */
        .box { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #111; border: 1px solid #ff0000; padding: 25px; z-index: 100; width: 80%; max-width: 350px; }
        input { background: #000; border: 1px solid #ff0000; color: #fff; padding: 15px; width: 60%; text-align: center; font-size: 24px; letter-spacing: 10px; margin: 15px 0; }
        button { background: #ff0000; color: #000; border: none; padding: 12px; font-weight: bold; cursor: pointer; width: 100%; text-transform: uppercase; margin-top: 5px; }
        
        #video-container { width: 100vw; height: 100vh; background: #000; display: none; }
        video { width: 100%; height: 100%; object-fit: cover; }
        
        #blackout { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; display: none; z-index: 9999; }
        .controls { position: fixed; bottom: 20px; width: 100%; z-index: 100; display: none; flex-direction: column; align-items: center; gap: 10px; }
        .btn-row { display: flex; gap: 10px; width: 90%; }
        .status-msg { font-size: 12px; color: #888; margin-bottom: 10px; }
    </style>
</head>
<body>

    <div id="blackout" onclick="toggleStealth()"></div>
    <div class="header">SHIVAM SINGH SECURE REMOTE SYSTEM</div>

    <div class="box" id="mode-box">
        <h3 style="color:#ff0000">SELECT MODE</h3>
        <button onclick="showSetup('target')">SET PIN (TARGET DEVICE)</button>
        <button onclick="showSetup('master')" style="margin-top:10px; background:#222; color:#ff0000; border:1px solid #ff0000;">CONNECT (MASTER DEVICE)</button>
    </div>

    <div class="box" id="pin-box" style="display:none;">
        <h3 id="pin-title">SET 3-DIGIT PIN</h3>
        <input type="tel" id="pinInput" maxlength="3" placeholder="000">
        <button id="actionBtn" onclick="handleAction()">EXECUTE</button>
        <div class="status-msg" id="msg">Awaiting secure handshake...</div>
    </div>

    <div id="video-container">
        <video id="camView" autoplay playsinline muted></video>
    </div>

    <div class="controls" id="ui-controls">
        <div class="btn-row">
            <button onclick="initStream('user')">FRONT</button>
            <button onclick="initStream('environment')">BACK</button>
        </div>
        <div class="btn-row">
            <button id="recBtn" onclick="toggleRec()" style="background:#fff; color:#000;">RECORDING</button>
            <button onclick="toggleStealth()" style="background:#ff0000; color:#000;">STEALTH</button>
        </div>
    </div>

    <script>
        let currentMode = '';
        let myStream = null;
        let recorder = null;
        let chunks = [];

        function showSetup(mode) {
            currentMode = mode;
            document.getElementById('mode-box').style.display = 'none';
            document.getElementById('pin-box').style.display = 'block';
            if(mode === 'master') {
                document.getElementById('pin-title').innerText = "ENTER TARGET PIN";
                document.getElementById('actionBtn').innerText = "CONNECT TO REMOTE";
            }
        }

        async function handleAction() {
            const pin = document.getElementById('pinInput').value;
            if(pin.length !== 3) return alert("Enter exactly 3 digits!");

            if(currentMode === 'target') {
                // Target sets the PIN and waits
                localStorage.setItem('spy_pin', pin);
                document.getElementById('msg').innerHTML = "PIN SET: " + pin + "<br>Waiting for Master connection...";
                document.getElementById('pinInput').disabled = true;
                // Auto-start camera in background for target
                await initStream('environment');
            } else {
                // Master tries to connect
                const savedPin = localStorage.getItem('spy_pin');
                if(pin === savedPin || pin === "999") { // Emergency bypass 999
                    document.getElementById('pin-box').style.display = 'none';
                    document.getElementById('video-container').style.display = 'block';
                    document.getElementById('ui-controls').style.display = 'flex';
                    await initStream('environment');
                } else {
                    alert("Incorrect PIN! Connection Refused.");
                }
            }
        }

        async function initStream(facing) {
            if (myStream) myStream.getTracks().forEach(t => t.stop());
            try {
                myStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: facing }, 
                    audio: true 
                });
                document.getElementById('camView').srcObject = myStream;
                document.getElementById('video-container').style.display = 'block';
                if ('wakeLock' in navigator) await navigator.wakeLock.request('screen');
            } catch (e) { alert("Permission Error: " + e); }
        }

        function toggleRec() {
            const btn = document.getElementById('recBtn');
            if (!recorder || recorder.state === "inactive") {
                chunks = [];
                recorder = new MediaRecorder(myStream);
                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = () => {
                    const blob = new Blob(chunks, { type: 'video/webm' });
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = `Shivam_Singh_Spy_${Date.now()}.webm`;
                    a.click();
                };
                recorder.start();
                btn.innerText = "STOP & SAVE";
                btn.style.background = "red";
            } else {
                recorder.stop();
                btn.innerText = "RECORDING";
                btn.style.background = "#fff";
            }
        }

        function toggleStealth() {
            const blackout = document.getElementById('blackout');
            blackout.style.display = (blackout.style.display === 'block') ? 'none' : 'block';
        }
    </script>
</body>
</html>
"""

@script10_bp.route('/')
def index():
    return render_template_string(REMOTE_UI)

