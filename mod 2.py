import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Load sales data
base = "data/raw"
sales = pd.read_csv(os.path.join(base, "transactions.csv"))

# Convert date column
sales['date'] = pd.to_datetime(sales['date'])

# -----------------------------------------------------
# 1. Aggregate to daily revenue
# -----------------------------------------------------
daily_sales = (
    sales.groupby("date")
         .agg(total_revenue=("revenue", "sum"))
         .reset_index()
         .sort_values("date")
)

# -----------------------------------------------------
# 2. Create a simple moving average forecast
# -----------------------------------------------------
window = 7  # 7-day moving average

daily_sales['moving_avg'] = daily_sales['total_revenue'].rolling(window=window).mean()

# Last moving average value will be the forecast base
last_ma = daily_sales['moving_avg'].iloc[-1]

# -----------------------------------------------------
# 3. Create 30-day future dates
# -----------------------------------------------------
future_dates = pd.date_range(
    start=daily_sales['date'].max() + pd.Timedelta(days=1),
    periods=30
)

forecast_values = [last_ma] * 30  # flat MA forecast

forecast_df = pd.DataFrame({
    "date": future_dates,
    "forecast_revenue": forecast_values
})

# -----------------------------------------------------
# 4. Save forecast output
# -----------------------------------------------------
os.makedirs("data/processed", exist_ok=True)
output_path = "data/processed/forecasting_output.csv"
forecast_df.to_csv(output_path, index=False)

# Show first few rows
forecast_df.head()


plt.figure(figsize=(10,5))
plt.plot(daily_sales['date'], daily_sales['total_revenue'], label="Actual Revenue")
plt.plot(daily_sales['date'], daily_sales['moving_avg'], label="7-Day MA")
plt.plot(forecast_df['date'], forecast_df['forecast_revenue'], linestyle='--', label="Forecast")
plt.legend()
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Sales Forecast")
plt.show()

print("mod 2 done")