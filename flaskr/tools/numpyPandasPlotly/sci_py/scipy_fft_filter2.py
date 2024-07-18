import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

# Generate a 1 kHz sine wave with noise
fs = 10000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
signal = np.sin(2 * np.pi * 1000 * t) + np.random.normal(0, 0.5, len(t))

# Compute the FFT of the signal
fft_result = np.fft.rfft(signal)
freq = np.fft.rfftfreq(len(t), d=1/fs)

max_signal_freq = freq[np.argmax(np.abs(fft_result))]

# Design a bandpass filter
lowcut, highcut = max_signal_freq-10, max_signal_freq+10  # Frequency range (Hz)
order = 4  # Filter order
nyq = 0.5 * fs
low = lowcut / nyq
high = highcut / nyq
b, a = butter(order, [low, high], btype='band')

# Apply the filter
filtered_signal = lfilter(b, a, signal)

# Plot the original signal, FFT, and filtered signal
plt.figure(figsize=(10, 6))
plt.subplot(4, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(freq, np.abs(fft_result), label='rFFT')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 300)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(t, filtered_signal, label='Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

# Compute the FFT of the signal
fft_result2 = np.fft.rfft(filtered_signal)
freq = np.fft.rfftfreq(len(t), d=1/fs)

plt.subplot(4, 1, 4)
plt.plot(freq, np.abs(fft_result2), label='rFFT filtered')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 300)
plt.legend()

plt.tight_layout()
plt.show()
