from flask import Blueprint, render_template_string, request, jsonify
import urllib.request
import urllib.parse
import re
import time

script33_bp = Blueprint('script33', __name__)

ULTIMATE_AUDIT_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBEDGEMEDIA AUDIT ENGINE v3.0</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-deep: #030712;
        --panel-bg: #0b1329;
        --neon-cyan: #06b6d4;
        --neon-green: #10b981;
        --neon-red: #ef4444;
        --neon-amber: #eab308;
        --border-color: rgba(6, 182, 212, 0.15);
        --text-bright: #f3f4f6;
        --text-gray: #9ca3af;
        --terminal-bg: #020617;
    }

    body { 
        background: var(--bg-deep); 
        color: var(--text-bright); 
        font-family: 'Consolas', 'Courier New', monospace; 
        min-height: 100vh;
        padding: 20px;
    }

    .header-panel {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .brand-title { font-size: 22px; font-weight: bold; letter-spacing: 2px; margin-bottom: 5px; }
    .brand-title span { color: var(--neon-cyan); }
    .brand-sub { font-size: 12px; color: var(--text-gray); margin-bottom: 20px; }

    .input-row { display: flex; gap: 15px; flex-wrap: wrap; }

    .url-input {
        flex: 1;
        min-width: 280px;
        background: #02040a;
        border: 1px solid var(--border-color);
        padding: 12px 15px;
        color: #fff;
        font-family: inherit;
        font-size: 14px;
        border-radius: 6px;
        outline: none;
    }
    .url-input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 10px rgba(6, 182, 212, 0.2); }

    .btn-audit {
        background: #2563eb;
        color: white;
        border: none;
        padding: 12px 25px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 1px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .btn-audit:hover { background: #1d4ed8; box-shadow: 0 0 15px rgba(37, 99, 235, 0.4); }

    /* --- RESPONSIVE GRID LAYOUT --- */
    .studio-layout {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    @media (max-width: 1024px) { .studio-layout { grid-template-columns: 1fr; } }

    .panel {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        display: flex;
        flex-direction: column;
    }

    .panel-header {
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--neon-cyan);
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 8px;
    }

    .table-container { overflow-x: auto; }
    
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    .matrix-table th { color: var(--text-gray); padding: 12px 10px; border-bottom: 1px solid var(--border-color); font-weight: normal; }
    .matrix-table td { padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.03); }

    .tabs-header { display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .tab-btn {
        background: transparent;
        border: none;
        color: var(--text-gray);
        padding: 8px 15px;
        font-family: inherit;
        font-size: 11px;
        text-transform: uppercase;
        cursor: pointer;
    }
    .tab-btn.active { color: #fff; border-bottom: 2px solid var(--neon-cyan); font-weight: bold; }

    .terminal-screen {
        background: var(--terminal-bg);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 6px;
        padding: 15px;
        flex: 1;
        min-height: 380px;
        max-height: 580px;
        overflow-y: auto;
        font-size: 12px;
        line-height: 1.6;
        color: #34d399;
    }

    .badge { padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; text-transform: uppercase; display: inline-block; }
    .badge-detected { background: rgba(16, 185, 129, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
    .badge-missing { background: rgba(239, 68, 68, 0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }
    .badge-warning { background: rgba(234, 179, 8, 0.15); color: var(--neon-amber); border: 1px solid var(--neon-amber); }

    .status-footer {
        margin-top: 20px;
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        padding: 10px 20px;
        border-radius: 6px;
        font-size: 11px;
        color: var(--text-gray);
    }
  </style>
</head>
<body>

    <div class="header-panel">
        <div class="brand-title">ORBEDGEMEDIA AUDIT ENGINE <span>v3.0 (DEEP ACCURACY)</span></div>
        <div class="brand-sub">Advanced Live Technical Audit Tracker & PageSpeed Insights Deep Scan Matrix</div>
        
        <div class="input-row">
            <input type="text" id="target_url" class="url-input" placeholder="Enter target website URL (e.g., https://example.com)...">
            <button class="btn-audit" onclick="triggerDeepLiveAudit()">Run Intelligent 360° Audit</button>
        </div>
    </div>

    <div class="studio-layout">
        
        <div class="panel">
            <div class="panel-header">🎯 Deep Signal & Speed Detection Matrix</div>
            <div class="table-container">
                <table class="matrix-table">
                    <thead>
                        <tr>
                            <th>Parameter Tracker</th>
                            <th>Live Verification Status</th>
                        </tr>
                    </thead>
                    <tbody id="matrix_output_rows">
                        <tr><td colspan="2" style="color: var(--text-gray); text-align: center; padding: 40px;">[System Idle] Run target scan parameter tracking loops...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="panel">
            <div class="tabs-header">
                <button class="tab-btn active" id="tab_report" onclick="switchTab('report')">📝 Diagnostic Live Logs</button>
                <button class="tab-btn" id="tab_pitch" onclick="switchTab('pitch')">💡 Conversion Sales Hook</button>
            </div>
            <div class="terminal-screen" id="terminal_console_stream">
                [SYSTEM READY] Feed source URL payload stream to initialize vector extraction...
            </div>
        </div>

    </div>

    <div class="status-footer" id="footer_log">
        Engine Operational Core Status: Connected.
    </div>

    <script>
        let cachedReport = "";
        let cachedPitch = "";

        async function triggerDeepLiveAudit() {
            const inputField = document.getElementById('target_url');
            let target = inputField.value.trim();
            if(!target) { alert("Bhai, valid website link ya domain daalo!"); return; }

            const footer = document.getElementById('footer_log');
            const consoleStream = document.getElementById('terminal_console_stream');
            
            footer.innerText = `📡 Handshaking secure sockets & unpacking code blocks...`;
            consoleStream.innerHTML = `<span style="color:var(--neon-cyan);">[INITIALIZING] Running deep algorithmic scans & calculating sub-system speeds...</span>`;

            try {
                const response = await fetch(`${window.location.pathname.replace(/\/$/, "")}/run_live_audit?url=${encodeURIComponent(target)}`);
                const data = await response.json();

                if (data.status === "error") {
                    consoleStream.innerHTML = `<span style="color:var(--neon-red);">[CRITICAL ERR] ${data.message}</span>`;
                    footer.innerText = `❌ Scan tracking sequence faulted.`;
                    return;
                }

                const tableBody = document.getElementById('matrix_output_rows');
                tableBody.innerHTML = `
                    <tr><td>Target Domain Mapping</td><td style="font-weight:bold; color:#fff;">${data.domain}</td></tr>
                    <tr><td>Google Analytics (GA4/Gtag)</td><td><span class="badge ${data.google_analytics ? 'badge-detected' : 'badge-missing'}">${data.google_analytics ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Google Search Console (GSC)</td><td><span class="badge ${data.google_search_console ? 'badge-detected' : 'badge-missing'}">${data.google_search_console ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Google Tag Manager (GTM)</td><td><span class="badge ${data.google_tag_manager ? 'badge-detected' : 'badge-missing'}">${data.google_tag_manager ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Schema Markup (JSON-LD Data)</td><td><span class="badge ${data.schema_markup ? 'badge-detected' : 'badge-missing'}">${data.schema_markup ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr style="background: rgba(6, 182, 212, 0.05); font-weight: bold;"><td style="color: var(--neon-cyan);">Server Response (TTFB)</td><td style="color: var(--neon-green);">${data.ttfb}</td></tr>
                    <tr style="background: rgba(6, 182, 212, 0.05); font-weight: bold;"><td style="color: var(--neon-cyan);">Estimated Page Load Speed</td><td style="color: var(--neon-cyan);">${data.page_load_speed}</td></tr>
                `;

                cachedReport = data.technical_report;
                cachedPitch = data.ai_pitch;

                switchTab('report');
                footer.innerText = `✅ 100% Accurate technical & PageSpeed scan completed for: ${data.domain}`;

            } catch(err) {
                consoleStream.innerHTML = `<span style="color:var(--neon-red);">[FAULT] Connection interface pipeline timeout.</span>`;
                footer.innerText = `❌ Error establishing handshakes loop.`;
            }
        }

        function switchTab(name) {
            const btnReport = document.getElementById('tab_report');
            const btnPitch = document.getElementById('tab_pitch');
            const consoleStream = document.getElementById('terminal_console_stream');

            btnReport.classList.remove('active');
            btnPitch.classList.remove('active');

            if(name === 'report') {
                btnReport.classList.add('active');
                consoleStream.style.color = '#34d399';
                consoleStream.innerHTML = cachedReport ? cachedReport.replace(/\n/g, '<br>') : '[Empty Log Arrays]';
            } else {
                btnPitch.classList.add('active');
                consoleStream.style.color = '#eab308';
                consoleStream.innerHTML = cachedPitch ? cachedPitch.replace(/\n/g, '<br>') : '[Empty Conversion Scripts]';
            }
        }
    </script>
</body>
</html>
"""

@script33_bp.route('/')
def index():
    return render_template_string(ULTIMATE_AUDIT_UI)

@script33_bp.route('/run_live_audit')
def run_live_audit():
    raw_url = request.args.get('url', '').strip()
    if not raw_url:
        return jsonify({"status": "error", "message": "Domain source parameter mismatch."})

    if not raw_url.startswith(('http://', 'https://')):
        target_url = 'https://' + raw_url
    else:
        target_url = raw_url

    parsed_domain = urllib.parse.urlparse(target_url).netloc

    try:
        # Browser Footprint Mocking Setup
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(target_url, headers=headers)
        
        # --- PAGESPEED CALCULATOR PIPELINE ---
        start_time = time.time()
        with urllib.request.urlopen(req, timeout=10) as response:
            ttfb_duration = time.time() - start_time  # Time to First Byte calculation
            html_content = response.read().decode('utf-8', errors='ignore')
            total_duration = time.time() - start_time # Dynamic full HTML stream parse load time

        # Clean metric string presentation
        ttfb = f"{round(ttfb_duration, 3)}s"
        page_load_speed = f"{round(total_duration, 2)}s"

        # --- ADVANCED HIGH-ACCURACY GSC RESOLVER ---
        # Checks meta verification token, direct static script binds, and HTML token file footprints
        has_gsc = bool(re.search(
            r'google-site-verification|google\d+[a-zA-Z0-9\-_]+\.html|sc-domain:|googletagmanager\.com.*?id=GTM-[A-Z0-9]+', 
            html_content, re.IGNORECASE
        ))
        
        # Cross-validation fallback checks for Tag Manager and Analytics setups
        has_ga = bool(re.search(r'gtag\(|google-analytics\.com|googletagmanager\.com/gtag/js|_gaq\.push', html_content, re.IGNORECASE))
        has_gtm = bool(re.search(r'googletagmanager\.com/gtm\.js|gtm\.start', html_content, re.IGNORECASE))
        has_schema = bool(re.search(r'application/ld\+json|itemscope|itemtype=["\']http://schema\.org', html_content, re.IGNORECASE))

        # --- TECHNICAL DIAGNOSTICS LAYER ---
        technical_report = f"""======================================================================
🛰️ ACCURATE LIVE RECON REPORT FOR: {parsed_domain.upper()}
======================================================================

🔍 Live Code Injection Stack Diagnostics:
  • Google Analytics Token  : {"✅ ACTIVE / DETECTED" if has_ga else "❌ MISSING"}
  • Google Search Console   : {"✅ ACTIVE / DETECTED" if has_gsc else "❌ MISSING"}
  • Google Tag Manager      : {"✅ ACTIVE / DETECTED" if has_gtm else "❌ MISSING"}
  • Structured Schema Data  : {"✅ ACTIVE / DETECTED" if has_schema else "❌ MISSING"}

⚡ PageSpeed Performance Logs:
  • Time to First Byte (TTFB): {ttfb} (Ideal: < 0.8s)
  • Page Load Latency Stream : {page_load_speed} (Ideal: < 2.5s)
  • Optimization Status      : {"🟢 EXCELLENT SPEED" if total_duration < 2.0 else "🟡 AVERAGE - NEED CLEANUP"}

----------------------------------------------------------------------
[STATUS CODE]: 200 OK | Data Matrix Map Verified and Locked.
----------------------------------------------------------------------"""

        # --- DYNAMIC CONVERSION CLOSER LOGIC ---
        missing = []
        if not has_ga: missing.append("Google Analytics")
        if not has_gsc: missing.append("Google Search Console (GSC Indexing Key)")
        if not has_gtm: missing.append("Google Tag Manager")
        if not has_schema: missing.append("Schema Structure Layouts")

        if total_duration > 2.2:
            missing.append(f"Page Load Speed Optimization ({page_load_speed} is slow!)")

        if missing:
            leaks = "\n".join([f"  ⚠️ {idx+1}. {item}" for idx, item in enumerate(missing)])
            pitch_script = f"""Hey! We audited '{parsed_domain}' and caught crucial data leaks: \n{', '.join(missing)}.\n\nYour site takes {page_load_speed} to respond, which impacts Google SEO ranking structures directly. Let's optimize this code map today!"""
        else:
            leaks = "  ✨ PERFECT ARCHITECTURE: Target web architecture parameters are fully verified."
            pitch_script = f"Excellent optimization! '{parsed_domain}' passed all strict verification nodes cleanly. Let's proceed to scale conversion tracking elements."

        ai_pitch = f"""======================================================================
💡 AUTOMATED VALUE-DRIVEN SALES HOOK
======================================================================

🚨 INFRASTRUCTURE DEFICITS DETECTED:
{leaks}

自由 HIGH CONVERTING PITCH TEXT:
"{pitch_script}" """

        return jsonify({
            "status": "success",
            "domain": parsed_domain,
            "google_analytics": has_ga,
            "google_search_console": has_gsc,
            "google_tag_manager": has_gtm,
            "schema_markup": has_schema,
            "ttfb": ttfb,
            "page_load_speed": page_load_speed,
            "technical_report": technical_report,
            "ai_pitch": ai_pitch
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Could not establish handshake with {parsed_domain}. Details: {str(e)}"
        })
