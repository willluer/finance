import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from utils import *
import datetime as dt
import matplotlib.pyplot as plt

def portfolio_optimization_fn(allocations,df):
    cumulative_returns = compute_cumulative_return(df,allocations)
    dr = compute_daily_returns(cumulative_returns)
    sh = compute_sharpe_ratio(dr)
    return -sh[0]

tickers = ["SPY","GLD"]
start_date = dt.datetime(2010,1,1)
end_date = dt.datetime(2010,12,31)

data = get_closing_prices(get_ticker_data(tickers,start_date,end_date),normalized=True)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = y = np.arange(0.0, 1.0, 0.005)
X, Y = np.meshgrid(x, y)
zs = np.array([portfolio_optimization_fn([x, y],data) for x,y in zip(np.ravel(X), np.ravel(Y))])

Z = zs.reshape(X.shape)
for i in range(len(X)):
    for j in range(len(X[i])):
        if not abs(X[i][j] + Y[i][j] - 1) < 0.001:
            X[i][j] = None
            Y[i][j] = None
            Z[i][j] = None

# ax.plot_surface(X, Y, -Z)
ax.scatter(X, Y, -Z)

ax.set_xlabel(tickers[0])
ax.set_ylabel(tickers[1])
ax.set_zlabel("Sharpe Ratio")
ax.set_title("Sharpe Ratio for Two Stock Portfolio Allocation")
plt.show()
