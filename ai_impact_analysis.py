import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time

# Configuration
DATA_FILE   = os.path.expanduser("~/Downloads/ai_sector_daily.csv")
OUTPUT_DIR  = os.path.expanduser("~/Downloads/Aktienmarkt_Analyse")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styles
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({'figure.figsize': (14, 7), 'font.size': 12, 'figure.dpi': 150})

print("=" * 60)
print("AI BOOM & BUBBLE EMPIRICAL ANALYSIS")
print("=" * 60)

start_time = time.time()
df = pd.read_csv(DATA_FILE, parse_dates=['Date'])

# Pivot table: Date as index, Symbols as columns, Close prices as values
df_close = df.pivot(index='Date', columns='Symbol', values='Close')
df_close.sort_index(inplace=True)
df_close.ffill(inplace=True)

# Daily and Cumulative Returns
daily_returns = df_close.pct_change().dropna()
cum_returns = (1 + daily_returns).cumprod() * 100

# Rolling 60-day correlation with NVDA
rolling_corr_nvda = daily_returns.rolling(window=60).corr(daily_returns['NVDA'])

# Helper for saving figures
def save_chart(name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    plt.savefig(path, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"📊 Saved: {name}.png")

report_lines = []
report_lines.append("======================================================")
report_lines.append("EMPIRISCHER BERICHT: KI-BOOM & INFRASTRUKTUR-BOTTLENECKS")
report_lines.append("Zeitraum: 2020-01-01 bis heute (Inkl. ChatGPT Launch)")
report_lines.append("======================================================\n")

# --- Performance Metrics ---
ann_returns = (daily_returns.mean() * 252) * 100
ann_vol = (daily_returns.std() * np.sqrt(252)) * 100

report_lines.append("1. GESAMTPERFORMANCE (Annualisiert)")
report_lines.append("-" * 40)
for sym in ann_returns.sort_values(ascending=False).index:
    report_lines.append(f"{sym:>6}: Rendite {ann_returns[sym]:>6.1f}% p.a. | Volatilität {ann_vol[sym]:>5.1f}% p.a.")
report_lines.append("\n")

# =========================================================================
# HYPOTHESIS 1: POWER & UTILITIES SPILLOVER
# =========================================================================
power_tickers = ['CEG', 'VST', 'NEE', 'D', 'GE', 'NVDA']
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
cum_returns[power_tickers].plot(ax=ax1, lw=2)
ax1.set_title("Hypothese 1: Stromversorger & Netz-Infrastruktur vs. NVDA (Kumulierte Rendite)", fontweight='bold')
ax1.set_ylabel("Index (100 = Jan 2020)")
ax1.set_yscale('log') # Log scale is better for exponential growth
ax1.axvline(pd.to_datetime('2022-11-30'), color='red', linestyle='--', label='ChatGPT Launch', lw=2)
ax1.legend()

rolling_corr_nvda[['CEG', 'VST', 'GE']].plot(ax=ax2, lw=2)
ax2.set_title("Rollierende 60-Tage Korrelation mit NVDA (CEG, VST, GE)", fontweight='bold')
ax2.set_ylabel("Korrelation (r)")
ax2.axhline(0, color='black', lw=1, ls='--')
save_chart("ai_power_utilities_spillover")

# =========================================================================
# HYPOTHESIS 1B: COOLING & GRID INFRASTRUCTURE
# =========================================================================
cooling_tickers = ['VRT', 'ETN', 'NVDA']
plt.figure(figsize=(14, 7))
cum_returns[cooling_tickers].plot(lw=2)
plt.title("Hypothese 1b: Rechenzentrum-Kühlung (VRT) & Grid (ETN) vs. NVDA", fontweight='bold')
plt.ylabel("Index (100 = Jan 2020)")
plt.yscale('log')
plt.axvline(pd.to_datetime('2022-11-30'), color='red', linestyle='--', label='ChatGPT Launch', lw=2)
plt.legend()
save_chart("ai_cooling_grid_infrastructure")

# =========================================================================
# HYPOTHESIS 2: HARDWARE SUPPLY CHAIN (HBM, Networking, Lithography)
# =========================================================================
hw_tickers = ['MU', 'AVGO', 'ASML', 'TSM', 'NVDA']
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
cum_returns[hw_tickers].plot(ax=ax1, lw=2)
ax1.set_title("Hypothese 2: Hardware Bottleneck Co-dependency (Kumulierte Rendite)", fontweight='bold')
ax1.set_ylabel("Index (100 = Jan 2020)")
ax1.set_yscale('log')
ax1.axvline(pd.to_datetime('2022-11-30'), color='red', linestyle='--', label='ChatGPT Launch', lw=2)
ax1.legend()

rolling_corr_nvda[['MU', 'AVGO', 'ASML', 'TSM']].plot(ax=ax2, lw=2)
ax2.set_title("Rollierende 60-Tage Korrelation mit NVDA", fontweight='bold')
ax2.set_ylabel("Korrelation (r)")
ax2.axhline(0, color='black', lw=1, ls='--')
save_chart("ai_hardware_supply_chain")

# =========================================================================
# HYPOTHESIS 3: BUBBLE VS STRUCTURAL (SMCI & PLTR vs NVDA & MSFT)
# =========================================================================
bubble_tickers = ['SMCI', 'PLTR', 'NVDA', 'MSFT']
plt.figure(figsize=(14, 7))
cum_returns[bubble_tickers].plot(lw=2)
plt.title("Hypothese 3: Spekulationsblase vs. Strukturelle Gewinner", fontweight='bold')
plt.ylabel("Index (100 = Jan 2020)")
plt.yscale('log')
plt.axvline(pd.to_datetime('2022-11-30'), color='red', linestyle='--', label='ChatGPT Launch', lw=2)
plt.legend()
save_chart("ai_bubble_vs_structural")

# Drawdown Analysis
rolling_max = df_close.cummax()
drawdowns = (df_close - rolling_max) / rolling_max * 100
max_drawdowns = drawdowns.min()

report_lines.append("2. DRAWDOWN ANALYSE (Maximum seit Jan 2020)")
report_lines.append("-" * 40)
for sym in max_drawdowns.sort_values().index:
    report_lines.append(f"{sym:>6}: {max_drawdowns[sym]:>6.1f}%")
report_lines.append("\n")

# Volatility Regimes (60-day annualized rolling)
rolling_vol = daily_returns.rolling(window=60).std() * np.sqrt(252) * 100
report_lines.append("3. SPITZEN-VOLATILITÄT (Höchste rollierende 60-Tage Volatilität)")
report_lines.append("-" * 40)
max_rolling_vol = rolling_vol.max()
for sym in max_rolling_vol.sort_values(ascending=False).index:
    report_lines.append(f"{sym:>6}: {max_rolling_vol[sym]:>6.1f}% p.a.")
report_lines.append("\n")

# Average Correlation with NVDA
avg_corr = daily_returns.corr()['NVDA'].drop('NVDA')
report_lines.append("4. KORRELATION MIT NVDA (Gesamtzeitraum)")
report_lines.append("-" * 40)
for sym in avg_corr.sort_values(ascending=False).index:
    report_lines.append(f"{sym:>6}: {avg_corr[sym]:>5.3f}")
report_lines.append("\n")

report_path = os.path.join(OUTPUT_DIR, "AI_Boom_Bubble_Empirischer_Bericht.txt")
with open(report_path, "w") as f:
    f.write("\n".join(report_lines))
print(f"📄 Saved Text Report: {report_path}")

print(f"\n✅ Analysis complete in {time.time() - start_time:.2f} seconds!")
