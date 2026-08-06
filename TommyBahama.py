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

#Tommy Bahama Food & Beverage Segment Analysis
f_and_b_yearly_revenue = {"2022": 109, "2025": 121}
f_and_b_quarter1_revenue = {"2024":35, "2025": 34}

growth_rate = (f_and_b_yearly_revenue["2025"] - f_and_b_yearly_revenue["2022"])/f_and_b_yearly_revenue["2022"] * 100
print( "Three Year Growth Rate of Tommy Bahama Food & Beverage Segment", growth_rate, "%")

first_quarter_growth_rate = (f_and_b_quarter1_revenue["2025"] - f_and_b_quarter1_revenue["2024"])/f_and_b_quarter1_revenue["2024"] * 100
print("First Quarter Growth Rate of Tommy Bahama Food & Beverage Segment", first_quarter_growth_rate, "%")

#Food and beverage segment grew 11% over three years and yet the first quarter of 2025 saw a 3% decline in revenue compared to first quarter of 2024.
#Did most of the growth happen between 2022-2024? 
#Has there been a decline in revenue since 2024 or is food & bev seasonal?

#Bar Chart of Food & Beverage Revenue
years = list(f_and_b_yearly_revenue.keys())
revenues = list(f_and_b_yearly_revenue.values())
plt.figure(figsize=(8,5))
plt.bar(years, revenues, color='purple')
plt.xlabel("Year")
plt.ylabel("Revenue In Millions")
plt.title("Tommy Bahama Food & Beverage Segment Yearly Revenue")
plt.savefig("tommy_bahama_food_beverage_yearly_revenue.png")

quarters = list(f_and_b_quarter1_revenue.keys())
quarter1_revenues = list(f_and_b_quarter1_revenue.values())
plt.figure(figsize=(8,5))
plt.bar(quarters, quarter1_revenues, color='green')
plt.xlabel("Year")
plt.ylabel("Revenue In Millions")
plt.title("Tommy Bahama Food & Beverage Segment First Quarter Revenue")
plt.savefig("tommy_bahama_food_beverage_first_quarter_revenue.png")


