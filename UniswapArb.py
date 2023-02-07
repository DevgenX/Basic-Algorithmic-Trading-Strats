import requests
import json
import time
import numpy as np
import pandas as pd


# Define the API endpoint and headers
endpoint = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2"
headers = {
    "Content-Type": "application/json"
}

# Define the query to get the latest prices of a token pair
query = """
{
  pair(id: "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D") {
    reserves
  }
}
"""

# Send the API request
response = requests.post(endpoint, headers=headers, data=json.dumps({"query": query}))

# Parse the API response
data = json.loads(response.text)
reserves = data["data"]["pair"]["reserves"]
price1 = reserves[0] / reserves[1]
price2 = 1 / price1

# Calculate the spread and z-score
spread = price1 - price2
z_score = spread / np.std(spread)

# Create a trading signal based on the z-score
signal = np.where(z_score > 1, -1, np.where(z_score < -1, 1, 0))

# Place a trade if the trading signal is not zero
if signal != 0:
    # Your trade logic here
    print("Placed a trade")
else:
    print("No trading signal")

time.sleep(60)  # wait for 60 seconds before checking again