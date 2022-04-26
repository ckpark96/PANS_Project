# from PANS_py.get_fk import calc_fk
from PANS_py.get_fk import *

sim_folder = 'pitzDaily_SST/'

cell_center = sim_folder + 'cell_centers_avg.csv'
time_avg_data = sim_folder + 'time_avg.csv'
edge_data = sim_folder + 'cell_edges.csv'

# calc_fk.extract_fk("omega", cell_center, time_avg_data, edge_data, "min", sim_folder)

manipulate_fk.fk_file_creater("fk_footer_pitz", sim_folder)