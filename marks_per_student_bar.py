import os
import pandas as pd
import matplotlib.pyplot as plt

CSV = "students.csv"

# Create a sample CSV automatically if not present
if not os.path.exists(CSV):
    sample = """id,name,math,physics,chemistry,english
S001,Aisha,85,78,92,88
S002,Omar,90,absent,85,82
S003,Sara,78,81,NaN,79
S004,Ali,92,88,91,not available
S005,Hassan, ,75,89,85
"""
    with open(CSV, "w", encoding="utf-8") as f:
        f.write(sample)
    print(f"Sample '{CSV}' created for demo.\n")

# 1. Load CSV
df = pd.read_csv(CSV)

# 2. Clean: trim names, normalize common bad tokens to NaN
df.columns = df.columns.str.strip()
if 'name' in df.columns:
    df['name'] = df['name'].astype(str).str.strip()

# Identify subject columns (exclude id and name)
subjects = [c for c in df.columns if c.lower() not in ('id', 'name')]

# Replace common non-numeric tokens with NA
df[subjects] = df[subjects].replace(
    to_replace=['absent', 'not available', 'not_available', 'NA', 'NaN', '', ' '],
    value=pd.NA
)

# Convert to numeric (invalid -> NaN)
for col in subjects:
    df[col] = pd.to_numeric(df[col].astype(str).str.strip(), errors='coerce')

# 3. Compute total marks per student (sum across subjects, skip NaN)
df['total_marks'] = df[subjects].sum(axis=1, skipna=True)

# For plotting labels, use name if present else use id
if 'name' in df.columns and df['name'].notna().any():
    labels = df['name'].fillna(df['id'])
else:
    labels = df['id']

totals = df['total_marks']

# 4. Plot bar chart
plt.figure(figsize=(8, 5))
bars = plt.bar(labels, totals)
plt.xlabel("Student")
plt.ylabel("Total Marks")
plt.title("Total Marks per Student")
plt.xticks(rotation=30, ha='right')
plt.tight_layout()

# add value labels on top of bars
for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, h + 0.5, f"{h:.0f}", ha='center', va='bottom', fontsize=9)

# Save and show
out_png = "marks_per_student.png"
plt.savefig(out_png)
print(f"Bar chart saved as: {out_png}")
plt.show()
