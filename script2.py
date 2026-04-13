import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape(url):
    if not url.startswith("http"):
        url = "http://" + url

    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"

        # 🔗 Links
        links = []
        for a in soup.find_all("a", href=True):
            full_link = urljoin(url, a['href'])
            links.append(full_link)

        # 🖼 Images
        images = []
        for img in soup.find_all("img", src=True):
            images.append(urljoin(url, img['src']))

        # 📝 Meta description
        desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            desc = meta.get("content", "")

        return f"""
        ✅ SCRAPE RESULT

        🌐 URL: {url}

        🏷 Title:
        {title}

        📄 Description:
        {desc}

        🔗 Total Links: {len(links)}
        {links[:20]}

        🖼 Total Images: {len(images)}
        {images[:10]}
        """

    except Exception as e:
        return f"❌ Error: {str(e)}"
