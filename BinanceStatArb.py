import numpy as np
import pandas as pd
import binance
import time

# Initialize the Binance client
client = binance.Client(api_key="your_api_key", api_secret="your_api_secret")

# Define the stock symbols and window size
symbol1 = "BTCUSDT"
symbol2 = "ETHUSDT"
window_size = 30

# Fetch the historical data for both symbols
klines1 = client.fetch_klines(symbol=symbol1, interval=binance.KLINE_INTERVAL_1HOUR, limit=window_size)
klines2 = client.fetch_klines(symbol=symbol2, interval=binance.KLINE_INTERVAL_1HOUR, limit=window_size)
data1 = pd.DataFrame(klines1, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
data2 = pd.DataFrame(klines2, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])

# Calculate the returns for both symbols
returns1 = (data1["Close"].astype(float) - data1["Open"].astype(float)) / data1["Open"].astype(float)
returns2 = (data2["Close"].astype(float) - data2["Open"].astype(float)) / data2["Open"].astype(float)

# Calculate the mean and covariance of the returns
mean1 = np.mean(returns1)
mean2 = np.mean(returns2)
cov = np.cov(returns1, returns2)

# Calculate the optimal weights for the portfolio
weights = np.dot(np.linalg.inv(cov), np.array([mean1, mean2]))
weights /= np.sum(weights)

# Get the current prices for both symbols
price1 = client.fetch_ticker(symbol=symbol1)["lastPrice"]
price2 = client.fetch_ticker(symbol=symbol2)["lastPrice"]

# Calculate the spread and z-score
spread = weights[0] * (price1 - price2)
z_score = spread / np.std(spread)

# Create a trading signal based on the z-score
signal = np.where(z_score > 1, -1, np.where(z_score < -1, 1, 0))

# Place a market order if the trading signal is not zero
if signal != 0:
    order = client.create_order(symbol=symbol1 + symbol2, side=binance.SIDE_SELL if signal == 1 else binance.SIDE_BUY, type=binance.ORDER_TYPE_MARKET, quantity=1)
    print("Placed an order:", order)
else:
    print("No trading signal")

time.sleep(60)  # wait for 60 seconds before checking again
