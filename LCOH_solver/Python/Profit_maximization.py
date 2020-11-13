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
val_steps = 30

x_range = np.linspace(x_min,x_max,val_steps)
y_range = np.linspace(y_min,y_max,val_steps)

df_profile_pv_check = pd.read_csv(
    LCOH_settings.path_folder_res_profiles + "\\" + val_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
arr_pv = df_profile_pv_check[['Load_factor']].to_numpy()
df_profile_onshore_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + val_cell + "_Onshore_" + str(
    LCOH_settings.val_reference_year) + ".csv")
arr_onshore = df_profile_onshore_check[['Load_factor']].to_numpy()

arr_unit = np.empty(shape=[len(y_range),len(x_range)])
arr_h2_volume = np.empty(shape=[len(y_range),len(x_range)])
arr_lcoh = np.empty(shape=[len(y_range),len(x_range)])

for i_x in range(0,len(x_range),1):
    print(i_x)
    x_temp = x_range[i_x]

    for i_y in range(0,len(y_range),1):
        #print(i_y)
        y_temp = y_range[i_y]

        df_data_input = LCOH_tools.fct_prepare_input_data('Default', val_country, val_system, val_electrolyser, val_year)

        [arr_lcoh[i_y, i_x], arr_h2_volume[i_y, i_x]] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_temp, y_temp)

        arr_unit[i_y, i_x] = val_area_utilizable/(x_temp/(val_energy_density_pv*val_land_dedication_pv)+y_temp/(val_energy_density_onshore*val_land_dedication_onshore))


arr_lcoh = np.where(arr_lcoh>20, 20, arr_lcoh)
lcoh_max = np.amax(arr_lcoh)

arr_profit = arr_unit*arr_h2_volume*(lcoh_max-arr_lcoh)/1000

arr_profit = np.nan_to_num(arr_profit, nan=0)


x_opti_hybrid = 1.73
y_opti_hybrid = 1.31
x_opti_pv = 2.19
y_opti_pv = 0
x_opti_wind = 0
y_opti_wind = 2.39



import plotly.graph_objects as go
import pandas as pd

df_check = pd.DataFrame(arr_profit, index=y_range, columns=x_range)

fig = go.Figure(
    data=go.Surface(x=x_range, y=y_range, z=df_check.values,colorscale='Viridis'),
    layout=go.Layout(
        width=600,
        height=600,
    ))

fig.add_trace(go.Scatter3d(x=[x_opti_hybrid, x_opti_hybrid], y=[y_opti_hybrid, y_opti_hybrid], z=[0, np.amax(arr_profit)*1.1]))
fig.add_trace(go.Scatter3d(x=[x_opti_pv, x_opti_pv], y=[y_opti_pv, y_opti_pv], z=[0, np.amax(arr_profit)*1.1]))
fig.add_trace(go.Scatter3d(x=[x_opti_wind, x_opti_wind], y=[y_opti_wind, y_opti_wind], z=[0, np.amax(arr_profit)*1.1]))


fig.update_layout(
    scene = dict(zaxis = dict(nticks=4,),  #range=[5,20]),
                 xaxis = dict(tickvals = list(range(0,len(x_range),1)),
                              ticktext= np.round(x_range,2)),
                 yaxis = dict(tickvals = list(range(0,len(y_range),1)),
                              ticktext = np.round(y_range,2))))

fig.show()

