import requests
import json
from flask import Blueprint, request, jsonify, render_template_string

script10_bp = Blueprint('script10', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Master V10 - OSINT Dashboard</title>
    <style>
        :root { --glow: #00ff00; --bg: #050505; }
        body { background: var(--bg); color: var(--glow); font-family: 'Courier New', monospace; margin: 0; padding: 20px; overflow-x: hidden; }
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .card { border: 1px solid var(--glow); padding: 15px; background: #000; box-shadow: 0 0 10px #0f02; position: relative; overflow: hidden; }
        .card h3 { border-bottom: 1px solid var(--glow); padding-bottom: 5px; margin-top: 0; font-size: 14px; text-transform: uppercase; }
        .terminal { height: 200px; overflow-y: auto; font-size: 12px; line-height: 1.5; color: #0f0; background: #080808; padding: 10px; border: 1px solid #222; }
        input { background: #000; border: 1px solid var(--glow); color: var(--glow); padding: 8px; width: 70%; outline: none; }
        button { background: var(--glow); color: #000; border: none; padding: 8px 15px; cursor: pointer; font-weight: bold; }
        .status-on { color: #0f0; font-weight: bold; }
        .blink { animation: blinker 1.5s linear infinite; color: red; }
        @keyframes blinker { 50% { opacity: 0; } }
        iframe { width: 100%; height: 200px; border: 1px solid #333; margin-top: 10px; }
    </style>
</head>
<body onload="initSystem()">

    <h1 style="text-align: center; text-shadow: 0 0 10px #0f0;">GHOST_MASTER_OSINT_V10</h1>
    <div style="text-align:center; margin-bottom: 20px;">
        <span class="status-on">[ SYSTEM ONLINE ]</span> | <span class="blink">[ ENCRYPTION ACTIVE ]</span>
    </div>

    <div class="grid-container">
        <div class="card">
            <h3>Device Fingerprint</h3>
            <div id="device-info" class="terminal">Fetching hardware data...</div>
        </div>

        <div class="card">
            <h3>IP Intelligence</h3>
            <div id="ip-info" class="terminal">Scanning network layers...</div>
        </div>

        <div class="card">
            <h3>GPS Precision Tracker</h3>
            <button onclick="getExactLocation()">REQUEST ACCESS</button>
            <div id="geo-info" class="terminal" style="height:120px; margin-top:10px;">Waiting for user permission...</div>
        </div>

        <div class="card">
            <h3>Phish/Sim Frame</h3>
            <input type="text" id="frame-url" placeholder="https://example.com">
            <button onclick="loadFrame()">LOAD</button>
            <iframe id="target-frame" src="https://www.bing.com"></iframe>
        </div>
    </div>

    <div class="card" style="margin-top: 15px;">
        <h3>Master System Logs</h3>
        <div id="master-logs" class="terminal" style="height: 150px;">[#] Ghost Kernel Loaded...\\n[#] Ready for input signals...</div>
    </div>

<script>
    const logs = document.getElementById('master-logs');
    
    function addLog(msg) {
        logs.innerText += `\\n[>] ${msg}`;
        logs.scrollTop = logs.scrollHeight;
    }

    async function initSystem() {
        addLog("Initializing Fingerprinting...");
        
        // Device Info
        const devInfo = {
            Platform: navigator.platform,
            Cores: navigator.hardwareConcurrency,
            Memory: navigator.deviceMemory + "GB",
            Language: navigator.language,
            Agent: navigator.userAgent
        };
        document.getElementById('device-info').innerText = JSON.stringify(devInfo, null, 2);
        
        // IP Info
        try {
            const res = await fetch('https://ipapi.co/json/');
            const data = await res.json();
            document.getElementById('ip-info').innerText = JSON.stringify(data, null, 2);
            addLog(`IP Detected: ${data.ip}`);
        } catch(e) { addLog("IP Scan Failed."); }
    }

    function getExactLocation() {
        addLog("Requesting GPS Permission...");
        navigator.geolocation.getCurrentPosition((p) => {
            const data = `Lat: ${p.coords.latitude}\\nLon: ${p.coords.longitude}\\nAcc: ${p.coords.accuracy}m`;
            document.getElementById('geo-info').innerText = data;
            addLog("GPS Coordinates Locked.");
            window.open(`https://www.google.com/maps?q=${p.coords.latitude},${p.coords.longitude}`, '_blank');
        }, (err) => {
            addLog("GPS Access Denied.");
            document.getElementById('geo-info').innerText = "User blocked access.";
        });
    }

    function loadFrame() {
        const url = document.getElementById('frame-url').value;
        if(url) {
            document.getElementById('target-frame').src = url;
            addLog(`Target Frame redirected to: ${url}`);
        }
    }
</script>
</body>
</html>
"""

@script10_bp.route('/')
def home():
    return render_template_string(INTERFACE)
