import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate

''' 
Dataset without duplpicates
# Obtain general dataset from Paraview:
# import msh file by creating .foam file -> Save Data
'''
# data = pd.read_csv('dataarrays.csv', header=0) # Not required if the cell centers values are obtained (as done below)
# epsData = data['epsilon']
# kData = data['k']
# volData = data['V']

##### Extracting cell center values is the fastest
##### Cell Centers -> Temporal Statistics (Untick Max, min and s.d.) -> Spreadsheet view -> Save
# centerData = pd.read_csv('cellCenters.csv', header=0)
# xcoord = centerData['Points_0']
# ycoord = centerData['Points_1']

''' 
Dataset with duplicates 
# Obtain cell length dataset from Paraview - these contain duplicates:
# import msh file by creating .foam file -> filter 'Extract Edges' -> filter 'Cell Size' -> Save Data
'''

# dupData = pd.read_csv('lengthData0.0.csv', header=0)
# lenData = dupData['Length']
# dupVolData = dupData['V']

##### Constants #####
# Cmu = 0.09

''' Extract k and epsilon data from OpenFOAM files '''
##### Constants #####
# dt = 0.01
# endT = 0.3
# rowskip = 21

def clean_data(filename, rowstoskip):
    '''
    For OpenFOAM files

    Cleans k or epsilon data, leaving only the relevant internalField values
    Thus, exclude boundaryField values and wall values
    '''
    data = pd.read_csv(filename, header=None, skiprows = rowstoskip)
    data = pd.to_numeric(data[0], errors='coerce') # convert non-numerics to NaN
    dataNaN = data.isnull()
    idx = np.where(dataNaN)[0][0]
    data = data[:idx]
    data = data.to_frame()

    return data.to_numpy()


def time_avg_data(timeStep, latestTime, rowstoskip): # Not required if temporal statistics filter is used in Paraview
    '''
    For OpenFOAM files
    
    Computes the time averages of k and epsilon
    '''
    variousTime = np.arange(timeStep, latestTime, timeStep)
    for count, t in enumerate(variousTime):
        if '9' in str(count): # Every 9th count does the t only have 1 decimal point
            t = np.round(t,1)
        else:
            t = np.round(t,2)
        kfile = clean_data(str(t)+'/k', rowstoskip)
        epsfile = clean_data(str(t)+'/epsilon', rowstoskip)
        
        if count == 0:
            kBigData = np.zeros((kfile.shape[0],variousTime.shape[0]))
            epsBigData = np.zeros((epsfile.shape[0],variousTime.shape[0]))
            kBigData[:,count] = kfile.reshape((kfile.shape[0]))
            epsBigData[:,count] = epsfile.reshape(epsfile.shape[0])
    
    kAvg = np.mean(kBigData, axis=1)
    epsAvg = np.mean(epsBigData, axis=1)

    return kAvg, epsAvg


''' Functions needed to extract minimum, maximum and average cell lengths '''

def drop_successive(df):
    '''
    Instead of dropping all the duplicates, this function only drops the consecutive duplicates

    Input:
    df should be a pandas.DataFrame of a a pandas.Series
    Output:
    df of ts with masked or dropped values
    '''
    #### Method 1 #####
    # df = df.mask(df.shift(1) == df) # Mask keeping the first occurrence
    # return df.dropna(axis=0, how='all') # Drop the values (e.g. rows are deleted)

    #### Method 2 ####
    dupBool = df.shift() != df # Mark those successive duplicates as False (non-duplicates as True)
    newdf = df.loc[dupBool] # Extract the values with True
    return newdf, dupBool

# cleanVolData, dupBoolean = drop_successive(dupVolData) # Only needed if taking from lengthData csv
# firstData = dupBoolean[dupBoolean].index # Extracts indices of True values
# invDupBoolean = ~dupBoolean

# testArr = np.array([0,0,0,0,1,1,1,0,0,0,2,2,3,2,2,1,1,0])
# testArr = pd.DataFrame({'0':testArr})['0']
# print(testArr)
# print(testArr.shift())
def consecutive_ranges(data, val):
    '''
    Get ranges for CONSECUTIVE duplicates
    '''
    isval = np.concatenate(([0], np.equal(data, val).view(np.int8), [0]))
    absdiff = np.abs(np.diff(isval))
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)

    return ranges
# print(testArr.shape)
# print(consecutive_ranges(testArr, 0))
# print(drop_successive(testArr)[0])

def duplicate_index(data):
    '''
    Finds index at which duplicates occur in supposedly non-duplicated data
    data: dataFrame type
    '''
    _bool = data.shift() == data
    dupIndex = np.where(_bool*1 == 1)[0][0]

    return dupIndex

def get_length_data(duplicate_data, non_duplicate_data, length_data, whichstat):
    '''
    Takes length_data and produces a statistical array with minimum, median and maximum length for each cell
    ### Not the most efficient method (but does the job) ###

    Input:
    duplicate_data: raw (volume) data that is inclusive of duplicates
    non_duplicate_data: raw cell data without duplicates
    length_data: length data
    whichstat: 'max', 'min' or 'avg' for maximum, minimum and average values of each cell respectively
    '''

    lenDataCopy = copy.deepcopy(length_data) # to not dirty the original length data
    lenStat = np.zeros((non_duplicate_data.shape[0],3))
    for count, val in enumerate(non_duplicate_data):
        _range = consecutive_ranges(duplicate_data, val)
        maxVal = np.nanmax(lenDataCopy[_range[0,0]:_range[0,1]])
        minVal = np.nanmin(lenDataCopy[_range[0,0]:_range[0,1]])
        midVal = np.nanmedian(lenDataCopy[_range[0,0]:_range[0,1]])

        if midVal==np.nan or minVal==np.nan or maxVal==np.nan:
            print(count, val)
        lenStat[count] = np.array([minVal, midVal, maxVal])

        for i in np.arange(_range[0,0],_range[0,1]):
            lenDataCopy[i] = np.random.rand() # Replace already processed values with random values to not include in range of next occurrences 

    if whichstat == 'min':
        return lenStat[:,0]
    elif whichstat == 'max':
        return lenStat[:,2]
    elif whichstat == 'avg':
        return np.mean(lenStat, axis=1)
    elif whichstat == 'all':
        return lenStat


def calculate_fk(type, k, epsilon_or_omega, length):
    '''
    Calculate fk using a given formula
    '''
    Cmu = 0.09 # Fixed
    if type == "epsilon":
        taylorLength = k**(3/2) / epsilon_or_omega
    elif type == "omega":
        taylorLength = k**(1/2) / epsilon_or_omega / Cmu
        

    fk = 1/np.sqrt(Cmu)*(length / taylorLength)**(2/3)
    return fk

def visualise_fk(x_coords, y_coords, fk, mask_xmin, mask_xmax, mask_ymin, mask_ymax):
    '''
    x_coords: x-coordinates of each cell (Obtained from Paraview via 'Cell center' filter)
    y_coords: y-coordinates of each cell (")
    mask_cond: mask between xmin and xmax & ymin and ymax
    '''
    dataLen = x_coords.shape[0]
    x = np.linspace(np.min(x_coords), np.max(x_coords), int(dataLen/3))
    y = np.linspace(np.min(y_coords), np.max(y_coords), int(dataLen/3))
    xx, yy = np.meshgrid(x,y)
    print('check1-went through meshgrid')
    Z = interpolate.griddata((x_coords, y_coords), fk, (xx,yy),method='linear')
    print('check2-went through interpolation')
    maskWhere = ((xx>mask_xmin)*1 + (xx<mask_xmax)*1 + (yy>mask_ymin)*1+ (yy<mask_ymax)*1) > 3
    print('check3-went through masking')
    Z = np.ma.array(Z, mask=maskWhere)
    plt.figure()
    plt.imshow(Z, origin='lower',
            extent=(x_coords.min(), x_coords.max(), y_coords.min(), y_coords.max()),
            aspect=(x_coords.max() - x_coords.min()) / (y_coords.max() - y_coords.min()))
    plt.colorbar()
    plt.show()
    return


def simpler_visual(x_coords, y_coords, fk):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, fk, c='red')
    plt.show()
    return 