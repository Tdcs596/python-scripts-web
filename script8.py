from flask import Blueprint, render_template_string, request, jsonify
import json
import logging

script8_bp = Blueprint('script8', __name__)

# GHOST MASTER INTERFACE UTILS - USING RAW STRINGS TO SHIELD SPECIAL CHARACTERS
INTERFACE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ghost Master V8.5 - Extreme Diagnostic OSINT</title>
    <style>
        :root { --glow: #00ff00; --bg: #030303; --card-bg: #09090b; --border-color: #16a34a; }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: var(--bg); color: var(--glow); font-family: 'Consolas', 'Courier New', monospace; padding: 20px; font-size: 12px; }
        .terminal-header { text-align: center; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px dashed var(--border-color); }
        .terminal-header h2 { font-size: 24px; text-transform: uppercase; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0, 255, 0, 0.3); }
        .terminal-header p { color: #888; font-size: 11px; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px; }
        
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 15px; }
        .card { border: 1px solid #1f2937; padding: 15px; background: var(--card-bg); border-radius: 6px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); transition: border-color 0.3s; }
        .card:hover { border-color: var(--border-color); }
        .card h3 { border-bottom: 1px solid #1f2937; padding-bottom: 6px; margin-bottom: 10px; font-size: 13px; color: #fff; text-transform: uppercase; display: flex; justify-content: space-between; }
        
        .row { display: flex; justify-content: space-between; border-bottom: 1px solid #111; padding: 5px 0; align-items: center; }
        .row span:first-child { color: #86efac; }
        .v { color: #ffff00; font-weight: bold; overflow-wrap: anywhere; text-align: right; margin-left: 10px; }
        
        button { background: var(--border-color); color: #000; border: none; padding: 12px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; text-transform: uppercase; border-radius: 4px; font-family: inherit; font-size: 11px; transition: 0.2s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        
        .console-box { margin-top: 20px; border: 1px solid #1f2937; border-radius: 6px; background: #000; }
        .console-title { background: #111; padding: 8px 15px; border-bottom: 1px solid #1f2937; font-size: 11px; text-transform: uppercase; color: #aaa; }
        #logs { height: 120px; overflow-y: auto; padding: 12px; color: #22c55e; font-size: 11px; line-height: 1.6; }
    </style>
</head>
<body onload="initializeDiagnostics()">

    <div class="terminal-header">
        <h2>⚡ GHOST MASTER SYSTEM PLATFORM V8.5 ⚡</h2>
        <p>Shivam Singh Omega Dashboard • Advanced Client Diagnostics Suite</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>💻 CORE HARDWARE MATRIX</h3>
            <div id="hw-matrix"></div>
        </div>

        <div class="card">
            <h3>📍 GEOLOCATION INFRASTRUCTURE</h3>
            <div id="loc-matrix">
                <div class="row"><span>Status:</span><span class="v" id="geo-status">STANDBY</span></div>
                <div class="row"><span>Latitude:</span><span class="v" id="geo-lat">N/A</span></div>
                <div class="row"><span>Longitude:</span><span class="v" id="geo-lon">N/A</span></div>
                <div class="row"><span>Accuracy Ring:</span><span class="v" id="geo-acc">N/A</span></div>
                <div class="row"><span>Timestamp:</span><span class="v" id="geo-time">N/A</span></div>
            </div>
            <button onclick="triggerGPSLock()">Lock Precise Coordinates</button>
        </div>

        <div class="card">
            <h3>🎮 GRAPHICS & SCREEN DISPLAY</h3>
            <div id="display-matrix"></div>
        </div>

        <div class="card">
            <h3>🔋 NETWORK METRICS & POWER</h3>
            <div id="net-matrix"></div>
        </div>

        <div class="card">
            <h3>🛡️ LOCAL AGENT CONFIGURATION</h3>
            <div id="agent-matrix"></div>
        </div>

        <div class="card">
            <h3>💾 BROWSER STORAGE QUOTA</h3>
            <div id="storage-matrix"></div>
        </div>
    </div>

    <div class="console-box">
        <div class="console-title">📜 System Stream Engine Logs</div>
        <div id="logs"></div>
    </div>

<script>
    const logContainer = document.getElementById('logs');
    
    function streamLog(message) {
        const timestamp = new Date().toISOString().slice(11, 19);
        logContainer.innerHTML += `[${timestamp}] [>] ${message}<br>`;
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    function insertRow(targetId, parameter, value) {
        const container = document.getElementById(targetId);
        if (container) {
            container.innerHTML += `<div class="row"><span>${parameter}:</span><span class="v">${value}</span></div>`;
        }
    }

    async function initializeDiagnostics() {
        streamLog("Booting diagnostic processing core...");

        // 1. Core Hardware Profiling
        insertRow('hw-matrix', 'Platform Architecture', navigator.platform || 'N/A');
        insertRow('hw-matrix', 'Logical CPU Cores', navigator.hardwareConcurrency || 'N/A');
        insertRow('hw-matrix', 'Allocated Device RAM', (navigator.deviceMemory ? navigator.deviceMemory + ' GB' : 'N/A'));
        insertRow('hw-matrix', 'Touch Input Nodes', navigator.maxTouchPoints || '0');
        insertRow('hw-matrix', 'Language Node Code', navigator.language || 'N/A');

        // 2. Advanced Graphics Engine Discovery
        const canvas = document.createElement('canvas');
        const glContext = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        let gpuVendor = 'N/A';
        let gpuRenderer = 'N/A';
        
        if (glContext) {
            const debugInfo = glContext.getExtension('WEBGL_debug_renderer_info');
            if (debugInfo) {
                gpuVendor = glContext.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
                gpuRenderer = glContext.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
            }
        }
        
        insertRow('display-matrix', 'Screen Resolution', `${screen.width}x${screen.height}`);
        insertRow('display-matrix', 'Available Bounds', `${screen.availWidth}x${screen.availHeight}`);
        insertRow('display-matrix', 'Device Pixel Ratio', window.devicePixelRatio || '1');
        insertRow('display-matrix', 'Color Depth Bit depth', `${screen.colorDepth} bits`);
        insertRow('display-matrix', 'GPU Sub-Renderer', gpuRenderer);

        // 3. Network Connection Parameters
        const netConnection = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
        insertRow('net-matrix', 'Network Online State', navigator.onLine ? 'CONNECTED' : 'DISCONNECTED');
        insertRow('net-matrix', 'Effective Pipeline Type', netConnection.effectiveType || 'N/A');
        insertRow('net-matrix', 'Downlink Link Capacity', (netConnection.downlink ? netConnection.downlink + ' Mbps' : 'N/A'));
        insertRow('net-matrix', 'Round Trip Estimate (RTT)', (netConnection.rtt ? netConnection.rtt + ' ms' : 'N/A'));

        // 4. Battery Level Monitoring
        if (navigator.getBattery) {
            try {
                const battery = await navigator.getBattery();
                insertRow('net-matrix', 'Power Storage Level', Math.round(battery.level * 100) + '%');
                insertRow('net-matrix', 'External Source Plugged', battery.charging ? 'YES' : 'NO');
            } catch (err) {
                insertRow('net-matrix', 'Power Storage Level', 'Access Restricted');
            }
        } else {
            insertRow('net-matrix', 'Power Storage Level', 'API Unsupported');
        }

        // 5. Environmental Agent Data
        insertRow('agent-matrix', 'Cookies Enabled Status', navigator.cookieEnabled ? 'TRUE' : 'FALSE');
        insertRow('agent-matrix', 'DoNotTrack Preference', navigator.doNotTrack || 'Unspecified');
        insertRow('agent-matrix', 'Automation State', navigator.webdriver ? 'BOT DETECTED' : 'STANDARD');
        insertRow('agent-matrix', 'Window Outer Dimensions', `${window.outerWidth}x${window.outerHeight}`);

        // 6. Local Storage Quota Discovery
        if (navigator.storage && navigator.storage.estimate) {
            try {
                const estimation = await navigator.storage.estimate();
                const totalSpaceGb = (estimation.quota / (1024 * 1024 * 1024)).toFixed(2);
                const consumedSpaceMb = (estimation.usage / (1024 * 1024)).toFixed(2);
                insertRow('storage-matrix', 'Total Storage Limit', `${totalSpaceGb} GB`);
                insertRow('storage-matrix', 'Current Allocation Space', `${consumedSpaceMb} MB`);
            } catch (err) {
                insertRow('storage-matrix', 'Storage Sandbox Metrics', 'Lookup Fail');
            }
        } else {
            insertRow('storage-matrix', 'Storage Sandbox Metrics', 'Unsupported');
        }

        // 7. Dynamic Gateway Target IP Resolution
        try {
            const serverResponse = await fetch('https://ipapi.co/json/');
            if (serverResponse.ok) {
                const ipDataset = await serverResponse.json();
                streamLog(`Public Endpoint Mapped: ${ipDataset.ip}`);
                streamLog(`Autonomous System Carrier: ${ipDataset.org}`);
                insertRow('agent-matrix', 'Mapped Public IP', ipDataset.ip);
                insertRow('agent-matrix', 'Registered Network ASN', ipDataset.org);
            }
        } catch (e) {
            streamLog("External IP Routing lookup blocked by Client Policy.");
        }

        streamLog("All static infrastructure diagnostic passes finalized.");
    }

    function triggerGPSLock() {
        document.getElementById('geo-status').innerText = "QUERYING LAYER...";
        streamLog("Initializing precise positioning validation layer...");
        
        if (!navigator.geolocation) {
            document.getElementById('geo-status').innerText = "UNSUPPORTED";
            streamLog("Error: Positioning engine interface absent on this platform.");
            return;
        }

        navigator.geolocation.getCurrentPosition((position) => {
            document.getElementById('geo-status').innerText = "LOCK ESTABLISHED";
            document.getElementById('geo-lat').innerText = position.coords.latitude;
            document.getElementById('geo-lon').innerText = position.coords.longitude;
            document.getElementById('geo-acc').innerText = position.coords.accuracy.toFixed(1) + " meters";
            document.getElementById('geo-time').innerText = new Date(position.timestamp).toISOString().slice(11,19);
            
            streamLog(`Success: System locked on coordinates: ${position.coords.latitude}, ${position.coords.longitude}`);
        }, (error) => {
            document.getElementById('geo-status').innerText = "ACCESS DENIED";
            if (error.code === error.PERMISSION_DENIED) {
                streamLog("Failure: Client explicit target rejected permission query.");
            } else {
                streamLog(`Positioning interface warning thrown: ${error.message}`);
            }
        }, { enableHighAccuracy: true, timeout: 10000 });
    }
</script>
</body>
</html>
"""

@script8_bp.route('/')
def home():
    return render_template_string(INTERFACE)

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script8_bp, url_prefix='/script8')
    app.run(debug=True, port=5000)
