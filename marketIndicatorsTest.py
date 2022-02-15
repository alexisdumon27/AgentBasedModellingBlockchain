from numpy.core.numeric import moveaxis
from numpy.lib.function_base import diff
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as anim

import numpy
from numpy import linspace, loadtxt, ones, convolve

ethereumData = pd.read_csv('cleanedEuthereumData.csv')

# https://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
def movingaverage(interval, window_size):
    window= numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')

def getCurrentMomentum(round, window):
    """
        calculate the difference over a constant 5-day period for a 5-day rate of change.
    """
    if round < window:
        return None
    else:
        difference = getCurrentPrice(round) - getCurrentPrice(round - window)
        return difference

# uses Ethereum data directly
def getCurrentPrice(round):
    return ethereumData['USD/ETH'].values[round]

def get_X_day_moving_average(round, window):
    if round < window:
        return None
    else:
        total = 0
        for i in range(window):
            total += getCurrentPrice(round - i)
        return total / window

def filter(flag, period, increase, decrease, boolean):

    return 0

# RULES TO IMPLEMENT #
"""
    for OPENING
    1. filter
    2. EMA
    3. MACD
    4. RSI
    5. 5-day moving average <-- implemented

    for CLOSING
    1. fixed exit level
    2. trailing exit levels
"""

test_set = [22.27, 22.19, 22.08, 22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61, 23.36, 24.05, 23.75, 23.83, 23.95, 23.63, 23.82, 23.87, 23.65, 23.19, 23.1, 23.33, 22.68, 23.1, 22.4, 22.17]

# exponential moving average
# https://www.investopedia.com/terms/e/ema.asp
# https://towardsdatascience.com/trading-toolbox-02-wma-ema-62c22205e2a9
def getEMA(round, window):
    ema10 = ethereumData['USD/ETH'].ewm(span = window, adjust= False).mean()
    df = pd.DataFrame()
    df["ema"] = numpy.round(ema10, decimals = 3)
    return df["ema"].values[round]

# Moving average Convergence Divergence
# https://www.investopedia.com/terms/m/macd.asp
def getMACD(round):
    return getEMA(round, 12) - getEMA(round, 26)

############# RUN THE CODE ################
# Live update of the values # replicates what the server does !!!
# https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
def plot_cont(xmax):
    y = []
    y_5_day_moving_averages = []
    y_10_day_moving_averages = []
    y_30_day_moving_averages = []

    y_10_day_exponential_moving_averages = []

    y_macds = []

    y_5_day_momentums = []
    y_10_day_momentums = []
    y_30_day_momentums = []
    fig, ax = plt.subplots(2, 1)

    def update(i):
        y_price = getCurrentPrice(i)
        y.append(y_price)

        y_5_ma = get_X_day_moving_average(i, 5)
        y_10_ma = get_X_day_moving_average(i, 10)
        y_30_ma = get_X_day_moving_average(i, 30)
        y_5_day_moving_averages.append(y_5_ma)
        y_10_day_moving_averages.append(y_10_ma)
        y_30_day_moving_averages.append(y_30_ma)

        y_10_ema = getEMA(i, 10)
        y_10_day_exponential_moving_averages.append(y_10_ema)

        y_macd = getMACD(i)
        y_macds.append(y_macd)

        y_5_day_momentum = getCurrentMomentum(i, 5)
        y_10_day_momentum = getCurrentMomentum(i, 10)
        y_30_day_momentum = getCurrentMomentum(i, 30)
        y_5_day_momentums.append(y_5_day_momentum)
        y_10_day_momentums.append(y_10_day_momentum)
        y_30_day_momentums.append(y_30_day_momentum)

        x = range(len(y))
        ax[0].clear()
        ax[0].plot(x, y)
        ax[0].plot(x, y_5_day_moving_averages, ls = "-")
        ax[0].plot(x, y_10_day_moving_averages, ls = "-")
        ax[0].plot(x, y_30_day_moving_averages, ls = "-")
        ax[0].plot(x, y_10_day_exponential_moving_averages, color = "black", ls = ":")

        ax[1].axhline(y = 0, color = 'r')
        ax[1].plot(x, y_5_day_momentums, color = 'purple')
        ax[1].plot(x, y_10_day_momentums, color = 'g')
        ax[1].plot(x, y_30_day_momentums, color = 'b')
        ax[1].plot(x, y_macds, color = 'black')



    a = anim.FuncAnimation(fig, update, frames=xmax, repeat=False)
    plt.show()

x = ethereumData['Date']

# plot_cont(len(x))

"""
The stock is said to be OVERBOUGHT when the
momentum oscillator reaches an extreme upper level
above the zero line and OVERSOLD when it reaches an
extreme lower level below the zero line. 

"""