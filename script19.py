from flask import Blueprint, render_template_string, request, jsonify
import google.generativeai as genai

script19_bp = Blueprint('script19', __name__)

# --- SET YOUR API KEY HERE ---
genai.configure(api_key="AIzaSyDWwsvK7C_vN4bgBcNvV2EAYaKGXNq_iRI")
model = genai.GenerativeModel('gemini-pro')

JARVIS_ADVANCED_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS AI | Shivam Singh</title>
    <style>
        body { background: #000; color: #00ff00; font-family: 'Consolas', monospace; text-align: center; margin: 0; padding: 20px; }
        .hud-container { border: 2px solid #00ff00; max-width: 700px; margin: auto; padding: 20px; background: rgba(0, 10, 0, 0.9); box-shadow: 0 0 30px #00ff0044; }
        
        /* JARVIS CIRCLE ANIMATION */
        .ai-core { width: 150px; height: 150px; border: 3px solid #00ff00; border-radius: 50%; margin: 30px auto; position: relative; 
                  display: flex; align-items: center; justify-content: center; animation: spin 4s linear infinite; }
        .ai-core::after { content: ''; width: 120px; height: 120px; border: 2px dashed #00ff00; border-radius: 50%; position: absolute; animation: spin-rev 2s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes spin-rev { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
        
        #response-text { color: #fff; font-size: 18px; margin: 20px; min-height: 50px; text-shadow: 0 0 5px #00ff00; }
        .mic-btn { background: #00ff00; color: #000; padding: 20px 40px; font-weight: bold; border: none; cursor: pointer; border-radius: 50px; transition: 0.3s; }
        .mic-btn:hover { box-shadow: 0 0 20px #00ff00; transform: scale(1.05); }
        .mic-btn.active { background: #ff0000; animation: blink 1s infinite; }
        @keyframes blink { 50% { opacity: 0.5; } }
    </style>
</head>
<body>
    <div class="hud-container">
        <h1>[ JARVIS SYSTEM ONLINE ]</h1>
        <div class="ai-core"><div id="core-status">READY</div></div>
        
        <div id="response-text">Welcome back, Shivam Sir. Systems are standing by.</div>
        
        <button id="micBtn" class="mic-btn" onclick="toggleMic()">INITIALIZE VOICE COMMAND</button>
        
        <p style="font-size: 10px; color: #444; margin-top: 20px;">POWERED BY SHIVAM SINGH AI ENGINE</p>
    </div>

    <script>
        const responseText = document.getElementById('response-text');
        const micBtn = document.getElementById('micBtn');
        const coreStatus = document.getElementById('core-status');

        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.pitch = 0.7; // Deep/Heavy voice
            utter.rate = 1.1;
            synth.speak(utter);
        }

        async function getAIResponse(prompt) {
            coreStatus.innerText = "THINKING";
            try {
                const res = await fetch('/script19/ask', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: prompt})
                });
                const data = await res.json();
                return data.response;
            } catch (err) { return "Sir, there was an error in my neural network."; }
        }

        function toggleMic() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                micBtn.classList.add('active');
                micBtn.innerText = "LISTENING...";
                coreStatus.innerText = "LISTENING";
            };

            recognition.onresult = async (event) => {
                const transcript = event.results[0][0].transcript;
                responseText.innerText = "YOU: " + transcript;
                
                const aiMsg = await getAIResponse(transcript);
                responseText.innerText = "JARVIS: " + aiMsg;
                speak(aiMsg);
                coreStatus.innerText = "ACTIVE";
            };

            recognition.onend = () => {
                micBtn.classList.remove('active');
                micBtn.innerText = "INITIALIZE VOICE COMMAND";
            };

            recognition.start();
        }
    </script>
</body>
</html>
"""

@script19_bp.route('/')
def index():
    return render_template_string(JARVIS_ADVANCED_UI)

@script19_bp.route('/ask', methods=['POST'])
def ask():
    user_prompt = request.json.get('prompt')
    # AI Logic
    try:
        response = model.generate_content(f"You are JARVIS, a loyal and highly intelligent AI assistant for Shivam Singh. Answer this shortly and coolly: {user_prompt}")
        return jsonify({'response': response.text})
    except:
        return jsonify({'response': "Sir, connection to the mainframe is unstable."})
