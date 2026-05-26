from flask import Blueprint, render_template_string, request, jsonify, send_file
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io
import logging

script28_bp = Blueprint('script28', __name__)

SCRAPER_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Ghost Scraper Fixed</title>
</head>
<body style="background:black;color:#00ffcc;font-family:Arial;padding:40px;text-align:center;">

<h1>Ghost Business Lead Scraper</h1>

<input type="text" id="query" placeholder="Hotels in Mumbai"
style="width:300px;padding:10px;">

<button onclick="runScraper()"
style="padding:10px 20px;background:#00ffcc;border:none;cursor:pointer;">
Start Scraping
</button>

<p id="status"></p>

<script>
async function runScraper() {

    let query = document.getElementById("query").value;

    if(!query){
        alert("Enter query");
        return;
    }

    document.getElementById("status").innerHTML = "Scraping started...";

    try{

        const response = await fetch('/script28/scrape', {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                query:query
            })
        });

        if(response.ok){

            document.getElementById("status").innerHTML = "Downloading Excel...";

            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = "business_leads.xlsx";
            a.click();

        } else {

            const err = await response.json();
            document.getElementById("status").innerHTML = err.message;

        }

    } catch(err){
        document.getElementById("status").innerHTML = "Server Error";
    }
}
</script>

</body>
</html>
"""

@script28_bp.route('/')
def home():
    return render_template_string(SCRAPER_UI)

@script28_bp.route('/scrape', methods=['POST'])
def scrape():

    try:

        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({
                "message": "Query missing"
            }), 400

        session = requests.Session()

        session.headers.update({
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        encoded_query = requests.utils.quote(query)

        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

        response = session.get(url, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        search_results = soup.find_all("div", class_="result")

        EMAIL_REGEX = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

        for item in search_results[:15]:

            try:

                title_tag = item.find("a", class_="result__a")

                if not title_tag:
                    continue

                business_name = title_tag.get_text(strip=True)

                website = title_tag.get("href", "")

                snippet_tag = item.find("a", class_="result__snippet")

                if not snippet_tag:
                    snippet_tag = item.find("div", class_="result__snippet")

                snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""

                phone = "N/A"

                phone_match = re.search(
                    r'(\+?\d[\d\s\-]{7,15}\d)',
                    snippet
                )

                if phone_match:
                    phone = phone_match.group(0)

                email = "N/A"

                instagram = ""
                facebook = ""

                if website.startswith("http"):

                    try:

                        web = session.get(
                            website,
                            timeout=5,
                            verify=False
                        )

                        html = web.text

                        emails = re.findall(EMAIL_REGEX, html)

                        if emails:
                            email = emails[0]

                        insta = re.findall(
                            r'https?://(?:www\.)?instagram\.com/[A-Za-z0-9_.]+',
                            html
                        )

                        if insta:
                            instagram = insta[0]

                        fb = re.findall(
                            r'https?://(?:www\.)?facebook\.com/[A-Za-z0-9_.]+',
                            html
                        )

                        if fb:
                            facebook = fb[0]

                    except Exception:
                        pass

                results.append({
                    "Business Name": business_name,
                    "Phone": phone,
                    "Website": website,
                    "Email": email,
                    "Instagram": instagram,
                    "Facebook": facebook,
                    "Description": snippet
                })

            except Exception as e:
                print(e)

        if not results:
            return jsonify({
                "message": "No data found"
            }), 404

        df = pd.DataFrame(results)

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="business_leads.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:

        logging.error(str(e))

        return jsonify({
            "message": str(e)
        }), 500


if __name__ == '__main__':

    from flask import Flask

    app = Flask(__name__)

    app.register_blueprint(script28_bp, url_prefix='/script28')

    app.run(debug=True, port=5000)
