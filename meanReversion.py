import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

# Define the stock symbol and API endpoint
symbol = ""
endpoint = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}"

# Fetch the historical data
response = requests.get(endpoint)
data = pd.read_html(response.text)[0]
data = data.iloc[::-1] # reverse the data to start from the earliest date
data.set_index("Date", inplace=True)

# Calculate the rolling mean and standard deviation
window_size = 30
rolling_mean = data["Adj Close"].rolling(window=window_size).mean()
rolling_std = data["Adj Close"].rolling(window=window_size).std()

# Create a mean reversion trading signal
z_score = (data["Adj Close"] - rolling_mean) / rolling_std
data["z_score"] = z_score
data["signal"] = np.where(z_score < -1, 1, 0)

# Plot the stock prices and trading signal
plt.plot(data["Adj Close"], label="Adj Close")
plt.plot(rolling_mean, label="Rolling Mean")
plt.plot(rolling_mean + rolling_std, label="Upper Band")
plt.plot(rolling_mean - rolling_std, label="Lower Band")
plt.fill_between(data.index, rolling_mean + rolling_std, rolling_mean - rolling_std, alpha=0.2)
plt.scatter(data.index, data["Adj Close"], c=data["signal"], cmap="viridis")
plt.legend()
plt.show()