import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the benchmarking output
bench_path = "data/processed/benchmarking_output.csv"
benchmark = pd.read_csv(bench_path)

# ----------------------------------
# 1. Select Features for Clustering
# ----------------------------------
features = [
    "total_revenue",
    "avg_price",
    "competitor_avg_price",
    "price_gap_avg",
    "avg_quantity",
    "avg_monthly_sales",
    "num_orders_month"
]

df_cluster = benchmark[features].copy()

# Handle missing values (if any)
df_cluster = df_cluster.fillna(df_cluster.mean())

# ----------------------------------
# 2. Standardize Features
# ----------------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_cluster)

# ----------------------------------
# 3. Apply K-Means Clustering
# ----------------------------------
k = 4  # choose 4 clusters for clear segmentation
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add cluster labels back to dataframe
benchmark["cluster"] = clusters

# ----------------------------------
# 4. Save Output
# ----------------------------------
output_path = "data/processed/merchant_clusters.csv"
benchmark.to_csv(output_path, index=False)

benchmark[["merchant_id", "cluster"]].head()


import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.scatter(
    benchmark["total_revenue"],
    benchmark["price_gap_avg"],
    c=benchmark["cluster"]
)

plt.xlabel("Total Revenue")
plt.ylabel("Price Gap Avg")
plt.title("Merchant Segmentation Clusters")
plt.show()

print("mod 3 done")