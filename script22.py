from flask import Blueprint, render_template_string, request, jsonify
import requests

script22_bp = Blueprint('script22', __name__)

# --- CONFIGURATION ---
API_TOKEN = "1308711346:P09E32lL"
API_URL = "https://leakosintapi.com/"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>PHANTOM_OSINT_API_v22</title>
    <style>
        body { background: #050505; color: #00ff00; font-family: 'Consolas', monospace; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: auto; border: 1px solid #00ff00; padding: 20px; background: #000; box-shadow: 0 0 30px #00ff0033; }
        .header { text-align: center; border-bottom: 2px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; }
        input { width: 60%; padding: 12px; background: #111; border: 1px solid #00ff00; color: #fff; }
        select { padding: 12px; background: #111; border: 1px solid #00ff00; color: #fff; }
        button { padding: 12px 25px; background: #00ff00; color: #000; border: none; font-weight: bold; cursor: pointer; }
        button:hover { background: #fff; }
        
        .results-area { margin-top: 20px; border-top: 1px solid #333; padding-top: 20px; }
        .db-card { background: #0a0a0a; border-left: 4px solid #00ff00; padding: 15px; margin-bottom: 15px; }
        .db-title { color: #fff; font-size: 18px; font-weight: bold; margin-bottom: 5px; }
        .data-row { font-size: 13px; margin: 5px 0; color: #ccc; }
        .data-label { color: #00ff00; font-weight: bold; }
        .loading { color: #ffeb3b; text-align: center; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>â˜£ï¸ PHANTOM API OSINT v22 â˜£ï¸</h1>
            <p>ADVANCED DATABASE SEARCH INTERFACE</p>
        </div>

        <div style="text-align:center;">
            <input type="text" id="query" placeholder="Enter Email, Name, or Number...">
            <select id="limit">
                <option value="100">Limit: 100</option>
                <option value="300">Limit: 300</option>
                <option value="500">Limit: 500</option>
            </select>
            <button onclick="performSearch()">EXECUTE SEARCH</button>
        </div>

        <div id="loader" class="loading">SEARCHING DATABASE NODES... PLEASE WAIT...</div>

        <div class="results-area" id="results-box">
            </div>
    </div>

    <script>
        async function performSearch() {
            const query = document.getElementById('query').value;
            const limit = document.getElementById('limit').value;
            const resultsBox = document.getElementById('results-box');
            const loader = document.getElementById('loader');
            
            if(!query) return alert("Search query required!");
            
            loader.style.display = "block";
            resultsBox.innerHTML = "";

            try {
                const res = await fetch('/script22/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: query, limit: parseInt(limit) })
                });
                const data = await res.json();
                loader.style.display = "none";

                if(data.error) {
                    resultsBox.innerHTML = `<div style="color:red; text-align:center;">ERROR: ${data.error}</div>`;
                    return;
                }

                if(!data.List || Object.keys(data.List).length === 0) {
                    resultsBox.innerHTML = `<div style="text-align:center;">NO RESULTS FOUND IN DATABASE</div>`;
                    return;
                }

                for (let db in data.List) {
                    let card = document.createElement('div');
                    card.className = "db-card";
                    card.innerHTML = `<div class="db-title">${db}</div>`;
                    
                    if(data.List[db].Data) {
                        data.List[db].Data.forEach(entry => {
                            let entryDiv = document.createElement('div');
                            entryDiv.style.marginBottom = "10px";
                            for(let key in entry) {
                                entryDiv.innerHTML += `<div class="data-row"><span class="data-label">${key}:</span> ${entry[key]}</div>`;
                            }
                            card.appendChild(entryDiv);
                        });
                    }
                    resultsBox.appendChild(card);
                }
            } catch (err) {
                loader.style.display = "none";
                alert("Connection to API node failed.");
            }
        }
    </script>
</body>
</html>
"""

@script22_bp.route('/')
def index():
    return render_template_string(UI)

@script22_bp.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    limit = data.get('limit', 100)

    # API Request as per documentation
    payload = {
        "token": API_TOKEN,
        "request": query,
        "limit": limit,
        "lang": "en"
    }

    try:
        # Documentation specifies data must be sent in JSON format
        response = requests.post(API_URL, json=payload, timeout=30)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

