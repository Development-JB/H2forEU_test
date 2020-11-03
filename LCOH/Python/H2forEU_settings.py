# Settings file

# Import packages
from pathlib import Path
import pandas as pd

# Import files
import H2forEU_config_general

val_reference_year = 2016
#val_turbine_type = 'Vestas_V112'
#val_turbine_type = 'Vestas_V80'
val_turbine_type = 'Enercon_E101'

#path_folder_res_profiles = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles"
path_folder_res_profiles = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2"
path_folder_gdx = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\gdx"
path_file_gms = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\H2forEU_LCOH_main.gms"
path_folder_gams_working_directory = 'C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\'

val_path_settings = Path(str(H2forEU_config_general.wd_l3)+"//Data//01Input//Settings.xls")
val_path_data_general = Path(str(H2forEU_config_general.wd_l3)+"//Data//01Input//Data_general.xls")
val_path_inputs = str(H2forEU_config_general.wd_l3)+"//Data//01Input//"
val_path_templates = str(H2forEU_config_general.wd_l3)+"//Data//00Templates//"
val_path_gdx_output = Path(str(H2forEU_config_general.wd_l1)+"//GAMS//gdx//")



df_system = pd.read_excel(val_path_settings, sheet_name = 'System')
lst_system = df_system.columns

df_electrolyser= pd.read_excel(val_path_settings, sheet_name = 'Electrolyser')
lst_electrolyser = df_electrolyser['Electrolyser'].tolist()

df_year = pd.read_excel(val_path_settings, sheet_name = 'Year')
lst_year = df_year['Year'].tolist()

df_cell = pd.read_excel(val_path_settings, sheet_name = 'Cell')
lst_cell = df_cell['Id_cell'].tolist()

lst_country = df_cell['Id_cell'].str[:3].drop_duplicates(keep='first').tolist()

df_data = pd.read_excel(val_path_data_general, sheet_name = 'Data')
df_data = df_data.drop(['Unit'], axis=1)
df_data = df_data.set_index(['Data_category1','Data_category2','Data_category3'])
df_data = df_data.interpolate(axis=1)
df_data = df_data.stack().reset_index(name='Value')
df_data = df_data.rename(columns={'level_3':'Year'})
df_data = df_data[df_data['Year'].isin(lst_year)]
df_data = df_data.set_index(['Data_category1','Data_category2','Data_category3','Year'])
