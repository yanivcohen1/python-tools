import matplotlib.pyplot as plt
import numpy as np
# from numpy.fft import fft, ifft
from scipy.fftpack import fft, ifft, fftfreq

sr = 2_000
# sampling interval
ts = 1.0/sr
t = np.arange(0,1,ts)

# generate forye serial of 3 freq 1. 4 7 and add them
freq = 1.
x = 3*np.sin(2*np.pi*freq*t)

freq = 4
x += np.sin(2*np.pi*freq*t)

freq = 7
x += 0.5* np.sin(2*np.pi*freq*t)

# FFT the signal
sig_fft = fft(x)
# copy the FFT results
sig_fft_filtered = sig_fft.copy()

# obtain the frequencies using scipy function
freq = fftfreq(len(x), d=1./2000)

# define the cut-off frequency
cut_off = 6

# high-pass filter by assign zeros to the
# FFT amplitudes where the absolute
# frequencies smaller than the cut-off
sig_fft_filtered[np.abs(freq) < cut_off] = 0

# get the filtered signal in time domain
filtered = ifft(sig_fft_filtered)

# plot the filtered signal
plt.figure(figsize = (10, 7))
plt.subplot(3, 1, 1)
plt.plot(t, 2*filtered, label="filter signal") # mull 2 for two sides
plt.plot(t, x, label="Original signal")
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
# plt.show()

# plot the FFT amplitude before and after
plt.subplot(3, 1, 2)
# plt.subplot(121)
plt.stem(freq, np.abs(sig_fft), 'b', \
         markerfmt=" ", basefmt="-b")
plt.title('Before filtering')
plt.xlim(0, 10)
plt.xlabel('Frequency (Hz)')
plt.ylabel('FFT Amplitude')

plt.subplot(3, 1, 3)
# plt.subplot(122)
plt.stem(freq, np.abs(sig_fft_filtered), 'b', \
         markerfmt=" ", basefmt="-b")
plt.title('After filtering')
plt.xlim(0, 10)
plt.xlabel('Frequency (Hz)')
plt.ylabel('FFT Amplitude')
plt.tight_layout()
plt.show()
