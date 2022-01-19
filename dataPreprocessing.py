import numpy
import math
import csv
import pandas as pd
from pandas import read_csv
import sys
from datetime import datetime


euthereumDatafile = pd.read_csv('ethereum2021data(incomplete).csv')

euthereumDatafile.drop(euthereumDatafile.columns.difference(['timestamp', 'open']), 1, inplace=True)

def timestampToDate(x):
    return datetime.fromtimestamp(x).date().strftime("%Y-%m-%d")

euthereumDatafile.rename(columns={'timestamp':'Date', 'open': 'USD/ETH'}, inplace=True)

euthereumDatafile['Date'] = euthereumDatafile['Date'].apply(timestampToDate)

euthereumDatafile.drop_duplicates(subset=['Date'], keep='first', inplace=True)

euthereumDatafile = euthereumDatafile.reindex(index=euthereumDatafile.index[::-1])

euthereumDatafile.reset_index(drop = True, inplace=True)

euthereumDatafile.to_csv('cleanedEuthereumData.csv')