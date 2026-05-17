from flask import Blueprint, render_template_string, request, jsonify
import http.client
import json

script24_bp = Blueprint('script24', __name__)

# --- CONFIGURATION ---
WEBSHARE_API_KEY = "gtauzqw8k9bnapntgzzxvmfx4zuepz3syul8vhzm"
WEBSHARE_API_HOST = "proxy.webshare.io"

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>WEBSHARE_PROXY_v24</title>
    <style>
        body { background: #0a0a0a; color: #ffeb3b; font-family: 'Courier New', monospace; padding: 20px; text-align: center; }
        .box { border: 2px solid #ffeb3b; background: #000; padding: 25px; box-shadow: 0 0 20px #ffeb3b44; display: inline-block; width: 95%; max-width: 900px; border-radius: 15px; }
        h2 { text-shadow: 0 0 10px #ffeb3b; margin-bottom: 20px; }
        button { padding: 12px 30px; background: #ffeb3b; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 8px; font-size: 16px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        #status { margin: 15px 0; color: #00ffcc; display: none; font-weight: bold; }
        .table-container { margin-top: 25px; background: #050505; border: 1px solid #333; padding: 10px; border-radius: 8px; display: none; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 12px; border-bottom: 1px solid #222; font-size: 13px; }
        th { color: #ffeb3b; text-transform: uppercase; border-bottom: 2px solid #ffeb3b; }
        td { color: #fff; word-break: break-all; }
        .copy-btn { padding: 3px 8px; background: #333; color: #fff; border: 1px solid #555; cursor: pointer; border-radius: 3px; font-size: 11px; }
        .copy-btn:hover { background: #ffeb3b; color: #000; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🌐 WEBSHARE PROXY MANAGER v24</h2>
        <p style="color: #888;">Fetch active proxy list from your Webshare account</p>
        
        <button onclick="fetchProxies()" id="fetch_btn">LOAD ACTIVE PROXIES</button>
        <div id="status">📡 FETCHING DATA FROM WEBSHARE NETWORKS...</div>
        
        <div id="result_container" class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>IP Address</th>
                        <th>Port</th>
                        <th>Username</th>
                        <th>Password</th>
                        <th>Valid</th>
                        <th>Credentials</th>
                    </tr>
                </thead>
                <tbody id="proxy_table_body">
                    </tbody>
            </table>
        </div>
    </div>

    <script>
        async function fetchProxies() {
            const btn = document.getElementById('fetch_btn');
            const status = document.getElementById('status');
            const container = document.getElementById('result_container');
            const tbody = document.getElementById('proxy_table_body');

            btn.disabled = true;
            status.style.display = "block";
            container.style.display = "none";
            tbody.innerHTML = "";

            try {
                const res = await fetch('/script24/get_proxies', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'}
                });
                const data = await res.json();
                
                status.style.display = "none";
                btn.disabled = false;

                if(data.status === "error" || !data.results) {
                    alert("Error: " + (data.message || "Failed to fetch data"));
                } else {
                    let html = "";
                    let proxyList = data.results;

                    for (let i = 0; i < proxyList.length; i++) {
                        let proxy = proxyList[i];
                        let fullString = proxy.proxy_address + ":" + proxy.port + ":" + proxy.username + ":" + proxy.password;
                        
                        html += '<tr>' +
                            '<td>' + proxy.proxy_address + '</td>' +
                            '<td>' + proxy.port + '</td>' +
                            '<td>' + proxy.username + '</td>' +
                            '<td>' + proxy.password + '</td>' +
                            '<td style="color:' + (proxy.valid ? "#00ffcc" : "#ff0055") + '">' + proxy.valid + '</td>' +
                            '<td><button class="copy-btn" onclick="navigator.clipboard.writeText(\'' + fullString + '\'); alert(\'Copied!\');">Copy</button></td>' +
                        '</tr>';
                    }
                    
                    tbody.innerHTML = html || '<tr><td colspan="6" style="text-align:center;">No proxies found in this account.</td></tr>';
                    container.style.display = "block";
                }
            } catch (e) {
                status.innerText = "❌ Connection Failed!";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

@script24_bp.route('/')
def index():
    return render_template_string(UI)

@script24_bp.route('/get_proxies', methods=['POST'])
def get_proxies():
    try:
        conn = http.client.HTTPSConnection(WEBSHARE_API_HOST)
        
        # Webshare authentication header syntax rule: 'Authorization': 'Token <key>'
        headers = {
            'Authorization': "Token " + WEBSHARE_API_KEY
        }

        # Endpoint as per official Webshare API endpoints documentation
        conn.request("GET", "/api/v2/proxy/list/?page=1&page_size=100", "", headers)
        res = conn.getresponse()
        raw_data = res.read().decode("utf-8")
        
        return jsonify(json.loads(raw_data))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
