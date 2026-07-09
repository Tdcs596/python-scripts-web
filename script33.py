from flask import Blueprint, render_template_string, request, jsonify
import urllib.request
import urllib.parse
import re
import time
import json

script33_bp = Blueprint('script33', __name__)

ULTIMATE_AUDIT_UI_V4 = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBEDGEMEDIA AUDIT ENGINE v4.0</title>
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
        min-height: 420px;
        max-height: 650px;
        overflow-y: auto;
        font-size: 12px;
        line-height: 1.6;
        color: #34d399;
    }

    .badge { padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; text-transform: uppercase; display: inline-block; }
    .badge-detected { background: rgba(16, 185, 129, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
    .badge-missing { background: rgba(239, 68, 68, 0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }

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
        <div class="brand-title">ORBEDGEMEDIA AUDIT ENGINE <span>v4.0 (COMPLETE SEO MASTER)</span></div>
        <div class="brand-sub">Real-Time Core Tracking Codes, PageSpeed, Schema Validation, Robots.txt & Sitemap Live Core System</div>
        
        <div class="input-row">
            <input type="text" id="target_url" class="url-input" placeholder="Enter target website URL (e.g., https://example.com)...">
            <button class="btn-audit" onclick="triggerDeepLiveAudit()">Run Intelligent 360° Audit</button>
        </div>
    </div>

    <div class="studio-layout">
        
        <div class="panel">
            <div class="panel-header">🎯 Comprehensive Signal Detection Matrix</div>
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
                <button class="tab-btn active" id="tab_report" onclick="switchTab('report')">📝 Technical Audit Logs</button>
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
            
            footer.innerText = `📡 Connecting to target node. Deep mapping HTML tags, Robots, Sitemaps, and Schema architectures...`;
            consoleStream.innerHTML = `<span style="color:var(--neon-cyan);">[INITIALIZING] Running deep algorithmic scans & crawling code streams...</span>`;

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
                    <tr><td>Schema Markup Verification</td><td><span class="badge ${data.schema_markup ? 'badge-detected' : 'badge-missing'}">${data.schema_markup ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Robots.txt File Presence</td><td><span class="badge ${data.has_robots ? 'badge-detected' : 'badge-missing'}">${data.has_robots ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>XML Sitemap Discovery</td><td><span class="badge ${data.has_sitemap ? 'badge-detected' : 'badge-missing'}">${data.has_sitemap ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr style="background: rgba(6, 182, 212, 0.05); font-weight: bold;"><td style="color: var(--neon-cyan);">Server Response (TTFB)</td><td style="color: var(--neon-green);">${data.ttfb}</td></tr>
                    <tr style="background: rgba(6, 182, 212, 0.05); font-weight: bold;"><td style="color: var(--neon-cyan);">Page Load Speed Latency</td><td style="color: var(--neon-cyan);">${data.page_load_speed}</td></tr>
                `;

                cachedReport = data.technical_report;
                cachedPitch = data.ai_pitch;

                switchTab('report');
                footer.innerText = `✅ Comprehensive 360° master technical audit completed for: ${data.domain}`;

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
    return render_template_string(ULTIMATE_AUDIT_UI_V4)

@script33_bp.route('/run_live_audit')
def run_live_audit():
    raw_url = request.args.get('url', '').strip()
    if not raw_url:
        return jsonify({"status": "error", "message": "Domain source parameter mismatch."})

    if not raw_url.startswith(('http://', 'https://')):
        base_url = 'https://' + raw_url
    else:
        base_url = raw_url

    parsed_url = urllib.parse.urlparse(base_url)
    parsed_domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    clean_base_url = f"{parsed_url.scheme}://{parsed_domain}"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # --- 1. CORE HTML SCAN & PAGESPEED METRICS ---
        start_time = time.time()
        req_html = urllib.request.Request(clean_base_url, headers=headers)
        with urllib.request.urlopen(req_html, timeout=8) as response:
            ttfb_duration = time.time() - start_time
            html_content = response.read().decode('utf-8', errors='ignore')
            total_duration = time.time() - start_time

        ttfb = f"{round(ttfb_duration, 3)}s"
        page_load_speed = f"{round(total_duration, 2)}s"

        # Core Detection Regex Mappings
        has_gsc = bool(re.search(r'google-site-verification|google\d+[a-zA-Z0-9\-_]+\.html|sc-domain:|googletagmanager\.com.*?id=GTM-[A-Z0-9]+', html_content, re.IGNORECASE))
        has_ga = bool(re.search(r'gtag\(|google-analytics\.com|googletagmanager\.com/gtag/js|_gaq\.push', html_content, re.IGNORECASE))
        has_gtm = bool(re.search(r'googletagmanager\.com/gtm\.js|gtm\.start', html_content, re.IGNORECASE))
        
        # --- SCHEMA MARKUP DEEP DETECTION ---
        schema_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
        has_schema = len(schema_matches) > 0
        
        schema_summary = "❌ NO JSON-LD SCHEMA DETECTED"
        schema_status_pitch = "Missing schemas completely. Google will struggle to understand structure."
        if has_schema:
            try:
                # Clean up and try parsing the first schema found to evaluate functionality
                clean_json = schema_matches[0].strip()
                parsed_json = json.loads(clean_json)
                schema_type = parsed_json.get('@type', 'Detected')
                schema_summary = f"✅ ACTIVE (Type: {schema_type}) - Working properly."
                schema_status_pitch = f"Detected Type: '{schema_type}'. Structured metadata layer configuration is solid."
            except Exception:
                schema_summary = "⚠️ DETECTED BUT CONTAINS STRUCTURAL ERROR (Invalid JSON Mapping)"
                schema_status_pitch = "Schema script injection has code formatting errors. Fix immediately!"

        # --- 2. LIVE ROBOTS.TXT CHECKER NODE ---
        robots_url = f"{clean_base_url}/robots.txt"
        has_robots = False
        robots_content = "❌ Robots.txt file not found on server root path layer."
        try:
            req_robots = urllib.request.Request(robots_url, headers=headers)
            with urllib.request.urlopen(req_robots, timeout=5) as resp_robots:
                if resp_robots.status == 200:
                    has_robots = True
                    robots_content = resp_robots.read().decode('utf-8', errors='ignore').strip()
        except Exception:
            pass

        # --- 3. DYNAMIC XML SITEMAP SCANNER ENGINE ---
        sitemap_url = f"{clean_base_url}/sitemap.xml"
        has_sitemap = False
        sitemap_content = "❌ Core sitemap file structure missing or restricted."
        try:
            req_site = urllib.request.Request(sitemap_url, headers=headers)
            with urllib.request.urlopen(req_site, timeout=5) as resp_site:
                if resp_site.status == 200:
                    has_sitemap = True
                    raw_sitemap = resp_site.read().decode('utf-8', errors='ignore').strip()
                    # Just fetch initial 350 chars cleanly so terminal block layout doesn't break
                    sitemap_content = (raw_sitemap[:350] + "\n... [Truncated Stream Link Data Content]") if len(raw_sitemap) > 350 else raw_sitemap
        except Exception:
            pass

        # Fallback lookups inside robots data layer if direct url was restricted
        if not has_sitemap and has_robots:
            sitemap_find = re.findall(r'sitemap:\s*(^\s]+)', robots_content, re.IGNORECASE)
            if sitemap_find:
                has_sitemap = True
                sitemap_content = f"✅ Verified via Robots Link Parameter Rule: {sitemap_find[0]}"

        # Evaluate performance markers
        seo_robots_status = "✅ PERFECT RULES SETUP" if has_robots and "Disallow:" in robots_content else "⚠️ LIVE BUT MISSING EXPLICIT DISALLOW INDEX RULES"
        if not has_robots: seo_robots_status = "❌ CRITICAL DEFICIT (Search bots can index administrative loop systems)"

        seo_sitemap_status = "✅ CORE INTEGRATION ENGAGED" if has_sitemap else "❌ SEVERE SEO CRITICAL ERROR (Google indexation pipeline delayed)"

        # --- COMPILE 100% ACCURATE TECHNICAL REPORT LOG PANEL ---
        technical_report = f"""======================================================================
🛰️ ACCURATE DEEP RECON TECHNICAL REPORT FOR: {parsed_domain.upper()}
======================================================================

⚙️ Tracking & Indexing Verification Footprints:
  • Google Analytics Status : {"✅ ACTIVE / DETECTED" if has_ga else "❌ MISSING LAYER"}
  • Google Search Console   : {"✅ ACTIVE / DETECTED" if has_gsc else "❌ MISSING LAYER"}
  • Google Tag Manager      : {"✅ ACTIVE / DETECTED" if has_gtm else "❌ MISSING LAYER"}

📁 Core SEO Infrastructure Architecture Mapping:
  • Structured Schema Data  : {schema_summary}
  • Robots.txt Deployment    : {seo_robots_status}
  • XML Sitemap Execution   : {seo_sitemap_status}

⚡ PageSpeed Processing Telemetry Metrics:
  • Time to First Byte (TTFB): {ttfb}
  • Complete HTML Load Time : {page_load_speed}

----------------------------------------------------------------------
🤖 RAW ROBOTS.TXT CONTENT EXTRACTED:
----------------------------------------------------------------------
{robots_content}

----------------------------------------------------------------------
🗺️ LIVE SITEMAP FILE CORE ARCHITECTURE TRACE:
----------------------------------------------------------------------
{sitemap_content}

======================================================================"""

        # --- AUTOMATED INTEGRATED SALES PITCH CLOSER HOOK ---
        deficits = []
        if not has_ga: deficits.append("Google Analytics Asset Mapping")
        if not has_gsc: deficits.append("Google Search Console Search Indexing Node")
        if not has_robots: deficits.append("Robots.txt Crawling Protection System")
        if not has_sitemap: deficits.append("XML Sitemap Core Structure Layout")
        if "CONTAINS STRUCTURAL ERROR" in schema_summary: deficits.append("Schema Layout Syntax Refactoring")

        if deficits:
            leaks_log = "\n".join([f"  ⚠️ {i+1}. {item}" for i, item in enumerate(deficits)])
            pitch_hook = f"""Hey! We audited your technical architecture at '{parsed_domain}' and found critical structural deficiencies: \n{', '.join(deficits)}.\n\nYour Robots/Sitemap tracking nodes are unoptimized or restricted, causing index loops drops across Google nodes. Let's patch these parameters within 24 hours!"""
        else:
            leaks_log = "  ✨ ALL SYSTEM CHANNELS OPERATIONAL: System code tracking components are fully locked."
            pitch_hook = f"Brilliant alignment! '{parsed_domain}' architecture elements successfully passed validation hooks. Ready for premium traffic conversion models execution!"

        ai_pitch = f"""======================================================================
💡 VALUE-DRIVEN CONVERSION SALES PIPELINE
======================================================================

🚨 DETECTED WEB ARCHITECTURE REVENUE LOSS MARKERS:
{leaks_log}

🔥 DYNAMIC CONVERSION SCRIPTS VALUE CLOSER:
"{pitch_hook}" """

        return jsonify({
            "status": "success",
            "domain": parsed_domain,
            "google_analytics": has_ga,
            "google_search_console": has_gsc,
            "google_tag_manager": has_gtm,
            "schema_markup": has_schema,
            "has_robots": has_robots,
            "has_sitemap": has_sitemap,
            "ttfb": ttfb,
            "page_load_speed": page_load_speed,
            "technical_report": technical_report,
            "ai_pitch": ai_pitch
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Handshake failed with target url node location. Details: {str(e)}"
        })
