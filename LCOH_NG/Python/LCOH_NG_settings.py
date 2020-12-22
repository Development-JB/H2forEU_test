# Settings file

# Import packages
from pathlib import Path
import pandas as pd
from datetime import date

# Import files
import LCOH_NG_config_general


### Settings
date_today = date.today().strftime('%y%m%d')
val_path_settings = Path(str(LCOH_NG_config_general.wd_l1)+"//Data//01Input//Settings.xls")
val_path_data_general = Path(str(LCOH_NG_config_general.wd_l1)+"//Data//01Input//Data_general.xls")
val_path_inputs = str(LCOH_NG_config_general.wd_l1)+"//Data//01Input//"
val_path_templates = str(LCOH_NG_config_general.wd_l1)+"//Data//00Templates//"


df_year = pd.read_excel(val_path_settings, sheet_name = 'Year')
lst_year = df_year['Year'].drop_duplicates(keep='first').tolist()

df_ctry = pd.read_excel(val_path_settings, sheet_name='Ctry')
lst_crty = df_ctry['Ctry_iso3'].drop_duplicates(keep='first').tolist()

df_technology = pd.read_excel(val_path_settings, sheet_name='Technology')
lst_technology = df_technology['Technology'].drop_duplicates(keep='first').tolist()

df_sensitivity = pd.read_excel(val_path_settings, sheet_name='Sensitivity')
lst_sensitivity = df_sensitivity['Sensitivity'].drop_duplicates(keep='first').tolist()
lst_sensitivity = lst_sensitivity + ['Default']

df_link_energy_type_technology = pd.read_excel(val_path_settings, sheet_name='Link_energy_type_technology')
df_link_energy_type_technology = df_link_energy_type_technology.set_index(['Technology'])


### Input Data
df_data = pd.read_excel(val_path_data_general, sheet_name = 'Data')
df_data = df_data.drop(['Unit'], axis=1)
df_data = df_data.set_index(['Data_category1','Data_category2','Data_category3'])
df_data = df_data.interpolate(axis=1)
df_data = df_data.stack().reset_index(name='Value')
df_data = df_data.rename(columns={'level_3':'Year'})
df_data = df_data[df_data['Year'].isin(lst_year)]
df_data['Sensitivity'] = 'Default'
df_data = df_data.set_index(['Sensitivity','Data_category1','Data_category2','Data_category3','Year'])