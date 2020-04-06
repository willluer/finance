import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10, 5]

def get_ticker_data(ticker_symbols,start_date,end_date):
    ticker_data_dict = {}
    for ticker in ticker_symbols:
        #get data on this ticker
        tickerData = yf.Ticker(ticker)

        #get the historical prices for this ticker
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

        #see your data
        ticker_data_dict[ticker] = tickerDf
    return ticker_data_dict

# expects columns to be ticker, data to be closing prices
def plot_data(df,title):
    df.plot()
    plt.grid()
    plt.title(title)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.show()

def plot_daily_returns(df,title,start,end):
    df[start:end].plot()
    plt.title(title)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.grid()
    plt.show()

# Normalize df
def normalize_df(df):
    return df/df.iloc[0,:]

# Computes daily returns for dataframe of a single or multiple stocks
def compute_daily_returns(df):
    returns = df.copy()
    # df[1:] gets all but first index
    # df[:-1] gets all but last index
    returns[1:] = (df[1:].values/df[:-1].values) - 1
    returns.iloc[0,:] = 0 # b/c no "previous" data for first day
    return returns

# Plot histogram and calculate kurtosis
def plot_hist(df):
    df.plot.hist(bins=50)
    kurtosis=df.kurtosis()
    plt.title("{} daily return histogram. Kurtosis={:.2f}".format(ticker,kurtosis))
    plt.show()

# Returns upper and lower bands, and rolling mean
def calculate_bollinger_bands(df):
    rolling_windows = df.rolling(20, min_periods=20)
    rolling_mean = rolling_windows.mean().dropna()
    rolling_std = rolling_windows.std().dropna()
    upper = rolling_mean + (2 * rolling_std)
    lower = rolling_mean - (2 * rolling_std)
    return upper,lower,rolling_mean

def plot_bollinger(data,bands,title):
    data.plot()
    upper,lower,rm = bands

    upper.plot(color="r")
    lower.plot(color="r")
    rm.plot(color="k")

    plt.title(title)
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.grid()
    plt.show()

def compute_cumulative_return(df,allocations):
    cr = df.dot(allocations).rename("CR") # Need to add name to Series
    return cr.to_frame()

def compute_sharpe_ratio(daily_returns,K=252):
    import math
    mean_daily = daily_returns.mean(axis=0) # Portfolio returns
    std_daily = daily_returns.std(axis=0) # Portfolio std
    sr = math.sqrt(K) * ((mean_daily) / std_daily)
    return sr

def get_closing_prices(df,normalized=True):
    # Get closing prices DF
    closing_prices = pd.DataFrame()
    for ticker in df:
        closing_prices[ticker] = df[ticker]["Close"]

    if normalized:
        return normalize_df(closing_prices)

    return closing_prices

def get_cumulative_return(df):
    return df["CR"][-1] - df["CR"][0]

# Input: tickers, portfolio allocation, start date, end date
# Output: Cumulative return, Sharpe Ratio, Volatility, Average daily return
def assess_portfolio(tickers,allocations,start_date,end_date,plot=False):
    closing_prices = get_closing_prices(get_ticker_data(tickers,start_date,end_date),normalized=True)
    cumulative_returns = compute_cumulative_return(closing_prices,allocations)
    daily_returns = compute_daily_returns(cumulative_returns)
    sharpe_ratio = compute_sharpe_ratio(daily_returns)
    cr = get_cumulative_return(cumulative_returns)
    vol = daily_returns["CR"].std()
    avg = daily_returns["CR"].mean()

    print("Sharpe Ratio: {}".format(sharpe_ratio))
    print("Volatility (daily std): {}".format(vol))
    print("Average Daily Return: {}".format(avg))
    print("Cumulative Return: {}".format(cr))

    if plot:
        spy = get_closing_prices(get_ticker_data(["SPY"],start_date,end_date),normalized=True)
        data = spy.join(cumulative_returns["CR"])
        plot_data(data,"SPY and Portfolio returns")

    return sharpe_ratio,cr,vol,avg
