from flask import Blueprint, render_template_string

script6_bp = Blueprint('script6', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Script6 - Pro Video Call</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #0a0a0a; color: #00ff00; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .header { padding: 20px; text-align: center; width: 100%; border-bottom: 1px solid #333; }
        .main-ui { width: 95%; max-width: 1000px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 20px; }
        video { width: 100%; border: 2px solid #00ff00; border-radius: 15px; background: #000; box-shadow: 0 0 15px #0f03; }
        .controls-panel { grid-column: span 2; background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }
        input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 12px; border-radius: 5px; outline: none; margin: 10px; width: 200px; }
        .btn { padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 5px; transition: 0.3s; }
        .btn-call { background: #00ff00; color: #000; }
        .btn-hangup { background: #ff0000; color: #fff; }
        .btn-tool { background: #333; color: #fff; }
        .status { color: yellow; font-size: 0.9rem; margin-top: 10px; }
        .peer-id-badge { background: #00ff00; color: #000; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h2>GHOST_VIDEO_PRO_V6</h2>
        <div id="status-text" class="status">Initializing System...</div>
    </div>

    <div class="main-ui">
        <div class="video-box">
            <p style="text-align:center;">LOCAL_STREAM (YOU)</p>
            <video id="local-video" autoplay muted playsinline></video>
        </div>
        <div class="video-box">
            <p style="text-align:center;">REMOTE_STREAM (FRIEND)</p>
            <video id="remote-video" autoplay playsinline></video>
        </div>

        <div class="controls-panel">
            <div style="margin-bottom: 15px;">
                YOUR ID: <span id="my-id" class="peer-id-badge">...</span>
            </div>
            <input type="text" id="remote-id" placeholder="Paste Friend's ID">
            <button class="btn btn-call" onclick="makeCall()">📞 START CALL</button>
            <button class="btn btn-hangup" onclick="endCall()">🛑 HANG UP</button>
            <br>
            <button class="btn btn-tool" onclick="toggleMic()">🎤 Mute/Unmute</button>
            <button class="btn btn-tool" onclick="toggleVid()">📷 Cam On/Off</button>
            <button class="btn btn-tool" style="background: #007bff;" onclick="shareScreen()">📺 Share Screen</button>
        </div>
    </div>

<script>
    const statusText = document.getElementById('status-text');
    const myIdDisplay = document.getElementById('my-id');
    const localVideo = document.getElementById('local-video');
    const remoteVideo = document.getElementById('remote-video');
    
    let peer, localStream, currentCall;

    // 1. Setup Camera
    async function initCamera() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            localVideo.srcObject = localStream;
            statusText.innerText = "Camera Ready. Waiting for ID...";
            setupPeer();
        } catch (err) {
            statusText.innerText = "Error: Camera Access Denied!";
        }
    }

    // 2. Setup PeerJS
    function setupPeer() {
        peer = new Peer();
        peer.on('open', id => {
            myIdDisplay.innerText = id;
            statusText.innerText = "System Online. Share your ID with a friend.";
        });

        peer.on('call', call => {
            statusText.innerText = "Incoming Call...";
            call.answer(localStream);
            handleConnection(call);
        });
    }

    function handleConnection(call) {
        currentCall = call;
        call.on('stream', stream => {
            remoteVideo.srcObject = stream;
            statusText.innerText = "Connected - Call in Progress";
        });
        call.on('close', () => {
            statusText.innerText = "Call Ended.";
            remoteVideo.srcObject = null;
        });
    }

    function makeCall() {
        const rid = document.getElementById('remote-id').value;
        if(!rid) return alert("Bhai, dost ki ID toh daal!");
        
        statusText.innerText = "Calling " + rid + "...";
        const call = peer.call(rid, localStream);
        handleConnection(call);
    }

    function endCall() {
        if(currentCall) currentCall.close();
        location.reload(); // Quick reset
    }

    function toggleMic() {
        const audioTrack = localStream.getAudioTracks()[0];
        audioTrack.enabled = !audioTrack.enabled;
        statusText.innerText = audioTrack.enabled ? "Mic On" : "Mic Muted";
    }

    function toggleVid() {
        const videoTrack = localStream.getVideoTracks()[0];
        videoTrack.enabled = !videoTrack.enabled;
        statusText.innerText = videoTrack.enabled ? "Camera On" : "Camera Off";
    }

    async function shareScreen() {
        try {
            const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
            if(currentCall) {
                const videoTrack = screenStream.getVideoTracks()[0];
                const sender = currentCall.peerConnection.getSenders().find(s => s.track.kind === 'video');
                sender.replaceTrack(videoTrack);
            }
            localVideo.srcObject = screenStream;
        } catch (e) {
            console.error(e);
        }
    }

    initCamera();
</script>
</body>
</html>
"""

@script6_bp.route('/')
def script6_home():
    return render_template_string(INTERFACE)
