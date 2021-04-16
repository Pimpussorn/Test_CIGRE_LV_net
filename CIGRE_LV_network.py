import os
import numpy as np
import pandas as pd
import tempfile
import pandapower as pp
from pandapower.control import ConstControl
from pandapower.timeseries import DFData
from pandapower.timeseries import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries
import pandapower.networks as nw
import gc



def run_grid(output_dir, data, datapoints):
    # 1. create test net
    #net = simple_test_net()
    net = nw.create_cigre_network_lv()

    # 2. create (random) data source
    n_timesteps = datapoints
    profiles, ds = load_input(data=data)
    # profiles, ds = create_data_source(n_timesteps) # n_timesteps
    # 3. create controllers (to control P values of the load and the sgen)
    net = create_controllers(net, ds)

    # time steps to be calculated. Could also be a list with non-consecutive time steps
    time_steps = range(0, n_timesteps)

    # 4. the output writer with the desired results to be stored to files.
    ow = create_output_writer(net, time_steps, output_dir)

    # 5. the main time series function
    run_timeseries(net, time_steps)

    '''Try to clear memory'''
    # for element in dir():
    #     if element[0:2] != "__":
    #         del globals()[element]
    # del element
    del n_timesteps
    del profiles
    del ds
    del time_steps
    del ow
    del net
    gc.collect()

    #return net


def load_input(data):
    profiles = pd.DataFrame()
    profiles['load1_p'] = data.loc[:]['Node_1'] / 1000000
    profiles['load2_p'] = data.loc[:]['Node_2'] / 1000000
    profiles['load3_p'] = data.loc[:]['Node_3'] / 1000000
    profiles['load4_p'] = data.loc[:]['Node_4'] / 1000000
    profiles['load5_p'] = data.loc[:]['Node_5'] / 1000000
    # profiles['load1_p'] = data.loc[:]['HH_1'] * 10 / 1000000
    # profiles['load2_p'] = data.loc[:]['HH_2'] * 10 / 1000000
    # profiles['load3_p'] = data.loc[:]['HH_3'] * 10 / 1000000
    # profiles['load4_p'] = data.loc[:]['HH_4'] * 10 / 1000000
    # profiles['load5_p'] = data.loc[:]['HH_5'] * 10 / 1000000


    ds = DFData(profiles)

    return profiles, ds



def create_controllers(net, ds):
    ConstControl(net, element='load', variable='p_mw', element_index=[1],
                 data_source=ds, profile_name=["load1_p"])
    ConstControl(net, element='load', variable='p_mw', element_index=[2],
                 data_source=ds, profile_name=["load2_p"])
    ConstControl(net, element='load', variable='p_mw', element_index=[3],
                 data_source=ds, profile_name=["load3_p"])
    ConstControl(net, element='load', variable='p_mw', element_index=[4],
                 data_source=ds, profile_name=["load4_p"])
    ConstControl(net, element='load', variable='p_mw', element_index=[5],
                 data_source=ds, profile_name=["load5_p"])
    # ConstControl(net, element='sgen', variable='p_mw', element_index=[0],
    #              data_source=ds, profile_name=["sgen1_p"])
    return net


def create_output_writer(net, time_steps, output_dir):
    ow = OutputWriter(net, time_steps, output_path=output_dir, output_file_type=".xlsx", log_variables=list()) # .csv .xls

    # # create a mask to get the indices of all the hv buses in the grid
    # mask_hv_buses = (net.bus.vn_kv > 70.0) & (net.bus.vn_kv < 380.0)
    # hv_busses_index = net.bus.loc[mask_hv_buses].index
    # # create a mask to get the indices of all the mv buses in the grid
    # mask_mv_buses = (net.bus.vn_kv > 1.0) & (net.bus.vn_kv < 70.0)
    # mv_busses_index = net.bus.loc[mask_mv_buses].index
    # # now define the output writer, so that it gets the indices and specify the evaluation functions
    # # since we want the maximum voltage of all mv buses, we provide the indices of the mv buses and the maximum
    # # function np.max. The variable "eval_name" is free to chose and contains the name of the column in
    # # which the results are saved.
    #pp.create_measurement(net,"p","trafo",0,)
    ow.log_variable('res_trafo', 'loading_percent') #, index=0 )
    ow.log_variable('res_trafo', 'loading_percent', eval_function=np.max)
    ow.log_variable('res_trafo', 'p_hv_mw')
    ow.log_variable('res_trafo', 'p_lv_mw')
    ow.log_variable('res_trafo', 'q_hv_mvar')
    ow.log_variable('res_trafo', 'q_lv_mvar')
    ow.log_variable('res_trafo', 'pl_mw')
    ow.log_variable('res_trafo', 'ql_mvar')
    ow.log_variable('res_trafo', 'vm_lv_pu')
    ow.log_variable('res_trafo', 'vm_hv_pu')
    ow.log_variable('res_trafo', 'i_lv_ka')
    ow.log_variable('res_trafo', 'i_hv_ka')
    ow.log_variable('res_bus', 'p_mw')
    ow.log_variable('res_bus', 'p_mw',  eval_function=np.sum, eval_name="lv_bus_sum_p") #index=[2,12],
    ow.log_variable('res_bus', 'vm_pu')
    ow.log_variable('res_bus', 'vm_pu', eval_function=np.max, eval_name="lv_bus_max")
    ow.log_variable('res_line', 'p_to_mw')
    ow.log_variable('res_line', 'i_to_ka')
    ow.log_variable('res_line', 'vm_to_pu')
    ow.log_variable('res_line', 'va_to_degree')
    ow.log_variable('res_line', 'loading_percent')
    return ow

# output_dir = os.path.join(tempfile.gettempdir(), "time_series_example")
# print("Results can be found in your local temp folder: {}".format(output_dir))
# if not os.path.exists(output_dir):
#     os.mkdir(output_dir)
# net_end = timeseries_example(output_dir)

print()


