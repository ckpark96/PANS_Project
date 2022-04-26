import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# def direction_avg(fileprefix, start, end, savename):
#     '''
#     This function aims to average a data of 3D domain in a single chosen dimension

#     Input:
#     fileprefix: prefix of the filename including folder name but excluding the numbering at the end


#     Output:
#     2D dataset with the third dimension averaged (aka flattened)
    
#     '''

#     for i in np.arange(start, end+1):
        
# df = pd.read_csv(fileprefix+str(i))
df = pd.read_csv('3Dsolut/sol_red.csv')
X  = df['Points:0'].unique()
Y  = df['Points:2'].unique()
Z  = df['Points:1'].unique()

vel_x = df['Velocity:0']
vel_y = df['Velocity:2']
vel_z = df['Velocity:1']
pres  = df['pressure']

uniqlen = X.shape[0]
newX    = np.zeros((uniqlen*uniqlen), dtype=float)
newY    = np.zeros_like(newX, dtype=float)
vel2D_x = np.zeros_like(newX, dtype=float)
vel2D_y = np.zeros_like(newX, dtype=float)
vel2D_z = np.zeros_like(newX, dtype=float)
pres2D  = np.zeros_like(newX, dtype=float)

for i, xval in enumerate(X):
    Xbool = (df['Points:0'] == xval)*1
    

    for j, yval in enumerate(Y):
        Ybool = (df['Points:2'] == yval)*1
        XYbool = Xbool * Ybool # Return True for same X- and Y-coordinates
        _len = np.sum(XYbool)
        # print('resolution in 3rd dimension =',_len) # Check if it returns pre-specified resolution
        
        idx = i*uniqlen+j
        print(idx)
        newX[idx]    = xval
        newY[idx]    = yval
        vel2D_x[idx] = np.sum(XYbool * vel_x) / _len
        vel2D_y[idx] = np.sum(XYbool * vel_y) / _len
        vel2D_z[idx] = np.sum(XYbool * vel_z) / _len
        pres2D[idx]  = np.sum(XYbool * pres) / _len

newZ = np.zeros_like(newX)
newdf = pd.DataFrame({'Points:0': newX, 'Points:1': newY, 'Points:2': newZ, 'Velocity:0': vel2D_x, 'Velocity:1': vel2D_y, 'Velocity:2': vel2D_z, 'Pressure': pres2D})
newdf.to_csv('test.csv', index=False)















    # return