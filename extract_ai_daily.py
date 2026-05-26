import duckdb
import os
from pathlib import Path
import time

# Configuration
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
ARCHIVE_DIR  = os.path.join(DOWNLOAD_DIR, "archive")
OUTPUT_FILE  = os.path.join(DOWNLOAD_DIR, "ai_sector_daily.csv")

AI_TICKERS = [
    'NVDA', 'MSFT', 'PLTR', 'TSM', 'ASML', 'AVGO', 'MU', 'SMCI', 
    'VRT', 'ETN', 'CEG', 'VST', 'D', 'NEE', 'GE'
]

print("=" * 60)
print("AI BOOM & BUBBLE - RAW DAILY DATA EXTRACTION")
print("=" * 60)

start_time = time.time()

# Gather the specific file paths for the tickers to avoid reading the whole 3.8GB
file_paths = []
missing = []
for ticker in AI_TICKERS:
    # Based on archive structure archive/A/AAPL.csv
    first_letter = ticker[0].upper()
    file_path = os.path.join(ARCHIVE_DIR, first_letter, f"{ticker}.csv")
    if os.path.exists(file_path):
        file_paths.append(file_path)
    else:
        # Fallback if structure is different
        pattern = os.path.join(ARCHIVE_DIR, "*", f"{ticker}.csv")
        import glob
        matches = glob.glob(pattern)
        if matches:
            file_paths.append(matches[0])
        else:
            missing.append(ticker)

if missing:
    print(f"WARNING: Could not find raw CSV files for: {missing}")

print(f"Found {len(file_paths)} raw CSV files for extraction.")

# Connect to DuckDB
con = duckdb.connect()
con.execute("SET memory_limit = '4GB'")

# Build a list of files formatted for DuckDB
files_list_str = "[" + ", ".join([f"'{f}'" for f in file_paths]) + "]"

print(f"\nExtracting daily data for dates >= 2022-11-30...")

# Execute extraction
query = f"""
    COPY (
        SELECT 
            regexp_extract(filename, '/([^/]+)\\.csv$', 1) AS Symbol,
            CAST(to_timestamp(CAST(timestamp AS BIGINT)) AS DATE) AS Date,
            CAST(open AS DOUBLE) AS Open,
            CAST(high AS DOUBLE) AS High,
            CAST(low AS DOUBLE) AS Low,
            CAST(close AS DOUBLE) AS Close,
            CAST(volume AS BIGINT) AS Volume
        FROM read_csv_auto({files_list_str}, header=True, ignore_errors=True, filename=True)
        WHERE CAST(to_timestamp(CAST(timestamp AS BIGINT)) AS DATE) >= DATE '2020-01-01'
        ORDER BY Symbol, Date
    ) TO '{OUTPUT_FILE}' (HEADER, DELIMITER ',');
"""

con.execute(query)

print(f"\n✅ Extraction complete in {time.time() - start_time:.2f} seconds!")
print(f"Saved to: {OUTPUT_FILE}")

# Quick verify
df = con.execute(f"SELECT Symbol, COUNT(*), MIN(Date), MAX(Date) FROM read_csv_auto('{OUTPUT_FILE}') GROUP BY Symbol").df()
print("\nExtracted Data Overview:")
print(df.to_string())
