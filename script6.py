from flask import Blueprint, render_template_string

script6_bp = Blueprint('script6', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost V6 - Screen Sync Pro</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #0a0a0a; color: #00ff00; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; align-items: center; min-height: 100vh; overflow-x: hidden; }
        .header { padding: 15px; text-align: center; width: 100%; border-bottom: 1px solid #333; background: #111; }
        .main-ui { width: 95%; max-width: 1100px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 20px; transition: 0.5s; }
        
        .video-box { position: relative; width: 100%; transition: all 0.5s ease; }
        video { width: 100%; border: 2px solid #00ff00; border-radius: 12px; background: #000; box-shadow: 0 0 15px #0f03; cursor: pointer; }
        
        /* Friend's Screen Big Mode */
        .big-mode { grid-column: span 2; width: 100%; }
        .small-mode { display: none; } /* Choti screen ko hide karne ke liye option */

        .controls-panel { grid-column: span 2; background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; text-align: center; }
        input { background: #000; border: 1px solid #00ff00; color: #00ff00; padding: 10px; border-radius: 5px; outline: none; margin: 5px; width: 180px; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 5px; transition: 0.3s; font-size: 12px; }
        .btn-call { background: #00ff00; color: #000; }
        .btn-hangup { background: #ff0000; color: #fff; }
        .btn-tool { background: #333; color: #fff; border: 1px solid #555; }
        .status { color: yellow; font-size: 0.8rem; margin-top: 5px; }
        .peer-id-badge { background: #00ff00; color: #000; padding: 3px 12px; border-radius: 20px; font-weight: bold; }
        
        .hint { font-size: 10px; color: #888; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h2 style="margin:0;">GHOST_VIDEO_PRO_V6</h2>
        <div id="status-text" class="status">Initializing...</div>
    </div>

    <div class="main-ui" id="ui-grid">
        <div class="video-box" id="local-box">
            <p style="text-align:center; font-size:12px;">LOCAL_STREAM (YOU)</p>
            <video id="local-video" autoplay muted playsinline></video>
        </div>
        <div class="video-box" id="remote-box">
            <p style="text-align:center; font-size:12px;">REMOTE_STREAM (CLICK TO ENLARGE)</p>
            <video id="remote-video" autoplay playsinline onclick="toggleBigMode()"></video>
        </div>

        <div class="controls-panel">
            <div style="margin-bottom: 10px;">
                YOUR ID: <span id="my-id" class="peer-id-badge">...</span>
            </div>
            <input type="text" id="remote-id" placeholder="Friend's ID">
            <button class="btn btn-call" onclick="makeCall()">📞 START CALL</button>
            <button class="btn btn-hangup" onclick="location.reload()">🛑 RESET</button>
            <br>
            <button class="btn btn-tool" onclick="toggleMic()">🎤 Mic</button>
            <button class="btn btn-tool" onclick="toggleVid()">📷 Cam</button>
            <button class="btn btn-tool" style="background: #007bff;" onclick="shareScreen()">📺 SHARE SCREEN</button>
            <p class="hint">Android Tip: Use "Desktop Site" mode for best Screen Share results.</p>
        </div>
    </div>

<script>
    const statusText = document.getElementById('status-text');
    const myIdDisplay = document.getElementById('my-id');
    const localVideo = document.getElementById('local-video');
    const remoteVideo = document.getElementById('remote-video');
    const remoteBox = document.getElementById('remote-box');
    const localBox = document.getElementById('local-box');
    
    let peer, localStream, currentCall;

    async function initCamera() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            localVideo.srcObject = localStream;
            statusText.innerText = "System Ready.";
            setupPeer();
        } catch (err) { statusText.innerText = "Mic/Cam Error!"; }
    }

    function setupPeer() {
        peer = new Peer();
        peer.on('open', id => { myIdDisplay.innerText = id; statusText.innerText = "Online."; });
        peer.on('call', call => {
            call.answer(localStream);
            handleConnection(call);
        });
    }

    function handleConnection(call) {
        currentCall = call;
        call.on('stream', stream => {
            remoteVideo.srcObject = stream;
            statusText.innerText = "Connected.";
        });
    }

    function makeCall() {
        const rid = document.getElementById('remote-id').value;
        if(!rid) return;
        const call = peer.call(rid, localStream);
        handleConnection(call);
    }

    // Android/Windows Screen Share
    async function shareScreen() {
        try {
            // Android par bhi Chrome popup dega "Start Recording/Casting" ka
            const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
            if(currentCall) {
                const videoTrack = screenStream.getVideoTracks()[0];
                const sender = currentCall.peerConnection.getSenders().find(s => s.track.kind === 'video');
                sender.replaceTrack(videoTrack);
            }
            localVideo.srcObject = screenStream;
            statusText.innerText = "Sharing Screen...";
        } catch (e) { alert("Screen Share Cancelled or Not Supported."); }
    }

    // Big/Small Mode Toggle
    function toggleBigMode() {
        remoteBox.classList.toggle('big-mode');
        if(remoteBox.classList.contains('big-mode')) {
            localBox.style.display = 'none'; // Jab friend badi screen ho toh apni hide kardo
            statusText.innerText = "Big Screen Mode (Click video to minimize)";
        } else {
            localBox.style.display = 'block';
            statusText.innerText = "Split Mode";
        }
    }

    function toggleMic() {
        const t = localStream.getAudioTracks()[0];
        t.enabled = !t.enabled;
        statusText.innerText = t.enabled ? "Mic On" : "Mic Off";
    }

    function toggleVid() {
        const t = localStream.getVideoTracks()[0];
        t.enabled = !t.enabled;
        statusText.innerText = t.enabled ? "Cam On" : "Cam Off";
    }

    initCamera();
</script>
</body>
</html>
"""

@script6_bp.route('/')
def script6_home():
    return render_template_string(INTERFACE)
