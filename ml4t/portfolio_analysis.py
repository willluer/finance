import datetime as dt
from utils import *
if __name__ == "__main__":
    # Example 1
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    tickers = ['GOOG', 'AAPL', 'GLD', 'XOM']
    alloc = [0.2, 0.3, 0.4, 0.1]
    assess_portfolio(tickers,alloc,start_date,end_date,plot=True)
    print()
    # Example 2
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    tickers = ['AXP', 'HPQ', 'IBM', 'HNZ']
    alloc = [0.0, 0.0, 0.0, 1.0]
    assess_portfolio(tickers,alloc,start_date,end_date,plot=True)
    print()

    # Example 3
    start_date = dt.datetime(2010,6,1)
    end_date = dt.datetime(2010,12,31)
    tickers = ['GOOG', 'AAPL', 'GLD', 'XOM']
    alloc = [0.2, 0.3, 0.4, 0.1]
    assess_portfolio(tickers,alloc,start_date,end_date,plot=True)
