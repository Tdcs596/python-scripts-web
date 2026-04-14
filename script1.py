from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
import socket
import ssl
import time
from datetime import datetime
import urllib3
import dns.resolver # Iske liye 'dnspython' chahiye requirements.txt mein

# Blueprint for app.py
script1_bp = Blueprint('script1', __name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def advanced_recon(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    report = ""
    
    try:
        # 1. Network Intel
        ip_addr = socket.gethostbyname(domain)
        
        # 2. DNS Records (MX & TXT) - Leak checking
        dns_info = ""
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            dns_info += f"● Mail Servers (MX): {[str(data.exchange) for data in mx_records]}\n"
            txt_records = dns.resolver.resolve(domain, 'TXT')
            dns_info += f"● TXT/SPF Records : {[str(data) for data in txt_records[:2]]}\n"
        except:
            dns_info += "● DNS Records     : Protected/Not Found\n"

        # 3. HTTP Headers & Server Leaks
        start_time = time.time()
        res = requests.get(url, timeout=10, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        load_time = round(time.time() - start_time, 3)
        
        server = res.headers.get('Server', 'Protected')
        powered_by = res.headers.get('X-Powered-By', 'Hidden')

        # 4. Security Audit (Advanced)
        sec_checks = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP/XSS",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "MIME-Sniff",
            "Permissions-Policy": "Feature-Control"
        }
        sec_report = ""
        for h, name in sec_checks.items():
            status = "✅ SAFE" if h in res.headers else "❌ VULNERABLE"
            sec_report += f"● {name.ljust(15)}: {status}\n"

        # 5. Robots.txt & Hidden Paths
        robots_url = f"https://{domain}/robots.txt"
        robots_res = requests.get(robots_url, timeout=5)
        robots_status = "✅ Exposed" if robots_res.status_code == 200 else "❌ Hidden"

        # 6. SEO & Meta Intel
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string[:50] if soup.title else "N/A"
        links_count = len(soup.find_all('a'))
        scripts_count = len(soup.find_all('script'))

        # FINAL FORMATTED REPORT
        report = f"""
[+] TARGET      : {url}
[+] IP ADDRESS  : {ip_addr}
[+] STATUS      : {res.status_code} OK
[+] LOAD SPEED  : {load_time}s
--------------------------------------------------
[🔍] INFRASTRUCTURE & SERVER INTEL
● Web Server    : {server}
● Backend Tech  : {powered_by}
● Robots.txt    : {robots_status}
{dns_info}
--------------------------------------------------
[🛡️] SECURITY VULNERABILITY AUDIT
{sec_report}
--------------------------------------------------
[📊] CONTENT & RECON DATA
● Page Title    : {title}...
● Internal JS   : {scripts_count} Scripts detected
● Total Links   : {links_count} Links found
● SSL Expiry    : {res.url.split(':')[0].upper()} encrypted
--------------------------------------------------
[!] SCAN COMPLETED : {datetime.now().strftime('%H:%M:%S')}
"""
        return report

    except Exception as e:
        return f"[-] ERROR: {str(e)}"

@script1_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        result = advanced_recon(url)
    
    return f"""
    <div style="background:#0a0a0a; color:#00ff00; font-family:'Courier New'; padding:20px; min-height:100vh;">
        <h2 style="color:#fff; border-bottom:2px solid #00ff00; display:inline-block;">⚡ CYBER MASTER PRO RECON v4.0</h2>
        <form method="POST" style="margin:20px 0;">
            <input name="url" placeholder="Enter target (tdcs.in)" style="background:#1a1a1a; color:#0f0; border:1px solid #0f0; padding:10px; width:300px;">
            <button type="submit" style="background:#00ff00; color:#000; border:none; padding:10px 20px; font-weight:bold; cursor:pointer;">INFILTRATE</button>
        </form>
        <div style="background:#000; border:1px solid #333; padding:20px; border-radius:5px; box-shadow: 0 0 15px rgba(0,255,0,0.2); white-space:pre-wrap; line-height:1.5;">
            {result if result else "[*] Awaiting target for deep reconnaissance..."}
        </div>
        <br>
        <a href="/" style="color:#888; text-decoration:none;">[ ESCAPE TO DASHBOARD ]</a>
    </div>
    """

