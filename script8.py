import requests
import json
from flask import Blueprint, request, jsonify, render_template_string

script8_bp = Blueprint('script8', __name__)

INTERFACE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Master V8.2 - Extreme OSINT</title>
    <style>
        :root { --glow: #00ff00; --bg: #050505; }
        body { background: var(--bg); color: var(--glow); font-family: 'Courier New', monospace; margin: 0; padding: 10px; font-size: 11px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; }
        .card { border: 1px solid var(--glow); padding: 10px; background: #000; box-shadow: 0 0 5px #0f02; }
        .card h3 { border-bottom: 1px solid var(--glow); padding-bottom: 3px; margin: 0 0 8px 0; font-size: 12px; color: #fff; text-transform: uppercase; }
        .row { display: flex; justify-content: space-between; border-bottom: 1px solid #111; padding: 3px 0; }
        .v { color: #ffff00; font-weight: bold; overflow-wrap: anywhere; text-align: right; margin-left: 10px; }
        button { background: var(--glow); color: #000; border: none; padding: 10px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 5px; text-transform: uppercase; }
        #logs { height: 70px; overflow-y: auto; background: #080808; padding: 5px; border: 1px solid #222; margin-top: 10px; color: #0f0; }
    </style>
</head>
<body onload="extractAll()">

    <h2 style="text-align: center; margin: 5px 0;">GHOST_EXTRACTOR_V8.2_EXTREME</h2>

    <div class="grid">
        <div class="card">
            <h3>💻 Hardware & OS</h3>
            <div id="hw"></div>
        </div>

        <div class="card">
            <h3>📍 Real-Time GPS</h3>
            <div id="loc">
                <div class="row"><span>Status:</span><span class="v" id="st">Ready</span></div>
                <div class="row"><span>Lat:</span><span class="v" id="lat">N/A</span></div>
                <div class="row"><span>Lon:</span><span class="v" id="lon">N/A</span></div>
                <div class="row"><span>Acc:</span><span class="v" id="acc">N/A</span></div>
            </div>
            <button onclick="getGPS()">Lock Coordinates</button>
        </div>

        <div class="card">
            <h3>🎮 Graphics & UI</h3>
            <div id="ui"></div>
        </div>

        <div class="card">
            <h3>🔋 Net & Power</h3>
            <div id="np"></div>
        </div>

        <div class="card">
            <h3>🛡️ Security & Social</h3>
            <div id="ss"></div>
        </div>
    </div>

    <div class="card" style="margin-top: 10px;">
        <h3>📜 System Master Logs</h3>
        <div id="logs"></div>
    </div>

<script>
    const l = document.getElementById('logs');
    function log(m) { l.innerText += `\\n[>] ${m}`; l.scrollTop = l.scrollHeight; }

    function add(id, k, v) {
        document.getElementById(id).innerHTML += `<div class="row"><span>${k}:</span><span class="v">${v}</span></div>`;
    }

    async function extractAll() {
        log("Booting Extraction Engine...");

        // Hardware
        add('hw', 'Model', navigator.platform);
        add('hw', 'Cores', navigator.hardwareConcurrency || 'N/A');
        add('hw', 'RAM', (navigator.deviceMemory || 'N/A') + ' GB');
        add('hw', 'Touch', navigator.maxTouchPoints > 0 ? 'Yes' : 'No');
        add('hw', 'UA', navigator.userAgent.substring(0, 30) + '...');

        // UI & GPU
        const c = document.createElement('canvas');
        const g = c.getContext('webgl');
        const d = g ? g.getExtension('WEBGL_debug_renderer_info') : null;
        add('ui', 'Res', `${screen.width}x${screen.height}`);
        add('ui', 'Ratio', window.devicePixelRatio);
        add('ui', 'GPU', d ? g.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'N/A');
        add('ui', 'Orient', screen.orientation ? screen.orientation.type : 'N/A');

        // Power & Net
        if(navigator.getBattery) {
            const b = await navigator.getBattery();
            add('np', 'Battery', Math.round(b.level * 100) + '%');
            add('np', 'Plugged', b.charging ? 'Yes' : 'No');
        }
        const n = navigator.connection || {};
        add('np', 'Speed', (n.downlink || 'N/A') + ' Mbps');
        add('np', 'Type', n.effectiveType || 'N/A');

        // Security & Social
        add('ss', 'AdBlock', (window.canRunAds === undefined) ? 'Detected' : 'None');
        add('ss', 'Incognito', 'Check Logs'); 
        
        // IP Info
        try {
            const r = await fetch('https://ipapi.co/json/');
            const j = await r.json();
            log(`Carrier: ${j.org}`);
            log(`IP: ${j.ip}`);
            add('ss', 'ISP', j.org);
            add('ss', 'City', j.city);
        } catch(e) { log("IP Scan Blocked."); }
    }

    function getGPS() {
        document.getElementById('st').innerText = "Requesting...";
        log("Bypassing GPS Layer...");
        navigator.geolocation.getCurrentPosition((p) => {
            document.getElementById('st').innerText = "LOCKED";
            document.getElementById('lat').innerText = p.coords.latitude;
            document.getElementById('lon').innerText = p.coords.longitude;
            document.getElementById('acc').innerText = p.coords.accuracy.toFixed(1) + "m";
            log("Exact Coordinates Extracted.");
            window.open(`https://www.google.com/maps?q=${p.coords.latitude},${p.coords.longitude}`);
        }, (e) => {
            document.getElementById('st').innerText = "DENIED";
            log("User rejected location.");
        }, {enableHighAccuracy: true});
    }
</script>
</body>
</html>
"""

@script8_bp.route('/')
def home():
    return render_template_string(INTERFACE)
