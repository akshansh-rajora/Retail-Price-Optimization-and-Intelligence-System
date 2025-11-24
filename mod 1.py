import pandas as pd
import numpy as np
import os

# Load data
base = "data/raw"
sales = pd.read_csv(os.path.join(base, "transactions.csv"))
competitors = pd.read_csv(os.path.join(base, "competitor_prices.csv"))
merchants = pd.read_csv(os.path.join(base, "merchants.csv"))

# ---------------------------
# 1. Merchant Sales Metrics
# ---------------------------
sales_metrics = (
    sales.groupby("merchant_id")
         .agg(
            total_revenue = ("revenue", "sum"),
            avg_price = ("price", "mean"),
            avg_quantity = ("quantity", "mean"),
            total_products = ("product_id", "nunique")
         )
         .reset_index()
)

# ---------------------------
# 2. Competitor Price Metrics
# ---------------------------
competitor_metrics = (
    competitors.groupby("product_id")
               .agg(
                    avg_competitor_price = ("competitor_price", "mean"),
                    merchant_price = ("merchant_price", "mean")
               )
               .reset_index()
)

# Price gap
competitor_metrics["price_gap"] = (
    competitor_metrics["avg_competitor_price"] - competitor_metrics["merchant_price"]
)

# ---------------------------
# 3. Merge merchant + competitor data
# ---------------------------
merged = sales.merge(competitor_metrics, on="product_id", how="left")

# Now compute merchant-level competitor comparison
merchant_comp_metrics = (
    merged.groupby("merchant_id")
          .agg(
              merchant_avg_price = ("merchant_price", "mean"),
              competitor_avg_price = ("avg_competitor_price", "mean"),
              price_gap_avg = ("price_gap", "mean")
          )
          .reset_index()
)

# ---------------------------
# 4. Combine all metrics
# ---------------------------
benchmark_df = sales_metrics.merge(merchant_comp_metrics, on="merchant_id", how="left")

# Add merchant attributes for richer benchmarking
benchmark_df = benchmark_df.merge(merchants, on="merchant_id", how="left")

# ---------------------------
# 5. Save Output
# ---------------------------
output_path = "data/processed/benchmarking_output.csv"
os.makedirs("data/processed", exist_ok=True)
benchmark_df.to_csv(output_path, index=False)

benchmark_df.head()
print("mod 1 done")