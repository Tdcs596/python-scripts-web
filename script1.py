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
    except: return None

def advanced_recon(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    
    # Ye headers bot protection bypass karne ke liye hain (Links fix karne ke liye)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    try:
        # 1. Network & SSL (Pehle wala features)
        ssl_info = get_ssl_details(domain)
        ip_addr = socket.gethostbyname(domain)
        
        # 2. DNS Intel (Pehle wala)
        dns_report = ""
        for r_type in ['A', 'MX', 'TXT', 'NS']:
            try:
                answers = dns.resolver.resolve(domain, r_type)
                dns_report += f"● {r_type.ljust(6)}: {[str(data) for data in answers[:2]]}\n"
            except: pass

        # 3. Main Request
        start_time = time.time()
        res = requests.get(url, timeout=15, verify=False, headers=headers)
        load_time = round(time.time() - start_time, 3)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 4. Security Audit (Pehle wala)
        sec_headers = {
            "Strict-Transport-Security": "HSTS (SSL Force)",
            "Content-Security-Policy": "CSP (XSS Filter)",
            "X-Frame-Options": "Clickjacking",
            "X-Content-Type-Options": "MIME Sniffing"
        }
        audit_res = ""
        for h, label in sec_headers.items():
            audit_res += f"● {label.ljust(20)}: {'✅ SECURE' if h in res.headers else '❌ VULNERABLE'}\n"

        # 5. Link & Image Extraction (The Fix)
        raw_links = [a.get('href') for a in soup.find_all('a', href=True)]
        images = [img.get('src') for img in soup.find_all('img', src=True)]
        
        # Links filter karna
        unique_links = list(set(raw_links))
        
        # 6. Sensitive Files (Pehle wala)
        files_check = ""
        for f in ['/robots.txt', '/sitemap.xml', '/.well-known/security.txt', '/.git/config']:
            try:
                f_res = requests.get(f"http://{domain}{f}", timeout=3, headers=headers)
                status = "🔓 EXPOSED" if f_res.status_code == 200 else "🔒 SECURE"
                files_check += f"● {f.ljust(22)}: {status}\n"
            except: pass

        # --- FINAL REPORT GENERATION ---
        report = f"""
[+] TARGET DOMAIN : {domain}
[+] IP ADDRESS    : {ip_addr}
[+] LOAD SPEED    : {load_time}s | STATUS: {res.status_code}
--------------------------------------------------
[🔒] SSL CERTIFICATE INTELLIGENCE
● Status      : {'✅ VALID' if ssl_info else '❌ INVALID'}
● Certificate : {ssl_info['issuer'] if ssl_info else 'N/A'}
● Expiry Date : {ssl_info['expiry'] if ssl_info else 'N/A'}
● Days Left   : {ssl_info['days'] if ssl_info else '0'} Days
--------------------------------------------------
[🛡️] SECURITY COMPLIANCE AUDIT
{audit_res}
--------------------------------------------------
[📡] DNS INFRASTRUCTURE DATA
{dns_report if dns_report else "● Records: Private/Hidden"}
--------------------------------------------------
[📂] SENSITIVE DIRECTORY SCAN
{files_check}
--------------------------------------------------
[🔍] CONTENT & OSINT DATA
● Page Title    : {soup.title.string.strip() if soup.title else 'N/A'}
● Total Images  : {len(images)}
● Total Links   : {len(raw_links)}
● Emails Found  : {", ".join(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', res.text))) or "None"}
--------------------------------------------------
[🔗] ALL EXTRACTED LINKS ({len(unique_links)})
"""
        # Saare links list karna
        for i, link in enumerate(unique_links):
            report += f"{i+1}. {link}\n"
            if i > 49: # Limit to 50 links so report doesn't crash browser
                report += "... (More links found, showing top 50)\n"
                break
                
        report += f"\n[!] SCAN FINISHED : {datetime.now().strftime('%H:%M:%S')}"
        return report

    except Exception as e:
        return f"[-] CRITICAL FAILURE: {str(e)}"

@script1_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        url = request.form.get("url")
        result = advanced_recon(url)
    
    return f"""
    <div style="background:#000; color:#0f0; font-family:'Courier New', monospace; padding:20px; min-height:100vh;">
        <h2 style="color:#fff; text-shadow: 0 0 10px #0f0;">💀 TDCS ULTIMATE RECON V6.0 (GOD MODE) 💀</h2>
        <form method="POST">
            <input name="url" placeholder="target.com" style="background:#111; color:#0f0; border:1px solid #0f0; padding:10px; width:350px;">
            <button type="submit" style="background:#0f0; color:#000; border:none; padding:10px 20px; font-weight:bold; cursor:pointer;">START INFILTRATION</button>
        </form>
        <div style="background:#000; border:1px solid #333; padding:20px; white-space:pre-wrap; margin-top:20px; box-shadow: 0 0 20px rgba(0,255,0,0.1);">
            {result if result else "[*] System Ready. Waiting for target authorization..."}
        </div>
        <br><a href="/" style="color:#666; text-decoration:none;">[ EXIT TO DASHBOARD ]</a>
    </div>
    """

