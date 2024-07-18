import numpy as np
import matplotlib.pyplot as plt

# Generate a 1 kHz sine wave with noise
fs = 10_000  # Sampling frequency (Hz)
t = np.linspace(0, 1, fs, endpoint=False)
signal = np.sin(2 * np.pi * 1000 * t) + np.random.normal(0, 0.5, len(t))

# Compute the FFT of the signal
fft_result = np.fft.fft(signal)
freq = np.fft.fftfreq(len(t), d=1/fs)

# Design a bandpass filter
filter_wide = 10
max_signal_freq = np.abs(freq[np.argmax(np.abs(fft_result))])
lowcut, highcut = max_signal_freq-filter_wide, max_signal_freq+filter_wide  # Frequency range (Hz)
sig_rfft_filtered = fft_result.copy()
sig_rfft_filtered[(freq < lowcut) | (freq > highcut)] = 0
sig_lfft_filtered = fft_result.copy()
sig_lfft_filtered[(-freq < lowcut) | (-freq > highcut)] = 0
sig_fft_filtered = sig_rfft_filtered + sig_lfft_filtered
# get the filtered signal in time domain
filtered_signal = np.fft.ifft(sig_fft_filtered)


# Plot the original signal, FFT, and filtered signal
plt.figure(figsize=(10, 6))
plt.subplot(4, 1, 1)
plt.plot(t, signal, label='Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(freq, np.abs(fft_result), label='FFT original')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 300)
plt.xlim(0, 2000)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(t, filtered_signal, label='Filtered Signal') # mulltiply 2 for bout sides
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0.10, 0.20)
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(freq, np.abs(sig_fft_filtered), label=f'FFT filtered wide {filter_wide} hz') # mulltiply 2 for bout sides
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.ylim(0, 300)
plt.xlim(0, 2000)
plt.legend()

plt.tight_layout()
plt.show()
