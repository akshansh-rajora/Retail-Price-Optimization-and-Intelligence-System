import pandas as pd
import matplotlib.pyplot as plt

# Load data
product_sentiment = pd.read_csv("data/processed/product_sentiment.csv")
pricing_with_sentiment = pd.read_csv("data/processed/pricing_recommendations_with_sentiment.csv")
products = pd.read_csv("data/raw/products.csv")  # Load products with category info

# 1. Histogram of product sentiment scores
plt.hist(product_sentiment['avg_product_sentiment'], bins=20, color='skyblue')
plt.xlabel("Average Product Sentiment")
plt.ylabel("Number of Products")
plt.title("Distribution of Product Sentiment Scores")
plt.show()

# 2. Scatter plot: Sentiment vs. Recommended Price
plt.scatter(pricing_with_sentiment['avg_product_sentiment'], 
            pricing_with_sentiment['suggested_price'], 
            alpha=0.7)
plt.xlabel("Average Product Sentiment")
plt.ylabel("Recommended Price")
plt.title("Sentiment vs. Recommended Price")
plt.show()

# 3. Boxplot: Recommended Price by Sentiment Quartile
pricing_with_sentiment['sentiment_quartile'] = pd.qcut(
    pricing_with_sentiment['avg_product_sentiment'], 4, labels=["Q1", "Q2", "Q3", "Q4"]
)
pricing_with_sentiment.boxplot(column='suggested_price', by='sentiment_quartile')
plt.xlabel("Sentiment Quartile")
plt.ylabel("Recommended Price")
plt.title("Recommended Price by Sentiment Quartile")
plt.suptitle("")  # Remove default title
plt.show()

# 4. If you want to see sentiment by product category (if available)
# Merge category into pricing_with_sentiment
pricing_with_sentiment = pricing_with_sentiment.merge(
    products[['product_id', 'category']],
    on='product_id',
    how='left'
)

if 'category' in pricing_with_sentiment.columns:
    pricing_with_sentiment.boxplot(column='avg_product_sentiment', by='category')
    plt.xlabel("Category")
    plt.ylabel("Average Product Sentiment")
    plt.title("Product Sentiment by Category")
    plt.suptitle("")
    plt.show()