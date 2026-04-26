from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# --- ADVANCED SPY UI BY SHIVAM SINGH ---
SPY_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Spy System - Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Courier New', monospace; margin: 0; overflow: hidden; }
        #video-container { width: 100vw; height: 100vh; position: relative; background: #000; }
        video { width: 100%; height: 100%; object-fit: cover; }
        
        #blackout { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: black; display: none; z-index: 9999; cursor: pointer;
        }

        .controls { 
            position: fixed; bottom: 20px; width: 100%; z-index: 100; 
            display: flex; flex-direction: column; align-items: center; gap: 10px;
        }
        .btn-row { display: flex; gap: 10px; }
        button { 
            background: #111; border: 1px solid #00ff00; color: #00ff00; 
            padding: 10px 15px; font-size: 12px; cursor: pointer; font-weight: bold;
        }
        button:active { background: #00ff00; color: #000; }
        .recording-btn { border-color: #ff0000; color: #ff0000; }
        
        .header { 
            position: fixed; top: 10px; width: 100%; text-align: center; 
            color: #ff0000; font-size: 14px; z-index: 10; font-weight: bold;
            text-shadow: 0 0 5px #000;
        }
    </style>
</head>
<body>

    <div id="blackout" onclick="toggleStealth()"></div>

    <div class="header">
        [LIVE] MONITORING SYSTEM - SHIVAM SINGH <span id="rec-status"></span>
    </div>

    <div id="video-container">
        <video id="camView" autoplay playsinline muted></video>
    </div>

    <div class="controls" id="ui-controls">
        <div class="btn-row">
            <button onclick="initCam('user')">FRONT CAM</button>
            <button onclick="initCam('environment')">BACK CAM</button>
        </div>
        <div class="btn-row">
            <button id="recordBtn" class="recording-btn" onclick="toggleRecording()">START RECORDING</button>
            <button onclick="toggleStealth()" style="background: #ff0000; color: #fff; border:none;">STEALTH MODE</button>
        </div>
        <div style="font-size: 10px; color: #888;">Note: Stealth mode on hone pe screen black ho jayegi.</div>
    </div>

    <script>
        let stream = null;
        let recorder = null;
        let chunks = [];

        async function initCam(mode) {
            if (stream) stream.getTracks().forEach(t => t.stop());

            try {
                // Audio: true taaki awaaz bhi sunayi de aur record ho
                stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: mode },
                    audio: true 
                });
                
                const video = document.getElementById('camView');
                video.srcObject = stream;
                
                // Audio playback for monitoring (Unmute if you want to hear live on same device)
                // video.muted = false; 

                if ('wakeLock' in navigator) await navigator.wakeLock.request('screen');
            } catch (e) {
                alert("Access Denied: " + e);
            }
        }

        function toggleRecording() {
            const btn = document.getElementById('recordBtn');
            const status = document.getElementById('rec-status');

            if (!recorder || recorder.state === "inactive") {
                chunks = [];
                recorder = new MediaRecorder(stream);
                recorder.ondataavailable = e => chunks.push(e.data);
                recorder.onstop = () => {
                    const blob = new Blob(chunks, { type: 'video/webm' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `Shivam_Singh_Record_${Date.now()}.webm`;
                    a.click();
                };
                recorder.start();
                btn.innerText = "STOP RECORDING";
                status.innerText = "● RECORDING";
            } else {
                recorder.stop();
                btn.innerText = "START RECORDING";
                status.innerText = "";
            }
        }

        function toggleStealth() {
            const blackout = document.getElementById('blackout');
            blackout.style.display = (blackout.style.display === 'block') ? 'none' : 'block';
        }

        window.onload = () => initCam('environment');
    </script>
</body>
</html>
"""

@script10_bp.route('/')
def index():
    return render_template_string(SPY_UI)
