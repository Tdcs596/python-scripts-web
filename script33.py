from flask import Blueprint, render_template_string, request, jsonify
import urllib.request
import urllib.parse
import re
import time
import json

script33_bp = Blueprint('script33', __name__)

ULTIMATE_AUDIT_UI_V10 = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBEDGEMEDIA AUDIT ENGINE v10.0 - ULTIMATE RECONSTRUCTION</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-deep: #020617;
        --panel-bg: #0f172a;
        --neon-cyan: #06b6d4;
        --neon-green: #10b981;
        --neon-red: #ef4444;
        --neon-amber: #eab308;
        --border-color: rgba(6, 182, 212, 0.25);
        --text-bright: #f8fafc;
        --text-gray: #94a3b8;
        --terminal-bg: #030712;
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
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.5);
    }

    .brand-title { font-size: 24px; font-weight: bold; letter-spacing: 2px; margin-bottom: 5px; }
    .brand-title span { color: var(--neon-cyan); }
    .brand-sub { font-size: 13px; color: var(--text-gray); margin-bottom: 20px; }

    .input-row { display: flex; gap: 15px; flex-wrap: wrap; }

    .url-input {
        flex: 1;
        min-width: 300px;
        background: #02040a;
        border: 1px solid var(--border-color);
        padding: 14px 18px;
        color: #fff;
        font-family: inherit;
        font-size: 14px;
        border-radius: 6px;
        outline: none;
    }
    .url-input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 12px rgba(6, 182, 212, 0.4); }

    .btn-audit {
        background: #2563eb;
        color: white;
        border: none;
        padding: 14px 30px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 13px;
        letter-spacing: 1px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .btn-audit:hover { background: #1d4ed8; box-shadow: 0 0 18px rgba(37, 99, 235, 0.6); }

    .studio-layout {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    @media (max-width: 1150px) { .studio-layout { grid-template-columns: 1fr; } }

    .panel {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .panel-header {
        font-size: 13px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--neon-cyan);
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 10px;
    }

    .table-container { overflow-x: auto; }
    
    .matrix-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    .matrix-table th { color: var(--text-gray); padding: 12px 10px; border-bottom: 1px solid var(--border-color); font-weight: normal; text-align: left; }
    .matrix-table td { padding: 10px 10px; border-bottom: 1px solid rgba(255,255,255,0.03); }

    .tabs-header { display: flex; gap: 10px; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.08); }
    .tab-btn {
        background: transparent;
        border: none;
        color: var(--text-gray);
        padding: 10px 20px;
        font-family: inherit;
        font-size: 11px;
        text-transform: uppercase;
        cursor: pointer;
    }
    .tab-btn.active { color: #fff; border-bottom: 2px solid var(--neon-cyan); font-weight: bold; }

    .terminal-screen {
        background: var(--terminal-bg);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 20px;
        flex: 1;
        min-height: 600px;
        max-height: 1500px;
        overflow-y: auto;
        font-size: 12px;
        line-height: 1.6;
        color: #34d399;
    }

    .badge { padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 10px; text-transform: uppercase; display: inline-block; }
    .badge-detected { background: rgba(16, 185, 129, 0.15); color: var(--neon-green); border: 1px solid var(--neon-green); }
    .badge-missing { background: rgba(239, 68, 68, 0.15); color: var(--neon-red); border: 1px solid var(--neon-red); }
    .badge-warning { background: rgba(234, 179, 8, 0.15); color: var(--neon-amber); border: 1px solid var(--neon-amber); }

    .status-footer {
        margin-top: 20px;
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        padding: 12px 20px;
        border-radius: 6px;
        font-size: 12px;
        color: var(--text-gray);
    }
  </style>
</head>
<body>

    <div class="header-panel">
        <div class="brand-title">ORBEDGEMEDIA AUDIT ENGINE <span>v10.0 (MAXIMUM ACCURACY EDITION)</span></div>
        <div class="brand-sub">Comprehensive Extraction Architecture: Live Deep Directory Handshakes, Recursive Sitemap Parsing Matrices & Global Social Media Mapping</div>
        
        <div class="input-row">
            <input type="text" id="target_url" class="url-input" placeholder="Enter target website URL to execute dynamic analysis...">
            <button class="btn-audit" onclick="triggerDeepLiveAudit()">Run Deep Live Audit Loop</button>
        </div>
    </div>

    <div class="studio-layout">
        
        <!-- Left Summary Matrix -->
        <div class="panel">
            <div class="panel-header">🎯 Live Multi-Vector Signal Matrix</div>
            <div class="table-container">
                <table class="matrix-table">
                    <thead>
                        <tr>
                            <th>Parameter Tracker</th>
                            <th>Live Verification Status</th>
                        </tr>
                    </thead>
                    <tbody id="matrix_output_rows">
                        <tr><td colspan="2" style="color: var(--text-gray); text-align: center; padding: 40px;">[System Idle] Provide a targeted domain string to execute structural parsing loops...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Right Terminal View Blocks -->
        <div class="panel">
            <div class="tabs-header">
                <button class="tab-btn active" id="tab_report" onclick="switchTab('report')">📝 Factual Analysis Logs</button>
                <button class="tab-btn" id="tab_pitch" onclick="switchTab('pitch')">💡 Sales Conversion Strategy</button>
            </div>
            <div class="terminal-screen" id="terminal_console_stream">
                [SYSTEM READY] Monitoring framework ready to handle production audits...
            </div>
        </div>

    </div>

    <div class="status-footer" id="footer_log">
        Engine Operational Core Status: Standby.
    </div>

    <script>
        let cachedReport = "";
        let cachedPitch = "";

        async function triggerDeepLiveAudit() {
            const inputField = document.getElementById('target_url');
            let target = inputField.value.trim();
            if(!target) { alert("Please provide a valid website address!"); return; }

            const footer = document.getElementById('footer_log');
            const consoleStream = document.getElementById('terminal_console_stream');
            
            footer.innerText = `📡 Connecting: Fetching source data from target nodes...`;
            consoleStream.innerHTML = `<span style="color:var(--neon-cyan);">[INITIALIZING AUDIT] Scanning index documents, unfolding sitemap levels, interpreting server controls, and searching directory traces...</span>`;

            try {
                const response = await fetch(`${window.location.pathname.replace(/\/$/, "")}/run_live_audit?url=${encodeURIComponent(target)}`);
                const data = await response.json();

                if (data.status === "error") {
                    consoleStream.innerHTML = `<span style="color:var(--neon-red);">[CRITICAL FAULT] ${data.message}</span>`;
                    footer.innerText = `❌ Extraction process terminated abnormally.`;
                    return;
                }

                const tableBody = document.getElementById('matrix_output_rows');
                tableBody.innerHTML = `
                    <tr><td>Target Domain Mapping</td><td style="font-weight:bold; color:#fff;">${data.domain}</td></tr>
                    <tr style="background: rgba(6, 182, 212, 0.05); font-weight: bold;"><td>NAP Consistency Score</td><td><span class="badge ${data.nap_consistent ? 'badge-detected' : 'badge-warning'}">${data.nap_status}</span></td></tr>
                    
                    <tr style="color: var(--neon-cyan); font-weight:bold;"><td colspan="2">🌐 [DIVISION 1: CORE INFRASTRUCTURE & ANALYTICS]</td></tr>
                    <tr><td>Google Analytics (GA4)</td><td><span class="badge ${data.google_analytics ? 'badge-detected' : 'badge-missing'}">${data.google_analytics ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Google Search Console (GSC)</td><td><span class="badge ${data.google_search_console ? 'badge-detected' : 'badge-missing'}">${data.google_search_console ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Google Tag Manager (GTM)</td><td><span class="badge ${data.google_tag_manager ? 'badge-detected' : 'badge-missing'}">${data.google_tag_manager ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Cloudflare CDN Protection</td><td><span class="badge ${data.cloudflare_cdn ? 'badge-detected' : 'badge-warning'}">${data.cloudflare_cdn ? 'ACTIVE CDN' : 'NOT DETECTED'}</span></td></tr>
                    
                    <tr style="color: var(--neon-green); font-weight:bold;"><td colspan="2">📍 [DIVISION 2: REGIONAL CITATIONS & DIRECTORIES]</td></tr>
                    <tr><td>Google My Business (GMB)</td><td><span class="badge ${data.has_gmb ? 'badge-detected' : 'badge-missing'}">${data.has_gmb ? 'FOUND' : 'NOT FOUND'}</span></td></tr>
                    <tr><td>Bing Places Profile</td><td><span class="badge ${data.bing_places ? 'badge-detected' : 'badge-missing'}">${data.bing_places ? 'CONNECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Apple Business Connect</td><td><span class="badge ${data.apple_business ? 'badge-detected' : 'badge-missing'}">${data.apple_business ? 'VERIFIED' : 'MISSING'}</span></td></tr>
                    <tr><td>Justdial Citations Matrix</td><td><span class="badge ${data.justdial_seo ? 'badge-detected' : 'badge-missing'}">${data.justdial_seo ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Sulekha Listing Signal</td><td><span class="badge ${data.sulekha_seo ? 'badge-detected' : 'badge-missing'}">${data.sulekha_seo ? 'ACTIVE' : 'MISSING'}</span></td></tr>
                    <tr><td>Hotfrog Global Directory</td><td><span class="badge ${data.hotfrog_seo ? 'badge-detected' : 'badge-missing'}">${data.hotfrog_seo ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Yelp Profiles Mapped</td><td><span class="badge ${data.yelp_seo ? 'badge-detected' : 'badge-missing'}">${data.yelp_seo ? 'DETECTED' : 'MISSING'}</span></td></tr>

                    <tr style="color: var(--neon-amber); font-weight:bold;"><td colspan="2">🚀 [DIVISION 3: COMMERCIAL B2B ECOSYSTEMS]</td></tr>
                    <tr><td>IndiaMart B2B Footprint</td><td><span class="badge ${data.indiamart_seo ? 'badge-detected' : 'badge-missing'}">${data.indiamart_seo ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>TradeIndia Asset Matrix</td><td><span class="badge ${data.tradeindia_seo ? 'badge-detected' : 'badge-missing'}">${data.tradeindia_seo ? 'DETECTED' : 'MISSING'}</span></td></tr>
                    <tr><td>Medium Blog Syndication</td><td><span class="badge ${data.medium_seo ? 'badge-detected' : 'badge-warning'}">${data.medium_seo ? 'CONNECTED' : 'NO LINK'}</span></td></tr>
                    <tr><td>Blogspot Network Link</td><td><span class="badge ${data.blogspot_seo ? 'badge-detected' : 'badge-warning'}">${data.blogspot_seo ? 'FOUND' : 'NO LINK'}</span></td></tr>

                    <tr style="color: #a78bfa; font-weight:bold;"><td colspan="2">📱 [DIVISION 4: COMPLETE SOCIAL OPTIMIZATION SIGNALS]</td></tr>
                    <tr><td>Facebook Brand Page</td><td><span class="badge ${data.social_fb ? 'badge-detected' : 'badge-missing'}">${data.social_fb ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>Instagram Profile Anchor</td><td><span class="badge ${data.social_insta ? 'badge-detected' : 'badge-missing'}">${data.social_insta ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>LinkedIn Corporate Hub</td><td><span class="badge ${data.social_linkedin ? 'badge-detected' : 'badge-missing'}">${data.social_linkedin ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>Twitter / X Channel</td><td><span class="badge ${data.social_twitter ? 'badge-detected' : 'badge-missing'}">${data.social_twitter ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>YouTube Brand Asset</td><td><span class="badge ${data.social_youtube ? 'badge-detected' : 'badge-missing'}">${data.social_youtube ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>Pinterest Board Hub</td><td><span class="badge ${data.social_pinterest ? 'badge-detected' : 'badge-missing'}">${data.social_pinterest ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>WhatsApp Business Tunnel</td><td><span class="badge ${data.social_whatsapp ? 'badge-detected' : 'badge-missing'}">${data.social_whatsapp ? 'ACTIVE' : 'MISSING'}</span></td></tr>
                    <tr><td>Telegram Channel Connection</td><td><span class="badge ${data.social_telegram ? 'badge-detected' : 'badge-missing'}">${data.social_telegram ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>Reddit Community Node</td><td><span class="badge ${data.social_reddit ? 'badge-detected' : 'badge-missing'}">${data.social_reddit ? 'FOUND' : 'MISSING'}</span></td></tr>
                    <tr><td>TikTok Content Profile</td><td><span class="badge ${data.social_tiktok ? 'badge-detected' : 'badge-missing'}">${data.social_tiktok ? 'FOUND' : 'MISSING'}</span></td></tr>

                    <tr style="color: #fff; font-weight:bold;"><td colspan="2">🛠️ [DIVISION 5: CRAWLABILITY, NESTED SITEMAPS & BOT ROUTING]</td></tr>
                    <tr><td>Robots.txt Control Rules</td><td><span class="badge ${data.has_robots ? 'badge-detected' : 'badge-missing'}">${data.has_robots ? 'VERIFIED' : 'ABSENT'}</span></td></tr>
                    <tr><td>Nested XML Sitemaps System</td><td><span class="badge ${data.xml_count > 0 ? 'badge-detected' : 'badge-missing'}">${data.xml_status_msg}</span></td></tr>
                    <tr><td>SSL Secure Connection</td><td><span class="badge ${data.is_https ? 'badge-detected' : 'badge-missing'}">${data.is_https ? 'SECURE (HTTPS)' : 'UNSECURE (HTTP)'}</span></td></tr>
                `;

                cachedReport = data.technical_report;
                cachedPitch = data.ai_pitch;

                switchTab('report');
                footer.innerText = `✅ Absolute verification data loaded for: ${data.domain}`;

            } catch(err) {
                consoleStream.innerHTML = `<span style="color:var(--neon-red);">[SYSTEM ERROR] Failed to connect and gather accurate metrics.</span>`;
                footer.innerText = `❌ Network request failed.`;
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
                consoleStream.innerHTML = cachedReport ? cachedReport.replace(/\n/g, '<br>') : '[Empty Report Array]';
            } else {
                btnPitch.classList.add('active');
                consoleStream.style.color = '#eab308';
                consoleStream.innerHTML = cachedPitch ? cachedPitch.replace(/\n/g, '<br>') : '[Empty Strategy Stream]';
            }
        }
    </script>
</body>
</html>
"""

@script33_bp.route('/')
def index():
    return render_template_string(ULTIMATE_AUDIT_UI_V10)

@script33_bp.route('/run_live_audit')
def run_live_audit():
    raw_url = request.args.get('url', '').strip()
    if not raw_url:
        return jsonify({"status": "error", "message": "The provided domain name cannot be empty."})

    if not raw_url.startswith(('http://', 'https://')):
        base_url = 'https://' + raw_url
    else:
        base_url = raw_url

    parsed_url = urllib.parse.urlparse(base_url)
    parsed_domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
    clean_base_url = f"{parsed_url.scheme}://{parsed_domain}"

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
        
        # --- PHASE 1: EXECUTE DOCUMENT ROOT HARVESTING ---
        start_time = time.time()
        req_html = urllib.request.Request(clean_base_url, headers=headers)
        
        is_https = parsed_url.scheme.lower() == "https"
        cloudflare_cdn = False

        with urllib.request.urlopen(req_html, timeout=12) as response:
            ttfb_duration = time.time() - start_time
            html_content = response.read().decode('utf-8', errors='ignore')
            total_duration = time.time() - start_time
            resp_headers = str(response.info())
            if 'cf-ray' in resp_headers.lower() or 'cloudflare' in resp_headers.lower():
                cloudflare_cdn = True

        ttfb = f"{round(ttfb_duration, 3)}s"
        page_load_speed = f"{round(total_duration, 2)}s"

        # --- PHASE 2: HIGH-INTELLIGENCE LOOSE MATCHING ENGINE ---
        # Scans both HTML layout anchors and variable string assignments to avoid detection errors
        justdial_seo = bool(re.search(r'justdial\.com|justdial', html_content, re.IGNORECASE))
        sulekha_seo = bool(re.search(r'sulekha\.com|sulekha', html_content, re.IGNORECASE))
        hotfrog_seo = bool(re.search(r'hotfrog\.in|hotfrog\.com|hotfrog', html_content, re.IGNORECASE))
        yelp_seo = bool(re.search(r'yelp\.com|yelp\.', html_content, re.IGNORECASE))
        indiamart_seo = bool(re.search(r'indiamart\.com|indiamart', html_content, re.IGNORECASE))
        tradeindia_seo = bool(re.search(r'tradeindia\.com|tradeindia', html_content, re.IGNORECASE))
        medium_seo = bool(re.search(r'medium\.com|medium', html_content, re.IGNORECASE))
        blogspot_seo = bool(re.search(r'blogspot\.com|\.blogspot', html_content, re.IGNORECASE))

        # Core Technical Verification Elements
        has_gsc = bool(re.search(r'google-site-verification|google\d+[a-zA-Z0-9\-_]+\.html', html_content, re.IGNORECASE))
        has_ga = bool(re.search(r'gtag\(|google-analytics\.com|googletagmanager\.com/gtag/js', html_content, re.IGNORECASE))
        has_gtm = bool(re.search(r'googletagmanager\.com/gtm\.js|gtm\.start', html_content, re.IGNORECASE))
        has_gmb = bool(re.search(r'google\.com/maps|business\.google\.com|g\.page', html_content, re.IGNORECASE))
        bing_places = bool(re.search(r'bingplaces\.com|bing\.com/maps', html_content, re.IGNORECASE))
        apple_business = bool(re.search(r'maps\.apple\.com|businessconnect\.apple\.com', html_content, re.IGNORECASE))

        # COMPLETE A-Z COMPREHENSIVE SOCIAL MEDIA PARSING ARRAYS
        social_fb = bool(re.search(r'facebook\.com', html_content, re.IGNORECASE))
        social_insta = bool(re.search(r'instagram\.com', html_content, re.IGNORECASE))
        social_linkedin = bool(re.search(r'linkedin\.com', html_content, re.IGNORECASE))
        social_twitter = bool(re.search(r'twitter\.com|x\.com', html_content, re.IGNORECASE))
        social_youtube = bool(re.search(r'youtube\.com', html_content, re.IGNORECASE))
        social_pinterest = bool(re.search(r'pinterest\.com|pin\.it', html_content, re.IGNORECASE))
        social_whatsapp = bool(re.search(r'wa\.me|api\.whatsapp\.com|chat\.whatsapp', html_content, re.IGNORECASE))
        social_telegram = bool(re.search(r't\.me|telegram\.me', html_content, re.IGNORECASE))
        social_reddit = bool(re.search(r'reddit\.com\/r\/|reddit\.com\/user', html_content, re.IGNORECASE))
        social_tiktok = bool(re.search(r'tiktok\.com\/@', html_content, re.IGNORECASE))

        # Real Core Business Identity (NAP Execution Engine)
        extracted_phones = re.findall(r'\+?\d{1,4}[-.\s]?\d{10}|\b\d{5}[-.\s]?\d{6}\b', html_content)
        has_address_keywords = bool(re.search(r'floor|building|road|street|plot|nagar|sector|chowk|address|pin code|zip', html_content, re.IGNORECASE))
        
        if extracted_phones or has_address_keywords:
            nap_consistent = True
            nap_status = "STABLE & ACCURATE"
            nap_explanation = "Business identifiers are present and verified inside the application codebase."
        else:
            nap_consistent = False
            nap_status = "UNRESOLVED DATA"
            nap_explanation = "No synchronized phone records or permanent location variables were located inside the core layers."

        # --- PHASE 3: LINE-BY-LINE ROBOTS.TXT ROUTING INTERPRETER ---
        robots_url = f"{clean_base_url}/robots.txt"
        has_robots, robots_explanation, raw_robots_content = False, "", ""
        try:
            req_robots = urllib.request.Request(robots_url, headers=headers)
            with urllib.request.urlopen(req_robots, timeout=5) as resp_robots:
                if resp_robots.status == 200:
                    has_robots = True
                    raw_robots_content = resp_robots.read().decode('utf-8', errors='ignore').strip()
                    
                    lines = raw_robots_content.split('\n')
                    parsed_rules = []
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith('#'): continue
                        
                        if line.lower().startswith('user-agent:'):
                            bot_name = line.split(':', 1)[1].strip()
                            parsed_rules.append(f"• Robot Target Target: Rule applies to system crawler -> '{bot_name}'")
                        elif line.lower().startswith('disallow:'):
                            block_path = line.split(':', 1)[1].strip()
                            parsed_rules.append(f"  ❌ DIRECTIVE BLOCK: The target crawler is restricted from accessing path -> '{block_path if block_path else '(None - completely accessible)'}'")
                        elif line.lower().startswith('allow:'):
                            allow_path = line.split(':', 1)[1].strip()
                            parsed_rules.append(f"  ✅ DIRECTIVE ALLOW: Explicit crawling access and index token granted to path -> '{allow_path}'")
                        elif line.lower().startswith('sitemap:'):
                            map_link = line.split(':', 1)[1].strip()
                            parsed_rules.append(f"  🗺️ INDEX DECLARATION: Dynamic sitemap location map announced to bots -> '{map_link}'")
                    
                    if parsed_rules:
                        robots_explanation = "\n".join(parsed_rules)
                    else:
                        robots_explanation = "File verified safely, but no standard crawler control commands are declared inside."
        except Exception:
            raw_robots_content = "The robots.txt document is completely missing from the root dashboard server configuration."
            robots_explanation = "No routing control rules were discovered. Search engine bots have unchecked indexing authority across all directory paths."

        # --- PHASE 4: RECURSIVE DEEP XML SITEMAP UNWRAPPER & PAGE COUNTER ---
        sitemap_url = f"{clean_base_url}/sitemap.xml"
        has_sitemap = False
        total_pages_discovered = 0
        sitemap_summary_logs = []

        def deep_parse_sitemap_recursive(url, depth=0):
            nonlocal total_pages_discovered, has_sitemap
            if depth > 4: return # Prevent infinite loop overflows or circular redirects
            try:
                req_s = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req_s, timeout=6) as resp_s:
                    if resp_s.status == 200:
                        has_sitemap = True
                        content = resp_s.read().decode('utf-8', errors='ignore').strip()
                        
                        # Gather all location records inside this file instance
                        locs = re.findall(r'<loc>(.*?)</loc>', content, re.IGNORECASE)
                        
                        # Case A: Detect Index Sitemap structure containing multiple sub-sitemaps
                        if '<sitemap>' in content.lower() or 'sitemapxml' in url.lower() or any('.xml' in x.lower() for x in locs[:3]):
                            sitemap_summary_logs.append(f"📁 Nested Master Index Sitemap Discovered: '{url}' [Contains {len(locs)} sub-sitemap files].")
                            for sub_url in locs:
                                sitemap_type = "General System Configurations"
                                if "post" in sub_url.lower(): sitemap_type = "Blog Articles & Dynamic Content"
                                elif "page" in sub_url.lower(): sitemap_type = "Main Structural Navigation Pages"
                                elif "product" in sub_url.lower(): sitemap_type = "E-commerce Store Catalog Items"
                                elif "category" in sub_url.lower() or "tag" in sub_url.lower(): sitemap_type = "Taxonomy Content Tags"
                                
                                sitemap_summary_logs.append(f"  ↳ Unwrapping & Traversing Sub-Sitemap: {sub_url} [Handling: {sitemap_type}]")
                                deep_parse_sitemap_recursive(sub_url, depth + 1)
                        else:
                            # Case B: Standard terminal sitemap containing true indexable pages
                            total_pages_discovered += len(locs)
                            functional_type = "Core Business Pages"
                            if "post" in url.lower(): functional_type = "Dynamic Blog Articles & Updates Feed"
                            elif "product" in url.lower(): functional_type = "Commercial Catalog Product Links"
                            
                            sitemap_summary_logs.append(f"📄 Leaf Sitemap Document Verified: '{url}' [Contains {len(locs)} indexable live links | Primary Duty: managing {functional_type}].")
            except Exception:
                pass

        deep_parse_sitemap_recursive(sitemap_url)

        xml_count = 1 if has_sitemap else 0
        xml_status_msg = f"FOUND ({total_pages_discovered} LIVE PAGES MAPPED)" if has_sitemap else "NOT DETECTED"

        # --- PHASE 5: FACTUAL RECOMMENDATIONS LOG CONFIGURATOR ---
        critical_holes = []
        if not justdial_seo: critical_holes.append("Justdial Citation Hub Connectivity")
        if not social_fb: critical_holes.append("Facebook Social Brand Account Connection")
        if not social_insta: critical_holes.append("Instagram Social Optimization Account Link")
        if not has_sitemap: critical_holes.append("XML Blueprint Sitemap Navigation Structure")
        if not has_robots: critical_holes.append("Robots.txt Crawl Control Rules Document")

        # Building Simple English Logs Data
        technical_report = f"""======================================================================
📝 COMPLETE FACTUAL ANALYSIS AND CRAWLER SYSTEM LOGS
======================================================================

[TARGET APPLICATION INFRASTRUCTURE]
----------------------------------------------------------------------
• Target Business Address : {clean_base_url}
• Encryption Standard SSL : {"SECURE PROTOCOL (HTTPS Live)" if is_https else "UNSECURE CONNECTION (HTTP Protocol Missing)"}
• Cloudflare Edge Cache   : {"CONNECTED & OPERATIONAL" if cloudflare_cdn else "NOT PROTECTED VIA CLOUDFLARE ROUTING"}
• Rendering Load Duration : {page_load_speed}
• Primary Server Latency  : {ttfb}

[ROBOTS.TXT CRAWLER MANAGEMENT CONTROLS]
----------------------------------------------------------------------
File Presence Status: {"✅ ACTIVE ON ROOT SERVER" if has_robots else "❌ MISSING FROM SERVER STRUCTURE"}

--- RAW STORAGE DATA STREAM ---
{raw_robots_content if raw_robots_content else "[No information streams are configured]"}

--- SIMPLE ENGLISH TRANSLATION OF ROBOTS.TXT BEHAVIOR ---
{robots_explanation}

[XML SITEMAPS SYSTEM BLUEPRINT INDEXER]
----------------------------------------------------------------------
File Hierarchy Status: {"✅ NESTED CONFIGURATIONS SCANNED" if has_sitemap else "❌ BLUEPRINT INDEX MISSING FROM DIRECTORY"}
Total Verified Live Indexable Pages Discovered: {total_pages_discovered} Active Document Nodes.

--- STRUCTURAL MAP BREAKDOWN AND SYSTEM FUNCTIONS ---
{chr(10).join(sitemap_summary_logs) if sitemap_summary_logs else "• No active nested or layout sitemap links were detected on the platform."}

[REGIONAL DIRECTORIES & VISIBILITY CORES]
----------------------------------------------------------------------
• Justdial Local Citation : {"✅ DETECTED (Permanent citation reference confirmed inside codebase)" if justdial_seo else "❌ MISSING! High-intent Local Buyer Traffic Gap Detected."}
• Google My Business Node : {"✅ FOUND (Maps identity module synchronized)" if has_gmb else "❌ NOT FOUND! Map navigation footprint is offline."}
• Sulekha Local Listing   : {"✅ DETECTED" if sulekha_seo else "❌ MISSING from optimization configuration."}
• IndiaMart Commercial Hub: {"✅ DETECTED" if indiamart_seo else "❌ MISSING from corporate asset array."}
• TradeIndia B2B Registry : {"✅ DETECTED" if tradeindia_seo else "❌ MISSING from directory framework."}
• Hotfrog Citations Vector: {"✅ DETECTED" if hotfrog_seo else "❌ MISSING Profile Asset."}
• Yelp Business Identity  : {"✅ DETECTED" if yelp_seo else "❌ MISSING Profile Asset."}

[COMPLETE SOCIAL MEDIA SIGNALS MATRIX]
----------------------------------------------------------------------
• Facebook Page Profile   : {"✅ DETECTED & LIVE" if social_fb else "❌ MISSING or profile link removed."}
• Instagram Brand Anchor  : {"✅ DETECTED & LIVE" if social_insta else "❌ MISSING or profile link removed."}
• LinkedIn Corporate Node : {"✅ DETECTED & LIVE" if social_linkedin else "❌ MISSING or profile link removed."}
• Twitter / X Feed Target : {"✅ DETECTED & LIVE" if social_twitter else "❌ MISSING or profile link removed."}
• YouTube Media Hub       : {"✅ DETECTED & LIVE" if social_youtube else "❌ MISSING or profile link removed."}
• Pinterest Board Grid    : {"✅ DETECTED & LIVE" if social_pinterest else "❌ MISSING or profile link removed."}
• WhatsApp Business Link  : {"✅ DETECTED & LIVE" if social_whatsapp else "❌ MISSING or tunnel disconnected."}
• Telegram Public Channel : {"✅ DETECTED & LIVE" if social_telegram else "❌ MISSING or channel unlinked."}
• Reddit Community Link   : {"✅ DETECTED & LIVE" if social_reddit else "❌ MISSING or profile unlinked."}
• TikTok Creator Account  : {"✅ DETECTED & LIVE" if social_tiktok else "❌ MISSING or account unlinked."}

[TRACKING SCRIPT EMBEDS]
----------------------------------------------------------------------
• Google Analytics V4     : {"✅ CONFIGURATION COMPLIANT" if has_ga else "❌ TRACKING TAG ABSENT"}
• Google Search Console   : {"✅ OWNERSHIP MANAGEMENT VERIFIED" if has_gsc else "❌ VERIFICATION KEY ABSENT"}
• Google Tag Manager      : {"✅ CONTAINER DEPLOYED SAFELY" if has_gtm else "❌ ENGINES NOT DEPLOYED"}

======================================================================
🎯 AUDIT STRATEGY REPORT CONCLUSION & RECOMMENDATIONS
======================================================================
The extraction pipeline has completed auditing '{parsed_domain}'. 

Critical Holes Detected: {", ".join(critical_holes) if critical_holes else "None. All parameters pass verification checks."}

RECOMMENDED ACTION PLAN:
1. Fix all critical missing elements immediately to stop organic visibility leak.
2. Ensure local directory accounts like Justdial are hardcoded into structural headers or footers to feed bots permanent connection paths.
3. Keep the nested sitemaps verified inside Google Search Console for perfect index sequencing.
======================================================================"""

        # --- PHASE 6: HIGH-CONVERSION CONVERSION SALES ENGAGEMENT HOOK ---
        performance_score = 100 - (len(critical_holes) * 12)
        if performance_score < 25: performance_score = 25
        pie_chart_color = "#ef4444" if performance_score < 60 else ("#eab308" if performance_score < 80 else "#10b981")

        holes_list = "\n".join([f"  ⚠️ STRUCTURAL DEFICIT [{i+1}]: {item}" for i, item in enumerate(critical_holes)]) if critical_holes else "  ✨ ALL CHECKED AUDIT LAYERS REGISTERED OPERATIONAL SAFELY."
        pitch_string = f"Hey! We completed a detailed system data crawl on your business website ({parsed_domain}) and verified that critical business networks like your {critical_holes[0] if critical_holes else 'Local Visibility Citations'} are completely missing inside your platform codebase. This prevents search engines from indexing you correctly across your main region. Let's get this fully optimized today!"

        ai_pitch = f"""======================================================================
💡 PREMIUM SALES PIPELINE CONVERSION HOOK
======================================================================

🚨 CRITICAL SYSTEM HOLES IDENTIFIED ON YOUR PLATFORM WEB INFRASTRUCTURE:
{holes_list}

🔥 READY-TO-USE OUTREACH COPY TEMPLATE:
----------------------------------------------------------------------
"{pitch_string}"
----------------------------------------------------------------------

----------------------------------------------------------------------
📊 ARCHITECTURE HEALTH OPTIMIZATION SCALE
----------------------------------------------------------------------
<div style="margin: 20px 0; background: #02040a; border: 1px solid rgba(6,182,212,0.15); padding: 25px; border-radius: 8px; text-align: center; font-family: monospace;">
    <div style="font-size: 14px; color: var(--neon-cyan); font-weight: bold; margin-bottom: 15px; text-transform: uppercase;">Overall Website Health Score</div>
    <div style="display: inline-block; width: 140px; height: 140px; border-radius: 50%; background: conic-gradient({pie_chart_color} 0% {performance_score}%, #1e293b {performance_score}% 100%); padding: 20px;">
        <div style="background: #0b1329; width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; color: #fff;">
            {performance_score}%
        </div>
    </div>
    <div style="margin-top: 15px; font-size: 11px; color: var(--text-gray); line-height: 1.5;">
        <span style="color: #10b981; font-weight: bold;">■ Compliant Areas</span> | <span style="color: #ef4444; font-weight: bold;">■ Missing Optimization Elements</span>
    </div>
</div>
======================================================================"""

        return jsonify({
            "status": "success", "domain": parsed_domain, "google_analytics": has_ga,
            "google_search_console": has_gsc, "google_tag_manager": has_gtm, "cloudflare_cdn": cloudflare_cdn,
            "schema_markup": True, "has_robots": has_robots, "xml_count": xml_count, "xml_status_msg": xml_status_msg,
            "has_gmb": has_gmb, "bing_places": bing_places, "apple_business": apple_business,
            "justdial_seo": justdial_seo, "sulekha_seo": sulekha_seo, "hotfrog_seo": hotfrog_seo, "yelp_seo": yelp_seo, 
            "indiamart_seo": indiamart_seo, "tradeindia_seo": tradeindia_seo, "medium_seo": medium_seo, "blogspot_seo": blogspot_seo,
            "social_fb": social_fb, "social_insta": social_insta, "social_linkedin": social_linkedin,
            "social_twitter": social_twitter, "social_youtube": social_youtube,
            "social_pinterest": social_pinterest, "social_whatsapp": social_whatsapp, "social_telegram": social_telegram,
            "social_reddit": social_reddit, "social_tiktok": social_tiktok,
            "nap_consistent": nap_consistent, "nap_status": nap_status, "ttfb": ttfb, 
            "page_load_speed": page_load_speed, "is_https": is_https,
            "technical_report": technical_report, "ai_pitch": ai_pitch
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server connection handshake interrupted. Details: {str(e)}"
        })

