import pandas as pd
import numpy as np
import os

# Load data
base = "data/raw"
comp = pd.read_csv(os.path.join(base, "competitor_prices.csv"))

# ------------------------------------
# 1. Compute Price Gap
# ------------------------------------
comp["price_gap"] = comp["competitor_price"] - comp["merchant_price"]

# Percentage difference
comp["pct_diff"] = (comp["price_gap"] / comp["merchant_price"]) * 100

# ------------------------------------
# 2. Create Pricing Recommendations
# ------------------------------------
def recommend(row):
    if row["pct_diff"] > 5:        # competitor price > merchant price by 5%
        return "Increase Price"
    elif row["pct_diff"] < -5:     # merchant price too high
        return "Decrease Price"
    else:
        return "Keep Same"

comp["recommendation"] = comp.apply(recommend, axis=1)

# ------------------------------------
# 3. Create Suggested Price (Optional)
# ------------------------------------
def suggest_price(row):
    if row["recommendation"] == "Increase Price":
        return round(row["merchant_price"] * 1.05, 2)
    elif row["recommendation"] == "Decrease Price":
        return round(row["merchant_price"] * 0.95, 2)
    else:
        return row["merchant_price"]

comp["suggested_price"] = comp.apply(suggest_price, axis=1)

# ------------------------------------
# 4. Save Output
# ------------------------------------
os.makedirs("data/processed", exist_ok=True)
output_path = "data/processed/pricing_recommendations.csv"
comp.to_csv(output_path, index=False)

comp.head()


import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.scatter(comp["merchant_price"], comp["competitor_price"], c=comp["pct_diff"])
plt.xlabel("Merchant Price")
plt.ylabel("Competitor Price")
plt.title("Price Comparison Scatter Plot")
plt.colorbar(label="Percentage Difference")
plt.show()


import matplotlib.pyplot as plt

plt.hist(df['maturity_score'], bins=10)
plt.xlabel("Maturity Score")
plt.ylabel("Number of Products")
plt.title("Market Maturity Distribution")
plt.show()

#####

plt.scatter(df['performance_score'], 
            df['maturity_score'], 
            c=df['cluster'], 
            alpha=0.7)

plt.xlabel("Performance Score")
plt.ylabel("Maturity Score")
plt.title("Market Segments (Clustered)")
plt.show()

#####

p = df.iloc[0]   # first product

labels = ["performance_score", "maturity_score", 
          "reliability_score", "risk_score"]
values = p[labels].values.tolist()

# Close the circle
values += values[:1]
angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
angles += angles[:1]

plt.polar(angles, values)
plt.fill(angles, values, alpha=0.3)
plt.title(f"Product Capability Map: {p['product_name']}")
plt.show()

print("mod 4 done")