import time
from datetime import date
import pandas as pd
import numpy as np

import LCOH_settings
import LCOH_call_function
import LCOH_tools


time_start = time.time()



df_result = pd.DataFrame([])
for i_country in LCOH_settings.lst_country[:1]:
    #print(i_country)

    lst_cell_country = [x for x in LCOH_settings.lst_cell if i_country in x]
    df_result_country = pd.DataFrame([])

    for i_cell in lst_cell_country[:1]:
        print(i_cell)

        df_profile_pv_temp = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + i_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_pv_temp = df_profile_pv_temp[['Load_factor']].to_numpy()
        df_profile_onshore_temp = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + i_cell + "_Onshore_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_onshore_temp = df_profile_onshore_temp[['Load_factor']].to_numpy()

        for i_system in LCOH_settings.lst_system[:]:
            #print(i_system)

            for i_electrolyser in LCOH_settings.lst_electrolyser[:]:
                #print(i_electrolyser)

                for i_sensitivity in LCOH_settings.lst_sensitivity[:]:
                    #print(i_sensitivity)

                    for i_year in LCOH_settings.lst_year[:]:
                        #print(i_year)

                        [lcoh_optimum, x_optimum, y_optimum, vol_optimum] = LCOH_call_function.run_optimization(i_sensitivity, i_country,i_system,i_electrolyser,i_year, arr_pv_temp, arr_onshore_temp)
                        df_result_temp = pd.DataFrame([[i_sensitivity, i_country,i_cell, i_system, i_electrolyser, i_year, x_optimum, y_optimum, lcoh_optimum, vol_optimum]],
                                                      columns=['Sensitivity','Country','Cell','System','Electrolyser','Year','PV','Onshore', 'Lcoh', 'H2_volume'])

                        df_result_country = df_result_country.append(df_result_temp)
                        df_result = df_result.append(df_result_temp)

        time_intermediate = time.time()
        print(time_intermediate-time_start)
print(df_result)


df_result.to_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH_solver\\"+str(LCOH_settings.date_today)+"_Results_LCOH_CentralEurope.csv", index=False)
df_result = df_result.set_index(['Sensitivity','Country','Cell','System','Electrolyser','Year'])



### Check
var_country = 'FRA'
var_cell = 'FRA_FR10'
var_system = 'PV'
var_electrolyser = 'Alkaline'
var_year = 2020
var_sensitivity = 'Default'

#LCOH_call_function.fct_check_results(var_sensititivity, var_country, var_cell, var_system, var_electrolyser, var_year, df_result)









