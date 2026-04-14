from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
import socket
import ssl
import time
from datetime import datetime
import urllib3
import dns.resolver
import re

script1_bp = Blueprint('script1', __name__)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ssl_details(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_str = cert.get('notAfter')
                issuer = dict(x[0] for x in cert.get('issuer'))
                expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.utcnow()).days
                return {
                    "expiry": expiry_date.strftime('%Y-%m-%d'),
                    "days": days_left,
                    "issuer": issuer.get('commonName', 'Unknown'),
                    "version": ssock.version()
                }
    except:
        return None

def advanced_recon(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    
    try:
        # 1. SSL DEEP SCAN
        ssl_info = get_ssl_details(domain)
        
        # 2. NETWORK & WHOIS-LITE
        ip_addr = socket.gethostbyname(domain)
        
        # 3. DNS HARVESTING (MX, TXT, NS, A)
        dns_report = ""
        for r_type in ['A', 'MX', 'TXT', 'NS', 'CNAME']:
            try:
                answers = dns.resolver.resolve(domain, r_type)
                dns_report += f"● {r_type.ljust(6)}: {[str(data) for data in answers]}\n"
            except: pass

        # 4. HTTP REQUEST & LEAK DETECTION
        start_time = time.time()
        res = requests.get(url, timeout=12, verify=False, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ReconBot/5.0"})
        load_time = round(time.time() - start_time, 3)
        
        # Header Leaks
        server = res.headers.get('Server', 'Protected/Hidden')
        powered = res.headers.get('X-Powered-By', 'Not Disclosed')
        via = res.headers.get('Via', 'None')

        # 5. SECURITY VULNERABILITY AUDIT (The BIG List)
        sec_headers = {
            "Strict-Transport-Security": "HSTS (SSL Force)",
            "Content-Security-Policy": "CSP (XSS Filter)",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "MIME Sniffing",
            "Referrer-Policy": "Data Leakage",
            "Permissions-Policy": "Hardware Access"
        }
        audit_res = ""
        for h, label in sec_headers.items():
            audit_res += f"● {label.ljust(20)}: {'✅ SECURE' if h in res.headers else '❌ VULNERABLE'}\n"

        # 6. CONTENT & OSINT DATA
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Email Discovery (Educational RegEx)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', res.text)
        email_leak = ", ".join(list(set(emails))[:3]) if emails else "No Public Emails Found"

        # Social & External Recon
        socials = []
        for a in soup.find_all('a', href=True):
            for p in ['fb.com', 'facebook', 'twitter', 'linkedin', 'instagram', 'github', 'youtube']:
                if p in a['href']: socials.append(p.split('.')[0])
        
        # 7. SENSITIVE FILES CHECK
        files_check = ""
        for f in ['/robots.txt', '/sitemap.xml', '/.well-known/security.txt', '/.git/config']:
            f_res = requests.get(f"http://{domain}{f}", timeout=3)
            status = "🔓 EXPOSED" if f_res.status_code == 200 else "🔒 SECURE"
            files_check += f"● {f.ljust(20)}: {status}\n"

        # --- THE MASTER REPORT ---
        return f"""
[+] TARGET DOMAIN : {domain}
[+] IP ADDRESS    : {ip_addr}
[+] RESPONSE TIME : {load_time}s | STATUS: {res.status_code}
--------------------------------------------------
[🔒] SSL/TLS ENCRYPTION LAYER
● Status      : {'✅ VALID' if ssl_info else '❌ INVALID/EXPIRED'}
● Certificate : {ssl_info['issuer'] if ssl_info else 'N/A'}
● Expiry Date : {ssl_info['expiry'] if ssl_info else 'N/A'}
● Days Left   : {ssl_info['days'] if ssl_info else '0'} Days
● Protocol    : {ssl_info['version'] if ssl_info else 'N/A'}
--------------------------------------------------
[🛡️] SECURITY COMPLIANCE AUDIT
{audit_res}
--------------------------------------------------
[📡] DNS INFRASTRUCTURE DATA
{dns_report if dns_report else "● Records: Private or Cloudflare Protected"}
--------------------------------------------------
[📂] SENSITIVE DIRECTORY SCAN
{files_check}
--------------------------------------------------
[🔍] OSINT & FINGERPRINTING
● Web Server  : {server}
● Tech Stack  : {powered}
● Proxy/Via   : {via}
● Emails Found: {email_leak}
● Socials     : {", ".join(set(socials)) if socials else "None Detected"}
● Total Assets: {len(soup.find_all('a'))} Links, {len(soup.find_all('img'))} Images
--------------------------------------------------
[!] SCAN FINISHED : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    except Exception as e:
        return f"[-] SYSTEM FAILURE: {str(e)}"

@script1_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        result = advanced_recon(url)
    
    return f"""
    <div style="background:#000; color:#00ff00; font-family:'Consolas', 'Courier New', monospace; padding:25px; min-height:100vh; border: 4px double #00ff00;">
        <h1 style="text-align:center; color:#fff; text-shadow: 0 0 15px #0f0;">💀 TDCS SHIKHOTECH - GHOST RECON 💀</h1>
        <hr style="border:1px solid #333;">
        <form method="POST" style="text-align:center; margin:20px;">
            <input name="url" placeholder="target.com" style="background:#111; color:#0f0; border:2px solid #0f0; padding:12px; width:400px; font-size:16px;">
            <button type="submit" style="background:#0f0; color:#000; border:none; padding:12px 25px; font-weight:bold; cursor:pointer; font-size:16px; box-shadow: 0 0 10px #0f0;">EXECUTE SCAN</button>
        </form>
        <div style="background:rgba(0,20,0,0.9); border:1px solid #0f0; padding:20px; white-space:pre-wrap; font-size:14px; box-shadow: inset 0 0 20px #000;">
            {result if result else "[*] System Initialized... Awaiting Target for Deep Analysis."}
        </div>
        <br>
        <div style="text-align:center;">
            <a href="/" style="color:#666; text-decoration:none; border: 1px solid #444; padding: 5px 10px;">[ TERMINATE SESSION ]</a>
        </div>
    </div>
    """
