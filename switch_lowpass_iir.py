# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 01:05:14 2017

@author: wattai
"""

from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    fs = 1000
    T = 10
    t = np.linspace(0, fs*T-1, fs*T)/fs
    x = np.sin(2*np.pi*1*t) + 0.5*np.random.randn(len(t))
    x = np.concatenate((np.zeros(len(t)//2), np.ones(len(t)//2)))
    # x[len(t)//2 -200: len(t)//2 -100] = 1
    # x[len(t)//2 +500: len(t)//2 +550] = 0

    wp = 0.5 / (fs/2)
    ws = 1.0 / (fs/2)
    gpass = 1
    gstop = 3
    b, a = sig.iirdesign(wp, ws, gpass, gstop,
                         analog=False, ftype='butter', output='ba')

    y = np.zeros(len(t))
    for k in range(len(t)):
        y[k] = b[0]*x[k] + b[1]*x[k-1] - a[1]*y[k-1]
        if y[k] > 0.95 and y[k-1] <= 0.95:
            print('t = %3f is 0.95/1.00 charging time!!' % (t[k]-t[len(t)//2]))

    plt.figure()
    plt.subplot(211)
    plt.plot(t, x)
    plt.ylabel('amplitude')
    plt.ylim(0-0.1, 1+0.1)
    plt.grid(True)
    plt.subplot(212)
    plt.plot(t, y)
    plt.xlabel('time [sec]')
    plt.ylabel('amplitude')
    plt.ylim(0-0.1, 1+0.1)
    plt.grid(True)
    plt.show()

    plt.figure()
    w, h = sig.freqz(b, a)
    plt.plot(w/(2*np.pi)*fs, 20 * np.log10(abs(h)))
    plt.ylabel('amplitude [dB]')
    plt.xlabel('frequency [Hz]')
    plt.grid(True)
    plt.show()
