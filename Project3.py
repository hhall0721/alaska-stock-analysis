import sqlite3
import yfinance as yf
import pandas as pd

#Imported Airline Stock Data(Same as Project2.py)
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

combined = pd.concat(all_closing_prices, axis=1, keys=tickers)
combined = combined.dropna()

#SQL Work
connection = sqlite3.connect("airlines.db")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
     date TEXT, 
    ticker TEXT, 
    close_price REAL
    )
    """)

cursor.execute("SELECT * FROM stock_prices")
rows = cursor.fetchall()
for row in rows:
    print(row)

#Reshaping the DataFrame from Wide to Long Format
wide_data = combined.reset_index()
print(wide_data.columns)
long_data = wide_data.melt(
    id_vars = "Date", 
    var_name = "ticker", 
    value_name = "close_price")
print(long_data.head())

#Note: Delete from stock_price mitigates duplicate entries but can't UPDATE data
cursor.execute("DELETE FROM stock_prices")
connection.commit()

#Long DataFrame to SQL Database
long_data.to_sql(
    "stock_prices", 
    connection, 
    if_exists="append", 
    index=False
)
cursor.execute("SELECT * FROM stock_prices")
rows = cursor.fetchall()
print(len(rows))

#Extract Data for a Specific Airline(e.g., ALK)
cursor.execute("SELECT * FROM stock_prices WHERE ticker = 'ALK'")
rows = cursor.fetchall()
print(len(rows))
cursor.execute(
    "SELECT AVG(close_price) " \
    "FROM stock_prices " \
    "WHERE ticker= 'ALK'")
fetched_avg = cursor.fetchone()
print(fetched_avg[0])

#Using 'GROUP BY' to Calculate AVG Close Price for each Airline
cursor.execute(
    "SELECT ticker, AVG(close_price) " \
    "FROM stock_prices " \
    "GROUP BY ticker")
fetched_avgs = cursor.fetchall()
print(fetched_avgs)
