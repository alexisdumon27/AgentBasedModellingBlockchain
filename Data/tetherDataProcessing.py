import pandas as pd
from pandas import read_csv
from datetime import datetime


tetherDatafile = pd.read_csv('USDT-USD.csv')

tetherDatafile.drop(tetherDatafile.columns.difference(['Date', 'Open']), 1, inplace=True)

tetherDatafile.rename(columns={'Open': 'USD/USDT'}, inplace=True)

tetherDatafile.to_csv('cleanedTetherData.csv', index = False)