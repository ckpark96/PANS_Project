import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RANS_file = "SST_cell_centers_avg.csv"
PANS_file = "fk02_cell_centers_avg.csv"
LES_file = "smaLES_cell_centers_avg.csv"
x_range = np.linspace(0.01, 0.26, 7)

def extract_param(filename, model_type):
    '''
    The .csv file for this function should be:
    slice-Z, cell center, temporal stats (more detail in docx)

    Input:
    filename - filename of the csv file as string
    model_type - Turbulence closure model type, RAS or LES in string

    Output:
    tuples of arrays - (x_coord, x_coord_unique, y_coord, k_avg)
    '''

    data = pd.read_csv(filename, header=0)

    #### Extract relevant parameters from the data
    x_coord = data['Points_0'].to_frame()
    y_coord = data['Points_1'].to_frame()
    u_avg   = data['U_average_0'].to_frame()
    p_avg   = data['p_average'].to_frame()


    if model_type == "RAS":
        k_avg = data['k_average'].to_frame()
        df      = x_coord.join(y_coord)
        _df     = df.join(k_avg)
        _df     = _df.join(u_avg)
        _df     = _df.join(p_avg)
        _df     = _df.sort_values(by=['Points_1'])
        x_coord = _df['Points_0']
        y_coord = _df['Points_1']
        k_avg   = _df['k_average']
        u_avg   = _df['U_average_0']
        p_avg   = _df['p_average']
        

    elif model_type == "LES":
        k_avg   = data['k_total_average'].to_frame()
        # k_avg   = data['k_average'].to_frame()
        df      = x_coord.join(y_coord)
        _df     = df.join(k_avg)
        _df     = _df.join(u_avg)
        _df     = _df.join(p_avg)
        _df     = _df.sort_values(by=['Points_1'])
        x_coord = _df['Points_0']
        y_coord = _df['Points_1']
        k_avg   = _df['k_total_average']
        # k_avg   = _df['k_average']
        u_avg   = _df['U_average_0']
        p_avg   = _df['p_average']
        # i_avg   = _df['turbint_average'].to_numpy


    #### Get unique x coordinate values
    x_coord_uniq = x_coord.drop_duplicates()

    #### Convert all to numpy array
    x_coord      = x_coord.to_numpy()
    x_coord_uniq = x_coord_uniq.to_numpy()
    y_coord      = y_coord.to_numpy()
    y_coord[y_coord==0] = 1e-8 # Set 0s to a small positive value so that they don't get removed later
    k_avg        = k_avg.to_numpy()
    k_avg[k_avg==0] = 1e-8
    u_avg        = u_avg.to_numpy()
    p_avg        = p_avg.to_numpy()

    return x_coord, x_coord_uniq, y_coord, k_avg, u_avg, p_avg


def stat_compare(x_range, data_tuple, data_to_plot, plot_scale):
    '''
    This function plots the comparison between turbulence models for their prediction of turbulence energy, k
    Input:
    x_range      - wanted values of x-axis for statistical analysis
    data_tuple   - tuples of data of models to be compared (preferrably 3) - LES should be first then PANS then RANS
    data_to_plot - parameter that is to be plotted ('k', 'u', or 'p')
    plot_scale   - scale as to which the parameter should be divided by to be well visualised in plot

    Output:
    plot for visual comparison

    '''
    fig, ax = plt.subplots()
    plot_title = "time averaged " + data_to_plot
    ax.set_title(plot_title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    x_ticks = np.hstack(([0],x_range))
    ax.set_xticks(x_ticks) 

    data_set = len(data_tuple)

    for i in x_range:

        for j in np.arange(data_set):
        
            data         = data_tuple[j]
            x_coord      = data[0]
            x_coord_uniq = data[1]
            y_coord      = data[2]
            k_avg        = data[3]
            u_avg        = data[4]
            p_avg        = data[5]
            
            xdiff = np.abs(x_coord_uniq - i)
            # print(np.min(xdiff))
            idxBool = (xdiff == np.min(xdiff))*1
            x = x_coord_uniq[idxBool==1]
            # print(x)
            xBool = (x == x_coord) * 1

            X = x_coord * xBool
            X = X[X!=0]
            Y = y_coord * xBool
            Y = Y[Y!=0]
            k = k_avg * xBool
            k = k[k!=0]
            u = u_avg * xBool
            u = u[u!=0]
            p = p_avg * xBool
            p = p[p!=0]

            print()

            
            if data_to_plot == 'k':
                # print(k[-1]) ## check boundary value
                # plot = k/plot_scale + x
                plot = k/100 + x
                
            elif data_to_plot == 'u':    
                plot = u/plot_scale + x
            elif data_to_plot == 'p':
                plot = p/plot_scale+ x

            start = 0
            end = None
            
            if j == 0:
                #### for LES
                ax.plot(plot[start:end], Y[start:end], color='k', label='LES')
            elif j == 1:
                # ax.scatter(plot[start:end], Y[start:end], color='r', marker ='.', label='PANS')
                print('')
            elif j == 2:
                # ax.scatter(plot[start:end], Y[start:end], color='b', marker ='.', label='SST')
                print('')

            ax.legend() if i == x_range[0] else None
    
    
    return 

RANS_data = extract_param(RANS_file, "RAS")
PANS_data = extract_param(PANS_file, "RAS")
LES_data = extract_param(LES_file, "LES")


stat_compare(x_range, (LES_data, PANS_data, RANS_data), 'k', 500)

plt.show()