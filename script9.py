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
            SET PRIVATE NO: <input type="text" id="my-custom-id" placeholder="Ex: 007, 999" style="width:50px; padding:5px; margin-bottom:0;">
            <button onclick="setPrivateID()" style="width:auto; padding:5px; font-size:10px;">SET</button>
        </div>
        
        <p id="status">NETWORK STATUS: <span id="stat-val" style="color:red;">OFFLINE</span></p>

        <input type="text" id="remote-id" placeholder="Enter Target Private Number">
        <br>
        <button class="btn-call" onclick="makeAudioCall()">DIAL NOW</button>
        <button class="btn-hangup" onclick="location.reload()">END CALL</button>
        <br>
        <button class="btn-rec" id="rec-btn" onclick="toggleRecording()" disabled>🔴 START RECORDING</button>
        
        <div id="incoming-call">
            <h3 style="color:red; margin:0;">⚠️ INCOMING CALL</h3>
            <p style="color:white; font-size:18px;">PRIVATE NUMBER</p>
            <button class="btn-call" style="width:80%;" onclick="answerCall()">ACCEPT</button>
        </div>
    </div>

<script>
    let peer, localStream, remoteStream, incomingCallObj;
    let mediaRecorder, chunks = [];
    const statVal = document.getElementById('stat-val');
    const recBtn = document.getElementById('rec-btn');

    async function initMic() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            statVal.innerText = "MIC ACTIVE";
            statVal.style.color = "yellow";
        } catch (e) { 
            statVal.innerText = "MIC ERROR! Check Permissions."; 
            console.error(e);
        }
    }

    function setPrivateID() {
        const customId = document.getElementById('my-custom-id').value;
        if(!customId) return alert("Number daal bhai!");
        if(peer) peer.destroy();
        
        peer = new Peer(customId); 
        
        peer.on('open', id => {
            statVal.innerText = "ONLINE AS: " + id;
            statVal.style.color = "#0f0";
        });

        peer.on('call', call => {
            incomingCallObj = call;
            document.getElementById('incoming-call').style.display = "block";
            document.getElementById('call-icon').innerText = "🔔";
            // Vibration alert for mobile
            if(navigator.vibrate) navigator.vibrate([500, 200, 500]);
        });

        peer.on('error', err => {
            console.error(err);
            alert("Error: " + err.type);
        });
    }

    function makeAudioCall() {
        const rid = document.getElementById('remote-id').value;
        if(!rid) return alert("Dost ka number toh daal!");
        if(!peer) return alert("Pehle SET dabake online aao!");
        
        const call = peer.call(rid, localStream);
        setupCallListeners(call);
    }

    function answerCall() {
        incomingCallObj.answer(localStream);
        document.getElementById('incoming-call').style.display = "none";
        setupCallListeners(incomingCallObj);
    }

    function setupCallListeners(call) {
        statVal.innerText = "CONNECTING...";
        
        call.on('stream', s => {
            remoteStream = s;
            const audio = new Audio();
            audio.srcObject = s;
            audio.play().catch(e => console.error("Audio Play Error:", e));
            
            statVal.innerText = "CONNECTED";
            statVal.style.color = "#0f0";
            recBtn.disabled = false; 
            document.getElementById('call-icon').innerText = "🔊";
        });

        call.on('close', () => {
            statVal.innerText = "CALL ENDED";
            recBtn.disabled = true;
        });
    }

    function toggleRecording() {
        if (!mediaRecorder || mediaRecorder.state === "inactive") {
            startRecording();
        } else {
            stopRecording();
        }
    }

    function startRecording() {
        if(!remoteStream) return alert("No remote stream found!");
        chunks = [];
        try {
            mediaRecorder = new MediaRecorder(remoteStream);
            mediaRecorder.ondataavailable = e => { if(e.data.size > 0) chunks.push(e.data); };
            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: 'audio/webm' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = `Ghost_Record_${Date.now()}.webm`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            };
            mediaRecorder.start();
            recBtn.innerText = "⏹️ STOP RECORDING";
            recBtn.classList.add('rec-active');
        } catch (e) {
            alert("Recording Error: " + e.message);
        }
    }

    function stopRecording() {
        if(mediaRecorder) mediaRecorder.stop();
        recBtn.innerText = "🔴 START RECORDING";
        recBtn.classList.remove('rec-active');
    }

    initMic();
</script>
</body>
</html>
"""

@script9_bp.route('/')
def script9_home():
    return render_template_string(INTERFACE)
