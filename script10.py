from flask import Blueprint, render_template_string

script10_bp = Blueprint('script10', __name__)

# Check karna yahan shuru ho raha hai
INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ghost CCTV V11</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; }
        video { width: 100%; max-width: 500px; background: #222; border: 2px solid #0f0; }
        button { padding: 10px; margin: 5px; cursor: pointer; background: #0f0; border: none; font-weight: bold; }
        .controls { background: #111; padding: 20px; border-top: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>[ GHOST CCTV V11 ]</h1>
    <video id="remote-video" autoplay playsinline muted></video>
    <div id="status">OFFLINE</div>
    
    <div class="controls">
        <input type="text" id="my-id" placeholder="Set My ID">
        <button onclick="startCam()">1. START CAM</button>
        <button onclick="flipCam()">🔄 FLIP</button>
        <br><br>
        <input type="text" id="target-id" placeholder="Enter Target ID">
        <button onclick="connect()">2. VIEW FEED</button>
    </div>

    <script>
        let peer, localStream, currentFacingMode = "environment";

        async function startCam() {
            const id = document.getElementById('my-id').value;
            if(!id) return alert("ID daalo bhai!");
            
            if(localStream) localStream.getTracks().forEach(t => t.stop());
            localStream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: currentFacingMode }, audio: true 
            });

            if(!peer) {
                peer = new Peer(id);
                peer.on('call', call => call.answer(localStream));
            }
            document.getElementById('status').innerText = "LIVE AS: " + id;
        }

        async function flipCam() {
            currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
            if(localStream) await startCam();
        }

        function connect() {
            const tid = document.getElementById('target-id').value;
            if(!peer) peer = new Peer();
            const call = peer.call(tid, new MediaStream());
            call.on('stream', s => {
                const v = document.getElementById('remote-video');
                v.srcObject = s;
                v.play();
                document.getElementById('status').innerText = "CONNECTED TO " + tid;
            });
        }
    </script>
</body>
</html>
""" 
# Upar wala ye """ (Triple Quote) check kar, ye miss ho raha tha tere code mein!

@script10_bp.route('/')
def script10_home():
    return render_template_string(INTERFACE)
