from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost CCTV V10 - Silent Monitor</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; text-align: center; margin: 0; overflow: hidden; }
        .monitor-frame { border: 2px solid #0f0; display: inline-block; margin-top: 20px; position: relative; width: 95%; max-width: 600px; height: 350px; background: #050505; }
        video { width: 100%; height: 100%; object-fit: cover; }
        .controls { padding: 20px; background: #111; border-top: 2px solid #0f0; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; margin: 5px; width: 60%; text-align: center; outline: none; }
        button { padding: 10px 20px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; margin: 5px; transition: 0.3s; }
        button:active { background: #008800; }
        .status-bar { font-size: 11px; padding: 5px; background: #002200; color: #0f0; display: flex; justify-content: space-between; padding: 5px 15px; }
        .rec-dot { height: 8px; width: 8px; background: red; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
        #logs { font-size: 10px; color: yellow; margin: 5px; }
    </style>
</head>
<body>
    <div class="status-bar">
        <span>[ SYSTEM: ONLINE ]</span>
        <span>ID: <b id="my-id">NONE</b></span>
        <span><span class="rec-dot"></span> LIVE FEED</span>
    </div>

    <div class="monitor-frame">
        <video id="remote-feed" autoplay playsinline></video>
        <div style="position:absolute; top:10px; left:10px; font-size:10px; text-align:left; pointer-events:none;">
            CAM_SOURCE: REMOTE_ENCRYPTED<br>
            TIME: <span id="timer">00:00:00</span><br>
            STATUS: <span id="stream-status" style="color:red;">NO FEED</span>
        </div>
    </div>

    <div class="controls">
        <div style="margin-bottom: 10px;">
            SET CCTV NO: <input type="text" id="custom-id" placeholder="Ex: 8888" style="width:80px;">
            <button onclick="bootCCTV()">BOOT CCTV</button>
        </div>
        
        <input type="text" id="target-id" placeholder="Enter CCTV ID to View">
        <br>
        <button onclick="connectToCCTV()" style="width:80%;">VIEW REMOTE FEED</button>
        <p id="logs">Ready. Waiting for Hardware...</p>
    </div>

<script>
    let peer, localStream;
    const logs = document.getElementById('logs');
    const remoteVideo = document.getElementById('remote-feed');
    const statusVal = document.getElementById('stream-status');

    async function stayAwake() {
        if ('wakeLock' in navigator) {
            try { await navigator.wakeLock.request('screen'); } catch (err) {}
        }
    }

    // --- CCTV MODE (Server) ---
    async function bootCCTV() {
        const cid = document.getElementById('custom-id').value;
        if(!cid) return alert("Pehle number set kar!");

        try {
            // Camera permission request
            localStream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: "environment" }, // Back camera focus
                audio: true 
            });
            
            peer = new Peer(cid);
            
            peer.on('open', id => {
                document.getElementById('my-id').innerText = id;
                logs.innerText = "CCTV IS LIVE. Now you can view from another device.";
                stayAwake();
            });

            peer.on('call', call => {
                logs.innerText = "Viewer connected!";
                call.answer(localStream); // Answer with camera stream
            });

            peer.on('error', err => {
                alert("ID Taken or Connection Error. Try another ID.");
                console.error(err);
            });

        } catch (e) {
            logs.innerText = "Error: Mic/Cam permission denied.";
        }
    }

    // --- MONITOR MODE (Viewer) ---
    function connectToCCTV() {
        const tid = document.getElementById('target-id').value;
        if(!tid) return alert("CCTV ID toh daalo!");

        if(!peer) {
            peer = new Peer(); // Create random peer for viewer
            peer.on('open', () => startViewer(tid));
        } else {
            startViewer(tid);
        }
    }

    function startViewer(tid) {
        logs.innerText = "Connecting to CCTV: " + tid;
        
        // viewer ko kuch nahi bhejna, par handshake ke liye empty stream zaroori hai
        const emptyStream = new AudioContext().createMediaStreamDestination().stream;
        
        const call = peer.call(tid, emptyStream);
        
        call.on('stream', s => {
            remoteVideo.srcObject = s;
            statusVal.innerText = "LIVE FEED";
            statusVal.style.color = "#0f0";
            logs.innerText = "Streaming live from " + tid;
        });

        call.on('error', err => {
            logs.innerText = "Failed to connect to ID: " + tid;
        });
    }

    // Timer Update
    setInterval(() => {
        const now = new Date();
        document.getElementById('timer').innerText = now.toLocaleTimeString();
    }, 1000);
</script>
</body>
</html>
"""

@script10_bp.route('/')
def script10_home():
    return render_template_string(INTERFACE)
