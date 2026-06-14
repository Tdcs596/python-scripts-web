from flask import Blueprint, render_template_string, request, jsonify
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import base64

script24_bp = Blueprint('script24', __name__)

ADVANCED_FORENSIC_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>FORTIFIEDBYTES | Elite Image Forensics Core</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-color: #030712;
        --panel-bg: rgba(17, 24, 39, 0.7);
        --neon-cyan: #06b6d4;
        --neon-amber: #f59e0b;
        --neon-rose: #f43f5e;
        --neon-emerald: #10b981;
        --border-color: rgba(6, 182, 212, 0.15);
        --text-main: #f3f4f6;
        --text-muted: #64748b;
    }

    body { 
        background: var(--bg-color); 
        color: var(--text-main); 
        font-family: 'Consolas', 'Courier New', monospace; 
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px;
        overflow-x: hidden;
    }

    .matrix-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(6, 182, 212, 0.02) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(6, 182, 212, 0.02) 1px, transparent 1px);
        background-size: 25px 25px;
        z-index: 1;
        pointer-events: none;
    }

    .workspace {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: row;
        width: 100%;
        max-width: 1400px;
        height: 90vh;
        min-height: 700px;
        border: 1px solid var(--border-color);
        background: var(--panel-bg);
        backdrop-filter: blur(25px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    /* --- LEFT SIDE: CONFIG DECK --- */
    .control-deck {
        width: 40%;
        min-width: 380px;
        background: rgba(3, 7, 18, 0.95);
        border-right: 1px solid var(--border-color);
        padding: 25px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow-y: auto;
    }

    .deck-header {
        border-bottom: 1px dashed var(--border-color);
        padding-bottom: 15px;
        margin-bottom: 15px;
    }

    .deck-title {
        font-size: 18px;
        font-weight: bold;
        letter-spacing: 2px;
        color: #fff;
    }
    .deck-title span { color: var(--neon-cyan); text-shadow: 0 0 10px rgba(6, 182, 212, 0.5); }

    label { 
        font-size: 10px; 
        color: var(--neon-cyan); 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        display: block; 
        margin-top: 15px; 
        margin-bottom: 5px; 
        font-weight: bold; 
    }

    .forensic-input { 
        width: 100%; 
        padding: 10px; 
        background: #010204; 
        border: 1px solid rgba(6, 182, 212, 0.25); 
        color: #fff; 
        font-family: inherit; 
        border-radius: 6px; 
        outline: none; 
        font-size: 12px;
    }
    .forensic-input:focus { border-color: var(--neon-cyan); box-shadow: 0 0 10px rgba(6, 182, 212, 0.2); }

    .editor-section-title {
        font-size: 11px;
        color: var(--neon-amber);
        margin-top: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding-bottom: 3px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* --- TIMELINE ACTION MATRIX BUTTONS --- */
    .btn { 
        width: 100%; 
        padding: 12px; 
        font-weight: bold; 
        border: none; 
        font-family: inherit; 
        cursor: pointer; 
        border-radius: 6px; 
        margin-top: 12px; 
        transition: all 0.2s ease; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        font-size: 12px;
    }
    .btn-compile { background: var(--neon-cyan); color: #000; }
    .btn-compile:hover { background: #fff; box-shadow: 0 0 15px rgba(255,255,255,0.4); }

    .btn-erase { background: rgba(244, 63, 94, 0.1); color: var(--neon-rose); border: 1px solid var(--neon-rose); }
    .btn-erase:hover { background: var(--neon-rose); color: #000; box-shadow: 0 0 15px rgba(244, 63, 94, 0.4); }

    /* --- RIGHT SIDE: TERMINAL VIEWER --- */
    .terminal-viewport {
        flex: 1;
        background: rgba(2, 4, 8, 0.98);
        padding: 25px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    }

    #terminal-output { 
        white-space: pre-wrap; 
        font-size: 12px; 
        line-height: 1.7; 
        color: #cbd5e1; 
    }

    .download-container {
        margin-top: 15px;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        animation: fadeIn 0.3s ease;
    }
    .dl-wrap-mod { background: rgba(245, 158, 11, 0.03); border: 1px dashed var(--neon-amber); }
    .dl-wrap-wipe { background: rgba(16, 185, 129, 0.03); border: 1px dashed var(--neon-emerald); }

    .dl-link {
        display: inline-block;
        padding: 10px 20px;
        text-decoration: none;
        font-weight: bold;
        border-radius: 6px;
        transition: 0.2s;
        text-transform: uppercase;
        font-size: 11px;
    }
    .dl-mod { background: var(--neon-amber); color: #000; }
    .dl-mod:hover { box-shadow: 0 0 15px var(--neon-amber); background: #fff; }
    .dl-wipe { background: var(--neon-emerald); color: #000; }
    .dl-wipe:hover { box-shadow: 0 0 15px var(--neon-emerald); background: #fff; }

    .location-btn {
        display: inline-block;
        margin-top: 8px;
        padding: 6px 12px;
        background: #3b82f6;
        color: white;
        text-decoration: none;
        font-size: 11px;
        border-radius: 4px;
        font-weight: bold;
    }
    .location-btn:hover { background: #fff; color: #000; }

    .brand-tag { 
        font-size: 9px; 
        color: var(--text-muted); 
        text-align: center; 
        letter-spacing: 3px; 
        text-transform: uppercase; 
        border-top: 1px dashed rgba(6, 182, 212, 0.1); 
        padding-top: 15px; 
        margin-top: 15px;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    @media (max-width: 950px) {
        .workspace { flex-direction: column; height: auto; }
        .control-deck { width: 100%; min-width: 100%; border-right: none; border-bottom: 1px solid var(--border-color); }
        .terminal-viewport { min-height: 450px; }
    }
  </style>
</head>
<body>

    <div class="matrix-bg"></div>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-header">
                    <div class="deck-title">🛰️ FORTIFIEDBYTES <span>OSINT-FORENSICS</span></div>
                </div>

                <label for="image_file">Target Image Stream (JPEG Recommended)</label>
                <input type="file" id="image_file" class="forensic-input" accept="image/*" onchange="extractQuantumMetadata()">

                <div class="editor-section-title">⚙️ Device & Software Layer</div>
                <label for="edit_make">Camera Brand (Make)</label>
                <input type="text" id="edit_make" class="forensic-input" placeholder="e.g., Apple / Samsung">

                <label for="edit_model">Device Structure Model</label>
                <input type="text" id="edit_model" class="forensic-input" placeholder="e.g., iPhone 15 Pro Max">

                <label for="edit_software">Processing Software</label>
                <input type="text" id="edit_software" class="forensic-input" placeholder="e.g., iOS 17.4">

                <label for="edit_datetime">Capture Timestamp</label>
                <input type="text" id="edit_datetime" class="forensic-input" placeholder="YYYY:MM:DD HH:MM:SS">

                <div class="editor-section-title">📍 GPS Satellite Geolocation</div>
                <label for="edit_lat">Latitude Decimal Coordinate</label>
                <input type="text" id="edit_lat" class="forensic-input" placeholder="e.g., 19.2812">

                <label for="edit_lon">Longitude Decimal Coordinate</label>
                <input type="text" id="edit_lon" class="forensic-input" placeholder="e.g., 72.8554">

                <button class="btn btn-compile" onclick="compileExifModification()">⚡ Modify & Rebuild Asset</button>
                <button class="btn btn-erase" onclick="wipeAllExifMetadata()">🚨 Wipe All Data & Download Clean Image</button>
            </div>
            <div class="brand-tag">SHIVAM SINGH OMEGA FORENSIC HUB</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output"><span style="color:var(--neon-cyan);">[TELEMETRY CORE ACTIVE]</span> Core modules awaiting image bitstream layout...<br>Upload an asset file to extract A to Z parameters, hardware specs, and satellite paths.</div>
        </div>
    </div>

    <script>
        // --- EXTRACTION ROUTINE (A TO Z DETAILS + GPS) ---
        async function extractQuantumMetadata() {
            const fileInput = document.getElementById('image_file');
            const term = document.getElementById('terminal-output');
            
            if (fileInput.files.length === 0) return;
            
            const file = fileInput.files[0];
            const reader = new FileReader();
            
            term.innerHTML = `<span style="color:var(--neon-cyan);">[SYSTEM COUPLING]</span> Parsing file bytes for forensic patterns: ${file.name}...\n`;
            
            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                
                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(`${currentPath}/extract_all`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: base64Image })
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        term.innerHTML += `\n<span style="color:var(--neon-rose);">[FAULT]</span> ${data.error}`;
                        return;
                    }
                    
                    // Core UI field updates
                    document.getElementById('edit_make').value = data.basic_data.Make || '';
                    document.getElementById('edit_model').value = data.basic_data.Model || '';
                    document.getElementById('edit_software').value = data.basic_data.Software || '';
                    document.getElementById('edit_datetime').value = data.basic_data.DateTime || '';
                    document.getElementById('edit_lat').value = data.gps_data.latitude || '';
                    document.getElementById('edit_lon').value = data.gps_data.longitude || '';
                    
                    // Comprehensive forensic log reporting printout
                    let report = `\n🧬 <span style="color:var(--neon-emerald);">[PARSING COMPLETED] TOTAL IMAGE DATA REPORT MATRIX</span>\n`;
                    report += `=============================================================\n`;
                    report += `📁 Structural Name : ${file.name}\n`;
                    report += `📐 Grid Resolution  : ${data.dimensions[0]} x ${data.dimensions[1]} Pixels\n`;
                    report += `🎨 Memory Channel  : ${data.format_mode}\n`;
                    report += `📦 Allocation Size : ${(file.size / 1024).toFixed(2)} KB\n`;
                    report += `=============================================================\n`;
                    report += `📡 EXTRACTED HARDWARE & IMAGE PARAMETERS:\n`;
                    
                    if (Object.keys(data.all_exif).length === 0) {
                        report += `  <span style="color:var(--neon-amber);">No EXIF attributes embedded within image standard headers.</span>\n`;
                    } else {
                        for (const [key, val] of Object.entries(data.all_exif)) {
                            report += `  🔹 ${key.padEnd(22)} : ${val}\n`;
                        }
                    }
                    
                    report += `=============================================================\n`;
                    report += `🛰️ SATELLITE GPS METRICS:\n`;
                    if (data.gps_data.has_gps) {
                        report += `  🎯 Latitude (Raw)  : ${data.gps_data.latitude}\n`;
                        report += `  🎯 Longitude (Raw) : ${data.gps_data.longitude}\n`;
                        report += `  🗺️ Geolocation     : Coordinates Found. Open tracing vector path down below:\n\n`;
                        report += `  <a href="https://www.google.com/maps/search/?api=1&query=${data.gps_data.latitude},${data.gps_data.longitude}" target="_blank" class="location-btn">🗺️ Open Map Vector Coordinates</a>\n`;
                    } else {
                        report += `  <span style="color:var(--text-muted);">No GPS coordinates mapped into asset structures.</span>\n`;
                    }
                    report += `=============================================================\n`;
                    
                    term.innerHTML = report;
                    
                } catch(err) {
                    term.innerHTML += `\n<span style="color:var(--neon-rose);">[CRITICAL FAULT]</span> Telemetry ingestion broken.`;
                }
            };
            reader.readAsDataURL(file);
        }

        // --- OPTION 1: REWRITE / MODIFY METADATA ---
        async function compileExifModification() {
            const fileInput = document.getElementById('image_file');
            const term = document.getElementById('terminal-output');
            
            if (fileInput.files.length === 0) { alert("Bhai, pehle image select karo!"); return; }
            
            const payload = {
                Make: document.getElementById('edit_make').value.trim(),
                Model: document.getElementById('edit_model').value.trim(),
                Software: document.getElementById('edit_software').value.trim(),
                DateTime: document.getElementById('edit_datetime').value.trim(),
                lat: document.getElementById('edit_lat').value.trim(),
                lon: document.getElementById('edit_lon').value.trim()
            };
            
            const reader = new FileReader();
            term.innerHTML += `\n\n<span style="color:var(--neon-amber);">[MODIFICATION ENGINE]</span> Syncing array blocks and overwriting metadata structures...`;
            
            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(`${currentPath}/modify_exif_advanced`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: base64Image, modifications: payload })
                    });
                    const data = await response.json();
                    
                    cleanDownloadWrappers();
                    
                    const div = document.createElement('div');
                    div.className = 'download-container dl-wrap-mod';
                    div.innerHTML = `<p style="color:var(--neon-amber); font-size:11px; margin-bottom:8px;">MODIFIED METADATA STRUCTURE RECORDED</p>
                                     <a href="data:image/jpeg;base64,${data.result_image}" download="modified_forensic_output.jpg" class="dl-link dl-mod">📥 Download Modified Asset</a>`;
                    term.appendChild(div);
                    term.innerHTML += `\n\n✅ <span style="color:var(--neon-emerald);">Asset headers patched successfully. Download ready below.</span>`;
                    
                    const vp = document.querySelector('.terminal-viewport');
                    vp.scrollTop = vp.scrollHeight;
                } catch(err) {
                    term.innerHTML += `\n[ERROR] Injection failed.`;
                }
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        // --- OPTION 2: CLEAR ALL METADATA (ANTI-FORENSICS WIPE) ---
        async function wipeAllExifMetadata() {
            const fileInput = document.getElementById('image_file');
            const term = document.getElementById('terminal-output');
            
            if (fileInput.files.length === 0) { alert("Bhai, wipe out karne ke liye ek image select karo!"); return; }
            
            const reader = new FileReader();
            term.innerHTML += `\n\n<span style="color:var(--neon-rose);">[ANTI-FORENSICS]</span> Executing zero-fill wipe cycle... Stripping ALL headers, GPS logs, and signatures...`;
            
            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(`${currentPath}/wipe_all`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: base64Image })
                    });
                    const data = await response.json();
                    
                    cleanDownloadWrappers();
                    
                    const div = document.createElement('div');
                    div.className = 'download-container dl-wrap-wipe';
                    div.innerHTML = `<p style="color:var(--neon-emerald); font-size:11px; margin-bottom:8px;">💥 ALL METADATA TRACES TOTALLY PURGED - ANONYMOUS ASSET READY</p>
                                     <a href="data:image/jpeg;base64,${data.result_image}" download="wiped_anonymous_image.jpg" class="dl-link dl-wipe">📥 Download Anonymous Image</a>`;
                    term.appendChild(div);
                    term.innerHTML += `\n\n💥 <span style="color:var(--neon-emerald);">Anti-Forensic wipe sequence complete. Location data, system logs, and tracking headers have been 100% neutralized.</span>`;
                    
                    // Reset input view controls to represent clean state
                    document.getElementById('edit_make').value = '';
                    document.getElementById('edit_model').value = '';
                    document.getElementById('edit_software').value = '';
                    document.getElementById('edit_datetime').value = '';
                    document.getElementById('edit_lat').value = '';
                    document.getElementById('edit_lon').value = '';
                    
                    const vp = document.querySelector('.terminal-viewport');
                    vp.scrollTop = vp.scrollHeight;
                } catch(err) {
                    term.innerHTML += `\n[ERROR] Wipe operation aborted.`;
                }
            };
            reader.readAsDataURL(fileInput.files[0]);
        }

        function cleanDownloadWrappers() {
            const items = document.querySelectorAll('.download-container');
            items.forEach(el => el.remove());
        }
    </script>
</body>
</html>
"""

@script24_bp.route('/')
def index():
    return render_template_string(ADVANCED_FORENSIC_UI)

@script24_bp.route('/extract_all', methods=['POST'])
def extract_all_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    if not image_b64:
        return jsonify({"error": "Empty tracking stream data context."}), 400
        
    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))
        
        all_exif = {}
        basic_data = {}
        gps_data = {"has_gps": False}
        
        raw_exif = image._getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # GPS Information Extract Matrix Logic
                if tag_name == "GPSInfo":
                    gps_info = {}
                    for gps_tag in value:
                        gps_sub_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_info[gps_sub_name] = value[gps_tag]
                    
                    # Convert EXIF Rational formats to standard coordinate mappings
                    if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                        try:
                            lat_data = gps_info["GPSLatitude"]
                            lon_data = gps_info["GPSLongitude"]
                            lat_ref = gps_info.get("GPSLatitudeRef", "N")
                            lon_ref = gps_info.get("GPSLongitudeRef", "E")
                            
                            lat = float(lat_data[0]) + float(lat_data[1])/60.0 + float(lat_data[2])/3600.0
                            lon = float(lon_data[0]) + float(lon_data[1])/60.0 + float(lon_data[2])/3600.0
                            
                            if lat_ref == "S": lat = -lat
                            if lon_ref == "W": lon = -lon
                            
                            gps_data["latitude"] = round(lat, 5)
                            gps_data["longitude"] = round(lon, 5)
                            gps_data["has_gps"] = True
                        except:
                            pass
                
                # String value casting for normal arrays
                if tag_name != "GPSInfo":
                    if isinstance(value, (str, int, float)):
                        all_exif[tag_name] = str(value)
                    elif isinstance(value, bytes):
                        all_exif[tag_name] = value.decode('utf-8', errors='ignore')
            
            # Populate essential key hooks
            basic_data["Make"] = all_exif.get("Make", "")
            basic_data["Model"] = all_exif.get("Model", "")
            basic_data["Software"] = all_exif.get("Software", "")
            basic_data["DateTime"] = all_exif.get("DateTime", "") or all_exif.get("DateTimeOriginal", "")

        return jsonify({
            "dimensions": image.size,
            "format_mode": image.mode,
            "all_exif": all_exif,
            "basic_data": basic_data,
            "gps_data": gps_data
        }), 200
    except Exception as e:
        return jsonify({"error": f"Extraction matrix analysis drop error: {str(e)}"}), 200

@script24_bp.route('/modify_exif_advanced', methods=['POST'])
def modify_exif_advanced_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    mods = data.get('modifications', {})
    
    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        new_exif = image.getexif()
        
        # Mapping base configuration structural tags
        # 271=Make, 272=Model, 305=Software, 306=DateTime
        exif_map = {"Make": 271, "Model": 272, "Software": 305, "DateTime": 306}
        for key, val in mods.items():
            if key in exif_map and val:
                new_exif[exif_map[key]] = str(val)
                
        # Patching / Modifying GPS Coordinate Data Array Maps if input exists
        if mods.get('lat') and mods.get('lon'):
            try:
                lat_deg = float(mods['lat'])
                lon_deg = float(mods['lon'])
                
                # Build raw tuple constraints matching EXIF standards format blocks
                def convert_to_exif_rational(val):
                    abs_val = abs(val)
                    d = int(abs_val)
                    m = int((abs_val - d) * 60)
                    s = round((abs_val - d - m/60) * 3600, 3)
                    return ((d, 1), (m, 1), (int(s*1000), 1000))
                
                gps_dict = {
                    1: "N" if lat_deg >= 0 else "S",
                    2: convert_to_exif_rational(lat_deg),
                    3: "E" if lon_deg >= 0 else "W",
                    4: convert_to_exif_rational(lon_deg)
                }
                # 34853 is the universal standard hex lookup token identifier for GPS tags array blocks
                new_exif[34853] = gps_dict
            except:
                pass

        output = io.BytesIO()
        image.save(output, format="JPEG", exif=new_exif)
        compiled_result = base64.b64encode(output.getvalue()).decode('utf-8')
        return jsonify({"result_image": compiled_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@script24_bp.route('/wipe_all', methods=['POST'])
def wipe_all_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    
    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))
        
        # Pure Image Core Extraction - Discards any background header binary buffers
        clean_img = Image.new(image.mode, image.size)
        clean_img.putdata(image.getdata())
        
        output = io.BytesIO()
        clean_img.save(output, format="JPEG") # Saving directly without parsing the exif mapping parameters
        compiled_result = base64.b64encode(output.getvalue()).decode('utf-8')
        
        return jsonify({"result_image": compiled_result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 200
