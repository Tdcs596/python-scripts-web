from flask import Blueprint, render_template_string

script7_bp = Blueprint('script7', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Script7 - Private Call & Recorder</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 20px; }
        .call-card { background: #111; border: 2px solid #00ff00; display: inline-block; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #0f02; width: 90%; max-width: 400px; }
        .avatar { width: 80px; height: 80px; background: #00ff00; border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: #000; }
        .rec-pulse { width: 12px; height: 12px; background: red; border-radius: 50%; display: inline-block; visibility: hidden; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 80%; border-radius: 5px; margin-bottom: 15px; text-align: center; outline: none; }
        button { padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 5px; width: 45%; transition: 0.3s; }
        .btn-call { background: #00ff00; color: #000; }
        .btn-hangup { background: #ff0000; color: #fff; }
        .btn-rec { background: #444; color: white; width: 93%; }
        #status { font-size: 12px; color: yellow; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="call-card">
        <div class="avatar">📞</div>
        <div id="rec-indicator"><span class="rec-pulse" id="pulse"></span> <small id="rec-text">NOT RECORDING</small></div>
        <h2 style="margin: 10px 0;">GHOST_CALL_REC</h2>
        
        <p style="font-size:11px; color:#888;">YOUR ID: <b id="my-id" style="color:#fff;">...</b></p>

        <input type="text" id="remote-id" placeholder="Paste Friend's ID">
        <br>
        <button class="btn-call" onclick="makeAudioCall()">CALL</button>
        <button class="btn-hangup" onclick="location.reload()">END</button>
        <br>
        <button class="btn-rec" id="recBtn" onclick="toggleRecording()" disabled>🔴 START RECORDING</button>
        
        <p id="status">Initializing Mic...</p>
    </div>

<script>
    let peer, localStream, remoteStream, currentCall;
    let mediaRecorder, chunks = [];
    const statusText = document.getElementById('status');
    const recBtn = document.getElementById('recBtn');

    async function init() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            statusText.innerText = "System Ready.";
            setupPeer();
        } catch (e) { statusText.innerText = "Mic Error!"; }
    }

    function setupPeer() {
        peer = new Peer();
        peer.on('open', id => document.getElementById('my-id').innerText = id);
        peer.on('call', call => {
            if(confirm("Accept Call?")) {
                call.answer(localStream);
                handleCall(call);
            }
        });
    }

    function handleCall(call) {
        currentCall = call;
        recBtn.disabled = false; // Call connect hone par recording enable
        call.on('stream', s => {
            remoteStream = s;
            const audio = new Audio();
            audio.srcObject = s;
            audio.play();
            statusText.innerText = "Connected.";
        });
    }

    function makeAudioCall() {
        const rid = document.getElementById('remote-id').value;
        const call = peer.call(rid, localStream);
        handleCall(call);
    }

    // --- RECORDING LOGIC ---
    function toggleRecording() {
        if (!mediaRecorder || mediaRecorder.state === "inactive") {
            startRecording();
        } else {
            stopRecording();
        }
    }

    function startRecording() {
        chunks = [];
        // Dono stream mix karna thoda tough hai, isliye hum Remote (dost) ki voice record karenge
        // Kyunki teri voice toh tere pas already hai.
        mediaRecorder = new MediaRecorder(remoteStream);
        
        mediaRecorder.ondataavailable = e => chunks.push(e.data);
        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, { type: 'audio/webm' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Ghost_Call_Record_${Date.now()}.webm`;
            a.click();
        };

        mediaRecorder.start();
        recBtn.innerText = "⏹️ STOP RECORDING";
        recBtn.style.background = "red";
        document.getElementById('pulse').style.visibility = "visible";
        document.getElementById('rec-text').innerText = "RECORDING ACTIVE";
    }

    function stopRecording() {
        mediaRecorder.stop();
        recBtn.innerText = "🔴 START RECORDING";
        recBtn.style.background = "#444";
        document.getElementById('pulse').style.visibility = "hidden";
        document.getElementById('rec-text').innerText = "SAVING FILE...";
    }

    init();
</script>
</body>
</html>
"""

@script7_bp.route('/')
def script7_home():
    return render_template_string(INTERFACE)

