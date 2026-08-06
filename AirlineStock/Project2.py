import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.arima.model import ARIMA

#For Airline Stock Correlation Analysis
tickers = ["ALK","DAL","UAL","LUV"]
all_airlines = []
for ticker in tickers:
    airline = yf.Ticker(ticker)
    all_airlines.append(airline)
all_histories = []
for ticker in all_airlines:
    history = ticker.history(period="1y")
    all_histories.append(history)
print(len(all_histories))
all_closing_prices = []
for history in all_histories:
    closing_prices = history["Close"]
    all_closing_prices.append(closing_prices)
print(len(all_closing_prices))
combined = pd.concat(all_closing_prices, axis=1, keys=tickers)
combined = combined.dropna()
correlation_matrix = combined.corr()
print(correlation_matrix)
plt.figure(figsize=(6,5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Between Airline Stocks')
plt.savefig('airline_correlation_heatmap.png')

#For Linear Regression Model
X = pd.DataFrame({'Day': range(len(combined))})
y = combined['ALK']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
model = LinearRegression()
model.fit(X_train, y_train)                  
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(mse)

#For Polynomial Regression Model
poly = PolynomialFeatures(degree=4)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
model_poly = LinearRegression()
model_poly.fit(X_train_poly, y_train)
predictions_poly = model_poly.predict(X_test_poly)
mse_poly = mean_squared_error(y_test, predictions_poly)
print(mse_poly)

#ARIMA Model for Stock Price Forecasting
arima_model = ARIMA(y_train, order=(30, 1, 0))
arima_fitted = arima_model.fit()
arima_predictions = arima_fitted.forecast(steps=len(y_test))
mse_arima = mean_squared_error(y_test, arima_predictions)
print(mse_arima)
