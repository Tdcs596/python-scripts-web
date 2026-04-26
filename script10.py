from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# --- SHIVAM SINGH REMOTE MONITORING UI ---
REMOTE_SPY_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Remote Spy - Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow: hidden; }
        .header { position: fixed; top: 10px; width: 100%; color: #ff0000; font-weight: bold; z-index: 10; text-shadow: 0 0 5px #000; font-size: 14px; }
        #video-container { width: 100vw; height: 100vh; background: #111; display: flex; align-items: center; justify-content: center; }
        video { width: 100%; height: 100%; object-fit: cover; border: 1px solid #333; }
        
        .setup-box { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #111; border: 1px solid #ff0000; padding: 30px; z-index: 100; width: 85%; max-width: 400px; }
        input { background: #000; border: 1px solid #ff0000; color: #fff; padding: 12px; width: 80%; text-align: center; margin-bottom: 15px; font-size: 16px; }
        
        #blackout { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; display: none; z-index: 9999; }

        .controls { position: fixed; bottom: 20px; width: 100%; z-index: 100; display: none; flex-direction: column; align-items: center; gap: 10px; }
        .btn-row { display: flex; gap: 10px; width: 90%; justify-content: center; }
        button { background: rgba(0, 0, 0, 0.8); border: 1px solid #ff0000; color: #ff0000; padding: 12px; font-size: 11px; font-weight: bold; cursor: pointer; flex: 1; text-transform: uppercase; }
        button:active { background: #ff0000; color: #000; }
        .active-rec { background: #fff !important; color: #ff0000 !important; }
    </style>
</head>
<body>

    <div id="blackout" onclick="toggleStealth()"></div>

    <div class="header">
        [SHIVAM SINGH] REMOTE CONNECTION SYSTEM <span id="status"></span>
    </div>

    <div class="setup-box" id="setup">
        <h2 style="color: #ff0000; font-size: 18px;">REMOTE HANDSHAKE</h2>
        <p style="font-size: 12px;">Enter Target Device ID / Number</p>
        <input type="tel" id="targetID" placeholder="91XXXXXXXXXX" maxlength="12">
        <button onclick="startConnection()" style="width: 85%; background: #ff0000; color: #000;">CONNECT TO TARGET</button>
        <p style="font-size: 10px; color: #555; margin-top: 10px;">Establishing Peer-to-Peer Tunneling...</p>
    </div>

    <div id="video-container">
        <video id="camView" autoplay playsinline muted></video>
    </div>

    <div class="controls" id="ui-controls">
        <div class="btn-row">
            <button onclick="changeCam('user')">FRONT CAM</button>
            <button onclick="changeCam('environment')">BACK CAM</button>
        </div>
        <div class="btn-row">
            <button id="recBtn" onclick="handleRecord()">RECORD FEED</button>
            <button onclick="toggleStealth()" style="background: #ff0000; color: #000; border: none;">STEALTH ON</button>
        </div>
    </div>

    <script>
        let stream = null;
        let recorder = null;
        let chunks = [];

        async function startConnection() {
            const id = document.getElementById('targetID').value;
            if (id.length < 10) return alert("Invalid Target ID!");

            document.getElementById('status').innerText = "[CONNECTING TO " + id + "]";
            document.getElementById('setup').style.display = 'none';
            document.getElementById('ui-controls').style.display = 'flex';

            try {
                // Device access with Audio
                stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' }, 
                    audio: true 
                });
                const video = document.getElementById('camView');
                video.srcObject = stream;
                
                if ('wakeLock' in navigator) await navigator.wakeLock.request('screen');
            } catch (e) {
                alert("Target Access Denied: " + e);
                location.reload();
            }
        }

        async function changeCam(mode) {
            if (stream) stream.getTracks().forEach(t => t.stop());
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: mode }, audio: true });
            document.getElementById('camView').srcObject = stream;
        }

        function handleRecord() {
            const btn = document.getElementById('recBtn');
            if (!recorder || recorder.state === "inactive") {
                chunks = [];
                recorder = new MediaRecorder(stream);
                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = () => {
                    const blob = new Blob(chunks, { type: 'video/webm' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `Shivam_Singh_Remote_${Date.now()}.webm`;
                    a.click();
                };
                recorder.start();
                btn.innerText = "STOP & SAVE";
                btn.classList.add('active-rec');
            } else {
                recorder.stop();
                btn.innerText = "RECORD FEED";
                btn.classList.remove('active-rec');
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
    return render_template_string(REMOTE_SPY_UI)
