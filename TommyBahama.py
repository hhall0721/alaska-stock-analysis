import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#Import OXM Stock History
oxm = yf.Ticker("OXM")
history = oxm.history(period="1y")
closing_prices = history["Close"]
print(closing_prices)

#Plot OXM Stock Price History
plt.figure(figsize=(8,5))
plt.plot(closing_prices.index, closing_prices, label="Closing Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Oxford Industries Stock Price History")
plt.legend()
plt.savefig("oxm_stock_price.png")

#30-Day Moving Average
moving_average = closing_prices.rolling(window=30).mean()
plt.figure(figsize=(8,5))
plt.plot(closing_prices.index, closing_prices, label="Closing Prices")
plt.plot(moving_average.index, moving_average, label="30-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Oxford Industries Stock Price with 30-Day Moving Average")
plt.legend()
plt.savefig("oxm_stock_price_moving_average.png")
