import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def scrape(url):
    if not url.startswith("http"):
        url = "http://" + url

    try:
        res = requests.get(url, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")

        domain = urlparse(url).netloc

        # 🏷 Title
        title = soup.title.string.strip() if soup.title else "No Title"

        # 📄 Description
        desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            desc = meta.get("content", "")

        # 🔗 Links
        internal_links = []
        external_links = []

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a['href'])

            if domain in link:
                internal_links.append(link)
            else:
                external_links.append(link)

        # 🖼 Images
        images = [urljoin(url, img['src']) for img in soup.find_all("img", src=True)]

        # 📧 Emails
        emails = set(re.findall(r"[\w\.-]+@[\w\.-]+", res.text))

        # 📱 Phone Numbers (basic pattern)
        phones = set(re.findall(r"\+?\d[\d\s\-]{8,15}\d", res.text))

        # 🧾 Forms
        forms = []
        for form in soup.find_all("form"):
            action = form.get("action")
            method = form.get("method", "GET")
            forms.append(f"{method} → {action}")

        # ⚙️ JS Files
        js_files = [urljoin(url, s['src']) for s in soup.find_all("script", src=True)]

        return f"""
================= 🔥 ADVANCED SCRAPE =================

🌐 URL: {url}

🏷 Title:
{title}

📄 Description:
{desc}

----------------------------------------------------

🔗 Internal Links ({len(internal_links)}):
{internal_links[:20]}

🌍 External Links ({len(external_links)}):
{external_links[:10]}

🖼 Images ({len(images)}):
{images[:10]}

📧 Emails Found ({len(emails)}):
{list(emails)}

📱 Phone Numbers ({len(phones)}):
{list(phones)}

🧾 Forms Found ({len(forms)}):
{forms}

⚙️ JS Files ({len(js_files)}):
{js_files[:10]}

=====================================================
"""

    except Exception as e:
        return f"❌ Error: {str(e)}"
