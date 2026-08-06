import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

#Linear Regression Model
alaska = yf.Ticker("ALK")
history = alaska.history(period="1y")
closing_prices = history["Close"]
days = range(len(closing_prices))

trend = np.polyfit(days, closing_prices, 1)
predicted_price = trend[0] * 25 + trend[1]
print(predicted_price)

#30-Day Moving Average
moving_avg = closing_prices.rolling(window=30).mean()
plt.figure(figsize=(8, 5))
plt.plot(closing_prices.index, closing_prices, label='Actual Prices')
plt.plot(closing_prices.index, moving_avg, label='30-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.title('Alaska Airlines (ALK) Stock Price with Moving Average')
plt.legend()
plt.savefig('alaska_stock_trend.png')
plt.show()

# Daily Returns (for Monte Carlo Simulation) 
daily_returns = closing_prices.pct_change()

# ---------- Monte Carlo Simulation Setup ----------
mu = daily_returns.mean()
sigma = daily_returns.std()

# ---------- Monte Carlo Simulation ----------
last_price = closing_prices.iloc[-1]
num_days = 30
num_simulations = 500
all_simulations = []

for sim in range(num_simulations):
    simulated_prices = [last_price]
    for day in range(num_days):
        random_shock = np.random.normal()
        next_price = simulated_prices[-1] * np.exp((mu - 0.5 * sigma**2) + sigma * random_shock)
        simulated_prices.append(next_price)
    all_simulations.append(simulated_prices)

print(len(all_simulations))

# ---------- Plot All Simulated Paths ----------
plt.figure(figsize=(8, 5))
for path in all_simulations:
    plt.plot(path, alpha=0.1, color='blue')
plt.xlabel('Days into the Future')
plt.ylabel('Simulated Price ($)')
plt.title('Alaska Airlines (ALK) — 500 Simulated Future Price Paths')
plt.savefig('alaska_monte_carlo.png')
plt.show()

# ---------- Summary Statistics ----------
final_prices = [path[-1] for path in all_simulations]

mean_final_price = np.mean(final_prices)
lower_bound = np.percentile(final_prices, 5)
upper_bound = np.percentile(final_prices, 95)

print("Average simulated price:", mean_final_price)
print("90% range:", lower_bound, "to", upper_bound)
