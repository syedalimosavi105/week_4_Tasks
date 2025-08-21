import os
import pandas as pd
import matplotlib.pyplot as plt

CSV = "monthly_sales.csv"

# create sample CSV if not present
if not os.path.exists(CSV):
    sample = """month,sales
Jan,12000
Feb,15000
Mar,13000
Apr,17000
May,16000
Jun,18000
Jul,19000
Aug,17500
Sep,18500
Oct,20000
Nov,19500
Dec,22000
"""
    with open(CSV, "w", encoding="utf-8") as f:
        f.write(sample)
    print(f"Sample '{CSV}' created.\n")

# load data
df = pd.read_csv(CSV)
# keep month order as in file (if needed convert to categorical with ordered months)
months_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
df['month'] = pd.Categorical(df['month'], categories=months_order, ordered=True)
df = df.sort_values('month')

# plot
plt.figure(figsize=(10,5))
plt.plot(df['month'], df['sales'], marker='o', linewidth=2)
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales (PKR)")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45)
plt.tight_layout()

out_file = "monthly_sales.png"
plt.savefig(out_file)
print(f"Chart saved as {out_file}")
plt.show()
