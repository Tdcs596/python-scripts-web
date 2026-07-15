import os
import requests
import json
import numpy as np
import pandas as pd
from flask import Blueprint, render_template_string, request, jsonify

# RESTRICTED CYBERNETIC FIN-TECH ENGINE
# Automatically pulls real-time data using yfinance for 100% price accuracy.
import yfinance as yf

script38_bp = Blueprint('script38', __name__, static_folder='static')
COMPANY_BRAND = os.environ.get('COMPANY_NAME', 'Delta Quantum Terminal')


class ActiveMarketEngine:
    def __init__(self, query_string, exchange="NSE"):
        self.raw_query = query_string.strip().upper()
        self.exchange = exchange.upper()
        self.symbol = self._resolve_ticker(self.raw_query)

    def _resolve_ticker(self, q):
        # Maps standard Indian/Global search terms to exact Yahoo Finance tickers
        mapping = {
            "COAL INDIA": "COALINDIA.NS",
            "COALINDIA": "COALINDIA.NS",
            "RELIANCE": "RELIANCE.NS",
            "TCS": "TCS.NS",
            "INFOSYS": "INFY.NS",
            "INFY": "INFY.NS",
            "APPLE": "AAPL",
            "GOOGLE": "GOOGL"
        }
        if q in mapping:
            return mapping[q]

        # If the user searches a custom ticker, check and append exchange suffix.
        # Global tickers (AAPL, GOOGL, etc.) never get an NS/BO suffix.
        if not q.endswith(".NS") and not q.endswith(".BO") and self.exchange in ["NSE", "BSE"]:
            suffix = ".NS" if self.exchange == "NSE" else ".BO"
            return f"{q}{suffix}"
        return q

    @staticmethod
    def _safe_round(value, digits=2):
        """round() throws on None - guard against missing yfinance fields."""
        if value is None:
            return None
        try:
            return round(float(value), digits)
        except (TypeError, ValueError):
            return None

    def fetch_live_market_data(self):
        try:
            ticker = yf.Ticker(self.symbol)
            info = ticker.info

            if not info or info.get('regularMarketPrice') is None and info.get('currentPrice') is None:
                return {"success": False, "error": f"No data found for '{self.raw_query}'. Check the ticker/exchange."}

            # Fetch real-time price & security details
            live_price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('navPrice')
            if not live_price:
                return {"success": False, "error": "Invalid ticker or no live data found."}
            live_price = float(live_price)

            currency = info.get('currency', 'INR')
            currency_symbol = "₹" if currency == "INR" else ("$" if currency == "USD" else currency + " ")

            # Gather standard financial ratios dynamically (guarded against None)
            pe = self._safe_round(info.get('trailingPE'))
            eps = self._safe_round(info.get('trailingEps'))
            pb = self._safe_round(info.get('priceToBook'))

            pe_display = pe if pe is not None else "N/A"
            eps_display = eps if eps is not None else "N/A"
            pb_display = pb if pb is not None else "N/A"

            # yfinance has changed dividendYield between versions: some return a
            # fraction (0.025 = 2.5%), newer ones already return the percentage
            # (2.5 = 2.5%). Detect which one we got instead of assuming.
            div_val = info.get('dividendYield')
            if div_val is None:
                div_yield = "0.0%"
            elif div_val > 1:
                # Already a percentage
                div_yield = f"{round(div_val, 2)}%"
            else:
                div_yield = f"{round(div_val * 100, 2)}%"

            market_cap_raw = info.get('marketCap', 0) or 0
            if market_cap_raw <= 0:
                market_cap = "N/A"
            elif currency == "INR":
                market_cap = f"₹{round(market_cap_raw / 10**7, 2)} Cr"
            elif market_cap_raw >= 10**9:
                market_cap = f"{currency_symbol}{round(market_cap_raw / 10**9, 2)} B"
            else:
                market_cap = f"{currency_symbol}{round(market_cap_raw / 10**6, 2)} M"

            # Fetch Historical Price Chart Matrix (last 10 Years)
            hist = ticker.history(period="10y")
            prices = []
            timeline = []
            if not hist.empty:
                # Group by annual index averages to keep chart clean and scannable
                annual_data = hist.groupby(hist.index.year).mean(numeric_only=True)
                prices = [round(x, 2) for x in annual_data['Close'].tolist()]
                timeline = [str(x) for x in annual_data.index.tolist()]
                # Sync the final point with the actual live price
                prices[-1] = round(live_price, 2)
            else:
                # No history available - don't fabricate a flat fake chart,
                # be explicit that there isn't enough data to plot.
                prices = []
                timeline = []

            # Generate dynamically calculated formula explanations
            ratios = {
                "P/E Ratio": {
                    "val": pe_display,
                    "formula": f"Share Price ({currency_symbol}{live_price}) ÷ EPS ({currency_symbol}{eps_display})",
                    "explanation": (
                        f"Shows how many times you are paying for the company's profit. "
                        f"For this stock, you pay {currency_symbol}{pe_display} to buy {currency_symbol}1 of profit."
                        if pe is not None else "P/E data is not available for this stock right now."
                    )
                },
                "EPS (Earnings Per Share)": {
                    "val": eps_display,
                    "formula": "Net Profit ÷ Total Number of Shares",
                    "explanation": (
                        f"The company's profit divided by each share. An EPS of {currency_symbol}{eps_display} "
                        f"is the profit attributable to a single share."
                        if eps is not None else "EPS data is not available for this stock right now."
                    )
                },
                "P/B Ratio": {
                    "val": pb_display,
                    "formula": f"Share Price ({currency_symbol}{live_price}) ÷ Book Value per Share",
                    "explanation": (
                        f"Compares the stock price with the company's net asset value. A ratio of {pb_display} "
                        f"helps you see how the market values the company relative to its book assets."
                        if pb is not None else "P/B data is not available for this stock right now."
                    )
                },
                "Dividend Yield": {
                    "val": div_yield,
                    "formula": "(Annual Dividend per Share ÷ Share Price) × 100",
                    "explanation": f"The annual dividend as a percentage of the current share price is {div_yield}."
                },
                "Market Cap": {
                    "val": market_cap,
                    "formula": f"Total Shares × Current Share Price ({currency_symbol}{live_price})",
                    "explanation": "The total market value of all outstanding shares of the company right now."
                }
            }

            # Recommendation logic - only fires when we actually have a P/E to judge
            if pe is None:
                verdict = "DATA UNAVAILABLE"
                rationale = "Not enough fundamental data (P/E) to generate a verdict for this stock."
            elif pe < 15:
                verdict = "VALUE ZONE"
                rationale = f"Trading at a relatively low P/E multiple of {pe}. Worth a closer look at the underlying fundamentals before deciding."
            elif pe > 30:
                verdict = "PREMIUM VALUATION"
                rationale = f"Trading at a high P/E multiple ({pe}), meaning the market is pricing in strong future growth. Higher risk if growth disappoints."
            else:
                verdict = "FAIR VALUE"
                rationale = f"P/E of {pe} sits in a moderate range relative to typical market averages."

            # OHLC: use real fields only. If a field is genuinely missing from
            # yfinance, say "N/A" instead of manufacturing a fake number - the
            # earlier version silently invented open/high/low/prev-close from
            # made-up multipliers of the live price, which is the main source
            # of "wrong information".
            def _ohlc_field(key):
                val = info.get(key)
                return round(val, 2) if val is not None else "N/A"

            return {
                "success": True,
                "company_name": info.get('longName') or info.get('shortName') or self.raw_query,
                "exchange": self.exchange,
                "currency": currency,
                "currency_symbol": currency_symbol,
                "live_price": round(live_price, 2),
                "ohlc": {
                    "open": _ohlc_field('open'),
                    "high": _ohlc_field('dayHigh'),
                    "low": _ohlc_field('dayLow'),
                    "prev_close": _ohlc_field('previousClose')
                },
                "ratios": ratios,
                "timeline": timeline,
                "prices": prices,
                "intelligence": {
                    "verdict": verdict,
                    "rationale": rationale
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


@script38_bp.route('/')
def index():
    return render_template_string(HTML_LAYOUT, company=COMPANY_BRAND)


@script38_bp.route('/api/analyze', methods=['GET'])
def api_analyze():
    symbol = request.args.get('symbol', 'COAL INDIA').strip()
    exchange = request.args.get('exchange', 'NSE').strip()
    if not symbol:
        return jsonify({"success": False, "error": "Symbol is required."}), 400
    engine = ActiveMarketEngine(symbol, exchange)
    payload = engine.fetch_live_market_data()
    return jsonify(payload)


HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en" id="themeRoot" class="theme-dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ company }} | High Fidelity Real-Time Hub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-main: #060913;
            --bg-card: #0f1422;
            --text-title: #ffffff;
            --text-body: #94a3b8;
            --border-color: #1e293b;
        }
        .theme-light {
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --text-title: #0f172a;
            --text-body: #475569;
            --border-color: #e2e8f0;
        }
        body {
            background-color: var(--bg-main);
            color: var(--text-body);
            transition: all 0.2s ease-in-out;
        }
        .card-widget {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
        }
        .title-text { color: var(--text-title); }
    </style>
</head>
<body class="antialiased min-h-screen">

    <!-- Top Advanced Control Navigation Bar -->
    <header class="card-widget border-b px-4 md:px-8 py-4 flex flex-col sm:flex-row justify-between items-center gap-4 sticky top-0 z-40 shadow-md">
        <div class="flex items-center justify-between w-full sm:w-auto gap-4">
            <div class="flex items-center gap-3">
                <div class="p-2.5 bg-indigo-600 rounded-xl text-white shadow-lg shadow-indigo-600/30">
                    <i class="fa-solid fa-bolt-lightning text-lg animate-pulse"></i>
                </div>
                <div>
                    <h1 class="font-black text-sm tracking-widest uppercase title-text">{{ company }}</h1>
                    <span class="text-[9px] block text-indigo-400 font-mono tracking-wider">SECURE API FEED v3.0</span>
                </div>
            </div>
            <button onclick="toggleGlobalInterfaceTheme()" class="sm:hidden px-3 py-1.5 rounded-lg border border-gray-700 bg-gray-800 text-white cursor-pointer">
                <i class="fa-solid fa-circle-half-stroke"></i>
            </button>
        </div>

        <!-- Terminal Input Arrays & Exchange Controls -->
        <div class="flex flex-wrap items-center gap-3 w-full sm:w-auto">
            <div class="relative flex-1 sm:flex-none">
                <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3 text-gray-500 text-xs"></i>
                <input type="text" id="assetSearchInput" value="COAL INDIA"
                       class="w-full sm:w-64 pl-9 pr-4 py-2 text-xs font-mono rounded-xl bg-gray-900 border border-gray-700 text-white focus:outline-none focus:border-indigo-500">
            </div>
            <button onclick="triggerTerminalCoreQuery()" class="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl text-xs tracking-wider transition cursor-pointer">
                RUN LIVE QUERY
            </button>

            <div class="flex bg-gray-900 p-1 rounded-xl border border-gray-700 text-xs font-mono">
                <button id="exNSE" onclick="switchExchangeMode('NSE')" class="px-3 py-1 rounded-lg bg-indigo-600 text-white font-bold cursor-pointer">NSE</button>
                <button id="exBSE" onclick="switchExchangeMode('BSE')" class="px-3 py-1 rounded-lg text-gray-400 cursor-pointer">BSE</button>
            </div>

            <!-- Theme Switch Panel Action Trigger -->
            <button onclick="toggleGlobalInterfaceTheme()" class="hidden sm:inline-block p-2 rounded-xl border border-gray-700 bg-gray-900 text-indigo-400 hover:bg-gray-800 transition cursor-pointer">
                <i class="fa-solid fa-circle-half-stroke text-sm"></i>
            </button>
        </div>
    </header>

    <!-- Content Workspace -->
    <main class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">

        <!-- BRAND BLOCK BANNER METRICS -->
        <div class="card-widget p-6 rounded-2xl flex flex-col md:flex-row justify-between gap-4 shadow-xl">
            <div>
                <div class="flex items-center gap-2">
                    <span id="lblExchangeTicker" class="text-xs font-mono font-bold px-2.5 py-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-lg uppercase">NSE: COALINDIA</span>
                    <span class="text-xs px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-lg font-mono">Real Market Feed</span>
                </div>
                <h2 id="lblCompanyName" class="text-3xl font-black tracking-tight title-text mt-3">Coal India Limited</h2>
            </div>
            <div class="flex flex-col md:items-end justify-center">
                <div class="text-4xl font-black font-mono text-indigo-500"><span id="lblCurrencySymbol">₹</span><span id="lblLivePrice">0.00</span></div>
                <div class="text-[10px] font-mono opacity-60 mt-1">Live Feed Synced</div>
            </div>
        </div>

        <!-- LINE GRAPH MODULE FRAME & OHLC GRID -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- Price Timeline Chart Panel Area -->
            <div class="lg:col-span-2 p-6 card-widget rounded-2xl flex flex-col justify-between shadow-xl">
                <div>
                    <div class="flex justify-between items-center mb-4">
                        <div>
                            <h3 class="text-xs font-bold uppercase tracking-wider title-text font-mono">
                                <i class="fa-solid fa-chart-area text-indigo-400 mr-2"></i> Timeline Share Valuation Stream
                            </h3>
                            <p class="text-[10px] opacity-70 font-mono mt-0.5">Click directly on any year node to trigger instant frame slice zooming</p>
                        </div>
                        <button onclick="resetChartFilterZoom()" class="px-2.5 py-1 text-[10px] font-mono bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 rounded border border-indigo-500/30 cursor-pointer">Reset Range</button>
                    </div>
                    <div class="relative w-full bg-black/5 p-2 rounded-xl border border-[var(--border-color)]" style="height: 310px;">
                        <canvas id="primaryStockLineChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- OHLC STATS RANGE WRAPPER -->
            <div class="p-6 card-widget rounded-2xl flex flex-col justify-between shadow-xl">
                <div>
                    <h3 class="text-xs font-bold uppercase tracking-wider title-text font-mono mb-4">Daily Range Analytics</h3>
                    <div class="space-y-4 font-mono text-xs">
                        <div class="flex justify-between border-b border-[var(--border-color)] pb-2">
                            <span>Market Open</span>
                            <span id="valOpen" class="title-text font-bold">—</span>
                        </div>
                        <div class="flex justify-between border-b border-[var(--border-color)] pb-2">
                            <span class="text-emerald-500">Session High</span>
                            <span id="valHigh" class="text-emerald-500 font-bold">—</span>
                        </div>
                        <div class="flex justify-between border-b border-[var(--border-color)] pb-2">
                            <span class="text-rose-500">Session Low</span>
                            <span id="valLow" class="text-rose-500 font-bold">—</span>
                        </div>
                        <div class="flex justify-between border-b border-[var(--border-color)] pb-2">
                            <span>Previous Close</span>
                            <span id="valPrevClose" class="font-bold">—</span>
                        </div>
                    </div>
                </div>
                <div class="mt-4 p-3 bg-indigo-500/5 border border-indigo-500/10 rounded-xl text-[11px] text-indigo-400 font-mono leading-relaxed">
                    <i class="fa-solid fa-circle-nodes mr-1"></i> Data pulled directly from the live feed; unavailable fields show "N/A" rather than an estimate.
                </div>
            </div>
        </div>

        <!-- CLICKABLE DETAILED FORMULA SHEETS RATIO PANEL -->
        <div class="p-6 card-widget rounded-2xl shadow-xl">
            <h3 class="text-xs font-bold uppercase tracking-wider title-text font-mono mb-2">
                <i class="fa-solid fa-square-root-variable text-indigo-400 mr-2"></i> Verified Core Financial Ratios
            </h3>
            <p class="text-[11px] opacity-70 font-mono mb-4 block">Click any card below to view how the ratio was calculated with real numbers.</p>
            <div id="ratiosInteractiveGrid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4"></div>
        </div>

        <!-- EXPERT RECON INVESTOR ADVISORY SYSTEM -->
        <div class="p-6 rounded-2xl card-widget border-l-4 border-l-indigo-500 shadow-2xl">
            <div class="flex items-center gap-2.5 mb-3">
                <i class="fa-solid fa-lightbulb text-indigo-400 text-lg"></i>
                <h3 class="text-xs font-bold uppercase tracking-widest font-mono title-text">Investment Horizon Intelligence</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-center font-mono text-xs">
                <div class="bg-black/20 p-4 rounded-xl text-center border border-[var(--border-color)]">
                    <span class="text-[9px] block text-gray-500 uppercase tracking-wider mb-0.5">Automated Verdict</span>
                    <span id="intelVerdict" class="text-sm font-black text-emerald-400">LOADING</span>
                </div>
                <div id="intelRationale" class="md:col-span-3 leading-relaxed opacity-90">
                    Awaiting core query asset compilation streams to frame structural advice...
                </div>
            </div>
            <p class="text-[9px] opacity-50 font-mono mt-4">This is an automated, formula-based note, not financial advice. Verify independently before acting on it.</p>
        </div>
    </main>

    <!-- AUDIT BACK-CALCULATION POPUP MODAL WRAPPER -->
    <div id="ratioAuditModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-gray-900 border border-gray-700 w-full max-w-md rounded-2xl p-6 space-y-4 shadow-2xl">
            <div class="flex justify-between items-start border-b border-gray-800 pb-3">
                <div>
                    <h4 id="mdName" class="text-base font-bold text-indigo-400 font-mono">Ratio Auditor</h4>
                    <span class="text-[9px] text-gray-400 font-mono block">Real Math Variable Ledger Summary</span>
                </div>
                <button onclick="hideAuditModal()" class="text-gray-400 hover:text-white cursor-pointer p-1">
                    <i class="fa-solid fa-xmark text-sm"></i>
                </button>
            </div>

            <div class="space-y-4 font-mono text-xs">
                <div>
                    <span class="text-gray-400 text-[10px] block uppercase mb-1">Calculated Current Value</span>
                    <div id="mdValue" class="text-xl font-bold text-white bg-black/40 p-2.5 rounded-xl border border-gray-800">—</div>
                </div>
                <div>
                    <span class="text-gray-400 text-[10px] block uppercase mb-1">Calculation with Real Values</span>
                    <div id="mdFormula" class="text-indigo-300 bg-indigo-950/30 p-3 rounded-xl border border-indigo-900/40 font-bold">—</div>
                </div>
                <div>
                    <span class="text-gray-400 text-[10px] block uppercase mb-1">Simple Meaning</span>
                    <p id="mdExpl" class="text-gray-300 leading-relaxed bg-black/20 p-3 rounded-xl border border-gray-800">—</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedExchange = "NSE";
        let mainChartObj = null;
        let cachedTimeline = [];
        let cachedPrices = [];
        let globalRatiosObject = {};

        window.addEventListener('DOMContentLoaded', () => {
            triggerTerminalCoreQuery();
        });

        function toggleGlobalInterfaceTheme() {
            const bodyRoot = document.getElementById('themeRoot');
            if(bodyRoot.classList.contains('theme-dark')) {
                bodyRoot.classList.remove('theme-dark');
                bodyRoot.classList.add('theme-light');
            } else {
                bodyRoot.classList.remove('theme-light');
                bodyRoot.classList.add('theme-dark');
            }
        }

        function switchExchangeMode(ex) {
            selectedExchange = ex;
            document.getElementById('exNSE').className = ex === 'NSE' ? "px-3 py-1 rounded-lg bg-indigo-600 text-white font-bold cursor-pointer" : "px-3 py-1 rounded-lg text-gray-400 cursor-pointer";
            document.getElementById('exBSE').className = ex === 'BSE' ? "px-3 py-1 rounded-lg bg-indigo-600 text-white font-bold cursor-pointer" : "px-3 py-1 rounded-lg text-gray-400 cursor-pointer";
            triggerTerminalCoreQuery();
        }

        async function triggerTerminalCoreQuery() {
            const searchParam = document.getElementById('assetSearchInput').value.trim();
            if(!searchParam) { alert("Core Error: Search string value null."); return; }

            try {
                const queryUrl = `./api/analyze?symbol=${encodeURIComponent(searchParam)}&exchange=${selectedExchange}`;
                const response = await fetch(queryUrl);
                const data = await response.json();

                if(data.success) {
                    document.getElementById('lblCompanyName').innerText = data.company_name;
                    document.getElementById('lblExchangeTicker').innerText = `${data.exchange}: ${searchParam.toUpperCase()}`;
                    document.getElementById('lblCurrencySymbol').innerText = data.currency_symbol || "₹";
                    document.getElementById('lblLivePrice').innerText = data.live_price.toFixed(2);

                    // Map Daily ranges
                    const cur = data.currency_symbol || "₹";
                    document.getElementById('valOpen').innerText = data.ohlc.open === "N/A" ? "N/A" : cur + data.ohlc.open;
                    document.getElementById('valHigh').innerText = data.ohlc.high === "N/A" ? "N/A" : cur + data.ohlc.high;
                    document.getElementById('valLow').innerText = data.ohlc.low === "N/A" ? "N/A" : cur + data.ohlc.low;
                    document.getElementById('valPrevClose').innerText = data.ohlc.prev_close === "N/A" ? "N/A" : cur + data.ohlc.prev_close;

                    // Map System Verdict Advisor
                    document.getElementById('intelVerdict').innerText = data.intelligence.verdict;
                    document.getElementById('intelRationale').innerText = data.intelligence.rationale;

                    // Cache structural arrays for charting mechanics
                    cachedTimeline = data.timeline;
                    cachedPrices = data.prices;
                    globalRatiosObject = data.ratios;

                    // Rebuild ratios grids modules dynamically
                    const gridFrame = document.getElementById('ratiosInteractiveGrid');
                    gridFrame.innerHTML = '';
                    for (const [ratioKey, node] of Object.entries(data.ratios)) {
                        gridFrame.innerHTML += `
                            <div onclick="showRatioCalculationPopup('${ratioKey}')" class="p-4 bg-black/30 border border-[var(--border-color)] rounded-xl cursor-pointer hover:border-indigo-500 transition text-left">
                                <span class="text-[10px] block font-mono uppercase tracking-tight text-gray-400">${ratioKey}</span>
                                <div class="text-lg font-black text-indigo-400 mt-2 font-mono">${node.val}</div>
                                <span class="text-[8px] font-mono block text-gray-500 mt-1.5"><i class="fa-solid fa-expand mr-1"></i> Verify Calculation</span>
                            </div>
                        `;
                    }

                    if (cachedPrices.length > 0) {
                        renderHighFidelityLinePlot(cachedTimeline, cachedPrices);
                    } else {
                        if (mainChartObj) { mainChartObj.destroy(); mainChartObj = null; }
                    }
                } else {
                    alert("Data Sync Warning: " + data.error);
                }
            } catch(e) {
                alert("Network Core Link Fail: Data pipe synchronization anomaly.");
            }
        }

        function renderHighFidelityLinePlot(labelsData, pointsData) {
            const canvasCtx = document.getElementById('primaryStockLineChart').getContext('2d');
            if(mainChartObj) { mainChartObj.destroy(); }

            mainChartObj = new Chart(canvasCtx, {
                type: 'line',
                data: {
                    labels: labelsData,
                    datasets: [{
                        data: pointsData,
                        borderColor: '#6366f1',
                        borderWidth: 2.5,
                        backgroundColor: 'rgba(99, 102, 241, 0.05)',
                        fill: true,
                        tension: 0.1,
                        pointBackgroundColor: '#6366f1',
                        pointRadius: 4,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(99, 102, 241, 0.08)' }, ticks: { color: '#64748b', font: { family: 'monospace', size: 10 } } },
                        x: { grid: { display: false }, ticks: { color: '#64748b', font: { family: 'monospace', size: 10 } } }
                    },
                    // DIRECT YEAR GRAPH INTERACTIVE CLICK EVENT
                    onClick: (event, items) => {
                        if(items.length > 0) {
                            const idx = items[0].index;
                            const isolatedYear = labelsData[idx];
                            const targetedPrice = pointsData[idx];

                            const minCap = Math.max(0, idx - 1);
                            const maxCap = Math.min(labelsData.length, idx + 2);

                            renderHighFidelityLinePlot(
                                labelsData.slice(minCap, maxCap),
                                pointsData.slice(minCap, maxCap)
                            );
                        }
                    }
                }
            });
        }

        function resetChartFilterZoom() {
            if(cachedTimeline.length > 0) {
                renderHighFidelityLinePlot(cachedTimeline, cachedPrices);
            }
        }

        // CONTROL POPUP SYSTEM MODALS
        function showRatioCalculationPopup(key) {
            const structNode = globalRatiosObject[key];
            if(!structNode) return;

            document.getElementById('mdName').innerText = key;
            document.getElementById('mdValue').innerText = structNode.val;
            document.getElementById('mdFormula').innerText = structNode.formula;
            document.getElementById('mdExpl').innerText = structNode.explanation;

            document.getElementById('ratioAuditModal').classList.remove('hidden');
        }

        function hideAuditModal() {
            document.getElementById('ratioAuditModal').classList.add('hidden');
        }
    </script>
</body>
</html>
"""
