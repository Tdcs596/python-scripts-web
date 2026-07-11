import os
import json
import time
import random
import csv
from io import StringIO
from flask import Blueprint, render_template_string, request, jsonify, session, redirect, url_for

# =========================================================================
# FACTORY CORE: EXPORT BLUEPRINT FOR APP.PY INTERNAL IMPORT
# =========================================================================
script34_bp = Blueprint('script34', __name__)

DATA_FILE = 'crm_data.json'
AUTH_USER = 'admin'
AUTH_PASS = '@#fsh@#admin123' 

# =========================================================================
# DATABASE CORE (NO-SQL JSON SCHEMATICS ENGINE)
# =========================================================================
def init_db():
    if not os.path.exists(DATA_FILE):
        initial_structure = {
            'leads': [],
            'customers': [],
            'tasks': [],
            'automation_queue': []
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(initial_structure, f, indent=4)

def db_read():
    init_db()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def db_write(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# =========================================================================
# MIDDLEWARE ENGINE
# =========================================================================
def is_authenticated():
    return session.get('crm_logged_in') is True

# =========================================================================
# FLASK ROUTING GATEWAYS
# =========================================================================
@script34_bp.route('/', methods=['GET'])
def index():
    if not is_authenticated():
        return render_template_string(HTML_LAYOUT, is_authenticated=False, login_error=None)
    return render_template_string(HTML_LAYOUT, is_authenticated=True, login_error=None)

@script34_bp.route('/action/login', methods=['POST'])
def action_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == AUTH_USER and password == AUTH_PASS:
        session['crm_logged_in'] = True
        return redirect(url_for('script34.index'))
    else:
        return render_template_string(HTML_LAYOUT, is_authenticated=False, login_error="Invalid credentials! Please try again.")

@script34_bp.route('/action/logout', methods=['GET'])
def action_logout():
    session.clear()
    return redirect(url_for('script34.index'))

# =========================================================================
# FLASK RESTFUL ASYNC API HOOKS (CRITICAL BUSINESS COMPUTATIONS LOGIC)
# =========================================================================
@script34_bp.route('/api/get_dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    
    total_value = sum(float(l.get('value', 0)) for l in db.get('leads', []))
    leads_count = len(db.get('leads', []))
    avg_value = total_value / leads_count if leads_count > 0 else 0

    stats = {
        'total_leads': leads_count,
        'total_customers': len(db.get('customers', [])),
        'pending_tasks': len([t for t in db.get('tasks', []) if t.get('status') != 'Completed']),
        'total_pipeline_value': total_value,
        'average_deal_size': avg_value,
        'total_queued_messages': len(db.get('automation_queue', [])),
        'lead_status_counts': {'New': 0, 'Contacted': 0, 'Proposal': 0, 'Lost': 0},
        'recent_activity': list(reversed(db.get('leads', [])))[:5]
    }
    
    for l in db.get('leads', []):
        status = l.get('status', 'New')
        if status in stats['lead_status_counts']:
            stats['lead_status_counts'][status] += 1
            
    return jsonify(stats)

@script34_bp.route('/api/save_lead', methods=['POST'])
def save_lead():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    lead_id = request.form.get('id', '')
    
    lead_data = {
        'id': int(lead_id) if lead_id else int(time.time()),
        'name': request.form.get('name', ''),
        'email': request.form.get('email', ''),
        'phone': request.form.get('phone', ''),
        'company': request.form.get('company', ''),
        'status': request.form.get('status', 'New'),
        'value': float(request.form.get('value', 0)),
        'date': request.form.get('date') if lead_id else time.strftime('%Y-%m-%d')
    }

    if lead_id:
        for idx, l in enumerate(db['leads']):
            if l['id'] == int(lead_id):
                db['leads'][idx] = lead_data
                break
    else:
        db['leads'].append(lead_data)
        
    db_write(db)
    return jsonify({'success': True, 'message': 'Lead saved successfully!'})

@script34_bp.route('/api/delete_lead', methods=['POST'])
def delete_lead():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    target_id = int(request.form.get('id', 0))
    db['leads'] = [l for l in db['leads'] if l['id'] != target_id]
    db_write(db)
    return jsonify({'success': True})

@script34_bp.route('/api/convert_to_customer', methods=['POST'])
def convert_to_customer():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    target_id = int(request.form.get('id', 0))
    
    target_lead = None
    for l in db['leads']:
        if l['id'] == target_id:
            target_lead = l
            break
            
    if target_lead:
        db['leads'] = [l for l in db['leads'] if l['id'] != target_id]
        db['customers'].append({
            'id': int(time.time()),
            'name': target_lead['name'],
            'email': target_lead['email'],
            'phone': target_lead['phone'],
            'company': target_lead['company'],
            'revenue': target_lead['value'],
            'joined_date': time.strftime('%Y-%m-%d')
        })
        db_write(db)
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Lead not found'})

@script34_bp.route('/api/get_leads', methods=['GET'])
def get_leads():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db_read().get('leads', []))

@script34_bp.route('/api/get_customers', methods=['GET'])
def get_customers():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db_read().get('customers', []))

@script34_bp.route('/api/save_task', methods=['POST'])
def save_task():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    db['tasks'].append({
        'id': int(time.time()),
        'title': request.form.get('title', ''),
        'due_date': request.form.get('due_date', ''),
        'priority': request.form.get('priority', 'Medium'),
        'status': 'Pending'
    })
    db_write(db)
    return jsonify({'success': True})

@script34_bp.route('/api/get_tasks', methods=['GET'])
def get_tasks():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db_read().get('tasks', []))

@script34_bp.route('/api/toggle_task', methods=['POST'])
def toggle_task():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    target_id = int(request.form.get('id', 0))
    for t in db['tasks']:
        if t['id'] == target_id:
            t['status'] = 'Pending' if t['status'] == 'Completed' else 'Completed'
            break
    db_write(db)
    return jsonify({'success': True})

@script34_bp.route('/api/delete_task', methods=['POST'])
def delete_task():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    target_id = int(request.form.get('id', 0))
    db['tasks'] = [t for t in db['tasks'] if t['id'] != target_id]
    db_write(db)
    return jsonify({'success': True})

@script34_bp.route('/api/get_automation_queue', methods=['GET'])
def get_automation_queue():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(db_read().get('automation_queue', []))

@script34_bp.route('/api/clear_automation_queue', methods=['GET', 'POST'])
def clear_automation_queue():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    db = db_read()
    db['automation_queue'] = []
    db_write(db)
    return jsonify({'success': True})

@script34_bp.route('/api/upload_automation_sheet', methods=['POST'])
def upload_automation_sheet():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    if 'automation_file' not in request.files:
        return jsonify({'success': False, 'message': 'No file detected.'})
        
    file = request.files['automation_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Empty spreadsheet selected.'})
        
    if file and file.filename.endswith('.csv'):
        stream = StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_input = csv.reader(stream)
        
        db = db_read()
        imported_count = 0
        
        for row in csv_input:
            if not row or (len(row) < 2): continue
            phone = ''.join(c for c in row[0] if c.isdigit() or c == '+')
            name = row[1] if len(row) > 1 and row[1] else 'Valued Client'
            email = row[2] if len(row) > 2 else ''
            message = row[3] if len(row) > 3 else 'Hello, this is an automated broadcast alert.'
            
            db['automation_queue'].append({
                'id': f"{int(time.time())}_{random.randint(100, 999)}",
                'phone': phone,
                'name': name,
                'email': email,
                'message': message,
                'timestamp': time.strftime('%Y-%m-%d %H:%M')
            })
            imported_count += 1
            
        db_write(db)
        return jsonify({'success': True, 'message': f'Successfully processed {imported_count} workflow contacts.'})
        
    return jsonify({'success': False, 'message': 'Invalid file layout format.'})

# =========================================================================
# FULL INTERFACE SPECIFICATION TEMPLATE LAYOUT (NO-TOUCH DESIGN ENGINE)
# =========================================================================
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrbitEdge Media | Enterprise CRM</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=300;400;500;600;700&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; transition: background-color 0.3s, color 0.3s; }
        .sidebar-link.active { background-color: #4f46e5; color: white; }
        .dark-mode { 
            --bg-panel: #111827; 
            --bg-main: #030712; 
            --text-main: #f9fafb; 
            --text-muted: #9ca3af; 
            --border-color: #1f2937; 
        }
        .light-mode { 
            --bg-panel: #ffffff; 
            --bg-main: #f3f4f6; 
            --text-main: #111827; 
            --text-muted: #6b7280; 
            --border-color: #e5e7eb; 
        }
        body { background-color: var(--bg-main); color: var(--text-main); }
        .panel-card { background-color: var(--bg-panel); border-color: var(--border-color); }
        .text-custom-main { color: var(--text-main); }
        .text-custom-muted { color: var(--text-muted); }
        .border-custom { border-color: var(--border-color); }
        .input-custom { background-color: var(--bg-main); border-color: var(--border-color); color: var(--text-main); }
    </style>
</head>
<body class="light-mode transition-all duration-300 antialiased selection:bg-indigo-500 selection:text-white">

{% if not is_authenticated %}
    <div class="min-h-screen flex items-center justify-center bg-gray-950 px-4">
        <div class="w-full max-w-md bg-gray-900 border border-gray-800 p-8 rounded-2xl shadow-2xl relative overflow-hidden">
            <div class="absolute -top-10 -right-10 w-32 h-32 bg-indigo-600/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-emerald-600/10 rounded-full blur-2xl pointer-events-none"></div>
            
            <div class="text-center mb-8">
                <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-500 shadow-xl shadow-indigo-500/30 mb-4">
                    <i class="fa-solid fa-chart-line text-2xl text-white animate-pulse"></i>
                </div>
                <h1 class="text-2xl font-extrabold text-white tracking-tight">OrbitEdge Media</h1>
                <p class="text-gray-400 text-sm mt-1">Management Portal Enterprise v4.0</p>
            </div>

            {% if login_error %}
                <div class="bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm p-3 rounded-xl mb-5 flex items-center gap-2">
                    <i class="fa-solid fa-circle-exclamation text-rose-500"></i> {{ login_error }}
                </div>
            {% endif %}

            <form action="/action/login" method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-1.5">Username</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500"><i class="fa-solid fa-user text-sm"></i></span>
                        <input type="text" name="username" required placeholder="admin" class="w-full bg-gray-950/50 border border-gray-800 rounded-xl pl-10 pr-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-gray-400 mb-1.5">Password</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500"><i class="fa-solid fa-lock text-sm"></i></span>
                        <input type="password" name="password" required placeholder="••••••••" class="w-full bg-gray-950/50 border border-gray-800 rounded-xl pl-10 pr-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200">
                    </div>
                </div>
                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-indigo-600/20 transition duration-200 cursor-pointer mt-2 tracking-wide text-sm">Login Engine</button>
            </form>
            <div class="mt-6 text-center border-t border-gray-800/60 pt-4"><p class="text-xs text-gray-600 tracking-wide">Pure Flask Secured Stack • SQL-Free Architecture</p></div>
        </div>
    </div>
{% else %}
    <div class="min-h-screen flex flex-col md:flex-row">
        
        <!-- SIDEBAR -->
        <aside class="w-full md:w-64 bg-gray-950 text-white flex flex-col border-r border-gray-900">
            <div class="p-6 border-b border-gray-900 flex items-center gap-3">
                <div class="p-2.5 bg-gradient-to-tr from-indigo-600 to-violet-500 rounded-xl shadow-md"><i class="fa-solid fa-bolt text-lg text-white"></i></div>
                <div>
                    <h2 class="font-bold text-base tracking-wide leading-none text-white">OrbitEdge</h2>
                    <span class="text-[10px] text-gray-400 uppercase tracking-widest mt-1 block">Media Agency CRM</span>
                </div>
            </div>
            <nav class="flex-1 p-4 space-y-1.5">
                <button onclick="switchTab('dashboard')" id="btn-dashboard" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-gauge w-5 text-center"></i> Dashboard</button>
                <button onclick="switchTab('leads')" id="btn-leads" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-bullseye w-5 text-center"></i> Pipeline & Leads</button>
                <button onclick="switchTab('customers')" id="btn-customers" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-users w-5 text-center"></i> Active Customers</button>
                <button onclick="switchTab('automation')" id="btn-automation" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-paper-plane w-5 text-center"></i> Bulk Automation</button>
                <button onclick="switchTab('tasks')" id="btn-tasks" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-list-check w-5 text-center"></i> Tasks & Follow-ups</button>
                <button onclick="switchTab('reports')" id="btn-reports" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-gray-400 hover:bg-gray-900 hover:text-white transition duration-150 cursor-pointer"><i class="fa-solid fa-chart-pie w-5 text-center"></i> Advanced Reports</button>
            </nav>
            <div class="p-4 border-t border-gray-900 space-y-2">
                <button onclick="toggleDarkMode()" class="w-full flex items-center justify-between px-4 py-2.5 rounded-xl bg-gray-900 text-xs font-semibold cursor-pointer text-gray-300 hover:text-white hover:bg-gray-850 transition">
                    <span>Appearance Mode</span><i id="theme-icon" class="fa-solid fa-moon"></i>
                </button>
                <a href="/action/logout" class="w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-semibold text-rose-400 hover:bg-rose-500/10 transition"><i class="fa-solid fa-right-from-bracket"></i> Clear Session</a>
            </div>
        </aside>

        <!-- MAIN MAIN CONTAINER -->
        <main class="flex-1 p-6 md:p-8 overflow-y-auto max-h-screen">
            
            <!-- Toast Notification Box -->
            <div id="toast" class="fixed bottom-5 right-5 z-50 transform translate-y-20 opacity-0 bg-gray-900 border border-emerald-500/30 text-white px-5 py-3.5 rounded-xl shadow-2xl flex items-center gap-3 transition-all duration-300 pointer-events-none">
                <div class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></div>
                <i class="fa-solid fa-circle-check text-emerald-400 text-lg"></i> <span id="toast-text" class="text-sm font-semibold tracking-wide"></span>
            </div>

            <!-- DASHBOARD TAB -->
            <div id="tab-dashboard" class="tab-content hidden space-y-8 animate-fadeIn">
                <div>
                    <h1 class="text-2xl font-bold tracking-tight text-custom-main">Main Command Dashboard</h1>
                    <p class="text-sm text-custom-muted">Live operational analytical monitoring dashboard.</p>
                </div>
                
                <!-- Stat Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 rounded-xl"><i class="fa-solid fa-bolt text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Leads</p><h3 id="stat-leads" class="text-2xl font-extrabold mt-0.5 text-custom-main">0</h3></div>
                    </div>
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 rounded-xl"><i class="fa-solid fa-wallet text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Clients</p><h3 id="stat-customers" class="text-2xl font-extrabold mt-0.5 text-custom-main">0</h3></div>
                    </div>
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-amber-500/10 text-amber-600 dark:text-amber-400 rounded-xl"><i class="fa-solid fa-circle-check text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Tasks</p><h3 id="stat-tasks" class="text-2xl font-extrabold mt-0.5 text-custom-main">0</h3></div>
                    </div>
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-blue-500/10 text-blue-600 dark:text-blue-400 rounded-xl"><i class="fa-solid fa-chart-line text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Pipeline</p><h3 id="stat-pipeline-value" class="text-2xl font-extrabold mt-0.5 text-custom-main">₹0</h3></div>
                    </div>
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-purple-500/10 text-purple-600 dark:text-purple-400 rounded-xl"><i class="fa-solid fa-calculator text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Avg Deal</p><h3 id="stat-avg-deal" class="text-2xl font-extrabold mt-0.5 text-custom-main">₹0</h3></div>
                    </div>
                    <div class="panel-card p-5 rounded-2xl shadow-sm border flex items-center gap-4">
                        <div class="p-3 bg-rose-500/10 text-rose-500 dark:text-rose-400 rounded-xl"><i class="fa-solid fa-paper-plane text-xl"></i></div>
                        <div><p class="text-[10px] font-bold uppercase tracking-widest text-custom-muted">Queued Msg</p><h3 id="stat-queued-messages" class="text-2xl font-extrabold mt-0.5 text-custom-main">0</h3></div>
                    </div>
                </div>

                <!-- Charts & Activity Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 panel-card p-6 rounded-2xl shadow-sm border flex flex-col justify-between">
                        <h3 class="font-bold text-base mb-4 flex items-center gap-2 text-custom-main"><i class="fa-solid fa-chart-simple text-indigo-600"></i> Pipeline Status Analysis</h3>
                        <div class="w-full h-72 relative"><canvas id="dashboardPipelineChart"></canvas></div>
                    </div>
                    <div class="panel-card p-6 rounded-2xl shadow-sm border flex flex-col">
                        <h3 class="font-bold text-base mb-4 flex items-center gap-2 text-custom-main"><i class="fa-solid fa-clock-rotate-left text-indigo-600"></i> Recent Activities</h3>
                        <div id="recent-activity-list" class="space-y-3 overflow-y-auto max-h-[288px] flex-1 pr-1"></div>
                    </div>
                </div>
            </div>

            <!-- LEADS TAB -->
            <div id="tab-leads" class="tab-content hidden space-y-6">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                    <div><h1 class="text-2xl font-bold tracking-tight text-custom-main">Sales Funnel Pipeline</h1><p class="text-sm text-custom-muted">Track and optimize incoming inquiries.</p></div>
                    <div class="flex gap-2.5">
                        <button onclick="exportLeadsToCSV()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2.5 rounded-xl shadow-lg shadow-emerald-600/10 text-xs tracking-wide flex items-center gap-2 cursor-pointer transition"><i class="fa-solid fa-file-csv"></i> Export CSV</button>
                        <button onclick="openLeadModal()" class="bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-4 py-2.5 rounded-xl shadow-lg shadow-indigo-600/10 text-xs tracking-wide flex items-center gap-2 cursor-pointer transition"><i class="fa-solid fa-plus"></i> New Lead</button>
                    </div>
                </div>
                <div class="panel-card p-4 rounded-xl border flex flex-col sm:flex-row gap-3 justify-between items-center">
                    <div class="relative w-full sm:w-72">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400"><i class="fa-solid fa-magnifying-glass text-xs"></i></span>
                        <input type="text" id="leadSearch" onkeyup="renderLeadsTable()" placeholder="Search client name or brand..." class="w-full input-custom border rounded-xl pl-9 pr-4 py-2 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <select id="leadFilterStatus" onchange="renderLeadsTable()" class="w-full sm:w-44 input-custom border rounded-xl px-3 py-2 text-xs focus:outline-none">
                        <option value="All">All Statuses</option><option value="New">New</option><option value="Contacted">Contacted</option><option value="Proposal">Proposal</option><option value="Lost">Lost</option>
                    </select>
                </div>
                <div class="panel-card rounded-xl border overflow-x-auto shadow-sm">
                    <table class="w-full text-left border-collapse min-w-[600px]">
                        <thead>
                            <tr class="border-b border-custom text-custom-muted text-[11px] font-bold uppercase tracking-widest bg-gray-500/5">
                                <th class="p-4">Client / Company</th><th class="p-4">Est Value</th><th class="p-4">Funnel Position</th><th class="p-4">Date Added</th><th class="p-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="leads-table-body" class="divide-y divide-custom text-xs text-custom-main"></tbody>
                    </table>
                </div>
            </div>

            <!-- CUSTOMERS TAB -->
            <div id="tab-customers" class="tab-content hidden space-y-6">
                <div><h1 class="text-2xl font-bold tracking-tight text-custom-main">Active Accounts Database</h1><p class="text-sm text-custom-muted">Clients converted from pipeline into official revenue generators.</p></div>
                <div class="panel-card p-4 rounded-xl border flex gap-3 items-center">
                    <div class="relative w-full sm:w-72">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400"><i class="fa-solid fa-magnifying-glass text-xs"></i></span>
                        <input type="text" id="customerSearch" onkeyup="renderCustomersTable()" placeholder="Search active accounts..." class="w-full input-custom border rounded-xl pl-9 pr-4 py-2 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                </div>
                <div class="panel-card rounded-xl border overflow-x-auto shadow-sm">
                    <table class="w-full text-left border-collapse min-w-[600px]">
                        <thead>
                            <tr class="border-b border-custom text-custom-muted text-[11px] font-bold uppercase tracking-widest bg-gray-500/5">
                                <th class="p-4">Customer Entity</th><th class="p-4">Corporate Brand</th><th class="p-4">Contact Logic</th><th class="p-4">Total Revenue Generated</th><th class="p-4">Acquisition Date</th>
                            </tr>
                        </thead>
                        <tbody id="customers-table-body" class="divide-y divide-custom text-xs text-custom-main"></tbody>
                    </table>
                </div>
            </div>

            <!-- AUTOMATION TAB -->
            <div id="tab-automation" class="tab-content hidden space-y-6">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                    <div>
                        <h1 class="text-2xl font-bold tracking-tight text-custom-main">Bulk Marketing & Message Automation</h1>
                        <p class="text-sm text-custom-muted">Upload CSV spreadsheets to dispatch automated triggers.</p>
                    </div>
                    <button onclick="clearAutomationLogs()" class="bg-rose-600/10 text-rose-500 dark:text-rose-400 border border-rose-500/20 hover:bg-rose-500/20 px-3 py-2 rounded-xl text-xs font-bold cursor-pointer transition flex items-center gap-2">
                        <i class="fa-solid fa-trash-can"></i> Clear Broadcast Records
                    </button>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="panel-card p-6 rounded-2xl border h-fit space-y-4 shadow-sm">
                        <h3 class="font-bold text-base text-indigo-500 flex items-center gap-2"><i class="fa-solid fa-file-excel"></i> Ingest Customer Sheet</h3>
                        <p class="text-xs text-custom-muted leading-relaxed">
                            Upload a <strong>CSV file</strong> structured exactly into the following schema grid:<br>
                            <span class="block mt-1.5 font-mono text-indigo-500 bg-indigo-500/5 p-2 rounded-lg border border-indigo-500/10">Col A: Phone | Col B: Name | Col C: Email | Col D: Message</span>
                        </p>
                        <form id="automation-upload-form" onsubmit="handleSheetUpload(event)" class="space-y-4">
                            <div class="border-2 border-dashed border-custom rounded-xl p-6 text-center hover:border-indigo-500 transition relative bg-gray-500/5 cursor-pointer">
                                <input type="file" id="automation_file" name="automation_file" accept=".csv" required class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
                                <i class="fa-solid fa-cloud-arrow-up text-3xl text-gray-400 mb-2 block"></i>
                                <p class="text-xs font-semibold text-custom-main">Click or Drag CSV Document</p>
                            </div>
                            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2.5 rounded-xl text-xs transition cursor-pointer flex items-center justify-center gap-2 shadow-md shadow-indigo-600/10">
                                <i class="fa-solid fa-gears"></i> Deploy Sheet Records
                            </button>
                        </form>
                    </div>

                    <div class="lg:col-span-2 panel-card p-6 rounded-2xl border flex flex-col shadow-sm">
                        <h3 class="font-bold text-base mb-4 flex items-center gap-2 text-custom-main"><i class="fa-solid fa-satellite-dish text-indigo-600"></i> Dispatched Broadcast Operational Grid</h3>
                        <div class="overflow-x-auto flex-1 max-h-[400px]">
                            <table class="w-full text-left border-collapse text-xs min-w-[500px]">
                                <thead>
                                    <tr class="border-b border-custom text-custom-muted font-bold uppercase tracking-wider bg-gray-500/5">
                                        <th class="p-3">Client Target</th>
                                        <th class="p-3">Automated Message Body</th>
                                        <th class="p-3 text-right">Dispatch Channels</th>
                                    </tr>
                                </thead>
                                <tbody id="automation-queue-body" class="divide-y divide-custom text-custom-main"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TASKS TAB -->
            <div id="tab-tasks" class="tab-content hidden space-y-6">
                <div><h1 class="text-2xl font-bold tracking-tight text-custom-main">Workflow Task Matrix</h1><p class="text-sm text-custom-muted">Internal activities and client engagement logs.</p></div>
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="panel-card p-6 rounded-2xl border h-fit shadow-sm">
                        <h3 class="font-bold text-base mb-4 text-indigo-500">Register New Objective</h3>
                        <form id="task-form" onsubmit="handleTaskSubmit(event)" class="space-y-4">
                            <div>
                                <label class="block text-xs font-bold text-custom-muted mb-1.5">Objective Task Title</label>
                                <input type="text" id="task_title" required placeholder="E.g., Design Review Blueprint" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs font-bold text-custom-muted mb-1.5">Due Deadline</label>
                                    <input type="date" id="task_due" required class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-custom-muted mb-1.5">Priority Weight</label>
                                    <select id="task_priority" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                                        <option value="High">High</option><option value="Medium" selected>Medium</option><option value="Low">Low</option>
                                    </select>
                                </div>
                            </div>
                            <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2.5 rounded-xl text-xs transition cursor-pointer shadow-md shadow-indigo-600/10">Inject Task Engine</button>
                        </form>
                    </div>
                    <div class="lg:col-span-2 panel-card p-6 rounded-2xl border flex flex-col shadow-sm">
                        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-5">
                            <h3 class="font-bold text-base flex items-center gap-2 text-custom-main">Active Strategic Roadmap</h3>
                            <div class="flex gap-2 w-full sm:w-auto">
                                <select id="taskFilterPriority" onchange="renderTasksList()" class="input-custom border rounded-xl px-2.5 py-1.5 text-xs focus:outline-none">
                                    <option value="All">All Priorities</option><option value="High">High Only</option><option value="Medium">Medium Only</option><option value="Low">Low Only</option>
                                </select>
                                <select id="taskFilterStatus" onchange="renderTasksList()" class="input-custom border rounded-xl px-2.5 py-1.5 text-xs focus:outline-none">
                                    <option value="All">All Statuses</option><option value="Pending">Pending</option><option value="Completed">Completed</option>
                                </select>
                            </div>
                        </div>
                        <div id="tasks-list" class="space-y-3 flex-1 overflow-y-auto max-h-[450px] pr-1"></div>
                    </div>
                </div>
            </div>

            <!-- REPORTS TAB -->
            <div id="tab-reports" class="tab-content hidden space-y-8">
                <div><h1 class="text-2xl font-bold tracking-tight text-custom-main">Advanced Analytical Business Reports</h1><p class="text-sm text-custom-muted">Visual intelligence telemetry summaries.</p></div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="panel-card p-6 rounded-2xl border shadow-sm">
                        <h3 class="font-bold text-base mb-6 text-center text-custom-main">Funnels Pipeline Component Breakdown</h3>
                        <div class="w-full max-w-[280px] mx-auto relative"><canvas id="reportPieChart"></canvas></div>
                    </div>
                    <div class="panel-card p-6 rounded-2xl border shadow-sm">
                        <h3 class="font-bold text-base mb-6 text-center text-custom-main">Gross Business Conversion Velocity</h3>
                        <div class="w-full max-w-[280px] mx-auto relative"><canvas id="reportDoughnutChart"></canvas></div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <!-- MODAL SPECIFICATIONS -->
    <div id="leadModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 opacity-0 pointer-events-none transition-all duration-300 px-4">
        <div class="w-full max-w-lg bg-[var(--bg-panel)] border border-[var(--border-color)] rounded-2xl shadow-2xl overflow-hidden transform scale-95 transition-all duration-300">
            <div class="bg-indigo-600 px-6 py-4 text-white flex justify-between items-center">
                <h3 id="modalTitle" class="font-bold text-sm tracking-wide">Initialize Core Funnel Record</h3>
                <button onclick="closeLeadModal()" class="text-white/70 hover:text-white text-lg cursor-pointer"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <form id="lead-form" onsubmit="handleLeadSubmit(event)" class="p-6 space-y-4">
                <input type="hidden" id="lead_id">
                <input type="hidden" id="lead_date">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Lead Client Name</label>
                        <input type="text" id="lead_name" required placeholder="Shivam Singh" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Corporate Brand Name</label>
                        <input type="text" id="lead_company" placeholder="OrbitEdge Media" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Email Coordinates</label>
                        <input type="email" id="lead_email" required placeholder="shivam@example.com" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Telephony Gateway (Phone)</label>
                        <input type="text" id="lead_phone" required placeholder="+91 9876543210" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Pipeline State Status</label>
                        <select id="lead_status" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                            <option value="New">New</option><option value="Contacted">Contacted</option><option value="Proposal">Proposal</option><option value="Lost">Lost</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-custom-muted mb-1.5">Estimated Capital Matrix</label>
                        <input type="number" step="0.01" min="0" id="lead_value" required placeholder="50000" class="w-full input-custom border rounded-xl p-2.5 text-xs focus:outline-none focus:border-indigo-500">
                    </div>
                </div>
                <div class="flex justify-end gap-2.5 pt-3 border-t border-custom mt-5">
                    <button type="button" onclick="closeLeadModal()" class="px-4 py-2 border border-custom text-xs font-bold rounded-xl hover:bg-gray-500/10 cursor-pointer text-custom-main transition">Terminate Process</button>
                    <button type="submit" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-xl cursor-pointer transition shadow-md shadow-indigo-600/10">Commit Database Entry</button>
                </div>
            </form>
        </div>
    </div>

    <!-- JAVASCRIPT APP ARCHITECTURE -->
    <script>
        let activeTab = 'dashboard';
        let rawLeads = [];
        let rawCustomers = [];
        let rawTasks = [];
        let rawAutomation = [];
        let pipelineChartInstance = null;
        let reportPieChartInstance = null;
        let reportDoughnutChartInstance = null;

        async function fetchAPI(endpoint, postData = null) {
            try {
                let options = postData ? { method: 'POST', body: postData } : { method: 'GET' };
                let response = await fetch(`/api/${endpoint}`, options);
                return await response.json();
            } catch (err) {
                console.error("AJAX Telemetry stream broke down:", err);
            }
        }

        function popToast(msg) {
            const el = document.getElementById('toast');
            document.getElementById('toast-text').innerText = msg;
            el.classList.remove('translate-y-20', 'opacity-0');
            setTimeout(() => el.classList.add('translate-y-20', 'opacity-0'), 3000);
        }

        window.addEventListener('DOMContentLoaded', () => {
            if (localStorage.getItem('theme') === 'dark') {
                toggleDarkMode(true);
            }
            switchTab('dashboard');
        });

        function toggleDarkMode(forceDark = false) {
            const body = document.body;
            const icon = document.getElementById('theme-icon');
            if (body.classList.contains('light-mode') || forceDark) {
                body.classList.remove('light-mode');
                body.classList.add('dark-mode');
                body.style.setProperty('--bg-main', '#030712');
                body.style.setProperty('--bg-panel', '#111827');
                body.style.setProperty('--text-main', '#f9fafb');
                body.style.setProperty('--border-color', '#1f2937');
                body.style.setProperty('--text-muted', '#9ca3af');
                icon.className = "fa-solid fa-sun text-amber-400";
                localStorage.setItem('theme', 'dark');
            } else {
                body.classList.remove('dark-mode');
                body.classList.add('light-mode');
                body.style.setProperty('--bg-main', '#f3f4f6');
                body.style.setProperty('--bg-panel', '#ffffff');
                body.style.setProperty('--text-main', '#111827');
                body.style.setProperty('--border-color', '#e5e7eb');
                body.style.setProperty('--text-muted', '#6b7280');
                icon.className = "fa-solid fa-moon";
                localStorage.setItem('theme', 'light');
            }
            if (pipelineChartInstance) loadDashboardEngine(); 
            if (activeTab === 'reports') loadReportsEngine();
        }

        function switchTab(target) {
            activeTab = target;
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.sidebar-link').forEach(el => el.classList.remove('active'));
            
            document.getElementById(`tab-${target}`).classList.remove('hidden');
            document.getElementById(`btn-${target}`).classList.add('active');

            if (target === 'dashboard') loadDashboardEngine();
            if (target === 'leads') loadLeadsEngine();
            if (target === 'customers') loadCustomersEngine();
            if (target === 'automation') loadAutomationEngine();
            if (target === 'tasks') loadTasksEngine();
            if (target === 'reports') loadReportsEngine();
        }

        async function loadDashboardEngine() {
            let stats = await fetchAPI('get_dashboard_stats');
            document.getElementById('stat-leads').innerText = stats.total_leads;
            document.getElementById('stat-customers').innerText = stats.total_customers;
            document.getElementById('stat-tasks').innerText = stats.pending_tasks;
            document.getElementById('stat-queued-messages').innerText = stats.total_queued_messages ?? 0;
            document.getElementById('stat-pipeline-value').innerText = '₹' + parseFloat(stats.total_pipeline_value).toLocaleString('en-IN');
            document.getElementById('stat-avg-deal').innerText = '₹' + parseFloat(stats.average_deal_size).toLocaleString('en-IN', {maximumFractionDigits: 0});

            let actList = document.getElementById('recent-activity-list');
            actList.innerHTML = '';
            if(stats.recent_activity.length === 0) {
                actList.innerHTML = `<p class="text-xs text-gray-500 text-center py-6">No recent activity found.</p>`;
            } else {
                stats.recent_activity.forEach(act => {
                    actList.innerHTML += `
                    <div class="flex items-center justify-between p-3 bg-gray-500/5 rounded-xl border border-custom">
                        <div>
                            <p class="text-xs font-bold text-custom-main">${act.name}</p>
                            <span class="text-[10px] text-custom-muted">${act.company || 'Individual Account'}</span>
                        </div>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-500 dark:text-indigo-400">${act.status}</span>
                    </div>`;
                });
            }
            renderPipelineGraph(stats.lead_status_counts);
        }

        function renderPipelineGraph(counts) {
            let ctx = document.getElementById('dashboardPipelineChart').getContext('2d');
            if (pipelineChartInstance) pipelineChartInstance.destroy();
            
            let isDark = document.body.classList.contains('dark-mode');
            let textColor = isDark ? '#9ca3af' : '#6b7280';

            pipelineChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(counts),
                    datasets: [{
                        label: 'Total Value Metric',
                        data: Object.values(counts),
                        backgroundColor: ['#6366f1', '#3b82f6', '#10b981', '#f43f5e'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } }, grid: { display: false } },
                        y: { ticks: { color: textColor, precision: 0, font: { family: 'Plus Jakarta Sans', size: 11 } }, grid: { color: isDark ? '#1f2937' : '#e5e7eb' } }
                    }
                }
            });
        }

        async function loadLeadsEngine() {
            rawLeads = await fetchAPI('get_leads');
            renderLeadsTable();
        }

        function renderLeadsTable() {
            let query = document.getElementById('leadSearch').value.toLowerCase();
            let filter = document.getElementById('leadFilterStatus').value;
            let tbody = document.getElementById('leads-table-body');
            tbody.innerHTML = '';

            let targetList = rawLeads.filter(l => {
                let matchesQuery = l.name.toLowerCase().includes(query) || l.company.toLowerCase().includes(query);
                let matchesFilter = filter === 'All' || l.status === filter;
                return matchesQuery && matchesFilter;
            });

            if(targetList.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" class="p-8 text-center text-gray-500 font-medium">No matching leads.</td></tr>`;
                return;
            }

            targetList.forEach(l => {
                tbody.innerHTML += `
                <tr class="hover:bg-gray-500/5 transition">
                    <td class="p-4 font-semibold text-custom-main">
                        <div class="text-xs font-bold">${l.name}</div><div class="text-[11px] text-custom-muted font-normal mt-0.5">${l.email} | ${l.phone}</div>
                    </td>
                    <td class="p-4 font-bold text-indigo-500 dark:text-indigo-400">₹${parseFloat(l.value).toLocaleString('en-IN')}</td>
                    <td class="p-4"><span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/20">${l.status}</span></td>
                    <td class="p-4 text-[11px] text-custom-muted">${l.date}</td>
                    <td class="p-4 text-right space-x-1 whitespace-nowrap">
                        <button onclick="convertLead(${l.id})" class="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20 px-2 py-1 rounded-lg transition cursor-pointer"><i class="fa-solid fa-crown"></i> Convert</button>
                        <button onclick='editLeadModal(${JSON.stringify(l)})' class="text-[10px] font-bold text-blue-600 dark:text-blue-400 bg-blue-500/10 hover:bg-blue-500/20 px-2 py-1 rounded-lg transition cursor-pointer"><i class="fa-solid fa-pen"></i></button>
                        <button onclick="deleteLead(${l.id})" class="text-[10px] font-bold text-rose-600 dark:text-rose-400 bg-rose-500/10 hover:bg-rose-500/20 px-2 py-1 rounded-lg transition cursor-pointer"><i class="fa-solid fa-trash"></i></button>
                    </td>
                </tr>`;
            });
        }

        function exportLeadsToCSV() {
            if (rawLeads.length === 0) {
                alert("No lead entries found to export!");
                return;
            }
            let csvContent = "data:text/csv;charset=utf-8,ID,Name,Company,Email,Phone,Status,Value,Date\\n";
            rawLeads.forEach(l => {
                let row = `${l.id},"${l.name}","${l.company}",${l.email},${l.phone},${l.status},${l.value},${l.date}`;
                csvContent += row + "\\n";
            });
            let encodedUri = encodeURI(csvContent);
            let link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "OrbitEdge_Leads_Report.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            popToast("CSV Export completed successfully!");
        }

        function openLeadModal() {
            document.getElementById('lead-form').reset();
            document.getElementById('lead_id').value = '';
            document.getElementById('modalTitle').innerText = "Initialize Core Funnel Record";
            let m = document.getElementById('leadModal');
            m.classList.remove('opacity-0', 'pointer-events-none');
            m.firstElementChild.classList.remove('scale-95');
        }

        function closeLeadModal() {
            let m = document.getElementById('leadModal');
            m.classList.add('opacity-0', 'pointer-events-none');
            m.firstElementChild.classList.add('scale-95');
        }

        function editLeadModal(lead) {
            openLeadModal();
            document.getElementById('modalTitle').innerText = "Modify Funnel Specifications";
            document.getElementById('lead_id').value = lead.id;
            document.getElementById('lead_name').value = lead.name;
            document.getElementById('lead_company').value = lead.company;
            document.getElementById('lead_email').value = lead.email;
            document.getElementById('lead_phone').value = lead.phone;
            document.getElementById('lead_status').value = lead.status;
            document.getElementById('lead_value').value = lead.value;
            document.getElementById('lead_date').value = lead.date;
        }

        async function handleLeadSubmit(e) {
            e.preventDefault();
            let fd = new FormData();
            fd.append('id', document.getElementById('lead_id').value);
            fd.append('name', document.getElementById('lead_name').value);
            fd.append('company', document.getElementById('lead_company').value);
            fd.append('email', document.getElementById('lead_email').value);
            fd.append('phone', document.getElementById('lead_phone').value);
            fd.append('status', document.getElementById('lead_status').value);
            fd.append('value', document.getElementById('lead_value').value);
            fd.append('date', document.getElementById('lead_date').value);

            let res = await fetchAPI('save_lead', fd);
            if(res.success) {
                closeLeadModal();
                popToast("Database Registry Updated!");
                loadLeadsEngine();
            }
        }

        async function deleteLead(id) {
            if(!confirm("Are you sure you want to delete this record?")) return;
            let fd = new FormData(); fd.append('id', id);
            await fetchAPI('delete_lead', fd);
            popToast("Entry wiped from core storage.");
            loadLeadsEngine();
        }

        async function convertLead(id) {
            let fd = new FormData(); fd.append('id', id);
            let res = await fetchAPI('convert_to_customer', fd);
            if(res.success) {
                popToast("Lead successfully converted to Active Customer!");
                loadLeadsEngine();
            }
        }

        async function loadCustomersEngine() {
            rawCustomers = await fetchAPI('get_customers');
            renderCustomersTable();
        }

        function renderCustomersTable() {
            let query = document.getElementById('customerSearch').value.toLowerCase();
            let tbody = document.getElementById('customers-table-body');
            tbody.innerHTML = '';

            let filtered = rawCustomers.filter(c => c.name.toLowerCase().includes(query) || c.company.toLowerCase().includes(query));

            if(filtered.length === 0) {
                tbody.innerHTML = `<tr><td colspan="5" class="p-8 text-center text-gray-500 font-medium">No active accounts.</td></tr>`;
                return;
            }

            filtered.forEach(c => {
                tbody.innerHTML += `
                <tr class="hover:bg-gray-500/5 transition">
                    <td class="p-4 font-bold text-custom-main">${c.name}</td>
                    <td class="p-4 text-custom-muted font-medium">${c.company || 'N/A'}</td>
                    <td class="p-4 text-[11px] font-semibold text-indigo-600 dark:text-indigo-400">${c.email} <br> ${c.phone}</td>
                    <td class="p-4 font-extrabold text-emerald-500">₹${parseFloat(c.revenue).toLocaleString('en-IN')}</td>
                    <td class="p-4 text-[11px] text-custom-muted">${c.joined_date}</td>
                </tr>`;
            });
        }

        async function loadAutomationEngine() {
            rawAutomation = await fetchAPI('get_automation_queue');
            renderAutomationTable();
        }

        function renderAutomationTable() {
            let tbody = document.getElementById('automation-queue-body');
            tbody.innerHTML = '';

            if (rawAutomation.length === 0) {
                tbody.innerHTML = `<tr><td colspan="3" class="p-6 text-center text-gray-500 font-medium">No records found. Upload a CSV file to begin.</td></tr>`;
                return;
            }

            rawAutomation.forEach(item => {
                let encodedText = encodeURIComponent(`Hello ${item.name},\\n\\n${item.message}`);
                let waLink = `https://api.whatsapp.com/send?phone=${item.phone}&text=${encodedText}`;
                let mailLink = `mailto:${item.email}?subject=Updates&body=${encodeURIComponent(item.message)}`;

                tbody.innerHTML += `
                <tr class="hover:bg-gray-500/5 transition border-b border-custom">
                    <td class="p-3 font-semibold text-custom-main">
                        <div class="font-bold">${item.name}</div>
                        <div class="text-[10px] text-custom-muted font-mono mt-0.5">${item.phone || 'No Phone'} | ${item.email || 'No Email'}</div>
                    </td>
                    <td class="p-3 text-custom-muted max-w-[220px] truncate" title="${item.message}">${item.message}</td>
                    <td class="p-3 text-right space-x-1.5 whitespace-nowrap">
                        <a href="${waLink}" target="_blank" class="inline-flex items-center gap-1 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 px-2.5 py-1 rounded-lg text-[10px] font-bold transition">
                            <i class="fa-brands fa-whatsapp"></i> Chat
                        </a>
                        <a href="${mailLink}" class="inline-flex items-center gap-1 bg-blue-500/10 hover:bg-blue-500/20 text-blue-600 dark:text-blue-400 px-2.5 py-1 rounded-lg text-[10px] font-bold transition">
                            <i class="fa-solid fa-envelope"></i> Email
                        </a>
                    </td>
                </tr>`;
            });
        }

        async function handleSheetUpload(e) {
            e.preventDefault();
            let fileInput = document.getElementById('automation_file');
            if (fileInput.files.length === 0) return;

            let fd = new FormData();
            fd.append('automation_file', fileInput.files[0]);

            let res = await fetchAPI('upload_automation_sheet', fd);
            if (res.success) {
                popToast(res.message);
                document.getElementById('automation-upload-form').reset();
                loadAutomationEngine();
            } else {
                alert(res.message);
            }
        }

        async function clearAutomationLogs() {
            if(!confirm("Are you sure you want to flush all automation records?")) return;
            let res = await fetchAPI('clear_automation_queue');
            if (res.success) {
                popToast("Automation log tables reset.");
                loadAutomationEngine();
            }
        }

        async function loadTasksEngine() {
            rawTasks = await fetchAPI('get_tasks');
            renderTasksList();
        }

        function renderTasksList() {
            let priorityFilter = document.getElementById('taskFilterPriority').value;
            let statusFilter = document.getElementById('taskFilterStatus').value;
            let container = document.getElementById('tasks-list');
            container.innerHTML = '';

            let filteredTasks = rawTasks.filter(t => {
                let matchesPriority = (priorityFilter === 'All' || t.priority === priorityFilter);
                let matchesStatus = (statusFilter === 'All' || t.status === statusFilter);
                return matchesPriority && matchesStatus;
            });

            if(filteredTasks.length === 0) {
                container.innerHTML = `<p class="text-xs text-gray-500 text-center py-8 font-medium">No matching objectives found.</p>`;
                return;
            }

            filteredTasks.forEach(t => {
                let isComp = t.status === 'Completed';
                container.innerHTML += `
                <div class="flex items-center justify-between p-4 bg-gray-500/5 border border-custom rounded-xl transition ${isComp ? 'opacity-40 line-through':''}">
                    <div class="flex items-center gap-3">
                        <input type="checkbox" ${isComp ? 'checked':''} onclick="toggleTask(${t.id})" class="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 border-custom bg-transparent cursor-pointer">
                        <div>
                            <p class="text-xs font-bold text-custom-main">${t.title}</p>
                            <span class="text-[10px] text-custom-muted"><i class="fa-solid fa-calendar text-[9px] mr-1"></i>Deadline: ${t.due_date}</span>
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <span class="text-[9px] font-bold px-2 py-0.5 rounded-full ${t.priority==='High'?'bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20':'bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20'}">${t.priority}</span>
                        <button onclick="deleteTask(${t.id})" class="text-gray-400 hover:text-rose-500 text-xs transition p-1 cursor-pointer"><i class="fa-solid fa-trash-can"></i></button>
                    </div>
                </div>`;
            });
        }

        async function handleTaskSubmit(e) {
            e.preventDefault();
            let fd = new FormData();
            fd.append('title', document.getElementById('task_title').value);
            fd.append('due_date', document.getElementById('task_due').value);
            fd.append('priority', document.getElementById('task_priority').value);
            
            await fetchAPI('save_task', fd);
            document.getElementById('task-form').reset();
            popToast("Task objective deployed successfully.");
            loadTasksEngine();
        }

        async function toggleTask(id) {
            let fd = new FormData(); fd.append('id', id);
            await fetchAPI('toggle_task', fd);
            loadTasksEngine();
        }

        async function deleteTask(id) {
            let fd = new FormData(); fd.append('id', id);
            await fetchAPI('delete_task', fd);
            popToast("Task record eliminated.");
            loadTasksEngine();
        }

        async function loadReportsEngine() {
            let stats = await fetchAPI('get_dashboard_stats');
            let ctxPie = document.getElementById('reportPieChart').getContext('2d');
            let ctxDoughnut = document.getElementById('reportDoughnutChart').getContext('2d');

            if (reportPieChartInstance) reportPieChartInstance.destroy();
            if (reportDoughnutChartInstance) reportDoughnutChartInstance.destroy();

            let isDark = document.body.classList.contains('dark-mode');
            let legendColor = isDark ? '#9ca3af' : '#6b7280';

            let chartOptions = {
                responsive: true,
                plugins: { 
                    legend: { 
                        position: 'bottom', 
                        labels: { 
                            boxWidth: 10, 
                            color: legendColor,
                            font: { size: 10, family: 'Plus Jakarta Sans', weight: 500 } 
                        } 
                    } 
                }
            };

            reportPieChartInstance = new Chart(ctxPie, {
                type: 'pie',
                data: {
                    labels: Object.keys(stats.lead_status_counts),
                    datasets: [{
                        data: Object.values(stats.lead_status_counts),
                        backgroundColor: ['#6366f1', '#3b82f6', '#10b981', '#f43f5e'],
                        borderWidth: isDark ? 2 : 1,
                        borderColor: isDark ? '#111827' : '#ffffff'
                    }]
                },
                options: chartOptions
            });

            reportDoughnutChartInstance = new Chart(ctxDoughnut, {
                type: 'doughnut',
                data: {
                    labels: ['Pipeline Inbounds', 'Converted Global Accounts'],
                    datasets: [{
                        data: [stats.total_leads, stats.total_customers],
                        backgroundColor: ['#6366f1', '#10b981'],
                        borderWidth: isDark ? 2 : 1,
                        borderColor: isDark ? '#111827' : '#ffffff'
                    }]
                },
                options: chartOptions
            });
        }
    </script>
{% endif %}
</body>
</html>
"""

