import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def backtest(monthly_income, ticker, start_date, end_date, interval='1d'):
    sub_interval = int(interval[0])
    interval = "1" + interval[1:]
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    
    # Simulation variables
    cash = 0
    shares = 0
    total_invested = 0
    portfolio_value = []
    invested_cash_over_time = []
    interval_income = monthly_income / ({"1d": 30.4375, "1wk": 4.3482142857, "1mo": 1}[interval] / sub_interval)
    sub_interval_index = 0
    
    for date, row in data.iterrows():
        sub_interval_index += 1
        sub_interval_index %= sub_interval
        if sub_interval_index != 0:
            continue
        
        price = row['Close'].iloc[0]
        cash = interval_income
        total_invested += cash
        
        fee = max(min_fee, cash * percentage_fee)
        shares += (cash - fee) / price
        
        # Track portfolio value
        total_value = shares * price
        portfolio_value.append((date, total_value, shares))
        invested_cash_over_time.append((date, total_invested))

    # Convert results to a DataFrame
    portfolio_df = pd.DataFrame(portfolio_value, columns=['Date', 'Portfolio Value', 'Shares'])
    portfolio_df.set_index('Date', inplace=True)
    invested_cash_df = pd.DataFrame(invested_cash_over_time, columns=['Date', 'Invested Cash'])
    invested_cash_df.set_index('Date', inplace=True)
    return portfolio_df, invested_cash_df


def get_yearly(change, years):
    return (change + 1) ** (1 / years) - 1


def plot_show():   
    plt.title(f'Back test for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Return [%]')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    

def run(intervals):
    plt.figure(figsize=(13, 7))
    plt.margins(x=0.01, y=0.01)
    colors = ["blue", "red", "green", "orange", "purple", "brown", "gray", "olive", "cyan"]
    for index, interval in enumerate(intervals):
        portfolio_df, invested_cash_df = backtest(monthly_income, ticker, start_date, end_date, interval=interval)
        plt.plot(100*portfolio_df["Portfolio Value"]/invested_cash_df["Invested Cash"]-100, label=f"Buy interval {interval}", color=colors[index])



# Define parameters
ticker = "SPY"                      # Stock ticker
monthly_income = 400                # Monthly income for investment
min_fee = 4.0                       # Minimum fee for each transaction
percentage_fee = 0.0029             # Percentage fee for each transaction
intervals = ["1mo", "2mo", "3mo", "4mo"]    # Buy intervals to test
start_date = "1995-01-01"           # Start date for backtest
end_date = "2025-02-01"             # End date for backtest

# years = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days / 365.25


run(intervals)
plot_show()