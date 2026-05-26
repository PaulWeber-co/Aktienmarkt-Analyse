"""
Vorverarbeitungs-Script: Aktienmarkt-Datensatz
Kaggle: All Stock Market Data (Daily Updates) – 44 Mio. Zeilen, 3,54 GB

Dieses Script reduziert den Datensatz mit DuckDB auf ca. 150-200 MB
(Wochenaggregation mit Metriken) – direkt importierbar in Power BI.

Datensatzstruktur:
    archive/A/AAPL.csv, archive/B/BA.csv, etc.
    Spalten: high, close, open, volume, low, timestamp (Unix-Timestamp)
    Kein Symbol in den Dateien – Dateiname = Symbol

Voraussetzungen:
    pip install duckdb pandas

Nutzung:
    1. Kaggle-Datensatz herunterladen und entpacken nach ~/Downloads/archive
    2. python preprocess_stocks.py
    3. Output: stocks_weekly_powerbi.csv -> in Power BI laden
"""

import duckdb
import pandas as pd
from pathlib import Path
import time
import os
import glob

# ============================================================
# KONFIGURATION
# ============================================================
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
ARCHIVE_DIR  = os.path.join(DOWNLOAD_DIR, "archive")
OUTPUT_FILE  = os.path.join(DOWNLOAD_DIR, "stocks_weekly_powerbi.csv")

# Prüfe ob der Datensatz vorhanden ist
if not os.path.isdir(ARCHIVE_DIR):
    print(f"FEHLER: Ordner '{ARCHIVE_DIR}' nicht gefunden!")
    print("Bitte den Kaggle-Datensatz herunterladen und entpacken.")
    exit(1)

# Finde alle CSV-Dateien
csv_pattern = os.path.join(ARCHIVE_DIR, "*", "*.csv")
csv_files = glob.glob(csv_pattern)
print(f"Gefundene CSV-Dateien: {len(csv_files):,}")

if len(csv_files) < 10:
    print("FEHLER: Zu wenige CSV-Dateien gefunden!")
    exit(1)

# ============================================================
# 1. DuckDB-Verbindung
# ============================================================
print("\nVerbinde DuckDB ...")
con = duckdb.connect()

# Speicher-Konfiguration für große Datensätze
con.execute("SET memory_limit = '4GB'")
con.execute("SET threads = 4")

# ============================================================
# 2. Alle CSVs einlesen mit Dateinamen als Symbol
# ============================================================
print(f"\nLese alle CSV-Dateien aus {ARCHIVE_DIR} ...")
start_load = time.time()

# DuckDB kann mit read_csv_auto und filename Parameter arbeiten
# Die CSVs haben: high, close, open, volume, low, timestamp
con.execute(f"""
    CREATE VIEW raw_stocks AS
        SELECT
            -- Symbol aus dem Dateinamen extrahieren (z.B. "/archive/A/AAPL.csv" → "AAPL")
            regexp_extract(filename, '/([^/]+)\\.csv$', 1) AS Symbol,
            -- Unix-Timestamp in Datum konvertieren
            CAST(to_timestamp(CAST(timestamp AS BIGINT)) AS DATE) AS Date,
            CAST(open AS DOUBLE) AS Open,
            CAST(high AS DOUBLE) AS High,
            CAST(low AS DOUBLE) AS Low,
            CAST(close AS DOUBLE) AS Close,
            CAST(volume AS BIGINT) AS Volume
        FROM read_csv_auto(
            '{csv_pattern}',
            header       = True,
            ignore_errors= True,
            filename     = True
        )
""")

# Stichprobe zur Qualitätsprüfung
sample = con.execute("SELECT * FROM raw_stocks LIMIT 5").df()
print(f"\nLaden abgeschlossen in {time.time() - start_load:.1f}s")
print("\n--- Stichprobe ---")
print(sample.to_string())
total = con.execute("SELECT COUNT(*) FROM raw_stocks").fetchone()[0]
print(f"\nGesamtzeilen in Rohdaten: {total:,}")

# ============================================================
# 3. Datenqualität: Basisfilter
# ============================================================
print("\nWende Datenqualitätsfilter an ...")
con.execute("""
    CREATE VIEW cleaned AS
        SELECT *
        FROM raw_stocks
        WHERE Close  > 0
          AND Open   > 0
          AND High  >= Low
          AND Volume  > 0
          AND Date   IS NOT NULL
          AND Symbol IS NOT NULL
          AND Symbol != ''
""")
clean_count = con.execute("SELECT COUNT(*) FROM cleaned").fetchone()[0]
print(f"Zeilen nach Filterung: {clean_count:,} "
      f"(entfernt: {total - clean_count:,})")

# ============================================================
# 4. Tagesrendite berechnen (Basis für Volatilität)
# ============================================================
print("\nBerechne Tagesrenditen ...")
con.execute("""
    CREATE VIEW with_returns AS
        SELECT *,
            (Close - LAG(Close) OVER (
                PARTITION BY Symbol ORDER BY Date)
            ) / NULLIF(LAG(Close) OVER (
                PARTITION BY Symbol ORDER BY Date), 0) AS Return_Daily
        FROM cleaned
""")

# ============================================================
# 5. Aggregation auf WOCHENEBENE (Ziel: ~150 MB+)
# ============================================================
print("\nAggregiere auf Wochenebene ...")
start = time.time()

df_weekly = con.execute("""
    SELECT
        Symbol,
        -- Wochenstart (Montag) als Referenzdatum
        DATE_TRUNC('week', Date)                 AS Week_Start,
        YEAR(Date)                               AS Year,
        MONTH(Date)                              AS Month,
        WEEKOFYEAR(Date)                         AS WeekNum,
        -- OHLC-Daten der Woche
        FIRST(Open ORDER BY Date)                AS Open_BOW,
        LAST(Close ORDER BY Date)                AS Close_EOW,
        MAX(High)                                AS High_Week,
        MIN(Low)                                 AS Low_Week,
        AVG(Close)                               AS Close_Avg,
        -- Volumen
        SUM(Volume)                              AS Volume_Total,
        AVG(Volume)                              AS Volume_Avg,
        -- Wöchentliche Rendite (EOW zu BOW)
        (LAST(Close ORDER BY Date) / NULLIF(FIRST(Open ORDER BY Date), 0)) - 1  AS Return_Weekly,
        -- Wöchentliche Volatilität (Std. der Tagesrenditen × √5)
        STDDEV(Return_Daily) * SQRT(5)           AS Vol_Weekly,
        -- Annualisierte Volatilität
        STDDEV(Return_Daily) * SQRT(252)         AS Vol_Annual,
        -- Anzahl Handelstage in der Woche
        COUNT(*)                                 AS TradingDays,
        -- Max Tagesverlust (Worst Day)
        MIN(Return_Daily)                        AS Return_WorstDay,
        -- Max Tagesgewinn (Best Day)
        MAX(Return_Daily)                        AS Return_BestDay

    FROM with_returns
    WHERE Return_Daily IS NOT NULL
    GROUP BY Symbol, DATE_TRUNC('week', Date),
             YEAR(Date), MONTH(Date), WEEKOFYEAR(Date)
    ORDER BY Symbol, Week_Start
""").df()

elapsed = time.time() - start
print(f"Aggregation abgeschlossen in {elapsed:.1f}s – {len(df_weekly):,} Zeilen")

# ============================================================
# 6. Post-Processing in Pandas
# ============================================================
print("\nPost-Processing ...")

# Rundung für kleinere Dateigröße
for col in ["Return_Weekly", "Vol_Weekly", "Vol_Annual", "Return_WorstDay", "Return_BestDay"]:
    if col in df_weekly.columns:
        df_weekly[col] = df_weekly[col].round(6)

for col in ["Close_Avg", "Open_BOW", "Close_EOW", "High_Week", "Low_Week"]:
    if col in df_weekly.columns:
        df_weekly[col] = df_weekly[col].round(4)

df_weekly["Volume_Avg"] = df_weekly["Volume_Avg"].round(0)

# Plausibilitäts-Check: entferne extreme Ausreißer (> 500% Wochenrendite)
before = len(df_weekly)
df_weekly = df_weekly[
    (df_weekly["Return_Weekly"].abs() < 5.0) &
    (df_weekly["Vol_Weekly"]   < 5.0)
]
print(f"Ausreißer entfernt: {before - len(df_weekly):,} Zeilen")

# ============================================================
# 7. Größen-Check und ggf. Anpassung
# ============================================================
# Schätze die Dateigröße (~120 Bytes pro Zeile)
estimated_size_mb = len(df_weekly) * 120 / (1024**2)
print(f"\nGeschätzte Dateigröße (wöchentlich): {estimated_size_mb:.0f} MB")
print(f"Endgültige Zeilen:  {len(df_weekly):,}")
print(f"Eindeutige Ticker:  {df_weekly['Symbol'].nunique():,}")
print(f"Zeitraum:           {df_weekly['Week_Start'].min()} – {df_weekly['Week_Start'].max()}")
print(f"Spalten:            {list(df_weekly.columns)}")

# Falls wöchentlich zu wenig → tägliche Daten
if estimated_size_mb < 130:
    print("\n⚠️  Wöchentlich ergibt weniger als 130 MB. Wechsle zu täglichen Daten...")
    
    df_daily = con.execute("""
        SELECT
            Symbol,
            Date,
            YEAR(Date) AS Year,
            MONTH(Date) AS Month,
            ROUND(Open, 4) AS Open,
            ROUND(High, 4) AS High,
            ROUND(Low, 4) AS Low,
            ROUND(Close, 4) AS Close,
            Volume,
            ROUND(Return_Daily, 6) AS Return_Daily
        FROM with_returns
        WHERE Return_Daily IS NOT NULL
          AND Close > 0
          AND Volume > 0
        ORDER BY Symbol, Date
    """).df()
    
    before = len(df_daily)
    df_daily = df_daily[df_daily["Return_Daily"].abs() < 5.0]
    print(f"Ausreißer entfernt: {before - len(df_daily):,} Zeilen")
    
    daily_size_mb = len(df_daily) * 70 / (1024**2)
    print(f"Geschätzte Größe (täglich): {daily_size_mb:.0f} MB")
    
    # Falls tägliche Daten zu groß (> 600 MB), nur ab 2010
    if daily_size_mb > 600:
        print("Tägliche Daten sehr groß. Filtere auf ab 2010 ...")
        df_daily = df_daily[df_daily["Year"] >= 2010]
        daily_size_mb = len(df_daily) * 70 / (1024**2)
        print(f"Geschätzte Größe (ab 2010): {daily_size_mb:.0f} MB")
    
    print(f"\nEndgültige Zeilen:  {len(df_daily):,}")
    print(f"Eindeutige Ticker:  {df_daily['Symbol'].nunique():,}")
    
    OUTPUT_FILE = os.path.join(DOWNLOAD_DIR, "stocks_daily_powerbi.csv")
    print(f"\nExportiere nach '{OUTPUT_FILE}' ...")
    df_daily.to_csv(OUTPUT_FILE, index=False)
else:
    # Export der Wochendaten
    print(f"\nExportiere nach '{OUTPUT_FILE}' ...")
    df_weekly.to_csv(OUTPUT_FILE, index=False)

# ============================================================
# 8. Ergebnis
# ============================================================
size_mb = Path(OUTPUT_FILE).stat().st_size / (1024 ** 2)
print(f"\n{'='*60}")
print(f"✅ Fertig! Dateigröße: {size_mb:.1f} MB")
print(f"📁 Datei: {OUTPUT_FILE}")

if size_mb < 150:
    print(f"\n⚠️  Die Datei ist nur {size_mb:.1f} MB (Ziel: 150+ MB).")
elif size_mb > 500:
    print(f"\n⚠️  Die Datei ist {size_mb:.1f} MB (> 500 MB).")
    print("Für Power BI ggf. weitere Filterung nötig.")
else:
    print(f"\n✅ Dateigröße im Zielbereich: {size_mb:.1f} MB")

print(f"\n→ Nächster Schritt: Datei in Power BI Desktop importieren")
print("  Datenquelle: Datei -> Text/CSV -> Datei auswählen")
