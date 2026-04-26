from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# --- REMOTE SPY UI BY SHIVAM SINGH ---
REMOTE_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remote Access - Shivam Singh</title>
    <style>
        body { background: #000; color: #ff0000; font-family: 'Courier New', monospace; text-align: center; padding: 20px; }
        .box { border: 1px solid #ff0000; padding: 20px; background: #111; max-width: 400px; margin: auto; }
        input { background: #000; border: 1px solid #ff0000; color: #fff; padding: 10px; width: 80%; text-align: center; font-size: 18px; margin-bottom: 10px; }
        button { background: #ff0000; color: #000; border: none; padding: 12px 25px; font-weight: bold; cursor: pointer; width: 85%; }
        #monitor { display: none; margin-top: 20px; }
        video { width: 100%; border: 2px solid #fff; border-radius: 5px; }
        .stealth { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; display: none; z-index: 1000; }
    </style>
</head>
<body>

    <div id="blackout" class="stealth" onclick="this.style.display='none'"></div>

    <div class="box" id="login-box">
        <h2>[ SHIVAM SINGH REMOTE SPY ]</h2>
        <p>Enter Target Connection ID/Number:</p>
        <input type="tel" id="targetId" placeholder="+91 XXXX XXXX XX" maxlength="13">
        <button onclick="startRemote()">CONNECT & STREAM</button>
        <p style="font-size: 10px; color: #555; margin-top: 15px;">Note: Remote device must have permission enabled.</p>
    </div>

    <div id="monitor">
        <h3>🔴 LIVE FEED: CONNECTED</h3>
        <video id="remoteFeed" autoplay playsinline></video>
        <div style="margin-top: 10px;">
            <button onclick="toggleStealth()" style="background: #222; color: #ff0000; border: 1px solid #ff0000;">STEALTH MODE</button>
            <button id="recBtn" onclick="toggleRecord()" style="margin-top: 10px;">START RECORDING</button>
        </div>
    </div>

    <script>
        let stream = null;
        let recorder = null;
        let chunks = [];

        async function startRemote() {
            const num = document.getElementById('targetId').value;
            if(num.length < 10) return alert("Please enter a valid number/ID!");

            document.getElementById('login-box').innerHTML = "<h3>CONNECTING TO " + num + "...</h3><p>Waiting for handshake...</p>";

            try {
                // Requesting local stream (When you send this link to the target)
                stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                document.getElementById('login-box').style.display = 'none';
                document.getElementById('monitor').style.display = 'block';
                
                const video = document.getElementById('remoteFeed');
                video.srcObject = stream;
                
                if ('wakeLock' in navigator) await navigator.wakeLock.request('screen');
            } catch (err) {
                alert("Target Connection Failed: " + err);
                location.reload();
            }
        }

        function toggleStealth() {
            document.getElementById('blackout').style.display = 'block';
        }

        function toggleRecord() {
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
                    a.download = `Shivam_Singh_Spy_${Date.now()}.webm`;
                    a.click();
                };
                recorder.start();
                btn.innerText = "STOP & SAVE";
                btn.style.background = "#fff";
            } else {
                recorder.stop();
                btn.innerText = "START RECORDING";
                btn.style.background = "#ff0000";
            }
        }
    </script>
</body>
</html>

