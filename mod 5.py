import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

# Load reviews and pricing/benchmarks for integration
base = "data/raw"
reviews = pd.read_csv(os.path.join(base, "reviews.csv"))

# Initialize VADER
sid = SentimentIntensityAnalyzer()



# -----------------------------------------------------
# 1. Compute sentiment score for each review
# -----------------------------------------------------
reviews['sentiment'] = reviews['review'].apply(lambda x: sid.polarity_scores(str(x))['compound'])

import random

positive_phrases = [
    "works really well", "very reliable", "customers love it",
    "easy to use", "excellent performance", "highly recommended"
]

negative_phrases = [
    "has many issues", "poor reliability", "not satisfied",
    "performance is weak", "customer complaints", "needs improvement"
]

def generate_review(row):
    if row['performance_score'] > 70:
        return random.choice(positive_phrases)
    else:
        return random.choice(negative_phrases)


# -----------------------------------------------------
# 2. Product-level sentiment
# -----------------------------------------------------
product_sentiment = (
    reviews.groupby("product_id")
           .agg(avg_product_sentiment=("sentiment", "mean"))
           .reset_index()
)

# -----------------------------------------------------
# 3. Merchant-level sentiment
# -----------------------------------------------------
merchant_sentiment = (
    reviews.groupby("product_id")
           .agg(avg_merchant_sentiment=("sentiment", "mean"))
           .reset_index()
)

# -----------------------------------------------------
# 4. Merge sentiment with pricing recommendations
# -----------------------------------------------------
pricing_reco = pd.read_csv("data/processed/pricing_recommendations.csv")

pricing_with_sentiment = (
    pricing_reco.merge(product_sentiment, on="product_id", how="left")
)

# -----------------------------------------------------
# 5. Save outputs
# -----------------------------------------------------
os.makedirs("data/processed", exist_ok=True)
product_sentiment.to_csv("data/processed/product_sentiment.csv", index=False)
merchant_sentiment.to_csv("data/processed/merchant_sentiment.csv", index=False)
pricing_with_sentiment.to_csv("data/processed/pricing_recommendations_with_sentiment.csv", index=False)

pricing_with_sentiment.head()


print("mod 5 done")