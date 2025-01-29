import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def get_data(ticker, start_date, end_date):
    # Download historical data
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    return data


def backtest(data, monthly_income, frequency):
    data = data[['Close']].copy()
    
    # Resample data to daily frequency and create a purchase schedule
    data['Date'] = data.index
    purchase_schedule = data.resample(f'{frequency * 7}D').first().dropna()
    
    # Simulation variables
    cash = 0
    shares = 0
    total_invested = 0
    portfolio_value = []
    invested_cash_over_time = []
    
    last_income_date = None
    
    for date, row in data.iterrows():
        # Add monthly income on the first day of each month
        if last_income_date is None or date.month != last_income_date.month:
            cash += monthly_income
            total_invested += monthly_income
            last_income_date = date
        
        if date in purchase_schedule.index:
            # Calculate purchase amount
            price = row['Close'].iloc[0]
            investable_amount = cash
            fee = max(min_fee, investable_amount * percentage_fee)
            investable_amount -= fee

            if investable_amount > price:  # Ensure enough cash to buy at least 1 share
                shares_bought = investable_amount // price
                cash -= shares_bought * price + fee
                shares += shares_bought

        # Track portfolio value
        total_value = cash + shares * price
        portfolio_value.append((date, total_value, cash, shares))
        invested_cash_over_time.append((date, total_invested))

        
    # Convert results to a DataFrame
    portfolio_df = pd.DataFrame(portfolio_value, columns=['Date', 'Portfolio Value', 'Cash', 'Shares'])
    portfolio_df.set_index('Date', inplace=True)
    invested_cash_df = pd.DataFrame(invested_cash_over_time, columns=['Date', 'Invested Cash'])
    invested_cash_df.set_index('Date', inplace=True)
    return portfolio_df, invested_cash_df


def get_yearly(change, years):
    return (change + 1) ** (1 / years) - 1


def plot(data, portfolio_df, invested_cash_df):
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_df['Portfolio Value'], label='Portfolio Value', color='red')
    plt.plot(invested_cash_df['Invested Cash'], label='Invested Cash', color='blue')
    # plt.plot(data['Close'], label='Stock Price', color='green')
    plt.title(f'Portfolio Simulation for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()






# Define parameters
ticker = "SPYL.AS"  # Stock ticker
monthly_income = 400  # Monthly income for investment
frequency = 4  # Frequency of purchases in weeks
min_fee = 4.0  # Minimum fee for each transaction
percentage_fee = 0.0029  # Percentage fee (1%)
start_date = "2023-01-01"
end_date = "2025-01-20"
years = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days / 365.0




data = get_data(ticker, start_date, end_date)
portfolio_df, invested_cash_df = backtest(data, monthly_income, frequency)

total_return = (portfolio_df['Portfolio Value'].iloc[-1] / invested_cash_df['Invested Cash'].iloc[-1] - 1)
annualized_return = get_yearly(total_return, years)

print(f"\n\nFinal Portfolio Value after {years:.2f} years:", f"{portfolio_df['Portfolio Value'].iloc[-1]:.2f}", f"Return: {total_return*100:.2f}%", f"({annualized_return*100:.2f}%)\n\n")

plot(data, portfolio_df, invested_cash_df)