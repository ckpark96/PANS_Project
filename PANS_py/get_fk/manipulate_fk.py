import pandas as pd
import numpy as np
from csv import reader

def fk_file_creater(footer_file, fk_folder):
    '''
    Creates an fk file readable by OpenFOAM
    with wall boundaries as 0.1 and
    non-wall boundaries as 1.0
    '''
    parent_folder = "PANS_py/get_fk/"

    # num_cells = pd.DataFrame( list(reader([num_of_cells])))
    fk_head = pd.read_csv(parent_folder + "fk_header",header=None)
    footerFile = parent_folder + footer_file
    fk_foot = pd.read_csv(footerFile,header=None)
    # fk_footfoot = pd.read_csv("fk_footer2",header=None)
    # fk_end = pd.read_csv("fk_end",header=None)
    # boundFielddf = pd.DataFrame([boundary_Field])
    # bFieldVal = pd.DataFrame(100*np.ones((boundary_Field)))
    fk = pd.read_csv(fk_folder + "fk.csv",header=None)
    intField = pd.DataFrame([fk.shape[0]])
    # cylidf = pd.DataFrame([cylinder])
    # cyliVal = pd.DataFrame(100*np.ones((cylinder)))

    fk_file = fk_head.append(intField)
    fk_file = fk_file.append(pd.DataFrame(['(']))
    fk_file = fk_file.append(fk)
    fk_file = fk_file.append(fk_foot)
    # fk_file = fk_file.append(boundFielddf)
    # fk_file = fk_file.append(pd.DataFrame(['(']))
    # fk_file = fk_file.append(bFieldVal)
    # fk_file = fk_file.append(fk_footfoot)
    # fk_file = fk_file.append(cylidf)
    # fk_file = fk_file.append(pd.DataFrame(['(']))
    # fk_file = fk_file.append(cyliVal)
    # fk_file = fk_file.append(fk_end)
    file_name = fk_folder + "fk_openfoam"
    fk_file.to_csv(file_name, index=False, header=False)
    return 



