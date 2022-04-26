import pandas as pd
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq
import matplotlib.pyplot as plt


def mode_extract(startTime, endTime, folderName, dt, window, ax, _param, which='upper'):
    '''
    Input:
    endTime: the last time step of the csv files
    folderName: name of the folder that contains the lift files
    dt: time step of the output files of the simulations
    numModes: number of first n modes to be displayed
    '''

    start = startTime
    end = endTime
    steps = np.arange(0, end-start+1)
    Time = np.zeros_like(steps,dtype=float)
    Lift = np.zeros_like(steps,dtype=float)

    for i in steps:

        # df = pd.read_csv(folderName + '/drag_' + str(i+start) + '.csv')
        df = pd.read_csv(folderName + str(i+start) + '.csv')
        t = df['Time'][0]
        # L = np.sum(df['Drag'])
        L = np.sum(df[_param])
        Time[i] = t
        Lift[i] = L

    N = end-start+1
    _lift = fft(Lift)
    _freq = np.linspace(0, 1/dt, N)
    
    ax[0].plot(_freq[:N//2], np.abs(_lift[:N//2]), marker='.', label=which) # 2nd half is just a mirror image of the first half 

    ####### Plot some frequencies of corresponding strouhal numbers ################
    _L = 0.034641
    _u = 16.6
    f_st = lambda st: st*_u/_L
    f_st_vec = np.vectorize(f_st)

    strouhals = np.arange(0.1, 0.3+0.01, 0.05)
    print(strouhals)
    freqs = f_st_vec(strouhals)
    if which == 'upper':
        for i in np.arange(strouhals.shape[0]):
            ax[0].plot([freqs[i],freqs[i]], [0, 1.5*sorted(set(np.abs(_lift[:N//2])))[-2]], label=str(np.round(strouhals[i],3)))

    #################################################################################

    _lift_sort = np.array(sorted(np.abs(_lift[:N//2]), reverse=True))
    loc = np.nonzero(np.round(_lift_sort[1:10],5)[:,None] == np.round(np.abs(_lift[:N//2]),5))[1]
    modes = _freq[loc]
    print(modes)


    freq = fftfreq(N, dt)
    _lift_mean = _lift.copy()
    _lift_mean[np.abs(freq) > 1] = 0
    # _lift_mean[np.abs(freq) < 0.001] = 127000 ## to correct the mean for the LES

    _lift_filtered1 = _lift.copy()
    _lift_filtered1[np.abs(freq) > modes[0]+window+1] = 0
    _lift_filtered1[np.abs(freq) < modes[0]-window-1] = 0
    filtered1 = ifft(_lift_mean+_lift_filtered1)

    for j in range(1,len(modes)+1):
        if np.abs(modes[j] - modes[0]) > window:
            mode2 = modes[j]
            last = j
            break

    _lift_filtered2 = _lift.copy()
    _lift_filtered2[np.abs(freq) > mode2+window+1] = 0
    _lift_filtered2[np.abs(freq) < mode2-window-1] = 0
    filtered2 = ifft(_lift_mean+_lift_filtered1+_lift_filtered2)

    for j in range(last+1,len(modes)+1):
        if np.abs(modes[j] - mode2) > window and np.abs(modes[j] - modes[0]) > window :
            mode3 = modes[j]
            # last = j
            break

    _lift_filtered3 = _lift.copy()
    _lift_filtered3[np.abs(freq) > mode3+window+1] = 0
    _lift_filtered3[np.abs(freq) < mode3-window-1] = 0
    filtered3 = ifft(_lift_mean+_lift_filtered1+_lift_filtered2+_lift_filtered3)
    print('modes:', modes[0], mode2, mode3)

    ax[1].plot(Time, Lift, marker='.', alpha=0.5, label=which + ': true data')

    ax[1].plot(Time, filtered1, alpha=0.8, label=which +': 1st mode')
    # ax[1].plot(Time, filtered2, alpha=0.8, label=which +': 1st+2nd mode')
    # ax[1].plot(Time, filtered3, alpha=0.8, label=which+': 1st+2nd+3rd mode')

    ax[0].legend()  
    ax[1].legend()

    return 



####### for LES

fig1, ax1 = plt.subplots(2,1)
fig1.suptitle('LES new')
# mode_extract(0,492, 'LESdragTop/drag_', 0.00025, 9, ax1, 'upper')
# mode_extract(0,492, 'LESdragBot/drag_', 0.00025, 9, ax1, 'lower')

mode_extract(0,492, 'LESLiftData/Lift_', 0.00025, 9, ax1, 'Lift', 'lower')

###### for PANS fk=0.2

# fig, ax = plt.subplots(2,1)
# fig.suptitle('PANS fk=0.2')
# mode_extract(130, 300, 'PANSdrag_low/drag_', 0.001, 12, 'lower')
# mode_extract(130, 300, 'PANSdrag_up/drag_', 0.001, 12, 'upper')


###### for PANS fk=0.4

# fig2, ax2 = plt.subplots(2,1)
# fig2.suptitle('PANS fk=0.4')
# mode_extract(0, 164, 'PANS04_bot/Drag_', 0.001, 12, ax2, 'Drag','lower')
# mode_extract(0, 164, 'PANS04_top/Drag_', 0.001, 12, ax2, 'Drag', 'upper')


###### for SST

# fig, ax = plt.subplots(2,1)
# fig.suptitle('SST')
# mode_extract(0, 229, 'SSTdrag_bot/drag_', 0.001, 12, 'lower')
# mode_extract(0, 229, 'SSTdrag_top/drag_', 0.001, 12, 'upper')


plt.show()
