import pandas as pd
import numpy as np

import LCOH_tools
import LCOH_settings


val_country = 'FRA'
val_cell = 'FRA_FR10'
val_system = 'Hybrid'
val_electrolyser = 'Alkaline'
val_year = 2020
val_sensitivity = 'Default'
val_area_utilizable = 12
val_energy_density_pv = 170
val_land_dedication_pv = 0.03
val_energy_density_onshore = 5
val_land_dedication_onshore = 1

x_min = 0
x_max = 5
y_min = 0
y_max = 5
val_steps = 10

x_range = np.linspace(x_min,x_max,val_steps)
y_range = np.linspace(y_min,y_max,val_steps)

df_profile_pv_check = pd.read_csv(
    LCOH_settings.path_folder_res_profiles + "\\" + val_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
arr_pv = df_profile_pv_check[['Load_factor']].to_numpy()
df_profile_onshore_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + val_cell + "_Onshore_" + str(
    LCOH_settings.val_reference_year) + ".csv")
arr_onshore = df_profile_onshore_check[['Load_factor']].to_numpy()

arr_profit = np.empty(shape=[len(y_range),len(x_range)])

for i_x in range(0,len(x_range),1):
    print(i_x)
    x_temp = x_range[i_x]

    for i_y in range(0,len(y_range),1):
        print(i_y)
        y_temp = y_range[i_y]

        df_data_input = LCOH_tools.fct_prepare_input_data('Default', val_country, val_system, val_electrolyser, val_year)

        [lcoh, h2_volume] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_temp, y_temp)
        print(lcoh)
        print(h2_volume)

        if x_temp == 0:

        elif y_temp == 0:

        elif (x_temp == 0) & (y_temp == 0):

        else:
            arr_profit(i_y, i_x) = val_area_utilizable/(x_temp/(val_energy_density_pv*val_land_dedication_pv)+y_temp/(val_energy_density_onshore*val_land_dedication_onshore))


