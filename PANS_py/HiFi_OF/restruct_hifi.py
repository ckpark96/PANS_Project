'''
This program aims to restructure the HiFi .csv dataset to one that is readable by OpenFOAM
The required parameters to be extracted are: U, p, k_LES, tauij_LES 
'''
import os
import shutil
import numpy as np
import pandas as pd
from pathlib import Path


avg_period = np.round(0.00825617201037862, 7) # round to 7 dp
# print(avg_period)

folder = 'LESPhaseAvgData_withBoundaries/'
blockdf = pd.read_csv(folder+'meshBlockNames.csv')
# print(blockdf.shape)
# internalField needs to come first
blockNames = pd.unique(blockdf['Block Name']) # internalField, inlet, topwall, botwall, prism, outlet
file_prefix = 'lesPhaseAvgBound_'
print(blockNames)

### need to loop through all time steps
### This is for a single time step
res = 100
time = np.arange(0,2)
write_time = np.linspace(0, avg_period, res+1)[:-1]


for t in time:
    Path("./LES_processed/"+str(write_time[t])).mkdir(0o755, parents=True, exist_ok=True)
    # access = 0o755
    # os.makedirs("/"+str(write_time[t]),access)
    df = pd.read_csv(folder+file_prefix+str(t)+'.csv')
    # print(df.columns)
    # Write location line which includes the time step
    Loc = '    location    "' + str(write_time[t]) + '";\n' 

    veldim = "[0 1 -1 0 0 0 0]"
    pdim   = "[0 2 -2 0 0 0 0]" # OF uses kinematic pressure = pres/rho
    kdim   = pdim
    taudim = pdim

    for block in blockNames: # various boundaries
        blockBool = blockdf['Block Name']==block
        N = np.sum(blockBool)
        fields = df[blockBool] # remove other boundaries/fields


        if block=='internalMesh':
            # for count, param in enumerate(params):

            ############### PRESSURE ###############
            shutil.copy2('OF_header', 'LES_processed/'+str(write_time[t])+'/p')
            copy_pres_file = open("LES_processed/"+str(write_time[t])+"/p","a") # open with append option
            
            copy_pres_file.write("    class       volScalarField;\n")
            copy_pres_file.write(Loc)
            copy_pres_file.write("    object      p;\n}\n")
            copy_pres_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
            copy_pres_file.write("dimensions      "+ pdim + ";\n \n")
            copy_pres_file.write("internalField   nonuniform List<scalar> \n"+str(N)+"\n(\n")

            pdf = fields['Pressure']
            pdf.to_csv('presField',index=False, header=False)

            presField_file = open('presField','r')
            copy_pres_file.write(presField_file.read())
            presField_file.close()
            copy_pres_file.write(")\n;\n")

            presFooter_file = open('p_footer','r')
            copy_pres_file.write(presFooter_file.read())
            presFooter_file.close()
            copy_pres_file.close()
            ############### END OF PRESSURE ###############




            ############### VELOCITY ###############
            shutil.copy2('OF_header', 'LES_processed/'+str(write_time[t])+'/U_LES')
            copy_vel_file = open('LES_processed/'+str(write_time[t])+'/U_LES',"a")

            copy_vel_file.write("    class       volVectorField;\n")
            copy_vel_file.write(Loc)
            copy_vel_file.write("    object      U_LES;\n}\n")
            copy_vel_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
            copy_vel_file.write("dimensions      "+ veldim + ";\n \n")
            copy_vel_file.write("internalField   nonuniform List<vector> \n"+str(N)+"\n(\n")

            Udf = pd.DataFrame()
            Udf['left'] = np.full(shape=N,fill_value='(')
            Udf[['U0','U1','U2']] = fields[['Velocity_0','Velocity_1', 'Velocity_2']]
            Udf['right'] = np.full(shape=N,fill_value=')')
            Udf.to_csv('velField',sep=' ',index=False, header=False)

            velField_file = open('velField','r')
            copy_vel_file.write(velField_file.read())
            velField_file.close()
            copy_vel_file.write(")\n;\n")

            velFooter_file = open('U_footer','r') # footers need to be updated
            copy_vel_file.write(velFooter_file.read())
            velFooter_file.close()
            copy_vel_file.close()
            ################ END OF VELOCITY ###############



            ################ tau_ij ################
            shutil.copy2('OF_header', 'LES_processed/'+str(write_time[t])+'/tauij_LES')
            copy_tau_file = open('LES_processed/'+str(write_time[t])+'/tauij_LES',"a")
            copy_tau_file.write("    class       volSymmTensorField;\n")
            copy_tau_file.write(Loc)
            copy_tau_file.write("    object      tauij_LES;\n}\n")
            copy_tau_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
            copy_tau_file.write("dimensions      "+ taudim + ";\n \n")
            copy_tau_file.write("internalField   nonuniform List<symmTensor> \n"+str(N)+"\n(\n")

            taudf = pd.DataFrame()
            taudf['left'] = np.full(shape=N,fill_value='(')
            taudf[['tau11','tau12','tau13','tau22','tau23','tau33']] = fields[['tau_11','tau_12','tau_13','tau_22','tau_23','tau_33']]
            taudf['right'] = np.full(shape=N,fill_value=')')
            taudf.to_csv('tauField',sep=' ',index=False, header=False)
            tauField_file = open('tauField','r')
            copy_tau_file.write(tauField_file.read())
            tauField_file.close()
            copy_tau_file.write(")\n;\n")

            tauFooter_file = open('tauij_footer','r')
            copy_tau_file.write(tauFooter_file.read())
            tauFooter_file.close()
            copy_tau_file.write("\n ")

            # copy_tau_file.close()
            ################ END OF TAU_IJ ################




            ################ TKE #################
            shutil.copy2('OF_header', 'LES_processed/'+str(write_time[t])+'/k_LES')
            copy_tke_file = open("LES_processed/"+str(write_time[t])+"/k_LES","a") # open with append option
            copy_tke_file.write("    class       volScalarField;\n")
            copy_tke_file.write(Loc)
            copy_tke_file.write("    object      k_LES;\n}\n")
            copy_tke_file.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // \n \n")
            copy_tke_file.write("dimensions      "+ kdim + ";\n \n")
            copy_tke_file.write("internalField   nonuniform List<scalar> \n"+str(N)+"\n(\n")

            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n\nboundaryField\n{\n    Side\n    {\n        type            empty;\n    }")
            ############### END OF TKE ################

        if block == 'Inlet':
            copy_tke_file.write("\n    Inlet\n    {\n        type            calculated;\n        value           nonuniform List<scalar>")
            copy_tke_file.write("\n"+str(N)+"\n(\n")
            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n    }")

        if block == 'botWall':
            copy_tke_file.write("\n    botWall\n    \n        type            calculated;\n        value           nonuniform List<scalar>")
            copy_tke_file.write("\n"+str(N)+"\n(\n")
            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n    }")
        
        if block == 'topWall':
            copy_tke_file.write("\n    topWall\n    \n        type            calculated;\n        value           nonuniform List<scalar>")
            copy_tke_file.write("\n"+str(N)+"\n(\n")
            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n    }")

        if block == 'Prism':
            copy_tke_file.write("\n    prism\n    \n        type            calculated;\n        value           nonuniform List<scalar>")
            copy_tke_file.write("\n"+str(N)+"\n(\n")
            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n    }")

        if block == 'Outlet':

            ################ tau_ij #################
            copy_tau_file.write(str(N))
            copy_tau_file.write("\n(\n")
            taudf = pd.DataFrame()
            taudf['left'] = np.full(shape=N,fill_value='(')
            taudf[['tau11','tau12','tau13','tau22','tau23','tau33']] = fields[['tau_11','tau_12','tau_13','tau_22','tau_23','tau_33']].reset_index(drop=True)
            taudf['right'] = np.full(shape=N,fill_value=')')
            taudf.to_csv('tauField',sep=' ',index=False, header=False)
            tauField_file = open('tauField','r')
            copy_tau_file.write(tauField_file.read())
            tauField_file.close()
            copy_tau_file.write(")\n;\n    }\n}\n\n\n// ************************************************************************* //")
            copy_tau_file.close()
            ################ END OF tau_ij #################



            ################ TKE #################
            copy_tke_file.write("\n    outlet\n    \n        type            calculated;\n        value           nonuniform List<scalar>")
            copy_tke_file.write("\n"+str(N)+"\n(\n")
            tkedf = fields['k']
            tkedf.to_csv('tkeField',index=False, header=False)
            tkeField_file = open('tkeField','r')
            copy_tke_file.write(tkeField_file.read())
            tkeField_file.close()
            copy_tke_file.write(")\n;\n    }\n}\n\n\n// ************************************************************************* //")
            copy_tke_file.close()
            ################ END OF TKE #################





    
    #### Here all the paramters need to be saved into a folder representing a single time step
    



# ###### internal Field
# IFbool = df['Block Name']=='internal Mesh'
