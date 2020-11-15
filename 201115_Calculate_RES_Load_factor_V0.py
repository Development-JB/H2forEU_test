import pandas as pd
import glob
import numpy as np

from datetime import date

val_date_today = date.today().strftime('%y%m%d')

val_turbine_type = 'Enercon_E101'

path_folder_res_profiles = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2\\"
files = path_folder_res_profiles+'*PV_2016.csv'

## List all cell for which there are data available
lst_cell = []
for i_file in glob.glob(files):

    i_cell = i_file[-20:-12]
    lst_cell = lst_cell + [i_cell]


## Extract all data
df_data = pd.DataFrame([])
df_missing_data = pd.DataFrame([])
for i_cell in lst_cell:

    try:
        df_solar = pd.read_csv(path_folder_res_profiles+i_cell+'_PV_2016.csv')
        df_solar = df_solar.rename(columns={'Load_factor':'Load_factor_solar'})
        df_wind = pd.read_csv(path_folder_res_profiles+i_cell+'_Onshore_2016.csv')
        df_wind = df_wind.rename(columns={'Load_factor':'Load_factor_wind'})

        df_res = pd.merge(df_solar[['Timestamp','Load_factor_solar']],df_wind[['Timestamp','Load_factor_wind']], how='outer', on='Timestamp')

        val_load_factor_solar = df_res['Load_factor_solar'].mean()
        val_load_factor_wind = df_res['Load_factor_wind'].mean()
        val_correlation = df_res['Load_factor_solar'].corr(df_res['Load_factor_wind'])

        df_data_temp = pd.DataFrame([[i_cell, val_load_factor_solar, val_load_factor_wind, val_correlation]], columns=['Id_cell', 'PV', 'Wind', 'Correlation'])
        df_data = df_data.append(df_data_temp)
    except:
        df_missing_data_temp = pd.DataFrame([[i_cell]], columns=['Id_cell'])
        df_missing_data = df_missing_data.append(df_missing_data_temp)

df_data.to_csv(path_folder_res_profiles+str(val_date_today)+'_Summary_cells.csv', index=False)
df_missing_data.to_csv(path_folder_res_profiles+str(val_date_today)+'_MissingData_cells.csv', index=False)