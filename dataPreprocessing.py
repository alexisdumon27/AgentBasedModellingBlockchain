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
    return datetime.fromtimestamp(x).date()

euthereumDatafile.rename(columns={'open': 'USD/ETH'}, inplace=True)

euthereumDatafile['timestamp'] = euthereumDatafile['timestamp'].apply(timestampToDate)

euthereumDatafile.drop_duplicates(subset=['timestamp'], keep='first', inplace=True)

euthereumDatafile = euthereumDatafile.reindex(index=euthereumDatafile.index[::-1])

euthereumDatafile.reset_index(drop = True, inplace=True)

euthereumDatafile.to_csv('cleanedEuthereumData.csv')