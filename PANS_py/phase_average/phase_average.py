import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.interpolate import interp1d
from scipy.fftpack import fft, ifft, fftfreq

'''
This program will try to extract the phase averages for LES, PANS and RANS simulation and pair them with phase coordinates to kick off data assimilation
step 1: plot the actual lift-time data and observe where the first root is located at and how many roots there are
step 2: use these 2 values to average the data
'''



#### For PANS and RANS
def freqdata(filename, plot=False):
    df = pd.read_csv(filename)

    t = df['Time'].to_numpy()
    lift = df['Lift'].to_numpy()

    if plot == True:
        plt.figure()
        plt.plot(t,lift,'-o', label='data')

    return t, lift



################ Observations needed to be made in order to preoceed with further computations ####################


def phase_avg_params_RAS(first_zero, last_zero, num_zeros, foldername, dt, res, paramfile, start, end, x_range):

    '''
    Input:
        first_zero: approximate guess of where the first zero is in terms of time
        num_zeros: exact number of zeros(roots) present in the data
        foldername: name of the folder of simulation containing the forces.csv file (include '/' at the back)
        dt: timestep in simulation
        res: wanted resolution in each period aka number of points in a single period
        paramfile: the folder and name of which the parameter files start as - parameter file must contain the coordinates, x-velocity, y-velocity, k, kU, omega, omegaU and pressure
        start: the number of which the parameter files start from
        end: the number of which the parameter files end as
        x_range: the x-locations that the analysis is wanted at


    '''

    t, lift = freqdata(foldername+'forces.csv')
    N = t.shape[0]
    _lift = fft(lift)
    _freq = np.linspace(0, 1/dt, N)

    ################ Obtaining the dominant frequency and thus the main period

    fftfreqplot = _freq[:N//2]
    fftliftplot = np.abs(_lift[:N//2])

    maxFFTlift = np.max(fftliftplot)
    maxidx = np.where(fftliftplot==maxFFTlift)[0]
    domfreq = fftfreqplot[maxidx]
    print(domfreq)
    period = 1/domfreq[0]



    ################ Obtain the zero intercepts of the periodic wave 
    liftfunc = interp1d(t, lift, 'quadratic', fill_value='extrapolate') # extrapolation is required due to fsolve's nature

    # xguess = np.linspace(first_zero, first_zero+period*(num_zeros/2+0.1), num_zeros)
    xguess = np.linspace(first_zero, last_zero+0.00001, num_zeros)
    zerotimes = fsolve(liftfunc, xguess)
    # print('xguess:', xguess)
    # print('fsolve roots:', zerotimes)
    # print(zerotimes.shape)
    # _uniqroots = np.unique(zerotimes.round(decimals=4))
    # _uniqdiff = _uniqroots[1:] - _uniqroots[:-1]
    # _uniqbool = _uniqdiff > np.mean(_uniqdiff)
    # print(np.sum(_uniqbool))
    # plt.scatter(xguess, np.zeros_like(xguess), color='b', label='guesses')
    plt.scatter(zerotimes, np.zeros_like(zerotimes), color='r', label='roots')

    ################ Check if first zero starts off as positive sinusoidal wave - must use lift
    small = 0.00001
    zero1 = zerotimes[0]
    lift1 = liftfunc([zero1-small, zero1+small])
    grad1 = (lift1[1]-lift1[0])/(2*small)
    if grad1 > 0:
        print('positive sinusoidal, no changes made')

    else:
        print('negative sinusoidal, removing first root')
        zerotimes = zerotimes[1:]
        num_zeros -= 1



    ################ Retrieve the exact same phase for each period and average them - lift will be replaced with other parameters that are under concern (need new interpolation function)

    # for count, i in enumerate(zerotimes):
    
    for i in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

        if i < num_zeros//2:
            firstzero = zerotimes[2*i]
            secondzero = zerotimes[2*i+2]
            _t = np.linspace(firstzero, secondzero+0.000001, res)
            _partialLift = liftfunc(_t)

        else:
            _partialLift = np.zeros_like(_partialLift, dtype=float)

        if i == 0:
            lift_avg = _partialLift

        else:
            lift_avg = 1/(i+1) * (i*lift_avg + _partialLift)

    plt.plot(t, lift, marker='.', alpha=0.5, label='true data')
    plt.plot(_t, lift_avg, color='k', label='average')
    plt.legend()


    ################ Transfer over to phase coordinate system from temporal
    phase_coord = np.linspace(0, 2*np.pi+0.001, res)

    plt.figure()
    plt.plot(phase_coord, lift_avg)


    ################# Using other parameters instead of Lift
    ##### Need to take into account: time, wanted parameter and location (Need to use Paraview to save params at diff timesteps as .csv file)
    ##### each location as a wide range of values due to the y-coordinates so instead of having a single value for a (x,t), now there'll be a whole set of values
    ##### can try 2d interpolation maybe

    x_true = np.zeros_like(x_range, dtype=float)

    ###### Create large empty arrays to gather 3 dimensional array: dim 1: x locations, dim 2: y locations, dim 3: time 
    ###### Unable to pre-define the exact shape due to unknown length of y-coordinates
    x_vel_allx = []
    y_vel_allx = []
    k_allx = []
    kU_allx = []
    omega_allx = []
    omegaU_allx = []
    pres_allx = []



    for count, j in enumerate(x_range): # loop through all the wanted x-coordinate values

        time = np.zeros((end+1))

        for i in np.arange(start,end+0.1): # loop through all the time steps

            filename = foldername + paramfile + str(int(i)) + '.csv'
            df = pd.read_csv(filename)
            df = df.sort_values(by=['Points:1']) # sort accord to increasing y-coord value
            t = df['Time'][0] # every row has the same time value for each file so just take the first
            time[int(i)] = t
            x_coord = df['Points:0']
            y_coord = df['Points:1']
            x_vel = df['U:0']
            y_vel = df['U:1']
            k = df['k']
            kU = df['kU']
            omega = df['omega']
            omegaU = df['omegaU']
            # pres = df['p']

            x_coord = (x_coord.to_frame()).reset_index(drop=True)
            x_coord_uniq = (x_coord.drop_duplicates()).reset_index(drop=True)
            x_coord = x_coord.to_numpy()
            x_coord = np.reshape(x_coord, (x_coord.shape[0]))

            # Set 0s to a small positive value so that they don't get removed later
            # for _var in (y_coord, x_vel, y_vel, k, kU, omega, omegaU, pres):
                # _var[_var==0] = 1e-8
                # _var = (_var.to_frame()).reset_index(drop=True)
            
            y_coord[y_coord==0] = 1e-8
            # y_coord = (y_coord.to_frame()).reset_index(drop=True)
            x_vel[x_vel==0] = 1e-8
            # x_vel = (x_vel.to_frame()).reset_index(drop=True)
            y_vel[y_vel==0] = 1e-8
            # y_vel = (y_vel.to_frame()).reset_index(drop=True)
            k[k==0] = 1e-8
            # k = (k.to_frame()).reset_index(drop=True)
            kU[kU==0] = 1e-8
            # kU = (kU.to_frame()).reset_index(drop=True)
            omega[omega==0] = 1e-8
            # omega = (omega.to_frame()).reset_index(drop=True)
            omegaU[omegaU==0] = 1e-8
            # omegaU = (omegaU.to_frame()).reset_index(drop=True)
            # pres[pres==0] = 1e-8
            # pres = (pres.to_frame()).reset_index(drop=True)


            ###### find the location of wanted x-axis value in the unique x array and mark it as 1 (True)
            xdiff = np.abs(x_coord_uniq - j)
            idxBool = (xdiff == np.min(xdiff))*1

            ###### Using this found value in the unique x array, mark the same value in the large x array as 1 (True)
            x = x_coord_uniq[idxBool==1]
            x = (x.dropna()).to_numpy()[0][0]
            xBool = (x_coord == x) * 1
            xBool = np.reshape(xBool, (xBool.shape[0]))
            # print(xBool.shape)
            # print(np.sum(xBool))
            # if np.sum(xBool) < int(57/2):
            # xBool = (np.abs(x - x_coord)<1e-3) * 1

            ############# Using the Boolean array, mark the corresponding values of that x-coordinate true in the rest of the parameters and clean the array by removing the 0s
            # for _var in (x_coord, y_coord, x_vel, y_vel, k, kU, omega, omegaU, pres):
            #     _var[:] = _var[:] * xBool
            #     _var[:] = _var[_var!=0]
            #     _var.reshape() 

            _x_coord = x_coord * xBool
            _x_coord = _x_coord[_x_coord!=0]
            _x_coord = np.reshape(_x_coord, (_x_coord.shape[0],1))
            _y_coord = y_coord * xBool
            _y_coord = (_y_coord[_y_coord!=0]).to_numpy()
            _y_coord = np.reshape(_y_coord, (_y_coord.shape[0],1))
            _x_vel = x_vel * xBool
            _x_vel = (_x_vel[_x_vel!=0]).to_numpy()
            _x_vel = np.reshape(_x_vel, (_x_vel.shape[0],1))
            _y_vel = y_vel * xBool
            _y_vel = (_y_vel[_y_vel!=0]).to_numpy()
            _y_vel = np.reshape(_y_vel, (_y_vel.shape[0],1))
            _k = k * xBool
            _k = (_k[_k!=0]).to_numpy()
            _k = np.reshape(_k, (_k.shape[0],1))
            _kU = kU * xBool
            _kU = (_kU[_kU!=0]).to_numpy()
            _kU = np.reshape(_kU, (_k.shape[0],1))
            _omega = omega * xBool
            _omega = (_omega[_omega!=0]).to_numpy()
            _omega = np.reshape(_omega, (_omega.shape[0],1))
            _omegaU = omegaU * xBool
            _omegaU = (_omegaU[_omegaU!=0]).to_numpy()
            _omegaU = np.reshape(_omegaU, (_omegaU.shape[0],1))
            # _pres = pres * xBool
            # _pres = (_pres[_pres!=0]).to_numpy()
            # _pres = np.reshape(_pres, (_pres.shape[0],1))

            ###### create a large array with columns representing the various time steps, rows representing values at different y-coord positions
            if i==0:
                x_vel_gather = _x_vel
                y_vel_gather = _y_vel
                k_gather = _k
                kU_gather = _kU
                omega_gather = _omega
                omegaU_gather = _omegaU
                # pres_gather = _pres
            else:
                x_vel_gather = np.hstack((x_vel_gather,_x_vel))
                y_vel_gather = np.hstack((y_vel_gather,_y_vel))
                k_gather = np.hstack((k_gather,_k))
                kU_gather = np.hstack((kU_gather,_kU))
                omega_gather = np.hstack((omega_gather,_omega))
                omegaU_gather = np.hstack((omegaU_gather,_omegaU))
                # pres_gather = np.hstack((pres_gather,_pres))

        x_true[count] = _x_coord[0]

        ####################### Creating phase averaged data

        ###### create functions for each parameter
        x_vel_func = interp1d(time, x_vel_gather) # automatically interpolates in the last axis which is the time axis in this case
        y_vel_func = interp1d(time, y_vel_gather)
        k_func = interp1d(time, k_gather)
        kU_func = interp1d(time, kU_gather)
        omega_func = interp1d(time, omega_gather)
        omegaU_func = interp1d(time, omegaU_gather)
        # pres_func = interp1d(time, pres_gather)

        ###### Average the paramaters for every period
        for k in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

            if k < num_zeros//2:
                firstzero = zerotimes[2*k]
                secondzero = zerotimes[2*k+2]
                _t = np.linspace(firstzero, secondzero+0.000001, res)
                _partial_x_vel = x_vel_func(_t)
                _partial_y_vel = y_vel_func(_t)
                _partial_k = k_func(_t)
                _partial_kU = kU_func(_t)
                _partial_omega = omega_func(_t)
                _partial_omegaU = omegaU_func(_t)
                # _partial_pres = pres_func(_t)

            else:
                _partial_x_vel = np.zeros_like(_partial_x_vel, dtype=float)
                _partial_y_vel = np.zeros_like(_partial_y_vel, dtype=float)
                _partial_k = np.zeros_like(_partial_k, dtype=float)
                _partial_kU = np.zeros_like(_partial_kU, dtype=float)
                _partial_omega = np.zeros_like(_partial_omega, dtype=float)
                _partial_omegaU = np.zeros_like(_partial_omegaU, dtype=float)
                # _partial_pres = np.zeros_like(_partial_pres, dtype=float)

            if k == 0:
                x_vel_avg = _partial_x_vel
                y_vel_avg = _partial_y_vel
                k_avg = _partial_k
                kU_avg = _partial_kU
                omega_avg = _partial_omega
                omegaU_avg = _partial_omegaU
                # pres_avg = _partial_pres

            else:
                x_vel_avg = 1/(k+1) * (k*x_vel_avg + _partial_x_vel)
                y_vel_avg = 1/(k+1) * (k*y_vel_avg + _partial_y_vel)
                k_avg = 1/(k+1) * (k*k_avg + _partial_k)
                kU_avg = 1/(k+1) * (k*kU_avg + _partial_kU)
                omega_avg = 1/(k+1) * (k*omega_avg + _partial_omega)
                omegaU_avg = 1/(k+1) * (k*omegaU_avg + _partial_omegaU)
                # pres_avg = 1/(k+1) * (k*pres_avg + _partial_pres)

        ##### Add the phase averaged data to a big array which will contain all the phase averages of each wanted-x-location
        x_vel_allx.append(x_vel_avg)
        y_vel_allx.append(y_vel_avg)
        k_allx.append(k_avg)
        kU_allx.append(kU_avg)
        omega_allx.append(omega_avg)
        omegaU_allx.append(omegaU_avg)
        # pres_allx.append(pres_avg)
        print(k_avg.shape)
        plt.figure()
        plt.plot(phase_coord, x_vel_avg[100,:], label='x vel')
        plt.plot(phase_coord, y_vel_avg[100,:], label='y vel')
        plt.plot(phase_coord, k_avg[100,:], label='k')
        plt.legend()

    # unique y values are the same for every paramter and also for every x value (assuming the wanted x is located at the wake)
    y_uniq = _y_coord

    ###### convert the list of to a 3D array for more flexible usages
    x_vel_allx = np.array(x_vel_allx)
    y_vel_allx = np.array(y_vel_allx)
    k_allx = np.array(k_allx)
    kU_allx = np.array(kU_allx)
    omega_allx = np.array(omega_allx)
    omegaU_allx = np.array(omegaU_allx)
    # pres_allx = np.array(pres_allx)

    # return x_true, y_uniq, x_vel_allx, y_vel_allx, k_allx, kU_allx, omega_allx, omegaU_allx, pres_allx
    return x_true, y_uniq, x_vel_allx, y_vel_allx, k_allx, kU_allx, omega_allx, omegaU_allx


############################################################### LES ##############################################################
res = 100
x_range = np.linspace(0.05, 0.4, 4)
foldername = 'slice_avg_time_varying_k/' 
paramfile = 'LESparams_'
def phase_avg_params_LES(res, x_range, foldername, paramfile):
    '''
    Input:
        res: resolution wanted in a single period
        x_range: range of x values where the analysis is to be conducted at
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

    # ax[0].plot(FFTfreq, fftlift, marker='.') # 2nd half is just a mirror image of the first half 

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
    print(domfreq)
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
    xguess = np.array([0.1772, 0.1814, 0.1856, 0.1897, 0.1941, 0.1985, 0.2022, 0.2064, 0.2102, 0.2141, 0.2181, 0.2222, 0.2265, 0.2306, 0.2346, 0.2391, 0.2430, 0.2474, 0.2515, 0.2552, 0.2591, 0.2635, 0.2678, 0.2721, 0.2761, 0.2801, 0.2844, 0.2887, 0.2928, 0.2968])
    zerotimes = fsolve(liftfunc, xguess)
    plt.scatter(zerotimes, np.zeros_like(zerotimes), color='r', label='roots')


    for i in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

        if i < num_zeros//2:
            firstzero = zerotimes[2*i]
            secondzero = zerotimes[2*i+2]
            _t = np.linspace(firstzero, secondzero+0.000001, res)
            _partialLift = liftfunc(_t)

        else:
            _partialLift = np.zeros_like(_partialLift, dtype=float)

        if i == 0:
            lift_avg = _partialLift

        else:
            lift_avg = 1/(i+1) * (i*lift_avg + _partialLift)

    plt.plot(_t, lift_avg, color='k', label='average')

    phase_coord = np.linspace(0, 2*np.pi+0.001, res)

    plt.figure()
    plt.plot(phase_coord, lift_avg)
    plt.legend()



    ############ Onto averaging other paramters of LES
    x_true = np.zeros_like(x_range, dtype=float)
    x_vel_allx = []
    y_vel_allx = []
    z_vel_allx = []
    tau_11_allx = []
    tau_12_allx = []
    tau_13_allx = []
    tau_22_allx = []
    tau_23_allx = []
    tau_33_allx = []
    k_allx = []
    pres_allx = []

    for count, j in enumerate(x_range): # loop through all the wanted x-coordinate values

        time = np.zeros((end+1))

        for i in np.arange(start,end+0.1): # loop through all the time steps

            filename = foldername + paramfile + str(int(i)) + '.csv'
            df = pd.read_csv(filename)
            df = df.sort_values(by=['Points:1']) # sort accord to increasing y-coord value
            t = df['Time'][0] # every row has the same time value for each file so just take the first
            time[int(i)] = t
            x_coord = df['Points:0']
            y_coord = df['Points:1']
            x_vel = df['Velocity_0']
            y_vel = df['Velocity_1']
            z_vel = df['Velocity_2']
            tau_11 = df['tau_11']
            tau_12 = df['tau_12']
            tau_13 = df['tau_13']
            tau_22 = df['tau_22']
            tau_23 = df['tau_23']
            tau_33 = df['tau_33']
            k = df['k']
            pres = df['Pressure']

            x_coord = (x_coord.to_frame()).reset_index(drop=True)
            x_coord_uniq = (x_coord.drop_duplicates()).reset_index(drop=True)
            x_coord = x_coord.to_numpy()
            x_coord = np.reshape(x_coord, (x_coord.shape[0]))

            _vars = [y_coord, x_vel, y_vel, z_vel, tau_11, tau_12, tau_13, tau_22, tau_23, tau_33, k, pres]

            # y_coord[y_coord==0] = 1e-8
            # x_vel[x_vel==0]     = 1e-8
            # y_vel[y_vel==0]     = 1e-8
            # k[k==0]             = 1e-8
            # pres[pres==0]       = 1e-8

            for m in range(len(_vars)):
                _vars[m][:][_vars[m][:]==0] = 1e-8

            xdiff   = np.abs(x_coord_uniq - j)
            idxBool = (xdiff == np.min(xdiff))*1

            x = x_coord_uniq[idxBool==1]
            x = (x.dropna()).to_numpy()[0][0]
            xBool = (x_coord == x) * 1
            xBool = np.reshape(xBool, (xBool.shape[0]))

            # _vars2 = [x_coord, y_coord, x_vel, y_vel, z_vel, tau_11, tau_12, tau_13, tau_22, tau_23, tau_33, k, pres]

            # for n in range(len(_vars2)):
            #     _vars2[n][:] =  _vars2[n][:] * xBool
            #     _vars2[n][:] = _vars2[n][:][_vars2[n][:]!=0]
            #     _vars2[n][:] = np.reshape(_vars2[n][:], (_vars2[n][:].shape[0],1))

            _x_coord = x_coord * xBool
            _x_coord = _x_coord[_x_coord!=0]
            _x_coord = np.reshape(_x_coord, (_x_coord.shape[0],1))
            _y_coord = y_coord * xBool
            _y_coord = (_y_coord[_y_coord!=0]).to_numpy()
            _y_coord = np.reshape(_y_coord, (_y_coord.shape[0],1))
            _x_vel = x_vel * xBool
            _x_vel = (_x_vel[_x_vel!=0]).to_numpy()
            _x_vel = np.reshape(_x_vel, (_x_vel.shape[0],1))
            _y_vel = y_vel * xBool
            _y_vel = (_y_vel[_y_vel!=0]).to_numpy()
            _y_vel = np.reshape(_y_vel, (_y_vel.shape[0],1))
            _z_vel = z_vel * xBool
            _z_vel = (_z_vel[_z_vel!=0]).to_numpy()
            _z_vel = np.reshape(_z_vel, (_z_vel.shape[0],1))
            _tau_11 = tau_11 * xBool
            _tau_11 = (_tau_11[_tau_11!=0]).to_numpy()
            _tau_11 = np.reshape(_tau_11, (_tau_11.shape[0],1))
            _tau_12 = tau_12 * xBool
            _tau_12 = (_tau_12[_tau_12!=0]).to_numpy()
            _tau_12 = np.reshape(_tau_12, (_tau_12.shape[0],1))
            _tau_13 = tau_13 * xBool
            _tau_13 = (_tau_13[_tau_13!=0]).to_numpy()
            _tau_13 = np.reshape(_tau_13, (_tau_13.shape[0],1))
            _tau_22 = tau_22 * xBool
            _tau_22 = (_tau_22[_tau_22!=0]).to_numpy()
            _tau_22 = np.reshape(_tau_22, (_tau_22.shape[0],1))
            _tau_23 = tau_23 * xBool
            _tau_23 = (_tau_23[_tau_23!=0]).to_numpy()
            _tau_23 = np.reshape(_tau_23, (_tau_23.shape[0],1))
            _tau_33 = tau_33 * xBool
            _tau_33 = (_tau_33[_tau_33!=0]).to_numpy()
            _tau_33 = np.reshape(_tau_33, (_tau_33.shape[0],1))

            _k = k * xBool
            _k = (_k[_k!=0]).to_numpy()
            _k = np.reshape(_k, (_k.shape[0],1))
            _pres = pres * xBool
            _pres = (_pres[_pres!=0]).to_numpy()
            _pres = np.reshape(_pres, (_pres.shape[0],1))

            if i==0:
                x_vel_gather = _x_vel
                y_vel_gather = _y_vel
                z_vel_gather = _z_vel
                tau_11_gather = _tau_11
                tau_12_gather = _tau_12
                tau_13_gather = _tau_13
                tau_22_gather = _tau_22
                tau_23_gather = _tau_23
                tau_33_gather = _tau_33
                k_gather = _k
                pres_gather = _pres
            else:
                x_vel_gather = np.hstack((x_vel_gather,_x_vel))
                y_vel_gather = np.hstack((y_vel_gather,_y_vel))
                z_vel_gather = np.hstack((z_vel_gather,_z_vel))
                tau_11_gather = np.hstack((tau_11_gather,_tau_11))
                tau_12_gather = np.hstack((tau_12_gather,_tau_12))
                tau_13_gather = np.hstack((tau_13_gather,_tau_13))
                tau_22_gather = np.hstack((tau_22_gather,_tau_22))
                tau_23_gather = np.hstack((tau_23_gather,_tau_23))
                tau_33_gather = np.hstack((tau_33_gather,_tau_33))
                k_gather = np.hstack((k_gather,_k))
                pres_gather = np.hstack((pres_gather,_pres))

        x_true[count] = x_coord[0]

        ####################### Creating phase averaged data

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
        pres_func = interp1d(time, pres_gather)

        for k in np.arange((num_zeros-1)//2): # Number of waves = int(Nzero-1 / 2)

            if k < num_zeros//2:
                firstzero = zerotimes[2*k]
                secondzero = zerotimes[2*k+2]
                _t = np.linspace(firstzero, secondzero+0.000001, res)
                _partial_x_vel = x_vel_func(_t)
                _partial_y_vel = y_vel_func(_t)
                _partial_z_vel = z_vel_func(_t)
                _partial_tau_11 = tau_11_func(_t)
                _partial_tau_12 = tau_11_func(_t)
                _partial_tau_13 = tau_11_func(_t)
                _partial_tau_22 = tau_11_func(_t)
                _partial_tau_23 = tau_11_func(_t)
                _partial_tau_33 = tau_11_func(_t)
                _partial_k = k_func(_t)
                _partial_pres = pres_func(_t)
                

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
                _partial_pres = np.zeros_like(_partial_pres, dtype=float)

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
                pres_avg = _partial_pres

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
                pres_avg = 1/(k+1) * (k*pres_avg + _partial_pres)

        x_vel_allx.append(x_vel_avg)
        y_vel_allx.append(y_vel_avg)
        z_vel_allx.append(z_vel_avg)
        tau_11_allx.append(tau_11_avg)
        tau_12_allx.append(tau_12_avg)
        tau_13_allx.append(tau_13_avg)
        tau_22_allx.append(tau_22_avg)
        tau_23_allx.append(tau_23_avg)
        tau_33_allx.append(tau_33_avg)        
        k_allx.append(k_avg)
        pres_allx.append(pres_avg)
        # print(k_avg.shape)

        # yval = 50
        # print(k_avg.shape)
        # plt.figure()
        # plt.plot(phase_coord, x_vel_avg[yval,:], label='x vel')
        # plt.plot(phase_coord, y_vel_avg[yval,:], label='y vel')
        # plt.plot(phase_coord, k_avg[yval,:], label='k')
        # plt.legend()

    # unique y values are the same for every paramter and also for every x value (assuming the wanted x is located at the wake)
    y_uniq = _y_coord

    ###### convert the list of to a 3D array for more flexible usages
    x_vel_allx = np.array(x_vel_allx)
    y_vel_allx = np.array(y_vel_allx)
    k_allx = np.array(k_allx)
    pres_allx = np.array(pres_allx)

    return x_true, y_uniq, x_vel_allx, y_vel_allx, z_vel_allx, tau_11_allx, tau_12_allx, tau_13_allx, tau_22_allx, tau_23_allx, tau_33_allx, k_allx, pres_allx



################ PANS and RANS #######################



PANSfolder = 'triPrism_PANS_fk02_v9/'
# freqdata(PANSfolder+'forces.csv', True)
timestep_ = 0.001
firstzero_ = 0.251
lastzero_ = 0.499983
Nzero_ = 53
_start = 0
_end = 400
_paramfile = 'params/params_'
resolution = 100
_x_range = np.linspace(0.05, 0.4, 1) # wanted x-axis locations for analysis


# phase_avg_params_RAS(firstzero_, lastzero_, Nzero_, PANSfolder, timestep_, resolution, _paramfile, _start, _end, _x_range)

phase_avg_params_LES(resolution, _x_range, 'LES_flattened_kData/', 'LESdata_')
plt.show()

# df = pd.read_csv('slice_avg_time_varying_k/LESparams_5.csv')