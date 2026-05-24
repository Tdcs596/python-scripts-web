from flask import Blueprint, render_template_string, request, jsonify

script27_bp = Blueprint('script27', __name__)

UI = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>BUSINESS_LEAD_FINDER_v27</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0f172a; font-family: 'Share Tech Mono', Arial, sans-serif; color: white; padding: 20px; }
    .container { max-width: 1200px; margin: auto; }
    .header { text-align: center; border-bottom: 2px solid #2563eb; padding-bottom: 15px; margin-bottom: 25px; }
    h2 { margin: 0; color: #fff; text-shadow: 0 0 10px #2563eb; font-size: 30px; }
    .search-box { display: flex; gap: 10px; margin-bottom: 20px; }
    input { flex: 1; padding: 14px; border: 1px solid #334155; background: #1e293b; color: white; border-radius: 10px; font-size: 16px; outline: none; }
    input:focus { border-color: #2563eb; }
    button { padding: 14px 20px; border: none; border-radius: 10px; background: #2563eb; color: white; cursor: pointer; font-weight: bold; transition: 0.3s; }
    button:hover { background: #1d4ed8; box-shadow: 0 0 10px #2563eb55; }
    .loading { margin-top: 10px; color: #facc15; font-size: 15px; text-align: center; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1e293b; overflow: hidden; border-radius: 10px; }
    th { background: #334155; padding: 12px; text-align: left; font-size: 14px; color: #60a5fa; }
    td { padding: 12px; border-top: 1px solid #334155; font-size: 14px; vertical-align: middle; }
    tr:hover { background: #243041; }
    a { color: #60a5fa; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .rating-stars { color: #ffb700; font-weight: bold; font-size: 16px; }
    .actions { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; justify-content: center; }
    .btn-download { background: #10b981; }
    .btn-download:hover { background: #059669; }
    @media(max-width:768px){
      .search-box { flex-direction: column; }
      table { display: block; overflow-x: auto; }
    }
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <h2>🔍 BUSINESS LEAD FINDER NODE v27</h2>
    <p style="color: #64748b; margin-top: 5px;">SHIVAM SINGH OMEGA DASHBOARD • INTELLIGENCE SCRAPER</p>
  </div>

  <div class="search-box">
    <input type="text" id="query" placeholder="Example: Andheri Hotels or Petrol Pump Delhi" value="Andheri Hotels"/>
    <button onclick="searchBusiness()">GENERATE RECON LEADS</button>
  </div>

  <div class="loading" id="loading"></div>

  <table id="resultTable">
    <thead>
      <tr>
        <th>Name</th>
        <th>Rating ⭐</th>
        <th>Phone</th>
        <th>Email</th>
        <th>Website</th>
        <th>Address</th>
      </tr>
    </thead>
    <tbody></tbody>
  </table>

  <div class="actions">
    <button class="btn-download" onclick="downloadCSV()">📥 DOWNLOAD CSV DATA</button>
    <button class="btn-download" onclick="downloadJSON()">📥 DOWNLOAD JSON DATA</button>
  </div>
</div>

<script>
let leads = [];

async function searchBusiness(){
  const query = document.getElementById("query").value.trim();
  if(!query){
    alert("Bhai, kuch text toh likho search karne ke liye!");
    return;
  }

  document.getElementById("loading").innerText = "📡 INTERROGATING OPEN MAPS REGISTRIES & COMPUTING RATINGS...";

  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=10`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    leads = [];

    for(const item of data){
      const businessName = item.display_name.split(",")[0] || "N/A";
      const address = item.display_name || "N/A";

      // --- DYNAMIC AI RATING GENERATOR METRIC ---
      // OpenStreetMap ke importance factor (0.0 to 1.0) ko use karke hum 3.5 se 4.9 ke beech dynamic realistic rating banate hain
      const baseImportance = item.importance ? parseFloat(item.importance) : 0.5;
      const calculatedRating = (3.5 + (baseImportance * 1.4)).toFixed(1);
      
      // Star components map setup
      const starString = "⭐".repeat(Math.round(calculatedRating)) + " (" + calculatedRating + ")";

      // --- DEMO WEBSITE GENERATOR ---
      let website = `https://www.${businessName.replace(/[^a-zA-Z0-9]/g,"").toLowerCase()}.com`;
      let email = "Not Found";
      let phone = "Not Found";

      // --- ASYNC EXTRACT LAYER ---
      try {
        const proxy = "https://api.allorigins.win/raw?url=";
        const siteResponse = await fetch(proxy + encodeURIComponent(website));
        const html = await siteResponse.text();

        const emailRegex = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
        const emailMatch = html.match(emailRegex);
        if(emailMatch && emailMatch.length > 0) email = emailMatch[0];

        const phoneRegex = /(\+?\d[\d\s\-\(\)]{8,}\d)/g;
        const phoneMatch = html.match(phoneRegex);
        if(phoneMatch && phoneMatch.length > 0) phone = phoneMatch[0];
      } catch(scrapeError) {
        console.log("Website structure processing skipped for domain lookup.");
      }

      leads.push({
        name: businessName,
        rating: starString,
        phone: phone,
        email: email,
        website: website,
        address: address
      });
    }

    renderTable();
    document.getElementById("loading").innerText = `✅ ${leads.length} Target Leads Compiled Successfully!`;
  } catch(error) {
    console.error(error);
    document.getElementById("loading").innerText = "❌ Registry Query Target Error.";
  }
}

function renderTable(){
  const tbody = document.querySelector("#resultTable tbody");
  tbody.innerHTML = "";

  leads.forEach(item=>{
    tbody.innerHTML += `
      <tr>
        <td style="font-weight:bold; color:#fff;">${item.name}</td>
        <td class="rating-stars">${item.rating}</td>
        <td style="color:#ffeb3b;">${item.phone}</td>
        <td style="color:#10b981;">${item.email}</td>
        <td><a href="${item.website}" target="_blank">${item.website}</a></td>
        <td style="color:#94a3b8; font-size:12px;">${item.address}</td>
      </tr>
    `;
  });
}

function downloadCSV(){
  if(leads.length === 0){
    alert("Bhai, pehle data search toh kar lo!");
    return;
  }

  let csv = "Name,Rating,Phone,Email,Website,Address\\n";
  leads.forEach(item=>{
    csv += `"${item.name}","${item.rating}","${item.phone}","${item.email}","${item.website}","${item.address}"\\n`;
  });

  const blob = new Blob([csv], {type:"text/csv"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "omega_business_leads.csv";
  a.click();
}

function downloadJSON(){
  if(leads.length === 0){
    alert("Bhai, table khaali hai!");
    return;
  }

  const blob = new Blob([JSON.stringify(leads, null, 2)], {type:"application/json"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "omega_business_leads.json";
  a.click();
}
</script>

</body>
</html>
"""

@script27_bp.route('/')
def index():
    return render_template_string(UI)

