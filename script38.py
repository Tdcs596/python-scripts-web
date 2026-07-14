import os
import yfinance as yf
import pandas as pd
import numpy as np
import threading
import time
import matplotlib
# Headless operations compliance for Render cloud container environment
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Blueprint, render_template_string, request, jsonify

# 1. DEFINE THE BLUEPRINT EXPECTED BY APP.PY MASTER ROUTER
script38_bp = Blueprint('script38', __name__, static_folder='static')

COMPANY_NAME = os.environ.get('COMPANY_NAME', 'Alpha Intelligence Suite')
chart_lock = threading.Lock()

class FundamentalAnalysisEngine:
    def __init__(self, ticker_symbol):
        self.ticker_str = ticker_symbol.upper().strip()
        self.ticker = yf.Ticker(self.ticker_str)
        self.info = {}
        self.financials = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()

    def fetch_corporate_data(self):
        """Fetch raw data and secure fallbacks for local structural parsing"""
        try:
            self.info = self.ticker.info
            self.financials = self.ticker.financials
            self.balance_sheet = self.ticker.balance_sheet
            if not self.info or 'longName' not in self.info:
                return False
            return True
        except Exception:
            return False

    def compute_financial_matrix(self):
        """Calculate A to Z crucial operational ratios structurally"""
        info = self.info
        
        # Valuation & Basic Architecture Metrics
        pe_ratio = info.get('trailingPE') or info.get('forwardPE') or 0.0
        pb_ratio = info.get('priceToBook') or 0.0
        ps_ratio = info.get('priceToSalesTrailing12Months') or 0.0
        peg_ratio = info.get('pegRatio') or 0.0
        roe = (info.get('returnOnEquity') or 0.0) * 100
        roa = (info.get('returnOnAssets') or 0.0) * 100
        
        # Leverage & Liquidity Matrix
        current_ratio = info.get('currentRatio') or 0.0
        quick_ratio = info.get('quickRatio') or 0.0
        debt_to_equity = info.get('debtToEquity') or 0.0  # Percentage scale representation usually
        
        # Profitability Margins
        gross_margin = (info.get('grossMargins') or 0.0) * 100
        operating_margin = (info.get('operatingMargins') or 0.0) * 100
        net_margin = (info.get('profitMargins') or 0.0) * 100
        dividend_yield = (info.get('dividendYield') or 0.0) * 100

        ratios = {
            "P/E Ratio": {"val": round(pe_ratio, 2), "desc": "Price to Earnings: Valuation against income benchmarks.", "health": "Good" if 0 < pe_ratio < 25 else "Overvalued"},
            "P/B Ratio": {"val": round(pb_ratio, 2), "desc": "Price to Book: Evaluation of asset baseline capitalization.", "health": "Good" if pb_ratio < 3 else "High Valuation"},
            "P/S Ratio": {"val": round(ps_ratio, 2), "desc": "Price to Sales: Revenue validation multiplier.", "health": "Normal" if ps_ratio < 5 else "Premium Scale"},
            "PEG Ratio": {"val": round(peg_ratio, 2), "desc": "Price/Earnings to Growth: Growth normalization matrix.", "health": "Underpriced" if 0 < peg_ratio < 1 else "Aggressive Pricing"},
            "Return on Equity (ROE)": {"val": f"{round(roe, 2)}%", "desc": "Efficiency at turning equity investments into corporate gains.", "health": "Strong" if roe > 15 else "Underperforming"},
            "Return on Assets (ROA)": {"val": f"{round(roa, 2)}%", "desc": "Operational yield produced per absolute capital asset dollar.", "health": "Excellent" if roa > 7 else "Low Efficiency"},
            "Current Ratio": {"val": round(current_ratio, 2), "desc": "Liquidity metric evaluating short term debt liabilities settlement.", "health": "Stable" if current_ratio >= 1.5 else "Liquidity Risk"},
            "Debt to Equity": {"val": f"{round(debt_to_equity, 2)}%" if debt_to_equity else "0.0%", "desc": "Capital 구조 leverages indicator measuring debt exposures.", "health": "Safe" if debt_to_equity < 100 else "Highly Leveraged"},
            "Net Profit Margin": {"val": f"{round(net_margin, 2)}%", "desc": "Absolute profit remaining per transactional top line revenue.", "health": "Lucrative" if net_margin > 12 else "Thin Margin"}
        }
        
        # Generate algorithmic structural conclusion
        score = 0
        if 0 < pe_ratio < 22: score += 2
        if roe > 15: score += 2
        if current_ratio >= 1.5: score += 2
        if debt_to_equity < 80: score += 2
        if net_margin > 10: score += 2
        
        if score >= 7:
            conclusion = "STRONGLY RECOMMENDED (BUY)"
            suggestion = f"The asset demonstrates high fundamental integrity, robust return matrices ({round(roe,1)}% ROE), clean structural balances with minimized liquidity exposures. Ideal long term equity addition."
            verdict_color = "text-emerald-500"
        elif score >= 4:
            conclusion = "NEUTRAL WATCHLIST (HOLD)"
            suggestion = "Fair macro stability but indicators signal sectoral optimization delays or premium valuation margins. Recommended to build positions in staggered intervals or await technical consolidations."
            verdict_color = "text-amber-500"
        else:
            conclusion = "HIGH SPECULATIVE RISK (AVOID/SELL)"
            suggestion = "Structural capital erosion elements found. High leverage profiles paired with sub-optimal asset management matrices indicate severe fundamental vulnerabilities. Capitals allocation not advised."
            verdict_color = "text-rose-500"

        return ratios, conclusion, suggestion, verdict_color, score

    def generate_distribution_pie(self, score, timestamp):
        """Build asset allocation pie visualizations securely with lock synchronization"""
        with chart_lock:
            labels = ['Fundamental Strength', 'Risk Vector Mitigation Margin']
            sizes = [score * 10, 100 - (score * 10)]
            colors = ['#38bdf8', '#334155']
            
            fig, ax = plt.subplots(figsize=(5, 5))
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, colors=colors, autopct='%1.0f%%', 
                startangle=140, textprops=dict(color="w", weight="bold")
            )
            
            # Adaptive aesthetic dark-cyber layer
            fig.patch.set_facecolor('#1e293b')
            ax.set_facecolor('#1e293b')
            for text in texts: text.set_color('#94a3b8')
            for autotext in autotexts: autotext.set_color('#0f172a')
                
            static_dir = os.path.join(os.path.dirname(__file__), 'static')
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
                
            graph_filename = f"{self.ticker_str}_{timestamp}_fin_report.png"
            graph_path = os.path.join(static_dir, graph_filename)
            plt.savefig(graph_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
            plt.close()
            return f"static/{graph_filename}"

# 2. APPLICATION CONTROLLER INTERFACES AND ROUTING
@script38_bp.route('/')
def index():
    return render_template_string(HTML_LAYOUT, company=COMPANY_NAME)

@script38_bp.route('/api/analyze', methods=['GET'])
def api_analyze():
    symbol = request.args.get('symbol', '').strip()
    if not symbol:
        return jsonify({'success': False, 'message': 'Target asset ticker parameter required.'}), 400
        
    engine = FundamentalAnalysisEngine(symbol)
    if not engine.fetch_corporate_data():
        return jsonify({'success': False, 'message': 'Failed to resolve market asset vectors. Ensure proper standard ticker usage (e.g., TSLA, INFY.NS)'}), 404
        
    ratios, conclusion, suggestion, color, score = engine.compute_financial_matrix()
    timestamp = int(time.time())
    chart_url = engine.generate_distribution_pie(score, timestamp)
    
    return jsonify({
        'success': True,
        'company_name': engine.info.get('longName', symbol),
        'sector': engine.info.get('sector', 'Global Operations Segment'),
        'currency': engine.info.get('currency', 'USD'),
        'ratios': ratios,
        'conclusion': conclusion,
        'suggestion': suggestion,
        'verdict_color': color,
        'chart_url': chart_url
    })

# ULTRA PREMIUM TAILWIND LIGHT AND DARK MATRIX SCHEMATICS
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en" id="masterHtml" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ company }} | Fundamental Recon Engine</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
        body { 
            font-family: 'Space Grotesk', sans-serif; 
            transition: background-color 0.3s ease, color 0.3s ease;
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 dark:bg-slate-900 dark:text-slate-100 light:bg-slate-50 light:text-slate-900 transition-all duration-300">

    <div class="min-h-screen flex flex-col xl:flex-row">
        <!-- Structural Sidebar Component -->
        <aside class="w-full xl:w-80 bg-slate-950 text-white flex flex-col border-b xl:border-r border-slate-800 p-6">
            <div class="flex items-center justify-between mb-8">
                <div class="flex items-center gap-3">
                    <div class="p-3 bg-gradient-to-br from-sky-500 to-blue-600 rounded-xl shadow-lg">
                        <i class="fa-solid fa-chart-line text-xl text-white"></i>
                    </div>
                    <div>
                        <h2 class="font-bold text-lg tracking-tight leading-none">FinRadar</h2>
                        <span class="text-[10px] text-sky-400 font-mono uppercase tracking-widest mt-1 block">ALGO ENGINE v38</span>
                    </div>
                </div>
                
                <!-- LIGHT / DARK MODE SWAP INTERFACE -->
                <button onclick="toggleAestheticMatrix()" class="p-2.5 rounded-xl bg-slate-900 border border-slate-700 hover:border-sky-400 transition cursor-pointer">
                    <i id="themeIcon" class="fa-solid fa-sun text-amber-400"></i>
                </button>
            </div>
            
            <div class="flex-1 space-y-3">
                <div class="p-4 bg-slate-900/50 border border-slate-800 rounded-xl">
                    <span class="text-[10px] uppercase font-mono text-slate-400 block mb-1">Execution Pipeline</span>
                    <div class="text-xs font-bold text-sky-400 flex items-center gap-1.5">
                        <span class="h-1.5 w-1.5 rounded-full bg-sky-400 animate-ping"></span> Live yFinance Socket Setup
                    </div>
                </div>
            </div>
            
            <div class="pt-4 border-t border-slate-800 text-center text-[10px] font-mono text-slate-500">
                Data Stream Sandbox Secure
            </div>
        </aside>

        <!-- Main Workspace Arena -->
        <main class="flex-1 p-6 xl:p-10 transition-colors duration-300 bg-slate-900 dark:bg-slate-900 light:bg-slate-100">
            <div class="flex flex-col sm:flex-row justify-between sm:items-center border-b border-slate-800 dark:border-slate-800 light:border-slate-300 pb-6 mb-8 gap-4">
                <div>
                    <h1 class="text-3xl font-extrabold tracking-tight dark:text-white light:text-slate-900">{{ company }}</h1>
                    <p class="text-sm dark:text-slate-400 light:text-slate-600 mt-1">Deep-Core Fundamental Analysis Ratio Extraction Matrix Terminal</p>
                </div>
            </div>

            <!-- Global Asset Selection Bar -->
            <div class="p-6 rounded-2xl mb-8 bg-slate-800 border border-slate-700 dark:bg-slate-800 dark:border-slate-700 light:bg-white light:border-slate-200 shadow-sm">
                <h3 class="text-xs font-bold uppercase tracking-widest dark:text-slate-400 light:text-slate-500 mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-magnifying-glass-chart text-sky-400"></i> Corporate Vector Formulation
                </h3>
                <div class="flex flex-col sm:flex-row gap-4">
                    <input type="text" id="assetSymbol" placeholder="Enter Asset Ticker String (e.g. TSLA, INFY.NS, RELIANCE.NS)" 
                           class="flex-1 bg-slate-900 border border-slate-700 dark:bg-slate-900 dark:border-slate-700 light:bg-slate-50 light:border-slate-300 text-sm p-3.5 rounded-xl text-white dark:text-white light:text-slate-900 font-mono focus:outline-none focus:border-sky-500">
                    <button onclick="launchFundamentalAudit()" class="bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold px-8 py-3.5 rounded-xl text-sm transition shadow-lg cursor-pointer tracking-wider uppercase">
                        Compute Matrix Data
                    </button>
                </div>
            </div>

            <!-- Loader Loop State -->
            <div id="loader" class="hidden text-center py-24 bg-slate-800 border border-slate-700 dark:bg-slate-800 dark:border-slate-700 light:bg-white light:border-slate-200 rounded-2xl">
                <i class="fa-solid fa-circle-notch fa-spin text-5xl text-sky-400"></i>
                <p class="text-sm dark:text-slate-400 light:text-slate-600 mt-6 font-mono animate-pulse">Parsing balance sheets, accounting assets ledger, and computing risk matrices...</p>
            </div>

            <!-- Output Reports Segment Matrix -->
            <div id="outputContainer" class="hidden space-y-8">
                
                <!-- TOP LEVEL SUMMARY ADAPTIVE COMPONENT -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <!-- Dynamic Verdict Card -->
                    <div class="lg:col-span-2 p-6 rounded-2xl flex flex-col justify-between bg-slate-800 border border-slate-700 dark:bg-slate-800 dark:border-slate-700 light:bg-white light:border-slate-200">
                        <div>
                            <span id="metaSector" class="text-[10px] font-mono tracking-widest text-sky-400 uppercase block mb-1">Corporate Segment</span>
                            <h2 id="metaTitle" class="text-2xl font-extrabold tracking-tight mb-4">Company Target Name</h2>
                            <hr class="border-slate-700 dark:border-slate-700 light:border-slate-200 mb-4">
                            
                            <label class="text-[11px] font-mono uppercase text-slate-400 block mb-1">Algorithmic Financial Verdict</label>
                            <div id="verdictOutput" class="text-2xl font-black uppercase tracking-wide mb-2">VERDICT SUMMARY</div>
                            <p id="suggestionOutput" class="text-xs dark:text-slate-300 light:text-slate-600 leading-relaxed font-mono">Detailed analytic reasoning will automatically display here based on score indices.</p>
                        </div>
                    </div>
                    
                    <!-- Graph Cluster Display Box -->
                    <div class="p-6 rounded-2xl bg-slate-800 border border-slate-700 dark:bg-slate-800 dark:border-slate-700 light:bg-white light:border-slate-200 flex flex-col justify-center items-center">
                        <span class="text-[11px] font-mono uppercase text-slate-400 mb-3 block w-full text-left"><i class="fa-solid fa-chart-pie text-sky-400 mr-1.5"></i> Strength Analysis Matrix</span>
                        <div class="p-3 border border-slate-700 dark:border-slate-700 light:border-slate-200 bg-slate-900 rounded-xl w-full flex justify-center">
                            <img id="analyticsChart" src="" alt="Fundamental Vector Distribution" class="max-h-52 object-contain">
                        </div>
                    </div>
                </div>

                <!-- METRIC SHEET DISPLAY AREA -->
                <div class="p-6 rounded-2xl bg-slate-800 border border-slate-700 dark:bg-slate-800 dark:border-slate-700 light:bg-white light:border-slate-200">
                    <h3 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4 flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-sky-400"></i> Comprehensive A to Z Fundamental Analysis Matrix Sheets
                    </h3>
                    <div id="ratiosGrid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                        <!-- Instantiated by JS array execution maps -->
                    </div>
                </div>

            </div>
        </main>
    </div>

    <script>
        function toggleAestheticMatrix() {
            const root = document.getElementById('masterHtml');
            const icon = document.getElementById('themeIcon');
            if (root.classList.contains('dark')) {
                root.classList.remove('dark');
                root.classList.add('light');
                icon.className = "fa-solid fa-moon text-indigo-500";
            } else {
                root.classList.remove('light');
                root.classList.add('dark');
                icon.className = "fa-solid fa-sun text-amber-400";
            }
        }

        async function launchFundamentalAudit() {
            const sym = document.getElementById('assetSymbol').value.trim();
            if(!sym) return alert("Structural System Interruption: Asset ticker variable input cannot be empty.");

            document.getElementById('loader').classList.remove('hidden');
            document.getElementById('outputContainer').classList.add('hidden');

            try {
                const response = await fetch(`./api/analyze?symbol=${sym}`);
                const data = await response.json();
                
                document.getElementById('loader').classList.add('hidden');
                
                if(data.success) {
                    document.getElementById('metaTitle').innerText = `${data.company_name} [${sym.toUpperCase()}]`;
                    document.getElementById('metaSector').innerText = `${data.sector} | Denominated in: ${data.currency}`;
                    
                    const verdict = document.getElementById('verdictOutput');
                    verdict.innerText = data.conclusion;
                    verdict.className = `text-2xl font-black uppercase tracking-wide mb-2 ${data.verdict_color}`;
                    
                    document.getElementById('suggestionOutput').innerText = data.suggestion;
                    document.getElementById('analyticsChart').src = './' + data.chart_url + '?cache=' + new Date().getTime();
                    
                    const ratioContainer = document.getElementById('ratiosGrid');
                    ratioContainer.innerHTML = '';
                    
                    for(const [name, obj] of Object.entries(data.ratios)) {
                        const scoreColor = obj.health === 'Good' || obj.health === 'Strong' || obj.health === 'Excellent' || obj.health === 'Stable' || obj.health === 'Lucrative' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20';
                        
                        ratioContainer.innerHTML += `
                            <div class="p-4 bg-slate-900/60 dark:bg-slate-900/60 light:bg-slate-50 border border-slate-700 dark:border-slate-700 light:border-slate-200 rounded-xl flex flex-col justify-between transition hover:border-sky-500/40 shadow-sm">
                                <div>
                                    <div class="flex justify-between items-start gap-2 mb-1">
                                        <span class="text-xs font-bold dark:text-slate-200 light:text-slate-800">${name}</span>
                                        <span class="text-[9px] font-mono border px-2 py-0.5 rounded-md font-bold uppercase ${scoreColor}">${obj.health}</span>
                                    </div>
                                    <p class="text-[11px] dark:text-slate-400 light:text-slate-500 leading-snug font-mono">${obj.desc}</p>
                                </div>
                                <div class="text-xl font-extrabold text-sky-400 mt-4 tracking-tight font-mono">${obj.val}</div>
                            </div>
                        `;
                    }
                    
                    document.getElementById('outputContainer').classList.remove('hidden');
                } else {
                    alert("Analysis Failure: " + data.message);
                }
            } catch(err) {
                document.getElementById('loader').classList.add('hidden');
                alert("Critical System Framework Interruption: Verify market asset connections or structural tags.");
            }
        }
    </script>
</body>
</html>
"""
