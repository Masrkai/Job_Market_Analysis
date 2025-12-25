import pandas as pd

CSV_FILE = r"/home/masrkaii/Job_Market_Analysis/Data/Scraped-back/Morocco/Software Engineering/Software Engineering.csv"

# =========================
# LOAD CSV
# =========================
df = pd.read_csv(CSV_FILE)

# =========================
# EMPTY FILE CHECK
# =========================
if df.empty:
    print("The CSV file is empty. No data to process.")
    exit()

print(f"Loaded {len(df)} rows.")

# =========================
# COLUMN DETECTION
# =========================
url_candidates = ["url", "job_url", "link", "job_link", "apply_link"]

url_column = next((c for c in url_candidates if c in df.columns), None)

if url_column is None:
    raise ValueError(
        f"No URL column found. Available columns: {df.columns.tolist()}"
    )

if "location" not in df.columns:
    raise ValueError("No 'location' column found in CSV.")

# =========================
# NORMALIZATION
# =========================
df["location"] = df["location"].astype(str).str.strip().str.lower()
df[url_column] = df[url_column].astype(str).str.strip()

# =========================
# DUPLICATE DETECTION
# =========================
duplicate_mask = df.duplicated(subset=["location", url_column], keep="first")
duplicate_count = duplicate_mask.sum()

# =========================
# DELETE DUPLICATES (INTENTIONAL)
# =========================
if duplicate_count == 0:
    print("No duplicated jobs found. CSV remains unchanged.")
else:
    print(f"Found {duplicate_count} duplicated jobs.")
    df_cleaned = df[~duplicate_mask]
    df_cleaned.to_csv(CSV_FILE, index=False)
    print(f"Duplicates removed. CSV now has {len(df_cleaned)} rows.")
