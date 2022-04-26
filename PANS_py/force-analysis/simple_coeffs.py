from gettext import npgettext


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq

df = pd.read_csv('SSTcoeffs.csv')

t = df['Time'].to_numpy()
# drag = df['Drag'].to_numpy()
lift = df['Lift'].to_numpy()


plt.figure()
plt.plot(t,lift,label='lift')
# plt.plot(t,drag,label='drag')
plt.legend()

# plt.show()
dt = 0.001
N = t.shape[0]
_lift = fft(lift)
# _drag = fft(drag)
_freq = np.linspace(0, 1/dt, N)

plt.figure()
plt.plot(_freq[:N//2], np.abs(_lift[:N//2]), marker='.', label='lift')
# plt.plot(_freq[:N//2], np.abs(_drag[:N//2]), marker='.', label='drag')
plt.legend()

plt.show()