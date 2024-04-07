import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft

df = pd.read_csv('flaskr/tools/numpyPandasPlotly/930-data-export.csv',
                 delimiter=',', parse_dates=[1])
df.rename(columns={'Selected Hour Timestamp (Hour Ending)':'hour',
                   'Selected Hour Demand (MWh)':'demand'},
          inplace=True)

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
