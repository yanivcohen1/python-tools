import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft
import numbers

# tack only columns ['Timestamp (Hour Ending)', 'Demand (MWh)']
df = pd.read_csv('flaskr/tools/numpyPandasPlotly/930-data-export.csv',
        delimiter=',', parse_dates=[0], usecols=['Timestamp (Hour Ending)', 'Demand (MWh)'])

df.rename(columns={'Timestamp (Hour Ending)':'hour',
                    'Demand (MWh)':'demand'},
          inplace=True)

# remove NaN
df = df[df['demand'].notna()]
# df[["hour"]] = df[["hour"]].apply(pd.to_datetime)
# df[["demand"]] = df[["demand"]].apply(pd.to_numeric)

# filter dates
start_date = '2024-04-06'
end_date = '2024-04-14'
df = df.loc[(df['hour'] >= start_date) & (df['hour'] <= end_date)]

plt.figure(figsize = (10, 5))
plt.plot(df['hour'], df['demand'])
plt.xlabel('Datetime')
plt.ylabel('California electricity demand (MWh)')
plt.xticks(rotation=25) # tilte the x label in 25 dgree
plt.show()

X = fft(df['demand'])
N = len(X)
n = np.arange(N)
# get the sampling rate
sr = 1 / (60*60)
T = N/sr
freq = n/T

# Get the one-sided specturm
n_oneside = N//2
# get the one side frequency
f_oneside = freq[:n_oneside]

plt.figure(figsize = (10, 5))
plt.plot(f_oneside, np.abs(X[:n_oneside]), 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.show()

# convert frequency to hour
t_h = 1/f_oneside / (60 * 60)

plt.figure(figsize=(10,5))
plt.plot(t_h, np.abs(X[:n_oneside])/n_oneside)
plt.xticks([12, 24, 48, 84, 168])
plt.xlim(0, 200)
plt.xlabel('Period ($hour$)')
plt.show()


# ------------ panda from csv

print(pd.to_datetime(['2018-10-26 12:00 -0530', '2018-10-26 12:00 -0500'],
                utc=True)[0]) # print in utc: 2018-10-26 17:30:00+00:00
# -------- panda for table data menipulation -------------------
csv = {
  "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
  "Profit": [200, 300, 400, 500, 600, 700],
  'time': [1, 2, 3],
}

table = pd.DataFrame(csv, columns=['Month', 'Sales', "Profit"])# option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.head(3))
#   Month  Sales  Profit
# 0   Jan   1000     200
# 1   Feb   1200     300
# 2   Mar   1500     400
