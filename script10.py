from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost CCTV V11 - Multi-Cam Monitor</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow: hidden; }
        .monitor-frame { border: 2px solid #0f0; display: inline-block; margin-top: 20px; position: relative; width: 95%; max-width: 600px; height: 350px; background: #050505; }
        video { width: 100%; height: 100%; object-fit: cover; background: #000; }
        .controls { padding: 20px; background: #111; border-top: 2px solid #0f0; height: 100vh; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; margin: 5px; width: 60%; text-align: center; outline: none; }
        button { padding: 10px 20px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; margin: 5px; transition: 0.3s; }
        button:hover { background: #00cc00; box-shadow: 0 0 10px #0f0; }
        .flip-btn { background: #ffaa00; color: #000; }
        .status-bar { font-size: 11px; padding: 5px; background: #002200; color: #0f0; display: flex; justify-content: space-between; padding: 5px 15px; border-bottom: 1px solid #0f0; }
        .rec-dot { height: 8px; width: 8px; background: red; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
        #logs { font-size: 12px; color: yellow; margin: 10px; height: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="status-bar">
        <span>[ SYSTEM: ONLINE ]</span>
        <span>MY_ID: <b id="my-id">---</b></span>
        <span><span class="rec-dot"></span> LIVE FEED</span>
    </div>

    <div class="monitor-frame">
        <video id="remote-feed" autoplay playsinline></video>
        <div style="position:absolute; top:10px; left:10px; font-size:10px; text-align:left; pointer-events:none; z-index:10; background: rgba(0,0,0,0.5); padding: 5px;">
            CAM_SOURCE: <span id="cam-mode">REMOTE</span><br>
            TIME: <span id="timer">00:00:00</span><br>
            STATUS: <span id="stream-status" style="color:red;">OFFLINE</span>
        </div>
    </div>

    <div class="controls">
        <div style="margin-bottom: 15px;">
            <input type="text" id="custom-id" placeholder="Set ID (e.g. 1234)" style="width:100px;">
            <button onclick="bootCCTV()">1. START CAMERA</button>
            <button class="flip-btn" onclick="flipCamera()">🔄 FLIP CAM</button>
        </div>
        
        <div style="border-top: 1px solid #333; padding-top: 15px;">
            <input type="text" id="target-id" placeholder="Enter Target CCTV ID">
            <button onclick="connectToCCTV()" style="width:80%; background: #00f; color: #fff;">2. VIEW REMOTE FEED</button>
        </div>
        <p id="logs">System Initialized...</p>
    </div>

<script>
    let peer, localStream, currentCall;
    let currentFacingMode = "environment"; // Default back camera
    const logs = document.getElementById('logs');
    const remoteVideo = document.getElementById('remote-feed');
    const statusVal = document.getElementById('stream-status');

    async function bootCCTV() {
        const cid = document.getElementById('custom-id').value;
        if(!cid) return alert("Bhai, pehle ID toh set kar!");

        try {
            logs.innerText = "Accessing " + currentFacingMode + " camera...";
            
            // Stop existing tracks if any
            if(localStream) {
                localStream.getTracks().forEach(track => track.stop());
            }

            localStream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: currentFacingMode }, 
                audio: true 
            });
            
            if(!peer) {
                peer = new Peer(cid);
                peer.on('open', id => {
                    document.getElementById('my-id').innerText = id;
                    logs.innerText = "CCTV LIVE | ID: " + id;
                });

                peer.on('call', call => {
                    logs.innerText = "Viewer connected!";
                    currentCall = call;
                    call.answer(localStream);
                });
            } else {
                logs.innerText = "Camera Updated to " + currentFacingMode;
                // If a call is active, we need to replace the track (Advanced)
                // For simplicity, the viewer should re-connect to see the flip
            }

        } catch (e) {
            logs.innerText = "Error: Camera Access Denied.";
            console.error(e);
        }
    }

    async function flipCamera() {
        currentFacingMode = (currentFacingMode === "user") ? "environment" : "user";
        document.getElementById('cam-mode').innerText = currentFacingMode.toUpperCase();
        if(localStream) {
            await bootCCTV(); // Re-initialize with new facing mode
        } else {
            logs.innerText = "Pehle camera start toh karle, bhai!";
        }
    }

    function connectToCCTV() {
        const tid = document.getElementById('target-id').value;
        if(!tid) return alert("Target ID daalo!");

        if(!peer) peer = new Peer(); 
        
        logs.innerText = "Connecting...";
        const dummyStream = new MediaStream(); 
        const call = peer.call(tid, dummyStream);
        
        call.on('stream', s => {
            remoteVideo.srcObject = s;
            remoteVideo.muted = true;
            remoteVideo.play().then(() => {
                statusVal.innerText = "LIVE FEED";
                statusVal.style.color = "#0f0";
                logs.innerText = "STREAMING FROM " + tid;
            });
        });
    }

    setInterval(() => {
        document.getElementById('timer').innerText = new Date().toLocaleTimeString();
    }, 1000);
</script>
</body>
</html>
