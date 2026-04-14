import requests
from bs4 import BeautifulSoup
import socket
import ssl
import time
from datetime import datetime
import urllib3

# SSL warnings bypass (Insecure sites ke liye)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(url):
    # 1. URL Cleanup & Domain Extraction
    if not url.startswith("http"):
        url = "http://" + url
    
    # Domain nikalna DNS aur SSL check ke liye
    domain = url.replace("https://", "").replace("http://", "").split('/')[0]
    
    # 2. Advanced Bot Bypass Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }

    report = f"╔══════════════════════════════════════════════════════════╗\n"
    report += f"║       🚀 ULTIMATE WEBSITE INTELLIGENCE REPORT            ║\n"
    report += f"╚══════════════════════════════════════════════════════════╝\n"
    report += f"Target URL : {url}\n"
    report += f"Scan Date  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"------------------------------------------------------------\n\n"

    try:
        # --- [NETWORK & IP RESOLVER] ---
        try:
            ip_addr = socket.gethostbyname(domain)
        except:
            ip_addr = "Could not resolve IP"

        # --- [SPEED TEST & PERFORMANCE] ---
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        end_time = time.time()
        load_speed = round(end_time - start_time, 3)

        report += f"[📡 NETWORK & PERFORMANCE]\n"
        report += f"● Server IP      : {ip_addr}\n"
        report += f"● Status Code    : {response.status_code}\n"
        report += f"● Response Time  : {load_speed} Seconds\n"
        report += f"● Server Tech    : {response.headers.get('Server', 'Hidden')}\n\n"

        # --- [SSL CERTIFICATE CHECKER] ---
        report += f"[🔒 SSL/SECURITY INFO]\n"
        if url.startswith("https"):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        expiry = cert.get('notAfter')
                        report += f"● SSL Status     : ✅ Active\n"
                        report += f"● Expiry Date    : {expiry}\n"
            except:
                report += f"● SSL Status     : ⚠️ SSL Check Failed\n"
        else:
            report += f"● SSL Status     : ❌ No HTTPS (Insecure)\n"

        # --- [SECURITY AUDIT - HEADERS] ---
        sec_headers = {
            "X-Frame-Options": "Clickjacking",
            "Content-Security-Policy": "XSS Protection",
            "Strict-Transport-Security": "HSTS",
            "X-Content-Type-Options": "MIME Sniffing"
        }
        for h, label in sec_headers.items():
            status = "✅ Found" if h in response.headers else "❌ Missing"
            report += f"● {label} ({h}): {status}\n"
        report += "\n"

        # --- [SEO & CONTENT OVERVIEW] ---
        soup = BeautifulSoup(response.text, 'html.parser')
        report += f"[🔍 SEO & CONTENT ANALYSIS]\n"
        report += f"● Page Title     : {soup.title.string if soup.title else 'N/A'}\n"
        
        meta = soup.find('meta', attrs={'name': 'description'})
        report += f"● Meta Desc      : {meta['content'] if meta else 'N/A'}\n"
        
        report += f"● Total Links    : {len(soup.find_all('a'))}\n"
        report += f"● Total Images   : {len(soup.find_all('img'))}\n\n"

        # --- [TECH DETECTOR] ---
        report += f"[🛠️ TECHNOLOGY DETECTION]\n"
        tech_stack = []
        html_content = response.text.lower()
        
        if "wp-content" in html_content: tech_stack.append("WordPress")
        if "next/static" in html_content: tech_stack.append("Next.js")
        if "cloudflare" in response.headers.get('Server', '').lower(): tech_stack.append("Cloudflare")
        if "php" in response.headers.get('X-Powered-By', '').lower(): tech_stack.append("PHP")
        if "react" in html_content: tech_stack.append("React.js")
        
        report += f"● Detected Tech  : {', '.join(tech_stack) if tech_stack else 'Generic/Other'}\n"

        report += f"\n------------------------------------------------------------\n"
        report += f"✅ Analysis Completed Successfully."
        return report

    except Exception as e:
        return f"❌ Error analyzing site: {str(e)}"
