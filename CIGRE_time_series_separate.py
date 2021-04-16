import os
import tempfile
import pandas as pd
from datetime import date



from CIGRE_LV_network import run_grid


def mkdir_p(mypath):
    '''Creates a directory. equivalent to using mkdir -p on the command line'''

    from errno import EEXIST
    from os import makedirs,path

    try:
        makedirs(mypath)
    except OSError as exc: # Python >2.5
        if exc.errno == EEXIST and path.isdir(mypath):
            pass
        else: raise

today = date.today()
day_now = today.strftime("%d%m%y")
'''To simulate time series in 1 year with 1-min resolution'''
datapoints_test = 365*24*60
'''To import power flow at each node (given in W)'''
file_ending = '1_050421' # '4_3_050421'
power_hh_to_grid_3 = pd.read_csv('power_exchange2grid_{}.csv'.format(file_ending), index_col=0, header=0)
'''Save the results at a temp folder'''
output_dir = os.path.join(tempfile.gettempdir(), "time_series_{}_oneyear_{}".format(file_ending,day_now))
print("Results can be found in your local temp folder: {}".format(output_dir))
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
'''To run the time series sim with CIGRE lv net'''
run_grid(output_dir, power_hh_to_grid_3, datapoints_test)
