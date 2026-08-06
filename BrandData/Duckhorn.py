#Duckhorn went private in 2024
# Constellation Brand(STZ)
#Constellation's stock has been on a fairly clear downward trend over the past year
#Is this reflecting broader wine/alcohol industry headwinds, or something more company-specific?
#How does wine's aging cycle affect your forecasting?

# Demand Consolidation Project - Built for meeting with Paul Finn (Duckhorn Portfolio)
# Creates a small SQLite database with a demand_forecast table (region, month, forecast_units)
# Inserts proportional regional wine demand data (NIAAA consumption data by U.S. Census region: South, West, Northeast, Midwest)
# Consolidate all four regions' forecasts into one total number per month 
# Result: January total demand = 36,000 units; February total demand = 36,800 units

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

#STZ Basic Stock Plotting
stz = yf.Ticker("STZ")
history = stz.history(period="1y")
closing_prices = history["Close"]
print(closing_prices)

plt.figure(figsize=(8,5))
plt.plot(closing_prices.index, closing_prices, label = "CLosing Prices")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.title("Constellation Stock Price History")
plt.legend()
plt.savefig("stz_stock_price.png")

moving_average = closing_prices.rolling(window = 30).mean()
plt.figure(figsize=(8,5))
plt.plot(closing_prices.index, closing_prices, label="Closing Prices")
plt.plot(moving_average.index, moving_average, label="30-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("30 Day Moving Average")
plt.title("Constellation Stock Moving Average")
plt.legend()
plt.savefig("stz_stock_price_moving_average.png")

#Demand Consolidation (SQL)
connection = sqlite3.connect("demand_planning.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS demand_forecast (
     region TEXT, 
    month TEXT, 
    forecast_units REAL
    )
    """)
demand_data = [
    ("West", "January", 9500),
    ("West", "February", 9600),
    ("South", "January", 12000),
    ("South", "February", 13000),
    ("Northeast", "January", 8000),
    ("Northeast", "February", 7800),
    ("Midwest", "January", 6500),
    ("Midwest", "February", 6400),
]
cursor.executemany(
    "INSERT OR REPLACE INTO demand_forecast VALUES (?, ?, ?)",
    demand_data
)
cursor.execute("DELETE FROM demand_forecast")
connection.commit()

cursor.execute("SELECT month, SUM(forecast_units) FROM demand_forecast GROUP BY month")
fetched_sum = cursor.fetchall()
print(fetched_sum)
