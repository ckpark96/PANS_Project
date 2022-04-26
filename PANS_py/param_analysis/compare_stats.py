import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def extract_param(filename, x_label, y_label, param_label):
    '''
    The .csv file for this function should be:
    slice-Z, cell center, temporal stats (more detail in docx)

    Input:
    filename - filename of the csv file as string
    model_type - Turbulence closure model type, RAS or LES in string

    Output:
    tuples of arrays - (x_coord, x_coord_unique, y_coord, param_avg)
    '''

    data = pd.read_csv(filename, header=0)

    #### Extract relevant parameters from the data
    x_coord   = data[x_label].to_frame()
    y_coord   = data[y_label].to_frame()
    param_avg = data[param_label].to_frame()

    # if type=='RAS':
    #     x_coord += 0.7853
    #     y_coord += 0.06

    df      = x_coord.join(y_coord)
    _df     = df.join(param_avg)
    _df     = _df.sort_values(by=[y_label]) # This is done so that during plotting the points are in order of increasing y
    x_coord = _df[x_label]
    y_coord = _df[y_label]
    param_avg   = _df[param_label]


    #### Get unique x coordinate values
    x_coord_uniq = x_coord.drop_duplicates()

    #### Convert all to numpy array
    x_coord      = x_coord.to_numpy()
    x_coord_uniq = x_coord_uniq.to_numpy()
    y_coord      = y_coord.to_numpy()
    param_avg    = param_avg.to_numpy()

    y_coord[y_coord==0]     = 1e-8 # Set 0s to a small positive value so that they don't get removed later
    param_avg[param_avg==0] = 1e-8

    return x_coord, x_coord_uniq, y_coord, param_avg

def stat_compare(x_range, data_tuple, scales):
    '''
    This function plots the comparison between turbulence models for their prediction of turbulence energy, k
    Input:
    x_range       - wanted values of x-axis for statistical analysis
    data_tuple    - tuples of data of models to be compared (preferrably 3) - LES should be first then PANS then RANS
    data_type     - tuples of strings of the names of the models
    param_to_plot - parameter that is to be plotted ('k', 'u', or 'p')
    plot_scale    - scale as to which the parameter should be divided by to be well visualised in plot

    Output:
    plot for visual comparison

    '''
    fig, ax = plt.subplots(1, x_range.shape[0])
    plot_title = "time averaged"
    fig.suptitle(plot_title)
    ax[0].set_xlabel("y")
    fig.supxlabel('x')

    data_set = len(data_tuple)
    colours = ['k', 'b', 'r', 'c']

    for count, i in enumerate(x_range):

        # ax[i].plot([i,i], [-0.06,0.06], color='grey', linestyle='dashed', alpha=0.8)
       
        for j in np.arange(data_set):
        
            data         = data_tuple[j]
            x_coord      = data[0]
            x_coord_uniq = data[1]
            y_coord      = data[2]
            param_avg    = data[3]
            xdiff = np.abs(x_coord_uniq - i)
            # print(np.min(xdiff))
            idxBool = (xdiff == np.min(xdiff))*1
            x = x_coord_uniq[idxBool==1]
            # print(x)
            xBool = (x == x_coord) * 1
            # if np.sum(xBool) < int(57/2):
            # xBool = (np.abs(x - x_coord)<1e-3) * 1

            X = x_coord * xBool
            X = X[X!=0]
            Y = y_coord * xBool
            Y = Y[Y!=0]
            # print(np.min(Y), np.max(Y))
            param = param_avg * xBool
            param = param[param!=0]
            # print(param.shape)

            _plot = param/scale + 0

            start = 0
            end = None
            col = colours[j]
            ax[count].plot(_plot, Y, color=col)
            if count !=0:
                ax[count].get_yaxis().set_visible(False)
    
    
    return 


_param = 'k'


if _param == 'k':
    les_param  = 'k_average'
    pans_param = 'k_average'
    # scales = [1000, 1000, 1000] # need to have a large scale factor for the LES k data
    scale = 1000

elif _param == 'u':
    les_param = 'Velocity_0_average'
    pans_param = 'U_average:0'
    # scales = [500, 500, 500] # need to have a large scale factor for the LES k data
    scale = 500


les_avg = extract_param('LES_param.csv', 'Points:0', 'Points:1', les_param) # data has z-axis as the vertical axis
pans_avg2 = extract_param('PANS02avg.csv', 'Points:0', 'Points:1', pans_param)
pans_avg2b = extract_param('PANS02bavg.csv', 'Points:0', 'Points:1', pans_param)

pans_avg4 = extract_param('PANS04avg.csv', 'Points:0', 'Points:1', pans_param)
pans_avg10 = extract_param('PANS10avg.csv', 'Points:0', 'Points:1', pans_param)
sst_avg = extract_param('SST_avg.csv', 'Points:0', 'Points:1', pans_param)


x_range = np.linspace(0.05, 0.4, 7)



stat_compare(x_range, [les_avg, pans_avg2, pans_avg4, sst_avg], scale)
plt.legend(['LES', 'PANS fk=0.2', 'PANS fk=0.4', 'sst'])

# stat_compare(x_range, [pans_avg2, pans_avg4, sst_avg], scales)
# plt.legend(['zero line','PANS fk=0.2', 'PANS fk=0.4','SST'])
plt.show()