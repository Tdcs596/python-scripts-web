from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# --- CCTV STEALTH UI BY SHIVAM SINGH ---
CCTV_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CCTV - Shivam Singh</title>
    <style>
        body { background: #000; color: #ff0000; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; overflow: hidden; }
        #video-container { width: 100vw; height: 100vh; background: #000; display: flex; align-items: center; justify-content: center; }
        video { width: 100%; height: 100%; object-fit: cover; }
        
        /* Stealth Mode Overlay */
        #blackout { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: black; display: none; z-index: 9999; 
        }

        .controls { 
            position: fixed; bottom: 30px; width: 100%; z-index: 100; 
            display: flex; flex-direction: column; align-items: center; gap: 15px; 
        }
        .btn-group { display: flex; gap: 10px; }
        button { 
            background: rgba(255, 0, 0, 0.1); border: 1px solid #ff0000; 
            color: #ff0000; padding: 12px 20px; font-weight: bold; cursor: pointer;
            text-transform: uppercase; letter-spacing: 1px;
        }
        button:active { background: #ff0000; color: #000; }
        .branding { 
            position: fixed; top: 20px; width: 100%; text-align: center; 
            font-size: 18px; font-weight: bold; color: #ff0000; 
            text-shadow: 0 0 10px #ff0000; z-index: 10;
        }
        .rec-indicator { color: red; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0; } }
    </style>
</head>
<body>

    <div id="blackout" onclick="toggleStealth()"></div>

    <div class="branding">
        <span class="rec-indicator">●</span> SHIVAM SINGH MONITORING SYSTEM
    </div>

    <div id="video-container">
        <video id="camView" autoplay playsinline muted></video>
    </div>

    <div class="controls" id="ui-controls">
        <div class="btn-group">
            <button onclick="switchCamera('user')">Front Cam</button>
            <button onclick="switchCamera('environment')">Back Cam</button>
        </div>
        <button onclick="toggleStealth()" style="width: 80%; background: #ff0000; color: #000;">
            ACTIVATE STEALTH MODE (BLACK SCREEN)
        </button>
    </div>

    <script>
        let currentStream = null;

        async function switchCamera(mode) {
            if (currentStream) {
                currentStream.getTracks().forEach(track => track.stop());
            }

            try {
                const constraints = {
                    video: { facingMode: mode },
                    audio: false
                };
                currentStream = await navigator.mediaDevices.getUserMedia(constraints);
                const video = document.getElementById('camView');
                video.srcObject = currentStream;
                
                // Screen Wake Lock
                if ('wakeLock' in navigator) {
                    await navigator.wakeLock.request('screen');
                }
            } catch (err) {
                alert("Error: Camera access denied!");
            }
        }

        function toggleStealth() {
            const blackout = document.getElementById('blackout');
            if (blackout.style.display === 'none' || blackout.style.display === '') {
                blackout.style.display = 'block';
            } else {
                blackout.style.display = 'none';
            }
        }

        // Start with back camera
        window.onload = () => switchCamera('environment');
    </script>
</body>
</html>
"""

@script10_bp.route('/')
def index():
    return render_template_string(CCTV_UI)
