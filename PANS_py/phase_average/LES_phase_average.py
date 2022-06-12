import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
from scipy.fftpack import fft, ifft, fftfreq

'''
This program aims to average LES data over each phase thus ultimately ending up with a data set of 1 single phase
This single phase will include 'res' number of points, excluding the last root (zero)
'''

res = 100
x_range = np.linspace(0.05, 0.4, 4)
foldername = 'slice_avg_time_varying_k/' 
paramfile = 'LESparams_'

def phase_avg_params_LES(res, foldername, paramfile):
    '''
    Input:
        foldername: name of the paramater file containing folder including '/' at the end
        paramfile: name of the file uptil the number which represents the timestep number
    
    '''
    # start, end and dt are fixed for LES dataset
    start = 0
    end = 492
    steps = np.arange(0, end-start+1)
    Time = np.zeros_like(steps,dtype=float)
    Lift = np.zeros_like(steps,dtype=float)
    dt = 0.00025

    for i in steps:

        df = pd.read_csv('LESLiftData/Lift_' + str(i+start) + '.csv')
        t = df['Time'][0]
        L = np.sum(df['Lift'])
        Time[i] = t
        Lift[i] = L

    N = end-start+1
    _lift = fft(Lift)
    _freq = np.linspace(0, 1/dt, N)
    FFTlift = np.abs(_lift[:N//2])
    FFTfreq = _freq[:N//2]

    fig,ax = plt.subplots()
    ax.plot(FFTfreq, FFTlift, marker='.') # 2nd half is just a mirror image of the first half 

    ####### Plot some frequencies of corresponding strouhal numbers ################
    # _L = 0.034641
    # _u = 16.6
    # f_st = lambda st: st*_u/_L
    # f_st_vec = np.vectorize(f_st)

    #################################################################################

    FFTlift_sort = np.array(sorted(FFTlift, reverse=True)) # descending order
    loc = np.nonzero(np.round(FFTlift_sort[:10],5)[:,None] == np.round(FFTlift,5))[1]
    modes = _freq[loc]
    # print(modes)
    meanfreq = modes[0]
    domfreq = modes[1]
    print('Dominant frequency mode:', domfreq)
    period = 1/domfreq

    freq = fftfreq(N, dt)
    _lift_mean = _lift.copy()
    _lift_mean[np.abs(freq) > 1] = 0
    meanlift = ifft(_lift_mean)

    _lift_filtered1 = _lift.copy()
    _lift_filtered1[np.abs(freq) > domfreq+1] = 0
    _lift_filtered1[np.abs(freq) < domfreq-1] = 0
    filtered1 = ifft(_lift_mean+_lift_filtered1)

    Lift = np.real(Lift)
    Lift0 = Lift - np.mean(Lift)

    plt.figure()
    plt.plot(Time, Lift0, marker='.', alpha=0.5, label='true data')
    # plt.plot(Time, filtered1, alpha=0.8, label='1st mode')

    liftfunc = interp1d(Time, Lift0, 'quadratic', fill_value='extrapolate')

    num_zeros = 30
    xguess = np.array([0.1772, 0.1814, 0.1856, 0.1897, 0.1941, 0.1985, 0.2022, 0.2064,\
         0.2102, 0.2141, 0.2181, 0.2222, 0.2265, 0.2306, 0.2346, 0.2391, 0.2430, 0.2474,\
              0.2515, 0.2552, 0.2591, 0.2635, 0.2678, 0.2721, 0.2761, 0.2801, 0.2844, 0.2887, 0.2928, 0.2968])
    zerotimes = fsolve(liftfunc, xguess)
    plt.scatter(zerotimes, np.zeros_like(zerotimes), color='r', label='roots')


    for i in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

        if i < num_zeros//2:
            firstzero = zerotimes[2*i]
            secondzero = zerotimes[2*i+2]
            period = secondzero - firstzero
            plot_t = np.linspace(firstzero, secondzero, res)
            _partialLift = liftfunc(plot_t)

        else:
            _partialLift = np.zeros_like(_partialLift, dtype=float)

        if i == 0:
            lift_avg = _partialLift
            period_avg = period

        else:
            lift_avg = 1/(i+1) * (i*lift_avg + _partialLift)
            period_avg = 1/(i+1) * (i*period_avg + period)

    print('average period is:', period_avg)
    plt.plot(plot_t, lift_avg, color='k', label='average')

    phase_coord = np.linspace(0, 2*np.pi+0.001, res)
    # phase_coord = np.arange(0, period_avg, 0.001)
    print(phase_coord)

    plt.figure()
    plt.plot(phase_coord, lift_avg)
    # plt.legend()



    ####################### Onto averaging other paramters of LES #########################

    time = np.zeros((end+1))

    for i in np.arange(start,end+0.1): # loop through all the time steps

        filename = foldername + paramfile + str(int(i)) + '.csv'
        df = pd.read_csv(filename)
        # df = df.sort_values(by=['Points:1']) # sort accord to increasing y-coord value
        t = df['Time'][0] # every row has the same time value for each file so just take the first
        time[int(i)] = t
        # if i == 0:
        #     x_coord = df['Points:0']
        #     y_coord = df['Points:1']
        x_vel = df['Velocity:0']
        y_vel = df['Velocity:1']
        z_vel = df['Velocity:2']
        tau_11 = df['tau_11']
        tau_12 = df['tau_12']
        tau_13 = df['tau_13']
        tau_22 = df['tau_22']
        tau_23 = df['tau_23']
        tau_33 = df['tau_33']
        k = df['k']
        # pres = df['Pressure']

        x_vel = np.reshape(x_vel.to_numpy(), (x_vel.shape[0],1))
        y_vel = np.reshape(y_vel.to_numpy(), (y_vel.shape[0],1))
        z_vel = np.reshape(z_vel.to_numpy(), (z_vel.shape[0],1))
        tau_11 = np.reshape(tau_11.to_numpy(), (tau_11.shape[0],1))
        tau_12 = np.reshape(tau_12.to_numpy(), (tau_12.shape[0],1))
        tau_13 = np.reshape(tau_13.to_numpy(), (tau_13.shape[0],1))
        tau_22 = np.reshape(tau_22.to_numpy(), (tau_22.shape[0],1))
        tau_23 = np.reshape(tau_23.to_numpy(), (tau_23.shape[0],1))
        tau_33 = np.reshape(tau_33.to_numpy(), (tau_33.shape[0],1))
        k = np.reshape(k.to_numpy(), (k.shape[0],1))
        # pres = np.reshape(pres.to_numpy(), (pres.shape[0],1))



        if i==0:
            x_vel_gather = x_vel
            y_vel_gather = y_vel
            z_vel_gather = z_vel
            tau_11_gather = tau_11
            tau_12_gather = tau_12
            tau_13_gather = tau_13
            tau_22_gather = tau_22
            tau_23_gather = tau_23
            tau_33_gather = tau_33
            k_gather = k
            # pres_gather = pres
        else:
            x_vel_gather = np.hstack((x_vel_gather,x_vel))
            y_vel_gather = np.hstack((y_vel_gather,y_vel))
            z_vel_gather = np.hstack((z_vel_gather,z_vel))
            tau_11_gather = np.hstack((tau_11_gather,tau_11))
            tau_12_gather = np.hstack((tau_12_gather,tau_12))
            tau_13_gather = np.hstack((tau_13_gather,tau_13))
            tau_22_gather = np.hstack((tau_22_gather,tau_22))
            tau_23_gather = np.hstack((tau_23_gather,tau_23))
            tau_33_gather = np.hstack((tau_33_gather,tau_33))
            k_gather = np.hstack((k_gather,k))
            # pres_gather = np.hstack((pres_gather,pres))


    ####################### Creating phase averaged data #####################@##

    ###### create functions for each parameter
    x_vel_func = interp1d(time, x_vel_gather) # automatically interpolates in the last axis which is the time axis in this case
    y_vel_func = interp1d(time, y_vel_gather)
    z_vel_func = interp1d(time, z_vel_gather)
    tau_11_func = interp1d(time, tau_11_gather)
    tau_12_func = interp1d(time, tau_12_gather)
    tau_13_func = interp1d(time, tau_13_gather)
    tau_22_func = interp1d(time, tau_22_gather)
    tau_23_func = interp1d(time, tau_23_gather)
    tau_33_func = interp1d(time, tau_33_gather)
    k_func = interp1d(time, k_gather)
    # pres_func = interp1d(time, pres_gather)

    for k in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

        if k < num_zeros//2:
            firstzero = zerotimes[2*k]
            secondzero = zerotimes[2*k+2] # actually it's not second zero but third zero which completes a period
            # _t = np.linspace(firstzero, secondzero, res+1)[:-1] ##### This need to be changed
            print(period_avg  / 1e-4)
            print(period_avg  // 1e-4)
            Num_steps = int(period_avg  / 1e-4) + 1
            print('Number of time steps:', Num_steps)
            _t = np.arange(0, period_avg, 1e-4) + firstzero
            print(_t)
            print('Validate num steps:', _t.shape[0])
            _partial_x_vel = x_vel_func(_t)
            # print(_partial_x_vel.shape)
            _partial_y_vel = y_vel_func(_t)
            _partial_z_vel = z_vel_func(_t)
            _partial_tau_11 = tau_11_func(_t)
            _partial_tau_12 = tau_12_func(_t)
            _partial_tau_13 = tau_13_func(_t)
            _partial_tau_22 = tau_22_func(_t)
            _partial_tau_23 = tau_23_func(_t)
            _partial_tau_33 = tau_33_func(_t)
            _partial_k = k_func(_t)
            # _partial_pres = pres_func(_t)
            

        else:
            _partial_x_vel = np.zeros_like(_partial_x_vel, dtype=float)
            _partial_y_vel = np.zeros_like(_partial_y_vel, dtype=float)
            _partial_z_vel = np.zeros_like(_partial_z_vel, dtype=float)
            _partial_tau_11 = np.zeros_like(_partial_tau_11, dtype=float)
            _partial_tau_12 = np.zeros_like(_partial_tau_12, dtype=float)
            _partial_tau_13 = np.zeros_like(_partial_tau_13, dtype=float)
            _partial_tau_22 = np.zeros_like(_partial_tau_22, dtype=float)
            _partial_tau_23 = np.zeros_like(_partial_tau_23, dtype=float)
            _partial_tau_33 = np.zeros_like(_partial_tau_33, dtype=float)
            _partial_k = np.zeros_like(_partial_k, dtype=float)
            # _partial_pres = np.zeros_like(_partial_pres, dtype=float)

        if k == 0:
            x_vel_avg = _partial_x_vel
            y_vel_avg = _partial_y_vel
            z_vel_avg = _partial_z_vel
            tau_11_avg = _partial_tau_11
            tau_12_avg = _partial_tau_12
            tau_13_avg = _partial_tau_13
            tau_22_avg = _partial_tau_22
            tau_23_avg = _partial_tau_23
            tau_33_avg = _partial_tau_33
            k_avg = _partial_k
            # pres_avg = _partial_pres

        else:
            x_vel_avg = 1/(k+1) * (k*x_vel_avg + _partial_x_vel)
            y_vel_avg = 1/(k+1) * (k*y_vel_avg + _partial_y_vel)
            z_vel_avg = 1/(k+1) * (k*z_vel_avg + _partial_z_vel)
            tau_11_avg = 1/(k+1) * (k*tau_11_avg + _partial_tau_11)
            tau_12_avg = 1/(k+1) * (k*tau_12_avg + _partial_tau_12)
            tau_13_avg = 1/(k+1) * (k*tau_13_avg + _partial_tau_13)
            tau_22_avg = 1/(k+1) * (k*tau_22_avg + _partial_tau_22)
            tau_23_avg = 1/(k+1) * (k*tau_23_avg + _partial_tau_23)
            tau_33_avg = 1/(k+1) * (k*tau_33_avg + _partial_tau_33)
            k_avg = 1/(k+1) * (k*k_avg + _partial_k)
            # pres_avg = 1/(k+1) * (k*pres_avg + _partial_pres)

        # z_coord = np.zeros_like(x_coord, dtype=float)

        # print(x_coord.shape)
        # print(x_vel_avg.shape)

    for r in np.arange(_t.shape[0]):

        # newdata = {'Point_0': x_coord, 'Point_1': y_coord, 'Point_2': z_coord, 'Velocity_0': x_vel_avg[:,r], 'Velocity_1': y_vel_avg[:,r], \
        # 'Velocity_2': z_vel_avg[:,r], 'tau_11': tau_11_avg[:,r], 'tau_12': tau_12_avg[:,r], 'tau_13': tau_13_avg[:,r], 'tau_22': tau_22_avg[:,r], \
        # 'tau_23': tau_23_avg[:,r], 'tau_33': tau_33_avg[:,r], 'k': k_avg[:,r], 'Pressure': pres_avg[:,r]}

        newdata = {'Velocity_0': x_vel_avg[:,r], 'Velocity_1': y_vel_avg[:,r], 'Velocity_2': z_vel_avg[:,r],\
             'tau_11': tau_11_avg[:,r], 'tau_12': tau_12_avg[:,r], 'tau_13': tau_13_avg[:,r], 'tau_22': tau_22_avg[:,r], \
        'tau_23': tau_23_avg[:,r], 'tau_33': tau_33_avg[:,r], 'k': k_avg[:,r]}

        newdf = pd.DataFrame(newdata)
        newfilename = 'LESCellPhaseAvgData/LESPhaseAvg_'+str(r) +'.csv'

        ##### Write into .csv data files
        newdf.to_csv(newfilename, index=False)

    return



resolution = 100 # 100 time steps within 1 period
phase_avg_params_LES(resolution, 'solFlat_CELLdata_ktauij/', 'SolFlatCellkcalc_')
plt.show()