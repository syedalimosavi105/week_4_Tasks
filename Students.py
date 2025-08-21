import os
import pandas as pd

CSV = "students.csv"

# create a sample file if not exists (so you can run immediately)
if not os.path.exists(CSV):
    sample = """id,name,math,physics,chemistry,english
S001,Aisha,85,78,92,88
S002,Omar, 90,absent,85,82
S003,Sara,78,81,NaN,79
S004,Ali,92,88,91,not available
S005,Hassan, ,75,89,85
"""
    with open(CSV, "w", encoding="utf-8") as f:
        f.write(sample)

# 1. Load CSV
df = pd.read_csv(CSV)

# 2. Clean column names and trim whitespace in string columns
df.columns = df.columns.str.strip()
if 'name' in df.columns:
    df['name'] = df['name'].astype(str).str.strip()

# 3. Identify subject columns (everything except id and name)
subjects = [c for c in df.columns if c.lower() not in ('id', 'name')]

# 4. Normalize common non-numeric tokens to NaN, strip spaces, and convert to numeric
df[subjects] = df[subjects].replace(
    to_replace=['absent', 'not available', 'not_available', 'NA', 'NaN', '', ' '],
    value=pd.NA
)

for col in subjects:
    # remove surrounding spaces then convert; invalid -> NaN
    df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')

# 5. Compute average per subject (skip NaN)
averages = df[subjects].mean().round(2)

# 6. Print results
print("Class average marks (per subject):")
for subj, avg in averages.items():
    print(f"- {subj}: {avg:.2f}")