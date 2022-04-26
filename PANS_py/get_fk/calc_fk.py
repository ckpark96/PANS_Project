from .celldata import *
import pandas as pd


def extract_fk(type, centerAvgDataFilename, paramDataFilename, edgeDataFilename, fk_stat, folder):
    '''
    Extracts values of fk for a wanted statistic based on 3 files from Paraview and saves as fk.csv file

    Inputs:
    type: "epsilon" or "omega" depending on the type of simulation run
    centerAvgDataFilename: File name of .csv file which in Paraview has following filters applied: slice, cell center
    paramDataFilename: File name of .csv file which in Paraview has following filters applied: slice, time average
    edgeDataFilename: File name of .csv file which in Paraview has following filters applied: slice, extract edges, cell size, time average
    fk_stat: statistic of fk that is desired i.e. 'min', 'max' or 'avg'
    '''

    #### Average Cell Center data
    centerAvgData = pd.read_csv(centerAvgDataFilename, header=0)
    xcoord = centerAvgData['Points_0']
    ycoord = centerAvgData['Points_1']

    paramData = pd.read_csv(paramDataFilename, header=0)
    if type == "epsilon":
        epsilonAvg = paramData['epsilon_average']
    elif type == "omega":
        epsilonAvg = paramData['omega_average']
    kAvg = paramData['k_average']


    #### Duplicate data with cell edge length
    edgeData = pd.read_csv(edgeDataFilename, header=0)
    edgeLength = edgeData['Length_average']
    dup_p = edgeData['p_average'] # duplicate data to use for length statistics
    nonDup_p = pd.read_csv(centerAvgDataFilename, header=0)['p_average']

    #### Calculate fk
    minLen = get_length_data(dup_p, nonDup_p, edgeLength, fk_stat)
    fk = calculate_fk(type, kAvg, epsilonAvg, minLen)

    #### Set those with values > 1 to 1
    fkBool = (fk > 1)*1 # Set those >1 to 1 and <1 to 0
    fkBool2 = (fk < 1)*1 # Those >1 are 0 and <1 are 1
    fk = fk * fkBool2 + fkBool # New fk

    fkfilename = folder + 'fk.csv'
    fk.to_csv(fkfilename,index=False, header=False)

    #### Masking condition: x>0, x<1, y>-0.5, y<0.5
    # visualise_fk(xcoord, ycoord, fk, 0, 1, -0.5, 0.5) #### Does not work with large dataset
    # simpler_visual(xcoord, ycoord, fk)

    return




