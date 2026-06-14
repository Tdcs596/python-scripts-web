from flask import Blueprint, render_template_string, request, jsonify
from PIL import Image
from PIL.ExifTags import TAGS
import io
import base64

script24_bp = Blueprint('script24', __name__)

FORENSIC_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>FORTIFIEDBYTES | Image Forensics Node</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-color: #020617;
        --panel-bg: rgba(15, 23, 42, 0.8);
        --neon-cyan: #06b6d4;
        --neon-amber: #f59e0b;
        --border-color: rgba(6, 182, 212, 0.2);
        --text-main: #f8fafc;
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
        padding: 20px;
        overflow-x: hidden;
    }

    /* --- BACKGROUND DECORATION --- */
    .grid-bg {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        z-index: 1;
        pointer-events: none;
    }

    /* --- MAIN WORKSPACE --- */
    .workspace {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: row;
        width: 100%;
        max-width: 1300px;
        height: 85vh;
        min-height: 650px;
        border: 1px solid var(--border-color);
        background: var(--panel-bg);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 30px rgba(6, 182, 212, 0.05);
    }

    /* --- LEFT SECTION: UPLOAD & INPUTS --- */
    .control-deck {
        width: 45%;
        min-width: 400px;
        background: rgba(8, 13, 28, 0.95);
        border-right: 1px solid var(--border-color);
        padding: 30px;
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
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 1.5px;
        color: #fff;
    }
    .deck-title span { color: var(--neon-cyan); text-shadow: 0 0 10px rgba(6, 182, 212, 0.4); }

    label { 
        font-size: 11px; 
        color: var(--neon-cyan); 
        text-transform: uppercase; 
        letter-spacing: 1px; 
        display: block; 
        margin-top: 20px; 
        margin-bottom: 8px; 
        font-weight: bold; 
    }

    .forensic-input { 
        width: 100%; 
        padding: 12px; 
        background: #02040a; 
        border: 1px solid rgba(6, 182, 212, 0.3); 
        color: #fff; 
        font-family: inherit; 
        border-radius: 8px; 
        outline: none; 
        font-size: 13px;
        transition: all 0.2s;
    }
    .forensic-input:focus { border-color: var(--neon-cyan); }

    .metadata-editor-box {
        margin-top: 15px;
        background: rgba(255, 255, 255, 0.02);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* --- RIGHT SECTION: FORENSIC MATRIX LOGS --- */
    .terminal-viewport {
        flex: 1;
        background: rgba(2, 6, 12, 0.95);
        padding: 30px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
    }

    #terminal-output { 
        white-space: pre-wrap; 
        font-size: 13px; 
        line-height: 1.8; 
        color: #e2e8f0; 
    }

    .btn-execute { 
        width: 100%; 
        padding: 15px; 
        font-weight: bold; 
        background: var(--neon-cyan); 
        color: #000; 
        border: none; 
        font-family: inherit; 
        cursor: pointer; 
        border-radius: 8px; 
        margin-top: 20px; 
        transition: all 0.25s ease; 
        text-transform: uppercase; 
        letter-spacing: 1.5px; 
    }
    .btn-execute:hover { background: #fff; box-shadow: 0 0 20px #fff; }

    .download-wrapper {
        margin-top: 20px;
        padding: 15px;
        background: rgba(245, 158, 11, 0.05);
        border: 1px dashed var(--neon-amber);
        border-radius: 10px;
        text-align: center;
    }

    .download-link {
        display: inline-block;
        padding: 10px 20px;
        background: var(--neon-amber);
        color: #000;
        text-decoration: none;
        font-weight: bold;
        border-radius: 6px;
        transition: 0.2s;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 1px;
    }
    .download-link:hover { box-shadow: 0 0 15px var(--neon-amber); background: #fff; }

    .brand-tag { 
        font-size: 10px; 
        color: var(--text-muted); 
        text-align: center; 
        letter-spacing: 3px; 
        text-transform: uppercase; 
        border-top: 1px dashed rgba(6, 182, 212, 0.2); 
        padding-top: 15px; 
        margin-top: 20px;
    }

    @media (max-width: 900px) {
        .workspace { flex-direction: column; height: auto; }
        .control-deck { width: 100%; min-width: 100%; border-right: none; border-bottom: 1px solid var(--border-color); }
        .terminal-viewport { min-height: 400px; }
    }
  </style>
</head>
<body>

    <div class="grid-bg"></div>

    <div class="workspace">
        <div class="control-deck">
            <div>
                <div class="deck-header">
                    <div class="deck-title">🛰️ FORTIFIEDBYTES <span>IMAGE-FORENSICS</span></div>
                </div>

                <label for="image_file">Upload Image For Metadata Analysis</label>
                <input type="file" id="image_file" class="forensic-input" accept="image/*" onchange="analyzeImageMetadata()" required>

                <div class="metadata-editor-box">
                  <h4 style="font-size:12px; color:var(--neon-cyan); letter-spacing:1px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:5px;">✍️ EXIF METADATA INJECTOR / EDITOR</h4>
                  
                  <label for="edit_make">Camera Manufacturer (Make)</label>
                  <input type="text" id="edit_make" class="forensic-input" placeholder="e.g., Apple / Canon">

                  <label for="edit_model">Device Model</label>
                  <input type="text" id="edit_model" class="forensic-input" placeholder="e.g., iPhone 15 Pro">

                  <label for="edit_software">Software / Firmware Layer</label>
                  <input type="text" id="edit_software" class="forensic-input" placeholder="e.g., Adobe Photoshop 2026">

                  <label for="edit_datetime">Creation Timestamp (YYYY:MM:DD HH:MM:SS)</label>
                  <input type="text" id="edit_datetime" class="forensic-input" placeholder="e.g., 2026:06:14 12:30:00">
                </div>

                <button class="btn-execute" onclick="injectMetadataVector()">⚡ Rewrite EXIF & Compile Asset</button>
            </div>
            <div class="brand-tag">EXIF DATA FRAUD DETECTION MATRIX</div>
        </div>

        <div class="terminal-viewport">
            <div id="terminal-output"><span style="color:var(--neon-cyan);">[METADATA MONITOR]</span> Awaiting target graphic stream asset...<br>Upload an image to extract forensic signatures, GPS tags, and core properties.</div>
        </div>
    </div>

    <script>
        // --- STEP 1: READ & EXTRACT METADATA ---
        async function analyzeImageMetadata() {
            const fileInput = document.getElementById('image_file');
            const term = document.getElementById('terminal-output');
            
            if (fileInput.files.length === 0) return;
            
            const file = fileInput.files[0];
            const reader = new FileReader();
            
            term.innerHTML = `<span style="color:var(--neon-cyan);">[INSPECTING SYSTEM]</span> Reading file byte sequences for: ${file.name}...\n`;
            
            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                
                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(`${currentPath}/extract_exif`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: base64Image })
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        term.innerHTML += `\n<span style="color:#f43f5e;">[ERROR]</span> ${data.error}`;
                        return;
                    }
                    
                    // Populate inputs with current fields for smooth modifications
                    document.getElementById('edit_make').value = data.extracted_exif.Make || '';
                    document.getElementById('edit_model').value = data.extracted_exif.Model || '';
                    document.getElementById('edit_software').value = data.extracted_exif.Software || '';
                    document.getElementById('edit_datetime').value = data.extracted_exif.DateTime || '';
                    
                    // Build highly descriptive Forensic Log Table
                    let logHtml = `\n🌟 <span style="color:#10b981;">[ANALYSIS SUCCESS] TARGET METADATA STREAM VERIFIED</span>\n`;
                    logHtml += `-------------------------------------------------------------\n`;
                    logHtml += `📐 Dimensions  : ${data.dimensions[0]}x${data.dimensions[1]} Pixels\n`;
                    logHtml += `🎨 Color Mode : ${data.format_mode}\n`;
                    logHtml += `📁 File Size  : ${(file.size / 1024).toFixed(2)} KB\n`;
                    logHtml += `-------------------------------------------------------------\n`;
                    logHtml += `⚙️ RAW EXIF PROPERTIES FOUND:\n`;
                    
                    if (Object.keys(data.extracted_exif).length === 0) {
                        logHtml += `<span style="color:#eab308;">⚠️ No pre-existing EXIF header bits found in this image. Ready for raw initialization.</span>\n`;
                    } else {
                        for (const [key, value] of Object.entries(data.extracted_exif)) {
                            logHtml += `🔹 ${key.padEnd(15)} : ${value}\n`;
                        }
                    }
                    logHtml += `-------------------------------------------------------------\n`;
                    term.innerHTML = logHtml;
                    
                } catch(err) {
                    term.innerHTML += `\n<span style="color:#f43f5e;">[CRITICAL ERROR]</span> Connection to telemetry engine dropped.`;
                }
            };
            reader.readAsDataURL(file);
        }

        // --- STEP 2: WRITE / INJECT CUSTOM METADATA ---
        async function injectMetadataVector() {
            const fileInput = document.getElementById('image_file');
            const term = document.getElementById('terminal-output');
            
            if (fileInput.files.length === 0) {
                alert("Bhai, pehle forensic trace ke liye image select karo!");
                return;
            }
            
            const payloadData = {
                Make: document.getElementById('edit_make').value.trim(),
                Model: document.getElementById('edit_model').value.trim(),
                Software: document.getElementById('edit_software').value.trim(),
                DateTime: document.getElementById('edit_datetime').value.trim()
            };
            
            const file = fileInput.files[0];
            const reader = new FileReader();
            
            term.innerHTML += `\n\n<span style="color:var(--neon-amber);">[COMPILE]</span> Executing image array manipulation & injecting custom header blocks...`;
            
            reader.onload = async function(e) {
                const base64Image = e.target.result.split(',')[1];
                
                try {
                    const currentPath = window.location.pathname.replace(/\/$/, "");
                    const response = await fetch(`${currentPath}/modify_exif`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ image: base64Image, modifications: payloadData })
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        term.innerHTML += `\n<span style="color:#f43f5e;">[MOD_ERR]</span> ${data.error}\n`;
                        return;
                    }
                    
                    term.innerHTML += `\n\n🎯 <span style="color:#10b981;">[SUCCESS] EXIF Headers Overwritten Flawlessly!</span>\n`;
                    term.innerHTML += `The modified forensic layer asset is compiled. Use the module anchor link to download:\n`;
                    
                    // Rebuild Download Card
                    const oldWrapper = document.querySelector('.download-wrapper');
                    if (oldWrapper) oldWrapper.remove();
                    
                    const wrap = document.createElement('div');
                    wrap.className = 'download-wrapper';
                    wrap.innerHTML = `<p style="color:#fde047; margin-bottom:10px; font-size:11px;">METADATA FRAUD SHIELD MODULATION COMPLETED</p>`;
                    
                    const dl = document.createElement('a');
                    dl.href = "data:image/jpeg;base64," + data.result_image;
                    dl.download = "fortified_forensic_output.jpg";
                    dl.className = "download-link";
                    dl.innerText = "📥 Download Modified Image";
                    
                    wrap.appendChild(dl);
                    term.appendChild(wrap);
                    
                    const vp = document.querySelector('.terminal-viewport');
                    vp.scrollTop = vp.scrollHeight;
                    
                } catch(err) {
                    term.innerHTML += `\n<span style="color:#f43f5e;">[CRITICAL FAULT]</span> Re-compilation script linkage broken.`;
                }
            };
            reader.readAsDataURL(file);
        }
    </script>
</body>
</html>
"""

@script24_bp.route('/')
def index():
    return render_template_string(FORENSIC_UI)

@script24_bp.route('/extract_exif', methods=['POST'])
def extract_exif_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    
    if not image_b64:
        return jsonify({"error": "Null graphics stream vector data received."}), 400
        
    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))
        
        exif_data = {}
        raw_exif = image._getexif()
        
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                # Filter values so they don't break JSON serializer arrays
                if isinstance(value, (str, int, float)):
                    exif_data[tag_name] = str(value)
                elif isinstance(value, bytes):
                    exif_data[tag_name] = value.decode('utf-8', errors='ignore')
                    
        return jsonify({
            "dimensions": image.size,
            "format_mode": image.mode,
            "extracted_exif": exif_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed compiling structural signatures: {str(e)}"}), 200

@script24_bp.route('/modify_exif', methods=['POST'])
def modify_exif_endpoint():
    data = request.json or {}
    image_b64 = data.get('image', '')
    modifications = data.get('modifications', {})
    
    if not image_b64:
        return jsonify({"error": "Empty target source binary."}), 400
        
    try:
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Ingesting clean runtime Pillow EXIF context mapping blocks
        new_exif = image.getexif()
        
        # Mapping properties to their correct EXIF standard hex key mappings
        # 271 = Make, 272 = Model, 305 = Software, 306 = DateTime
        exif_map = {"Make": 271, "Model": 272, "Software": 305, "DateTime": 306}
        
        for key, val in modifications.items():
            if key in exif_map and val:
                new_exif[exif_map[key]] = str(val)
                
        # Compiling stream back into memory buffer array
        output_buffer = io.BytesIO()
        image.save(output_buffer, format="JPEG", exif=new_exif)
        compiled_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        
        return jsonify({"result_image": compiled_base64}), 200
        
    except Exception as e:
        return jsonify({"error": f"EXIF rewriting stream compilation fault: {str(e)}"}), 200

if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)
    app.register_blueprint(script24_bp, url_prefix='/forensic')
    app.run(debug=True, port=5000)

