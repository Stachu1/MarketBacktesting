import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


def get_data(ticker, start_date, end_date):
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    return data


def backtest(data, leverage):
    # Calculate daily returns
    daily_returns = data['Close'].pct_change().dropna().astype(float)

    # Calculate leveraged cumulative returns
    leveraged_return = float(((1 + daily_returns * leverage).prod() - 1).iloc[0])

    # print(f"x{leverage:.2f} {leveraged_return*100:.2f}%")
    return leveraged_return


def get_yearly(change, years):
    return (change + 1) ** (1 / years) - 1


def plot(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label=ticker, color='blue')
    plt.title(ticker)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()






# Define parameters
ticker = "QQQ"
start_date = "2020-01-25"
end_date = "2025-01-25"
years = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days / 365.0




data = get_data(ticker, start_date, end_date)
plot(data)