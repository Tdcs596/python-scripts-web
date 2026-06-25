from flask import Blueprint, render_template_string, request, jsonify

script30_bp = Blueprint('script30', __name__)

REAL_SEJDA_UI = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-Time PDF Matrix Editor</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
        --bg-system: #f1f5f9;
        --nav-bar: #ffffff;
        --sejda-green: #10b981;
        --sejda-hover: #059669;
        --primary-blue: #3b82f6;
        --text-dark: #0f172a;
        --text-muted: #64748b;
        --border-line: #cbd5e1;
    }

    body { 
        background: var(--bg-system); 
        color: var(--text-dark); 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* --- SEJDA INTERACTIVE NAVBAR --- */
    .toolbar-header {
        background: var(--nav-bar);
        border-bottom: 1px solid var(--border-line);
        padding: 12px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    .brand-identity {
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }
    .brand-identity span {
        background: var(--primary-blue);
        color: white;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        margin-left: 5px;
    }

    .control-center {
        display: flex;
        gap: 10px;
    }

    .action-btn {
        background: #f8fafc;
        border: 1px solid var(--border-line);
        padding: 8px 16px;
        font-size: 13px;
        font-weight: 500;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.15s;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .action-btn:hover { background: #e2e8f0; border-color: var(--text-muted); }
    .action-btn.active { background: #eff6ff; color: var(--primary-blue); border-color: var(--primary-blue); }

    .btn-download {
        background: var(--sejda-green);
        color: #fff;
        font-weight: 600;
        border: none;
    }
    .btn-download:hover { background: var(--sejda-hover); }

    /* --- STUDIO STAGE WORKSPACE --- */
    .studio-viewport {
        flex: 1;
        padding: 30px 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow-y: auto;
    }

    /* --- LIVING REAL-TIME PDF PAGE CONTAINER --- */
    .pdf-render-frame {
        position: relative;
        background: #ffffff;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.02);
        border: 1px solid var(--border-line);
        margin-bottom: 25px;
        border-radius: 4px;
    }

    /* Transparent canvas matching vector sizing layers */
    .pdf-canvas-layer {
        display: block;
        z-index: 1;
    }

    /* --- LIVE INJECTED HIGH-PURITY EDITABLE WRAPPERS --- */
    .interactive-text-field {
        position: absolute;
        z-index: 10;
        border: 1px dashed transparent;
        padding: 1px 3px;
        outline: none;
        cursor: text;
        font-family: sans-serif;
        color: #000;
        white-space: pre;
        background: transparent;
        transform-origin: top left;
    }
    .interactive-text-field:hover {
        border-color: var(--primary-blue);
        background: rgba(59, 130, 246, 0.03);
    }
    .interactive-text-field:focus {
        border: 1px solid var(--primary-blue);
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-radius: 3px;
    }

    /* --- RECON STREAM INITIAL UPLOADER BOX --- */
    .uploader-dropzone {
        width: 100%;
        max-width: 600px;
        height: 280px;
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: 0.2s;
        padding: 20px;
    }
    .uploader-dropzone:hover { border-color: var(--primary-blue); background: #f8fafc; }
    
    .hidden-input { display: none; }
  </style>
</head>
<body>

    <div class="toolbar-header">
        <div class="brand-identity">📄 SHIVAM SINGH OMEGA EDITOR <span>ENGINE v2</span></div>
        
        <div class="control-center" id="engine_controls" style="display: none;">
            <button class="action-btn active" id="mode_text" onclick="setMode('text')">🔤 Edit/Add Text</button>
            <button class="action-btn" onclick="injectNewBlankText()">➕ Add New Paragraph</button>
        </div>

        <div>
            <button class="action-btn btn-download" id="btn_export" style="display: none;" onclick="exportModifiedMatrix()">Apply & Save Changes</button>
        </div>
    </div>

    <div class="studio-viewport" id="workspace_stage">
        <div class="uploader-dropzone" onclick="triggerFilePicker()">
            <span style="font-size: 50px; margin-bottom: 15px;">📥</span>
            <h3 style="font-size: 16px; margin-bottom: 5px;">Upload your actual PDF document</h3>
            <p style="color: var(--text-muted); font-size: 13px;">File stream will render dynamically into interactive text matrices</p>
            <input type="file" id="real_pdf_uploader" class="hidden-input" accept="application/pdf" onchange="ingestRealPdfDocument()">
        </div>
    </div>

    <script>
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js';
        
        let currentMode = 'text';
        let globalPdfDoc = null;

        function triggerFilePicker() {
            document.getElementById('real_pdf_uploader').click();
        }

        // --- REAL PDF DECODING & EXTRACTION LOOP ---
        async function ingestRealPdfDocument() {
            const uploader = document.getElementById('real_pdf_uploader');
            if (uploader.files.length === 0) return;

            const file = uploader.files[0];
            const fileReader = new FileReader();

            // Setup display parameters layout visibility handles
            document.getElementById('engine_controls').style.display = 'flex';
            document.getElementById('btn_export').style.display = 'block';
            
            const stage = document.getElementById('workspace_stage');
            stage.innerHTML = '<p style="color:var(--text-muted); font-size:14px;">📡 Unpacking PDF binary streams & mapping structural font layers...</p>';

            fileReader.onload = async function() {
                const typedarray = new Uint8Array(this.result);
                try {
                    globalPdfDoc = await pdfjsLib.getDocument(typedarray).promise;
                    stage.innerHTML = ''; // Wipe loader text strings

                    // Iterate over each structural page stream layer sequences
                    for (let pageNum = 1; pageNum <= globalPdfDoc.numPages; pageNum++) {
                        await renderInteractivePdfPage(pageNum);
                    }
                } catch (err) {
                    stage.innerHTML = `<p style="color:red; font-size:14px;">❌ Error processing binary: ${err.message}</p>`;
                }
            };
            fileReader.readAsArrayBuffer(file);
        }

        // --- RENDER DYNAMIC CANVAS + COORDINATE INLINE TEXT BLOCK MAPS ---
        async function renderInteractivePdfPage(pageNum) {
            const stage = document.getElementById('workspace_stage');
            const page = await globalPdfDoc.getPage(pageNum);
            
            const viewport = page.getViewport({ scale: 1.3 }); // Perfect resolution layout rendering scaling scale

            // Rebuild structural housing page element blocks
            const pageWrapper = document.createElement('div');
            pageWrapper.className = 'pdf-render-frame';
            pageWrapper.id = `page_container_${pageNum}`;
            pageWrapper.style.width = viewport.width + 'px';
            pageWrapper.style.height = viewport.height + 'px';

            const canvas = document.createElement('canvas');
            canvas.className = 'pdf-canvas-layer';
            const context = canvas.getContext('2d');
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            pageWrapper.appendChild(canvas);
            stage.appendChild(pageWrapper);

            // Render visual tracking back layers cleanly
            await page.render({ canvasContext: context, viewport: viewport }).promise;

            // Extract structural text layer object token coordinates dynamically!
            const textContent = await page.getTextContent();
            
            textContent.items.forEach(item => {
                // Ignore structural empty spatial characters or line return hooks
                if (!item.str.trim()) return;

                // Transform viewport vector mapping matrices to extract raw spatial pixel layouts
                const tx = pdfjsLib.Util.transform(viewport.transform, item.transform);
                
                const editableNode = document.createElement('div');
                editableNode.className = 'interactive-text-field';
                editableNode.contentEditable = 'true';
                editableNode.innerText = item.str;
                
                // Absolute structural alignment coordinates matching the under-layer drawing stream
                editableNode.style.left = tx[4] + 'px';
                editableNode.style.top = (viewport.height - tx[5] - (item.height * 1.1)) + 'px';
                editableNode.style.fontSize = item.height + 'px';
                
                pageWrapper.appendChild(editableNode);
            });

            // Handle blank user canvas click triggers to spawn interactive free-text elements
            pageWrapper.addEventListener('click', function(e) {
                if (e.target === canvas && currentMode === 'text') {
                    const box = pageWrapper.getBoundingClientRect();
                    const newX = (e.clientX - box.left) + 'px';
                    const newY = (e.clientY - box.top) + 'px';
                    
                    const newNode = document.createElement('div');
                    newNode.className = 'interactive-text-field';
                    newNode.contentEditable = 'true';
                    newNode.innerText = 'Click here to write text';
                    newNode.style.left = newX;
                    newNode.style.top = newY;
                    newNode.style.fontSize = '14px';
                    newNode.style.color = 'var(--primary-blue)';
                    
                    pageWrapper.appendChild(newNode);
                    setTimeout(() => newNode.focus(), 20);
                }
            });
        }

        function injectNewBlankText() {
            alert("Bhai, PDF page ke khali white space par kahi bhi click karo, wahan naya text block automatic ban jayega!");
        }

        // --- APPLICATION METRICS SAVE DISPATCH DISPATCH CONTROLLER ---
        function exportModifiedMatrix() {
            const modifications = [];
            document.querySelectorAll('.interactive-text-field').forEach(node => {
                modifications.push({
                    text: node.innerText,
                    x_pos: node.style.left,
                    y_pos: node.style.top
                });
            });

            console.log("Saving Sejda Core Delta Changes Map:", modifications);
            alert("Bhai, changes save ho gaye hain! Saari edited parameters aur positions console stream par compile ho gayi hain.");
        }
    </script>
</body>
</html>
"""

@script30_bp.route('/')
def index():
    return render_template_string(REAL_SEJDA_UI)
