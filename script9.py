from flask import Blueprint, render_template_string

# Blueprint ka naam script9 kar diya hai
script9_bp = Blueprint('script9', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Private Caller - V9</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Courier New', monospace; text-align: center; margin: 0; padding: 20px; }
        .call-card { background: #111; border: 2px solid #00ff00; display: inline-block; padding: 30px; border-radius: 20px; box-shadow: 0 0 30px #0f02; width: 90%; max-width: 400px; }
        .avatar { width: 80px; height: 80px; background: #00ff00; border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 40px; color: #000; }
        .status-dot { width: 10px; height: 10px; background: #0f0; border-radius: 50%; display: inline-block; margin-right: 5px; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 12px; width: 80%; border-radius: 5px; margin-bottom: 10px; text-align: center; outline: none; }
        button { padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; margin: 5px; width: 45%; transition: 0.3s; }
        .btn-call { background: #00ff00; color: #000; }
        .btn-hangup { background: #ff0000; color: #fff; }
        #incoming-call { display: none; background: #222; border: 1px dashed red; padding: 15px; margin-top: 15px; border-radius: 10px; animation: shake 0.5s infinite; }
        @keyframes shake { 0% { transform: translate(1px, 1px); } 10% { transform: translate(-1px, -2px); } 100% { transform: translate(1px, 1px); } }
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
        
        <p style="font-size:11px; color:#888;">NETWORK STATUS: <span id="status">OFFLINE</span></p>

        <input type="text" id="remote-id" placeholder="Enter Target Private Number">
        <br>
        <button class="btn-call" onclick="makeAudioCall()">DIAL NOW</button>
        <button class="btn-hangup" onclick="location.reload()">END CALL</button>
        
        <div id="incoming-call">
            <h3 style="color:red; margin:0;">⚠️ INCOMING CALL</h3>
            <p id="caller-name" style="color:white; font-size:18px;">PRIVATE NUMBER</p>
            <button class="btn-call" style="width:80%;" onclick="answerCall()">ACCEPT</button>
        </div>
    </div>

<script>
    let peer, localStream, currentCall, incomingCallObj;
    const statusText = document.getElementById('status');
    const incomingDiv = document.getElementById('incoming-call');

    async function initMic() {
        try {
            localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            statusText.innerText = "MIC ACTIVE";
        } catch (e) { statusText.innerText = "MIC ERROR!"; }
    }

    function setPrivateID() {
        const customId = document.getElementById('my-custom-id').value;
        if(!customId) return alert("Kuch number daal bhai!");
        
        if(peer) peer.destroy();
        
        // Peer creation with custom private number
        peer = new Peer(customId); 
        
        peer.on('open', id => {
            statusText.innerText = "ONLINE AS: " + id;
            statusText.style.color = "#0f0";
        });

        peer.on('call', call => {
            incomingCallObj = call;
            incomingDiv.style.display = "block";
            // Vibration & Sound alert
            if (navigator.vibrate) navigator.vibrate([500, 200, 500]);
            document.getElementById('call-icon').innerText = "🔔";
        });

        peer.on('error', err => {
            alert("This Number is already taken! Try another.");
            statusText.innerText = "ID TAKEN";
        });
    }

    function makeAudioCall() {
        const rid = document.getElementById('remote-id').value;
        if(!localStream) return alert("Pehle Mic toh allow kar!");
        if(!peer) return alert("Pehle apna Private Number SET kar!");
        
        const call = peer.call(rid, localStream);
        statusText.innerText = "DIALING " + rid + "...";
        
        call.on('stream', s => {
            const audio = new Audio();
            audio.srcObject = s;
            audio.play();
            statusText.innerText = "IN CALL WITH " + rid;
        });
    }

    function answerCall() {
        incomingCallObj.answer(localStream);
        incomingDiv.style.display = "none";
        statusText.innerText = "CALL CONNECTED";
        
        incomingCallObj.on('stream', s => {
            const audio = new Audio();
            audio.srcObject = s;
            audio.play();
        });
    }

    initMic();
</script>
</body>
</html>
"""

@script9_bp.route('/')
def script9_home():
    return render_template_string(INTERFACE)

