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
        print (difference)
        return difference

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


############# RUN THE CODE ################
# Live update of the values # replicates what the server does !!!
# https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
def plot_cont(xmax):
    y = []
    y_5_day_moving_averages = []
    y_10_day_moving_averages = []
    y_30_day_moving_averages = []

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

        y_5_day_momentum = getCurrentMomentum(i, 5)
        y_10_day_momentum = getCurrentMomentum(i, 10)
        y_30_day_momentum = getCurrentMomentum(i, 30)

        y_5_day_momentums.append(y_5_day_momentum)
        y_10_day_momentums.append(y_10_day_momentum)
        y_30_day_momentums.append(y_30_day_momentum)

        x = range(len(y))
        ax[0].clear()
        ax[0].plot(x, y)
        ax[0].plot(x, y_5_day_moving_averages)
        ax[0].plot(x, y_10_day_moving_averages)
        ax[0].plot(x, y_30_day_moving_averages)

        ax[1].axhline(y = 0, color = 'r')
        ax[1].plot(x, y_5_day_momentums, color = 'purple')
        ax[1].plot(x, y_10_day_momentums, color = 'g')
        ax[1].plot(x, y_30_day_momentums, color = 'b')


    a = anim.FuncAnimation(fig, update, frames=xmax, repeat=False)
    plt.show()

x = ethereumData['Date']

plot_cont(len(x))
# i want to graph the price per day and have the moving average