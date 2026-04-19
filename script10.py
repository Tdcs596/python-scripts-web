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
        .monitor-frame { border: 2px solid #0f0; display: inline-block; margin-top: 20px; position: relative; width: 90%; max-width: 600px; }
        video { width: 100%; background: #050505; transform: scaleX(-1); } /* Mirror effect for CCTV */
        .controls { padding: 20px; background: #111; border-top: 2px solid #0f0; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; margin: 5px; width: 60%; text-align: center; }
        button { padding: 10px 20px; background: #0f0; color: #000; border: none; font-weight: bold; cursor: pointer; margin: 5px; }
        .status-bar { font-size: 12px; padding: 5px; background: #002200; color: #0f0; display: flex; justify-content: space-between; px: 10px; }
        .rec-dot { height: 10px; width: 10px; background: red; border-radius: 50%; display: inline-block; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div class="status-bar">
        <span>[ SYSTEM: ONLINE ]</span>
        <span>ID: <b id="my-id">NONE</b></span>
        <span><span class="rec-dot"></span> LIVE</span>
    </div>

    <div class="monitor-frame">
        <video id="remote-feed" autoplay playsinline></video>
        <div id="overlay" style="position:absolute; top:10px; left:10px; font-size:10px; text-shadow: 1px 1px #000;">
            CAM_FEED_ENCRYPTED_<br><span id="timer">00:00:00</span>
        </div>
    </div>

    <div class="controls">
        <div style="margin-bottom: 15px;">
            SET CCTV NO: <input type="text" id="custom-id" placeholder="Ex: 8888" style="width:80px;">
            <button onclick="bootCCTV()">BOOT</button>
        </div>
        
        <input type="text" id="target-id" placeholder="Enter CCTV ID to View">
        <br>
        <button onclick="connectToCCTV()" style="width:80%;">VIEW REMOTE FEED</button>
        <p id="logs" style="font-size:10px; color:yellow;">Initializing Hardware...</p>
    </div>

<script>
    let peer, localStream;
    const logs = document.getElementById('logs');
    const remoteVideo = document.getElementById('remote-feed');

    // Prevent Sleep Mode (Background persistence)
    async function stayAwake() {
        if ('wakeLock' in navigator) {
            try { await navigator.wakeLock.request('screen'); } catch (err) {}
        }
    }

    async function bootCCTV() {
        const cid = document.getElementById('custom-id').value;
        if(!cid) return alert("Number daal bhai!");

        try {
            // Background persistence ke liye audio:true bhi zaroori hai
            localStream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: "environment" }, // Back camera by default
                audio: true 
            });
            
            peer = new Peer(cid);
            
            peer.on('open', id => {
                document.getElementById('my-id').innerText = id;
                logs.innerText = "CCTV ACTIVE & STEALTH MODE ENABLED";
                stayAwake();
            });

            peer.on('call', call => {
                logs.innerText = "REMOTE MONITOR CONNECTED";
                call.answer(localStream);
            });

        } catch (e) {
            logs.innerText = "Hardware Error: Mic/Cam Denied";
        }
    }

    function connectToCCTV() {
        const tid = document.getElementById('target-id').value;
        if(!peer) {
            // Viewer mode ke liye temporary peer
            peer = new Peer();
            peer.on('open', () => startCall(tid));
        } else {
            startCall(tid);
        }
    }

    function startCall(tid) {
        const call = peer.call(tid, localStream || new MediaStream()); // Empty stream if just viewing
        call.on('stream', s => {
            remoteVideo.srcObject = s;
            logs.innerText = "CONNECTED TO CCTV: " + tid;
        });
    }

    // Timer logic
    setInterval(() => {
        const now = new Date();
        document.getElementById('timer').innerText = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();
    }, 1000);

</script>
</body>
</html>
"""

@script10_bp.route('/')
def script10_home():
    return render_template_string(INTERFACE)

