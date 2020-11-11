# Settings file

# Import packages
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import date

# Import files
import LCOH_config_general

### Settings
date_today = date.today().strftime('%y%m%d')

tolerance = 0.001

### Optimization
x_min = 0
x_max = 10
y_min = 0
y_max = 10

dim_x = 4
dim_y = 4

dim_x_1d = 5

x_range_1d_init = np.linspace(x_min, x_max,dim_x_1d)
x_range_init = np.linspace(x_min, x_max,dim_x)
y_range_init = np.linspace(y_min, y_max,dim_y)

### Plotting
# Steps of crosscheck plot
check_steps = 10

### General
val_reference_year = 2016
#val_turbine_type = 'Vestas_V112'
#val_turbine_type = 'Vestas_V80'
val_turbine_type = 'Enercon_E101'

path_folder_res_profiles = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2"
val_path_settings = Path(str(LCOH_config_general.wd_l1)+"//Data//01Input//Settings.xls")
val_path_data_general = Path(str(LCOH_config_general.wd_l1)+"//Data//01Input//Data_general.xls")
val_path_inputs = str(LCOH_config_general.wd_l1)+"//Data//01Input//"
val_path_templates = str(LCOH_config_general.wd_l1)+"//Data//00Templates//"


df_system = pd.read_excel(val_path_settings, sheet_name = 'System')
lst_system = df_system.columns

df_electrolyser= pd.read_excel(val_path_settings, sheet_name = 'Electrolyser')
lst_electrolyser = df_electrolyser['Electrolyser'].tolist()

df_year = pd.read_excel(val_path_settings, sheet_name = 'Year')
lst_year = df_year['Year'].tolist()

df_cell = pd.read_excel(val_path_settings, sheet_name = 'Cell')
lst_cell = df_cell['Id_cell'].tolist()

lst_country = df_cell['Id_cell'].str[:3].drop_duplicates(keep='first').tolist()


### Input Data
df_data = pd.read_excel(val_path_data_general, sheet_name = 'Data')
df_data = df_data.drop(['Unit'], axis=1)
df_data = df_data.set_index(['Data_category1','Data_category2','Data_category3'])
df_data = df_data.interpolate(axis=1)
df_data = df_data.stack().reset_index(name='Value')
df_data = df_data.rename(columns={'level_3':'Year'})
df_data = df_data[df_data['Year'].isin(lst_year)]
df_data['Sensitivity'] = 'Default'

### Initiate Sensitivity
df_sensitivity = pd.read_excel(val_path_settings, sheet_name = 'Sensitivity')
df_sensitivity = df_sensitivity.drop(['Unit'], axis=1)
lst_sensitivity = ['Default'] + df_sensitivity['Sensitivity'].drop_duplicates( keep='first').tolist()
df_sensitivity = df_sensitivity.set_index(['Sensitivity','Data_category1','Data_category2','Data_category3'])
df_sensitivity = df_sensitivity.interpolate(axis=1).stack().reset_index(name='Value_sensitivity')
df_sensitivity = df_sensitivity.rename(columns={'level_4':'Year'})
df_sensitivity = df_sensitivity[df_sensitivity['Year'].isin(lst_year)]

for i_sensitivity in lst_sensitivity:

    if i_sensitivity != 'Default':

        df_sensitivity_temp = df_sensitivity[df_sensitivity['Sensitivity'] == i_sensitivity]
        df_sensitivity_temp = df_sensitivity_temp.drop(['Sensitivity'], axis=1)

        df_data_sensitivity_temp = df_data.copy()
        df_data_sensitivity_temp = df_data_sensitivity_temp.drop(['Sensitivity'], axis=1)

        df_data_sensitivity_temp = pd.merge(df_data_sensitivity_temp, df_sensitivity_temp, how='left', on=['Data_category1','Data_category2','Data_category3','Year'])
        df_data_sensitivity_temp['Value_sensitivity'] = df_data_sensitivity_temp['Value_sensitivity'].fillna(0)
        df_data_sensitivity_temp['Sensitivity'] = i_sensitivity
        df_data_sensitivity_temp['Value'] = df_data_sensitivity_temp['Value']*(1+df_data_sensitivity_temp['Value_sensitivity'])
        df_data_sensitivity_temp = df_data_sensitivity_temp.drop(['Value_sensitivity'], axis=1)

        df_data = df_data.append(df_data_sensitivity_temp)
        del df_data_sensitivity_temp, df_sensitivity_temp

df_data = df_data.set_index(['Sensitivity','Data_category1','Data_category2','Data_category3','Year'])



