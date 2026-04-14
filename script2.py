from flask import Blueprint, request
import requests
from bs4 import BeautifulSoup
import csv
import io
from urllib.parse import urljoin, urlparse

# Blueprint for app.py connection
script2_bp = Blueprint('script2', __name__)

def advanced_scrape(url):
    if not url.startswith("http"):
        url = "http://" + url
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        domain = urlparse(url).netloc

        # 1. Scraping All Links (Internal vs External)
        links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            if domain in full_url:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        # 2. Scraping All Media (Images & Alt Text)
        images = [{"src": img.get('src'), "alt": img.get('alt', 'No Alt')} for img in soup.find_all('img')]

        # 3. Scraping Structured Content (Headings & Paragraphs)
        headings = {
            "h1": [h.text.strip() for h in soup.find_all('h1')],
            "h2": [h.text.strip() for h in soup.find_all('h2')],
            "h3": [h.text.strip() for h in soup.find_all('h3')]
        }

        # 4. Scraping Table Data (If any)
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                rows.append(cells)
            tables.append(rows)

        # 5. Advanced Metadata (Emails & Phone Numbers - Regex-lite)
        # (Yahan hum basic text search kar rahe hain)
        text_content = soup.get_text()
        
        # Final Formatting
        report = f"📂 --- ADVANCED WEB SCRAPER REPORT: {domain} --- 📂\n"
        report += f"URL Checked: {url}\n"
        report += "--------------------------------------------------\n\n"
        
        report += f"[🔗 LINK ANALYSIS]\n"
        report += f"● Total Links Found    : {len(links)}\n"
        report += f"● Internal (Same Site) : {len(set(internal_links))}\n"
        report += f"● External (Outgoing)  : {len(set(external_links))}\n\n"

        report += f"[🖼️ MEDIA ASSETS]\n"
        report += f"● Images Found         : {len(images)}\n"
        for i, img in enumerate(images[:5]): # Sirf top 5 dikhayenge
            report += f"  └─ Image {i+1}: {img['src'][:50]}... (Alt: {img['alt']})\n"
        
        report += f"\n[📝 TEXT STRUCTURE]\n"
        report += f"● H1 Tags: {len(headings['h1'])} | H2 Tags: {len(headings['h2'])}\n"
        if headings['h1']:
            report += f"  └─ Main Topic: {headings['h1'][0]}\n"

        report += f"\n[📊 TABLE DATA]\n"
        report += f"● Total Tables Found   : {len(tables)}\n"
        if tables:
            report += f"  └─ First Table Row 1: {tables[0][0] if tables[0] else 'Empty'}\n"

        report += f"\n[📄 RAW SNIPPET (First 300 chars)]\n"
        report += f"{text_content.strip()[:300]}...\n"

        report += "\n--------------------------------------------------\n"
        report += "✅ Full Deep Scrape Completed."
        return report

    except Exception as e:
        return f"❌ Scraping Failed: {str(e)}"

@script2_bp.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        target_url = request.form.get("url")
        result = advanced_scrape(target_url)
    
    return f"""
    <div style="font-family: 'Courier New', monospace; padding: 20px; background-color: #f9f9f9;">
        <h2 style="color: #2c3e50;">🕷️ Advanced Web Scraper v2.0</h2>
        <p>Extract links, images, tables, and structured data instantly.</p>
        <form method="POST">
            <input name="url" placeholder="https://target-website.com" style="padding:12px; width:350px; border: 1px solid #ccc; border-radius: 4px;" required>
            <button type="submit" style="padding:12px 20px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer;">Start Scraping</button>
        </form>
        <br>
        <div style="background: #ffffff; padding: 20px; border-left: 5px solid #27ae60; box-shadow: 0 2px 5px rgba(0,0,0,0.1); white-space: pre-wrap;">
            {result if result else "Enter a URL to begin deep data extraction..."}
        </div>
        <br>
        <a href="/" style="text-decoration: none; color: #3498db;">⬅️ Back to Control Panel</a>
    </div>
    """
