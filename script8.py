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
    <title>Ghost Master V8 - Ultimate OSINT</title>
    <style>
        :root { --glow: #00ff00; --bg: #050505; }
        body { background: var(--bg); color: var(--glow); font-family: 'Courier New', monospace; margin: 0; padding: 15px; font-size: 13px; }
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px; }
        .card { border: 1px solid var(--glow); padding: 12px; background: #000; box-shadow: 0 0 8px #0f02; }
        .card h3 { border-bottom: 1px solid var(--glow); padding-bottom: 5px; margin-top: 0; font-size: 14px; color: #fff; }
        .terminal { height: 180px; overflow-y: auto; color: #0f0; background: #080808; padding: 8px; border: 1px solid #222; white-space: pre-wrap; }
        button { background: var(--glow); color: #000; border: none; padding: 8px 12px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 5px; }
        .highlight { color: yellow; }
    </style>
</head>
<body onload="initSystem()">

    <h2 style="text-align: center; text-shadow: 0 0 10px #0f0;">GHOST_SYSTEM_EXTRACTOR_V8</h2>

    <div class="grid-container">
        <div class="card">
            <h3>OS & Hardware (A-Z)</h3>
            <div id="hw-info" class="terminal">Scanning...</div>
        </div>

        <div class="card">
            <h3>Display & Graphics</h3>
            <div id="gpu-info" class="terminal">Scanning...</div>
        </div>

        <div class="card">
            <h3>Power & Network</h3>
            <div id="net-info" class="terminal">Scanning...</div>
        </div>

        <div class="card">
            <h3>IP & ISP Intelligence</h3>
            <div id="ip-info" class="terminal">Scanning...</div>
            <button onclick="getExactLocation()">GET GPS COORDINATES</button>
        </div>
    </div>

    <div class="card" style="margin-top: 15px;">
        <h3>Master Extraction Logs</h3>
        <div id="master-logs" class="terminal" style="height: 100px;">[#] Ghost Kernel v8.0 Booting...</div>
    </div>

<script>
    const logs = document.getElementById('master-logs');
    function addLog(msg) { logs.innerText += `\\n[>] ${msg}`; logs.scrollTop = logs.scrollHeight; }

    async function initSystem() {
        addLog("Analyzing System Architecture...");

        // 1. Hardware & OS Details
        const hw = {
            "OS_Platform": navigator.platform,
            "OS_Core_Version": navigator.appVersion,
            "CPU_Cores": navigator.hardwareConcurrency || "Hidden",
            "RAM_Size": navigator.deviceMemory ? navigator.deviceMemory + " GB" : "Protected",
            "User_Agent": navigator.userAgent,
            "Language": navigator.language,
            "Cookies_Enabled": navigator.cookieEnabled
        };
        document.getElementById('hw-info').innerText = JSON.stringify(hw, null, 2);

        // 2. Display & GPU
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl');
        const debugInfo = gl ? gl.getExtension('WEBGL_debug_renderer_info') : null;
        const gpu = {
            "Resolution": `${screen.width}x${screen.height}`,
            "Available_Res": `${screen.availWidth}x${screen.availHeight}`,
            "Color_Depth": screen.colorDepth + " bit",
            "GPU_Vendor": debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : "N/A",
            "GPU_Renderer": debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "N/A"
        };
        document.getElementById('gpu-info').innerText = JSON.stringify(gpu, null, 2);

        // 3. Battery & Network
        try {
            const battery = await navigator.getBattery();
            const net = navigator.connection || {};
            const pwr = {
                "Battery_Level": (battery.level * 100) + "%",
                "Charging": battery.charging ? "Yes" : "No",
                "Network_Type": net.effectiveType || "Unknown",
                "Downlink": net.downlink + " Mbps",
                "RTT": net.rtt + " ms"
            };
            document.getElementById('net-info').innerText = JSON.stringify(pwr, null, 2);
        } catch(e) { document.getElementById('net-info').innerText = "Battery/Net API Blocked."; }

        // 4. IP Intelligence
        try {
            const res = await fetch('https://ipapi.co/json/');
            const data = await res.json();
            document.getElementById('ip-info').innerText = JSON.stringify(data, null, 2);
            addLog(`Target IP: ${data.ip}`);
        } catch(e) { addLog("IP Check Failed."); }
    }

    function getExactLocation() {
        addLog("Requesting GPS Permission...");
        navigator.geolocation.getCurrentPosition((p) => {
            addLog("GPS Locked Successfully.");
            window.open(`https://www.google.com/maps?q=${p.coords.latitude},${p.coords.longitude}`);
        }, (err) => { addLog("Location Access Denied."); });
    }
</script>
</body>
</html>
"""

@script8_bp.route('/')
def home():
    return render_template_string(INTERFACE)

