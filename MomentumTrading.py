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

# Calculate the momentum
window_size = 30
momentum = data["Adj Close"].pct_change(window_size)

# Create a momentum trading signal
data["signal"] = np.where(momentum > 0, 1, 0)

# Plot the stock prices and trading signal
plt.plot(data["Adj Close"], label="Adj Close")
plt.scatter(data.index, data["Adj Close"], c=data["signal"], cmap="viridis")
plt.legend()
plt.show()