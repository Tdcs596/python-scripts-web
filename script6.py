from flask import Blueprint, render_template_string

script6_bp = Blueprint('script6', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Script6 - Private Video Call</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; text-align: center; margin: 0; padding: 20px; }
        .video-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px; }
        video { width: 45%; max-width: 400px; border: 2px solid #0f0; border-radius: 10px; background: #111; transform: scaleX(-1); }
        .controls { background: #111; padding: 20px; border: 1px solid #333; display: inline-block; border-radius: 10px; box-shadow: 0 0 20px #0f02; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; width: 200px; text-align: center; }
        button { padding: 10px 20px; font-weight: bold; cursor: pointer; border: none; margin: 5px; border-radius: 5px; }
        .call-btn { background: #0f0; color: #000; }
        .hangup-btn { background: #f00; color: #fff; }
        .peer-id-box { margin-bottom: 20px; font-size: 1.2rem; color: yellow; }
    </style>
</head>
<body>
    <h1>GHOST_VIDEO_CALL v1.0</h1>
    
    <div class="controls">
        <div class="peer-id-box">YOUR ID: <span id="my-id">Initializing...</span></div>
        <input type="text" id="remote-id" placeholder="Enter Friend's ID">
        <button class="call-btn" onclick="makeCall()">START CALL</button>
        <button class="hangup-btn" onclick="endCall()">HANG UP</button>
    </div>

    <div class="video-container">
        <div>
            <p>YOU</p>
            <video id="local-video" autoplay muted></video>
        </div>
        <div>
            <p>FRIEND</p>
            <video id="remote-video" autoplay></video>
        </div>
    </div>

<script>
    const myIdSpan = document.getElementById('my-id');
    const localVideo = document.getElementById('local-video');
    const remoteVideo = document.getElementById('remote-video');
    let peer, localStream, currentCall;

    // 1. Camera access lo
    navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
        localStream = stream;
        localVideo.srcObject = stream;

        // 2. Peer connection initialize karo
        peer = new Peer();

        peer.on('open', id => {
            myIdSpan.innerText = id;
        });

        // 3. Incoming Call handle karo
        peer.on('call', call => {
            if (confirm("Incoming video call! Accept?")) {
                call.answer(localStream);
                handleCall(call);
            }
        });
    }).catch(err => alert("Camera permission denied!"));

    function handleCall(call) {
        currentCall = call;
        call.on('stream', remoteStream => {
            remoteVideo.srcObject = remoteStream;
        });
    }

    function makeCall() {
        const remoteId = document.getElementById('remote-id').value;
        if (!remoteId) return alert("Enter Peer ID first!");
        
        const call = peer.call(remoteId, localStream);
        handleCall(call);
    }

    function endCall() {
        if(currentCall) currentCall.close();
        remoteVideo.srcObject = null;
        alert("Call Ended.");
    }
</script>
</body>
</html>
"""

@script6_bp.route('/')
def script6_home():
    return render_template_string(INTERFACE)

