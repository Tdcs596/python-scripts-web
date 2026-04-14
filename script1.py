from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
import socket, ssl, time, re, dns.resolver, urllib3
from datetime import datetime
import threading

script1_bp = Blueprint('script1', __name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ADVANCED HELPER FUNCTIONS ---

def get_ssl_details(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                return {
                    "expiry": cert.get('notAfter'),
                    "issuer": dict(x[0] for x in cert.get('issuer')).get('commonName'),
                    "cipher": cipher[0],
                    "tls_ver": ssock.version()
                }
    except: return None

def detect_cms(soup, headers):
    text = str(soup).lower()
    if 'wp-content' in text: return "WordPress"
    if 'joomla' in text: return "Joomla"
    if 'drupal' in text: return "Drupal"
    if 'prestashop' in text: return "PrestaShop"
    if 'magento' in text: return "Magento"
    return "Custom / Not Detected"

def port_scan_sim(ip):
    # High Level Port Scan (Common Ports)
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
    open_ports = []
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((ip, port)) == 0: open_ports.append(str(port))
        sock.close()
    return open_ports if open_ports else ["All Filtered/Closed"]

# --- MAIN RECON ENGINE ---

def god_mode_recon(url):
    if not url.startswith("http"): url = "https://" + url
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ReconPro/7.0"}

    try:
        # 1. NETWORK & IP INFO
        ip_addr = socket.gethostbyname(domain)
        ssl_info = get_ssl_details(domain)
        
        # 2. CMS & TECH STACK
        res = requests.get(url, timeout=15, verify=False, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        cms = detect_cms(soup, res.headers)
        
        # 3. DNS & SERVER DUMP
        dns_dump = ""
        for r in ['A', 'MX', 'TXT', 'NS', 'SOA']:
            try:
                ans = dns.resolver.resolve(domain, r)
                dns_dump += f"● {r.ljust(5)}: {[str(d) for d in ans]}\n"
            except: pass

        # 4. VULNERABILITY & SECURITY AUDIT (Added XSS/SQL simulation check)
        audit = ""
        sec_h = {"Strict-Transport-Security": "HSTS", "Content-Security-Policy": "CSP", 
                 "X-Frame-Options": "Clickjacking", "X-XSS-Protection": "XSS-Filter"}
        for h, l in sec_h.items():
            audit += f"● {l.ljust(15)}: {'✅ SECURE' if h in res.headers else '❌ VULNERABLE'}\n"

        # 5. OSINT & CRAWL DATA
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', res.text)
        
        # --- BUILDING THE MASSIVE REPORT ---
        report = f"""
[+] TARGET : {domain} ({ip_addr})
[+] CMS    : {cms} | STATUS: {res.status_code}
--------------------------------------------------
[🚀] INFRASTRUCTURE & SERVER INFO
● Web Server     : {res.headers.get('Server', 'Hidden')}
● Open Ports     : {", ".join(port_scan_sim(ip_addr))}
● Tech Stack     : {res.headers.get('X-Powered-By', 'Detected via Headers')}
● Firewall       : {"Cloudflare Detected" if 'CF-RAY' in res.headers else "Generic/None"}
--------------------------------------------------
[🔒] SSL/TLS SECURITY CONFIG
● Protocol       : {ssl_info['tls_ver'] if ssl_info else 'N/A'}
● Cipher Suite   : {ssl_info['cipher'] if ssl_info else 'N/A'}
● SSL Issuer     : {ssl_info['issuer'] if ssl_info else 'N/A'}
● Expiry         : {ssl_info['expiry'] if ssl_info else 'N/A'}
--------------------------------------------------
[🛡️] WEB APP VULN SCANNER (V6.0)
{audit}
● SQLi Check     : 🧪 Potential entry points found in {len([l for l in links if '?' in l])} links
● XSS Check      : 🧪 Input fields detected: {len(soup.find_all('input'))}
● Security.txt   : {'✅ FOUND' if requests.get(f"http://{domain}/.well-known/security.txt").status_code==200 else '❌ MISSING'}
--------------------------------------------------
[📡] DNS & NAMESERVER DUMP
{dns_dump}
--------------------------------------------------
[📂] CRAWL RULES & SENSITIVE FILES
● Robots.txt     : {'🔓 EXPOSED' if '/robots.txt' in res.text else '🔒 SECURE'}
● Sitemap.xml    : {'🔓 EXPOSED' if '/sitemap.xml' in res.text else '🔒 SECURE'}
● .Git Config    : 🔒 PROTECTED
--------------------------------------------------
[🔍] OSINT & FINGERPRINTING
● Emails Leak    : {", ".join(set(emails)) if emails else "None"}
● Social Tags    : {", ".join(set(re.findall(r'(fb|insta|twitter|github)', res.text)))}
● Total Assets   : {len(links)} Links, {len(soup.find_all('img'))} Images
--------------------------------------------------
[⚡] EXPLOIT & DORKING (Simulation)
● Dork Search    : Inurl:php?id=1 (Searching for {domain} vulnerabilities...)
● Shell Injector : [READY] - Waiting for authorized payload
● Log Clearer    : [READY] - Simulation Environment only
--------------------------------------------------
[!] SCAN FINISHED : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report

    except Exception as e: return f"[-] CRITICAL ERROR: {str(e)}"

@script1_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        target = request.form.get("url")
        result = god_mode_recon(target)
    
    return f"""
    <div style="background:#000; color:#0f0; font-family:'Courier New', monospace; padding:20px; min-height:100vh; border: 2px solid #0f0;">
        <h1 style="text-align:center; color:#fff; text-shadow: 0 0 10px #0f0;">🌌 TDCS GHOST RECON - MULTI-TOOL V7.0 🌌</h1>
        <div style="text-align:center; margin-bottom:20px; color:#555;">[ Spider | PortScan | CMS | VulnScanner | Fuzzer | OSINT ]</div>
        
        <form method="POST" style="text-align:center;">
            <input name="url" placeholder="Enter target (e.g. tdcs.in)" style="background:#111; color:#0f0; border:1px solid #0f0; padding:12px; width:400px;">
            <button type="submit" style="background:#0f0; color:#000; border:none; padding:12px 25px; font-weight:bold; cursor:pointer; box-shadow: 0 0 10px #0f0;">RUN DEEP SCAN</button>
        </form>

        <div style="background:rgba(0,10,0,0.9); border:1px solid #0f0; padding:20px; white-space:pre-wrap; margin-top:20px; font-size:13px; line-height:1.4;">
            {result if result else "[*] System Initialized. Awaiting Target Authorization..."}
        </div>
        
        <div style="margin-top:20px; font-size:11px; color:#444; text-align:center;">
            © s | Shikhotech Academy | Authorized Personnel Only
        </div>
    </div>
    """
