import yfinance as yf
import pandas as pd
import sqlite3 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#Impoted Airline Stock Data
tickers = ["ALK", "DAL", "UAL", "LUV"]
all_airlines = []

for ticker in tickers:
 airline = yf.Ticker(ticker)
 all_airlines.append(airline)

all_histories = []
for ticker in all_airlines:
    history = ticker.history(period="1y")
    all_histories.append(history)

all_closing_prices = []
for history in all_histories:
   closing_prices = history["Close"]
   all_closing_prices.append(closing_prices)

all_tomorrow_prices = []
for closing_prices in all_closing_prices:
   tomorrow_price = closing_prices.shift(-1)
   all_tomorrow_prices.append(tomorrow_price)

all_labels = []
for closing_prices, tomorrow_price in zip(all_closing_prices, all_tomorrow_prices):
   label = (tomorrow_price > closing_prices).astype(int)
   all_labels.append(label)


all_airline_tables = []
for closing_prices, label in zip(all_closing_prices, all_labels):
   airline_table = pd.concat([closing_prices, label], axis=1)
   airline_table.columns = ["Close", "Label"]
   all_airline_tables.append(airline_table)


combined = pd.concat(all_airline_tables, axis=0)
combined = combined.dropna()
print(combined.head())

X = combined["Close"].values.reshape(-1,1)
y = combined["Label"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Accuracy of Logistic Regression Model:", accuracy)
