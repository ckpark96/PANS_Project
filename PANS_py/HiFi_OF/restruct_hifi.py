'''
This program aims to restructure the HiFi .csv dataset to one that is readable by OpenFOAM
The required parameters to be extracted are: U, p, k_LES, tauij_LES 
'''
import shutil
import numpy as np
import pandas as pd


### need to loop through all time steps
### This is for a single time step
time = 0.1

df = pd.read_csv('TESTCSV.csv')
blockNames = pd.unique(df['Block Name'])

# Write location line which includes the time step
Loc = '    location    "' + str(time) + '";\n' 

veldim = "[0 1 -1 0 0 0 0]"
pdim   = "[0 2 -2 0 0 0 0]" # OF uses kinematic pressure = pres/rho
kdim   = pdim
taudim = pdim

for block in blockNames: # various boundaries
    blockBool = df['Block Name']==block
    N = np.sum(blockBool)


    if block=='internalMesh':
        fields = df[blockBool] # remove other boundaries

        # for count, param in enumerate(params):

        ##### PRESSURE #####
        shutil.copy2('OF_header', 'LES/'+str(time)+'/p')
        copy_pres_file = open("LES/"+str(time)+"/p","a") # open with append option
        
        copy_pres_file.write("    class       volScalarField;\n")
        copy_pres_file.write(Loc)
        copy_pres_file.write("    object      p;\n}\n")
        copy_pres_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
        copy_pres_file.write("dimensions      "+ pdim + ";\n \n")
        copy_pres_file.write("internalField   nonuniform List<scalar> \n"+str(N)+"\n(\n")

        pdf = fields['pressure_avg']
        pdf.to_csv('presField',index=False, header=False)

        presField_file = open('presField','r')
        copy_pres_file.write(presField_file.read())
        presField_file.close()
        copy_pres_file.write(")\n;\n")

        presFooter_file = open('p_footer','r')
        copy_pres_file.write(presFooter_file.read())
        presFooter_file.close()
        copy_pres_file.close()
        ##### END OF PRESSURE #####

        ##### VELOCITY #####
        shutil.copy2('OF_header', 'LES/'+str(time)+'/U')
        copy_vel_file = open('LES/'+str(time)+'/U',"a")

        copy_vel_file.write("    class       volVectorField;\n")
        copy_vel_file.write(Loc)
        copy_vel_file.write("    object      U;\n}\n")
        copy_vel_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
        copy_vel_file.write("dimensions      "+ veldim + ";\n \n")
        copy_vel_file.write("internalField   nonuniform List<vector> \n"+str(N)+"\n(\n")

        Udf = pd.DataFrame()
        Udf['left'] = np.full(shape=N,fill_value='(')
        Udf[['U0','U1','U2']] = fields[['Velocity:0_avg','Velocity:1_avg', 'Velocity:2_avg']]
        Udf['right'] = np.full(shape=N,fill_value=')')
        Udf.to_csv('velField',sep=' ',index=False, header=False)

        velField_file = open('velField','r')
        copy_vel_file.write(velField_file.read())
        velField_file.close()
        copy_vel_file.write(")\n;\n")

        velFooter_file = open('U_footer','r')
        copy_vel_file.write(velFooter_file.read())
        velFooter_file.close()
        copy_vel_file.close()
        ###### END OF VELOCITY #####






# ###### internal Field
# IFbool = df['Block Name']=='internal Mesh'
