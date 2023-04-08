from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, lfilter, freqz
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def plot_filter(ax1, ax2, cutoff):

    # Setting standard filter requirements.
    order = 6
    fs = 44000
    #cutoff = 50  # fs/2>cutoff

    b, a = butter_lowpass(cutoff, fs, order)

    # Plotting the frequency response.
    w, h = freqz(b, a, worN=8000)
    ax1.semilogx(0.5 * fs * w / np.pi, np.abs(h), 'b')
    ax1.semilogx(cutoff, 0.5 * np.sqrt(2), 'ko')
    ax1.axvline(cutoff, color='k')
    plt.xlim(0, 5000)
    plt.xlabel('Frequency [Hz]')
    ax1.grid()

    # Creating the data for filtration
    T = 5.0  # value taken in seconds
    n = int(T * fs)  # indicates total samples
    t = np.linspace(0, T, n, endpoint=False)

    data = np.sin(1.2 * 2 * np.pi * t) + 1.5 * np.cos(9 * 2 * np.pi * t) + 0.5 * np.sin(12.0 * 2 * np.pi * t)

    # Filtering and plotting
    y = butter_lowpass_filter(data, cutoff, fs, order)

    ax2.plot(t, data, 'b-', label='data')
    ax2.plot(t, y, 'g-', linewidth=2, label='filtered data')
    plt.xlabel('Time [sec]')
    plt.xlim(0, T)
    ax2.grid()
    ax2.legend()
    return()
# plt.subplots_adjust(hspace=0.35)
# plt.show()

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
# btype{‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}, optional
# The type of filter. Default is ‘lowpass’.