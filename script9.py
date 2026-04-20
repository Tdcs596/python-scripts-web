from flask import Blueprint, render_template_string

script9_bp = Blueprint('script9', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Private Caller - V9 REC</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 20px; }
        .call-card { background: #111; border: 2px solid #00ff00; display: inline-block; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #0f02; width: 90%; max-width: 400px; }
        .avatar { width: 80px; height: 80px; background: #00ff00; border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: #000; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 80%; border-radius: 5px; margin-bottom: 10px; text-align: center; outline: none; }
        button { padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 5px; width: 45%; transition: 0.3s; }
        .btn-call { background: #00ff00; color: #000; }
        .btn-hangup { background: #ff0000; color: #fff; }
        .btn-ctrl { background: #222; color: #0f0; border: 1px solid #0f0; font-size: 11px; }
        .active-off { border-color: red !important; color: red !important; }
        .btn-rec { background: #555; color: white; width: 93%; margin-top: 10px; }
        .rec-active { background: #ff0000 !important; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        #incoming-call { display: none; background: #222; border: 1px dashed red; padding: 15px; margin-top: 15px; border-radius: 10px; }
        #status { font-size: 11px; color: #888; }
    </style>
</head>
<body>
    <div class="call-card">
        <div class="avatar" id="call-icon">📞</div>
        <h2>GHOST_PRIVATE_CALL_V9</h2>
        
        <div style="font-size:11px; margin-bottom:15px; color:#aaa;">
            SET PRIVATE NO: <input type="text" id="my-custom-id" placeholder="Ex: 007" style="width:50px; padding:5px; margin-bottom:0;">
            <button onclick="setPrivateID()" style="width:auto; padding:5px; font-size:10px;">SET</button>
        </div>
        
        <p id="status">STATUS: <span id="stat-val" style="color:red;">OFFLINE</span></p>

        <div style="margin-bottom: 15px;">
            <button id="mic-toggle" class="btn-ctrl" onclick="toggleMic()">🎤 MIC: ON</button>
            <button id="spk-toggle" class="btn-ctrl" onclick="toggleSpeaker()">🔊 SPK: ON</button>
        </div>

        <input type="text" id="remote-id" placeholder="Enter Target Private Number">
        <br>
        <button class="btn-call" onclick="makeAudioCall()">DIAL NOW</button>
        <button class="btn-hangup" onclick="location.reload()">END CALL</button>
        <br>
        <button class="btn-rec" id="rec-btn" onclick="toggleRecording()" disabled>🔴 START RECORDING</button>
        
        <div id="incoming-call">
            <h3 style="color:red; margin:0;">⚠️ INCOMING CALL</h3>
            <button class="btn-call" style="width:80%;" onclick="answerCall()">ACCEPT</button>
        </div>
    </div>

    <audio id="remote-audio" autoplay></audio>

<script>
    let peer, localStream, remoteStream, incomingCallObj;
    let mediaRecorder, chunks = [];
    let micEnabled = true;
    let spkEnabled = true;

    const statVal = document.getElementById('stat-val');
    const recBtn = document.getElementById('rec-btn');
    const remoteAudio = document.getElementById('remote-audio');

    async function initMic() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            statVal.innerText = "MIC READY";
            statVal.style.color = "yellow";
        } catch (e) { statVal.innerText = "MIC ERROR"; }
    }

    // SPEAKER ON/OFF LOGIC
    function toggleSpeaker() {
        spkEnabled = !spkEnabled;
        remoteAudio.muted = !spkEnabled;
        const btn = document.getElementById('spk-toggle');
        btn.innerText = spkEnabled ? "🔊 SPK: ON" : "🔇 SPK: OFF";
        btn.classList.toggle('active-off', !spkEnabled);
    }

    // MIC ON/OFF LOGIC
    function toggleMic() {
        if(!localStream) return;
        micEnabled = !micEnabled;
        localStream.getAudioTracks()[0].enabled = micEnabled;
        const btn = document.getElementById('mic-toggle');
        btn.innerText = micEnabled ? "🎤 MIC: ON" : "🚫 MIC: OFF";
        btn.classList.toggle('active-off', !micEnabled);
    }

    function setPrivateID() {
        const customId = document.getElementById('my-custom-id').value;
        if(!customId) return;
        peer = new Peer(customId); 
        peer.on('open', id => {
            statVal.innerText = "ONLINE: " + id;
            statVal.style.color = "#0f0";
        });
        peer.on('call', call => {
            incomingCallObj = call;
            document.getElementById('incoming-call').style.display = "block";
        });
    }

    function makeAudioCall() {
        const rid = document.getElementById('remote-id').value;
        const call = peer.call(rid, localStream);
        setupCall(call);
    }

    function answerCall() {
        incomingCallObj.answer(localStream);
        document.getElementById('incoming-call').style.display = "none";
        setupCall(incomingCallObj);
    }

    function setupCall(call) {
        call.on('stream', s => {
            remoteStream = s;
            remoteAudio.srcObject = s;
            statVal.innerText = "CONNECTED";
            statVal.style.color = "#0f0";
            recBtn.disabled = false;
        });
    }

    // Recording logic (unchanged as requested)
    function toggleRecording() {
        if (!mediaRecorder || mediaRecorder.state === "inactive") {
            chunks = [];
            mediaRecorder = new MediaRecorder(remoteStream);
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'audio/webm' });
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = `Ghost_Call_${Date.now()}.webm`;
                a.click();
            };
            mediaRecorder.start();
            recBtn.innerText = "⏹️ STOP RECORDING";
            recBtn.classList.add('rec-active');
        } else {
            mediaRecorder.stop();
            recBtn.innerText = "🔴 START RECORDING";
            recBtn.classList.remove('rec-active');
        }
    }

    initMic();
</script>
</body>
</html>
"""

@script9_bp.route('/')
def script9_home():
    return render_template_string(INTERFACE)
