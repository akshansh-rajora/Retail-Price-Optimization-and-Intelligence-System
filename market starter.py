"""
Market Intelligence — Starter Script

This Python script does two things:
 1) Shows a small ASCII pipeline diagram (and references a local diagram image saved in the conversation).
 2) Generates small synthetic CSV datasets in `data/raw/` to get you started with the learning-mode project.

DIAGRAM IMAGE PATH (from uploaded image):
  /mnt/data/5da35213-3641-4107-91cd-f5e7e1969ce1.png

How to run:
  - Ensure you have Python 3.8+ and pandas & numpy installed:
      pip install pandas numpy
  - Run:
      python market_intel_starter.py
  - Generated files will be in `data/raw/` (transactions.csv, competitor_prices.csv, merchants.csv, reviews.csv)

"""

import os
import random
from datetime import datetime, timedelta
import csv
import pandas as pd
import numpy as np

# --------------- Configuration -----------------
OUT_DIR = "data/raw"
DIAGRAM_PATH = "/mnt/data/5da35213-3641-4107-91cd-f5e7e1969ce1.png"
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

os.makedirs(OUT_DIR, exist_ok=True)

# ---------------- ASCII Diagram ----------------
PIPELINE_DIAGRAM = r"""
Simple Market Intelligence Pipeline (learning mode)

[Raw CSVs] --> [Data Cleaning (pandas)] --> [Analytics]
                                     |            |-- Forecasting (Prophet/ARIMA)
                                     |            |-- Clustering (KMeans)
                                     |            |-- Price Intelligence (rules)
                                     |            |-- Sentiment (VADER/TextBlob)
                                     v
                                [Output CSVs]
                                     |
                                     v
                               [Tableau Desktop]

(For a visual diagram, see the uploaded image at: {diagram})
""".format(diagram=DIAGRAM_PATH)

print(PIPELINE_DIAGRAM)

# --------------- Synthetic Data Generators -----------------

def generate_merchants(n_merchants=10):
    merchants = []
    categories = ["Electronics", "Home", "Fashion", "Beauty", "Grocery"]
    regions = ["US", "AU"]
    for i in range(1, n_merchants+1):
        merchant_id = f"M{i:03d}"
        merchants.append({
            "merchant_id": merchant_id,
            "merchant_name": f"Merchant_{i}",
            "category": random.choice(categories),
            "region": random.choice(regions),
            "avg_monthly_sales": round(random.uniform(5000, 50000), 2),
            "num_orders_month": random.randint(50, 2000)
        })
    return pd.DataFrame(merchants)


def generate_products(n_products=40):
    products = []
    for i in range(1, n_products+1):
        pid = f"P{i:04d}"
        products.append({
            "product_id": pid,
            "product_name": f"Product_{i}",
            "category": random.choice(["Electronics","Home","Fashion","Beauty","Grocery"]) 
        })
    return pd.DataFrame(products)


def generate_transactions(merchants_df, products_df, n_days=180, avg_tx_per_day=6):
    rows = []
    start_date = datetime.utcnow().date() - timedelta(days=n_days)
    merchant_ids = merchants_df['merchant_id'].tolist()
    product_ids = products_df['product_id'].tolist()

    for single_date in (start_date + timedelta(n) for n in range(n_days)):
        n_tx = max(1, int(np.random.poisson(avg_tx_per_day)))
        for _ in range(n_tx):
            merchant = random.choice(merchant_ids)
            product = random.choice(product_ids)
            price = round(random.uniform(5, 500), 2)
            qty = random.choices([1,1,1,2,3], weights=[60,60,60,20,5])[0]
            revenue = round(price * qty, 2)
            rows.append({
                "date": single_date.isoformat(),
                "merchant_id": merchant,
                "product_id": product,
                "price": price,
                "quantity": qty,
                "revenue": revenue
            })
    df = pd.DataFrame(rows)
    return df


def generate_competitor_prices(products_df, merchants_df):
    rows = []
    competitor_names = ["CompA", "CompB", "CompC"]
    for _, prod in products_df.iterrows():
        product_id = prod['product_id']
        # For each product, assign a base price and competitor prices for a subset of merchants
        base_price = round(random.uniform(10, 400), 2)
        for merchant in merchants_df['merchant_id'].sample(n=max(3, len(merchants_df)//2)).tolist():
            merchant_price = round(base_price * random.uniform(0.8, 1.2), 2)
            # Competitor prices
            for comp in competitor_names:
                comp_price = round(base_price * random.uniform(0.85, 1.25), 2)
                rows.append({
                    "product_id": product_id,
                    "merchant_id": merchant,
                    "competitor": comp,
                    "competitor_price": comp_price,
                    "merchant_price": merchant_price,
                    "date": datetime.utcnow().date().isoformat()
                })
    return pd.DataFrame(rows)


def generate_reviews(products_df, n_reviews=300):
    sample_texts = [
        "Great product, fast delivery.",
        "Good value for money.",
        "Product quality was below expectation.",
        "Exceeded expectations, highly recommend!",
        "Packaging was damaged, but product is fine.",
        "Customer service did not respond.",
        "Five stars, will buy again.",
        "Size/color not as described.",
        "Amazing build quality and easy to use.",
        "Mediocre experience overall."
    ]
    rows = []
    product_ids = products_df['product_id'].tolist()
    for i in range(n_reviews):
        pid = random.choice(product_ids)
        rating = random.choice([1,2,3,4,5])
        text = random.choice(sample_texts)
        rows.append({
            "review_id": f"R{i:05d}",
            "product_id": pid,
            "review": text,
            "rating": rating,
            "date": (datetime.utcnow().date() - timedelta(days=random.randint(0, 365))).isoformat()
        })
    return pd.DataFrame(rows)

# ---------------- Generate and write CSVs ----------------
merchants_df = generate_merchants(12)
products_df = generate_products(45)
transactions_df = generate_transactions(merchants_df, products_df, n_days=120, avg_tx_per_day=8)
competitor_prices_df = generate_competitor_prices(products_df, merchants_df)
reviews_df = generate_reviews(products_df, n_reviews=260)

# Write CSVs
merchants_df.to_csv(os.path.join(OUT_DIR, "merchants.csv"), index=False)
products_df.to_csv(os.path.join(OUT_DIR, "products.csv"), index=False)
transactions_df.to_csv(os.path.join(OUT_DIR, "transactions.csv"), index=False)
competitor_prices_df.to_csv(os.path.join(OUT_DIR, "competitor_prices.csv"), index=False)
reviews_df.to_csv(os.path.join(OUT_DIR, "reviews.csv"), index=False)

print("\nGenerated files:")
for f in os.listdir(OUT_DIR):
    print(" -", os.path.join(OUT_DIR, f))

print(f"\nDiagram image is available at: {DIAGRAM_PATH}")
print("Open the generated CSVs in data/raw/ and start with the small-scale project steps.")
