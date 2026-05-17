from flask import Blueprint, render_template_string, request, jsonify
import mysql.connector
import json

script24_bp = Blueprint('script24', __name__)

UI = """
<!DOCTYPE html>
<html>
<head>
    <title>SECURE_DB_NODE_v24</title>
    <style>
        body { background: #050505; color: #00ff66; font-family: 'Share Tech Mono', monospace; padding: 20px; text-align: center; }
        .container { border: 2px solid #00ff66; background: #000; padding: 30px; box-shadow: 0 0 25px #00ff6633; display: inline-block; width: 90%; max-width: 700px; border-radius: 10px; text-align: left; }
        .header { text-align: center; border-bottom: 1px solid #00ff66; padding-bottom: 15px; margin-bottom: 20px; }
        h2 { margin-top: 0; color: #fff; text-shadow: 0 0 10px #00ff66; }
        .input-group { margin-bottom: 20px; text-align: center; }
        input { width: 70%; padding: 12px; background: #111; border: 1px solid #00ff66; color: #fff; font-size: 16px; border-radius: 5px; outline: none; text-align: center; }
        button { padding: 12px 30px; background: #00ff66; color: #000; border: none; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 15px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .status-node { color: #ffeb3b; text-align: center; margin: 15px 0; display: none; }
        .result-box { margin-top: 25px; background: #0a0a0a; border: 1px dashed #00ff66; padding: 15px; border-radius: 5px; display: none; max-height: 300px; overflow-y: auto; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; border-bottom: 1px solid #222; text-align: left; font-size: 14px; }
        th { color: #00ff66; border-bottom: 2px solid #00ff66; }
        td { color: #fff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>🛡️ SECURE DATABASE GATEWAY v24</h2>
            <p style="color: #666; margin: 0;">MEMBER OF SHIVAM SINGH OMEGA DASHBOARD</p>
        </div>

        <div class="input-group">
            <input type="text" id="username_input" placeholder="Enter Username to Search Safely">
            <br><br>
            <button onclick="queryDatabase()">EXECUTE PARAMETERIZED QUERY</button>
        </div>

        <div id="status" class="status-node">⚡ QUERIES BEING BOUND SEPARATELY FROM LOGIC...</div>
        <div id="result" class="result-box"></div>
    </div>

    <script>
        async function queryDatabase() {
            const inputVal = document.getElementById('username_input').value;
            const status = document.getElementById('status');
            const resultBox = document.getElementById('result');

            if(!inputVal) return alert("Bhai, kuch input toh daal!");

            status.style.display = "block";
            resultBox.style.display = "none";
            resultBox.innerHTML = "";

            try {
                const res = await fetch('/script24/vulnerable_endpoint', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ user_input: inputVal })
                });
                const data = await res.json();
                status.style.display = "none";

                if(data.status === "error") {
                    resultBox.innerHTML = '<p style="color:red; text-align:center;">❌ Error: ' + data.message + '</p>';
                } else if(data.results && data.results.length > 0) {
                    let tableHtml = '<table><thead><tr><th>USER DATA ROW</th></tr></thead><tbody>';
                    
                    for(let i = 0; i < data.results.length; i++) {
                        tableHtml += '<tr><td>' + JSON.stringify(data.results[i]) + '</td></tr>';
                    }
                    
                    tableHtml += '</tbody></table>';
                    resultBox.innerHTML = tableHtml;
                } else {
                    resultBox.innerHTML = '<p style="color:#ff0055; text-align:center;">No records found matching the exact string.</p>';
                }
                resultBox.style.display = "block";
            } catch (e) {
                status.innerText = "❌ Connection to local gateway failed!";
            }
        }
    </script>
</body>
</html>
"""

@script24_bp.route('/')
def index():
    return render_template_string(UI)

@script24_bp.route('/vulnerable_endpoint', methods=['POST'])
def vulnerable_endpoint():
    user_input = request.json.get('user_input')
    conn = None
    try:
        # Database connection mapping
        conn = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='test')
        cursor = conn.cursor()
        
        # Vulnerable query syntax
        query = "SELECT * FROM users WHERE username = '" + user_input + "'"
        cursor.execute(query)
        results = cursor.fetchall()
        
        return jsonify({"status": "success", "results": results})
        
    except mysql.connector.Error as err:
        # Insecure Error Handling: Database exception logs ko user UI par show karna
        return jsonify({"status": "error", "message": str(err)})
        
    finally:
        # Resource management optimization
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
