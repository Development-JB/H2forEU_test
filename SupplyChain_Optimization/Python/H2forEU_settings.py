# Settings file

# Import packages
from pathlib import Path
import pandas as pd
import numpy as np

# Import files
import H2forEU_config_general

val_reference_year = 2016

val_path_settings = Path(str(H2forEU_config_general.wd_l1)+"//Data//01Input//Input_settings.xls")
val_path_data_general = Path(str(H2forEU_config_general.wd_l1)+"//Data//01Input//Input_data_general.xls")
val_path_inputs = str(H2forEU_config_general.wd_l1)+"//Data//01Input//"
# val_path_templates = str(H2forEU_config_general.wd_l3)+"//Data//00Templates//"
val_path_gdx_output = Path(str(H2forEU_config_general.wd_l1)+"//GAMS//gdx//")

var_transport_national_distance_threshold = 1

df_set = pd.read_excel(val_path_settings, sheet_name='Sets')

df_year = df_set[['Year']]
df_year = df_year[~df_year['Year'].isna()]
df_year['Year'] = df_year['Year'].astype(int)
lst_year = df_year['Year'].tolist()

df_link_iteration_year = df_year.copy()
df_link_iteration_year['Iteration'] = list(range(1,len(df_year)+1,1))

df_node_production = df_set[['Node_production']]
df_node_production = df_node_production[df_node_production['Node_production'].astype(str) != 'nan']
lst_node_production = df_node_production['Node_production'].tolist()

df_node_export = df_set[['Node_export']]
df_node_export = df_node_export[df_node_export['Node_export'].astype(str) != 'nan']
lst_node_export = df_node_export['Node_export'].tolist()

df_node_import = df_set[['Node_import']]
df_node_import = df_node_import[df_node_import['Node_import'].astype(str) != 'nan']
lst_node_import = df_node_import['Node_import'].tolist()

df_energy_type = df_set[['Energy_type']]
df_energy_type = df_energy_type[df_energy_type['Energy_type'].astype(str) != 'nan']
lst_energy_type = df_energy_type['Energy_type'].tolist()

df_source = df_set[['Source']]
df_source = df_source[df_source['Source'].astype(str) != 'nan']
lst_source = df_source['Source'].tolist()

df_source_vres = df_set[['Source_vres']]
df_source_vres = df_source_vres[df_source_vres['Source_vres'].astype(str) != 'nan']
lst_source_vres = df_source_vres['Source_vres'].tolist()

df_technology = df_set[['Technology']]
df_technology = df_technology[df_technology['Technology'].astype(str) != 'nan']
lst_technology = df_technology['Technology'].tolist()

df_transport_national = df_set[['Transport_national']]
df_transport_national = df_transport_national[df_transport_national['Transport_national'].astype(str) != 'nan']
lst_transport_national = df_transport_national['Transport_national'].tolist()

df_transport_international = df_set[['Transport_international']]
df_transport_international = df_transport_international[df_transport_international['Transport_international'].astype(str) != 'nan']
lst_transport_international = df_transport_international['Transport_international'].tolist()

df_transport_national_mode = df_set[['Transport_national_mode']]
df_transport_national_mode = df_transport_national_mode[df_transport_national_mode['Transport_national_mode'].astype(str) != 'nan']
lst_transport_national_mode = df_transport_national_mode['Transport_national_mode'].tolist()

df_transport_international_mode = df_set[['Transport_international_mode']]
df_transport_international_mode = df_transport_international_mode[df_transport_international_mode['Transport_international_mode'].astype(str) != 'nan']
lst_transport_international_mode = df_transport_international_mode['Transport_international_mode'].tolist()

df_transport_conversion = df_set[['Transport_conversion']]
df_transport_conversion = df_transport_conversion[df_transport_conversion['Transport_conversion'].astype(str) != 'nan']
lst_transport_conversion = df_transport_conversion['Transport_conversion'].tolist()


df_link_node_production_export = pd.read_excel(val_path_data_general, sheet_name='Trans_national_distance')
df_link_node_production_export = df_link_node_production_export[['Node_production', 'Node_export']][df_link_node_production_export['Transport_national_distance']<= var_transport_national_distance_threshold]
df_link_node_production_export = df_link_node_production_export[df_link_node_production_export['Node_production'].isin(lst_node_production)]
df_link_node_production_export = df_link_node_production_export[df_link_node_production_export['Node_export'].isin(lst_node_export)]

df_link_node_export_import = pd.read_excel(val_path_data_general, sheet_name='Trans_international_distance')
df_link_node_export_import = df_link_node_export_import[['Node_export', 'Node_import']]
df_link_node_export_import = df_link_node_export_import[df_link_node_export_import['Node_import'].isin(lst_node_import)]
df_link_node_export_import = df_link_node_export_import[df_link_node_export_import['Node_export'].isin(lst_node_export)]

df_link_transport_national_mode = pd.read_excel(val_path_settings, sheet_name='Link_trans_national_mode')
df_link_transport_national_mode = df_link_transport_national_mode[['Transport_national', 'Transport_national_mode']]
df_link_transport_national_mode = df_link_transport_national_mode[df_link_transport_national_mode['Transport_national'].isin(lst_transport_national)]
df_link_transport_national_mode = df_link_transport_national_mode[df_link_transport_national_mode['Transport_national_mode'].isin(lst_transport_national_mode)]

df_link_transport_international_mode = pd.read_excel(val_path_settings, sheet_name='Link_trans_international_mode')
df_link_transport_international_mode = df_link_transport_international_mode[['Transport_international', 'Transport_international_mode']]
df_link_transport_international_mode = df_link_transport_international_mode[df_link_transport_international_mode['Transport_international'].isin(lst_transport_international)]
df_link_transport_international_mode = df_link_transport_international_mode[df_link_transport_international_mode['Transport_international_mode'].isin(lst_transport_international_mode)]


df_transport_national_distance = pd.read_excel(val_path_data_general, sheet_name='Trans_national_distance')
df_transport_national_distance = df_transport_national_distance[df_transport_national_distance['Node_production'].isin(lst_node_production)]
df_transport_national_distance = df_transport_national_distance[df_transport_national_distance['Node_export'].isin(lst_node_export)]
df_transport_national_distance = df_transport_national_distance[df_transport_national_distance['Transport_national_mode'].isin(lst_transport_national_mode)]
df_transport_national_distance = df_transport_national_distance.drop(['Unit'], axis=1)

df_transport_international_distance = pd.read_excel(val_path_data_general, sheet_name='Trans_international_distance')
df_transport_international_distance = df_transport_international_distance[df_transport_international_distance['Node_import'].isin(lst_node_import)]
df_transport_international_distance = df_transport_international_distance[df_transport_international_distance['Node_export'].isin(lst_node_export)]
df_transport_international_distance = df_transport_international_distance[df_transport_international_distance['Transport_international_mode'].isin(lst_transport_international_mode)]
df_transport_international_distance = df_transport_international_distance.drop(['Unit'], axis=1)

df_link_transport_conversion = pd.read_excel(val_path_settings, sheet_name='Link_trans_conversion')
df_link_transport_conversion = df_link_transport_conversion[df_link_transport_conversion['Transport_national'].isin(lst_transport_national)]
df_link_transport_conversion = df_link_transport_conversion[df_link_transport_conversion['Transport_international'].isin(lst_transport_international)]


df_link_source_energy_type = pd.read_excel(val_path_settings, sheet_name='LINK_SOURCE_ENERGY_TYPE')
df_link_source_energy_type = df_link_source_energy_type[['Source', 'Energy_type']]
df_link_source_energy_type = df_link_source_energy_type[df_link_source_energy_type['Source'].isin(lst_source)]
df_link_source_energy_type = df_link_source_energy_type[df_link_source_energy_type['Energy_type'].isin(lst_energy_type)]

df_link_source_technology = pd.read_excel(val_path_settings, sheet_name='LINK_SOURCE_TECHNOLOGY')
df_link_source_technology = df_link_source_technology[['Source', 'Technology']]
df_link_source_technology = df_link_source_technology[df_link_source_technology['Source'].isin(lst_source)]
df_link_source_technology = df_link_source_technology[df_link_source_technology['Technology'].isin(lst_technology)]



#Create Path
## Transport national
df_transport_path_national = pd.merge(df_transport_national_distance, df_link_transport_national_mode, how='left',on=['Transport_national_mode'])

## Transport international
df_transport_path_international = pd.merge(df_transport_international_distance, df_link_transport_international_mode,how='left', on=['Transport_international_mode'])


df_transport_path = pd.merge(df_transport_path_national, df_transport_path_international, how='left',on=['Node_export'])
df_transport_path = pd.merge(df_transport_path, df_link_transport_conversion, how='left',on=['Transport_national', 'Transport_international'])

df_transport_path['Transport_path'] = df_transport_path['Node_production'] \
                                      + '-' + df_transport_path['Transport_national'] \
                                      + '-' + df_transport_path['Node_export'] \
                                      + '-' + df_transport_path['Transport_international'] \
                                      + '-' + df_transport_path['Node_import']



# Create H2_System
df_link_source_energy_type_temp_res = df_link_source_energy_type[df_link_source_energy_type['Energy_type'].str.contains('PV|Onshore')][['Source']].drop_duplicates(keep='first')
df_link_source_node_production = df_node_production.copy()
df_link_source_node_production_temp_res = df_node_production[~df_node_production['Node_production'].str.contains('_CB|_CX')]
df_link_source_node_production_temp_res = pd.merge(df_link_source_node_production_temp_res.assign(A=1),df_link_source_energy_type_temp_res.assign(A=1), on=['A'])
df_link_source_node_production_temp_res = df_link_source_node_production_temp_res.drop(['A'], axis=1)
df_link_source_node_production_temp_non_res = df_node_production[df_node_production['Node_production'].str.contains('_CB|_CX')]
df_link_source_node_production = df_link_source_node_production_temp_res.append(df_link_source_node_production_temp_non_res)
df_link_source_node_production['Node_production'] = np.where(df_link_source_node_production['Node_production'].str.contains('_CB'),'Biomass',df_link_source_node_production['Node_production'])
df_link_source_node_production['Node_production'] = np.where(df_link_source_node_production['Node_production'].str.contains('_CX'),'Gas',df_link_source_node_production['Node_production'])

df_h2_system = pd.merge(df_link_source_node_production,df_link_source_energy_type, how='left',on=['Source'])
df_h2_system = pd.merge(df_h2_system,df_link_source_technology, how='left',on=['Source'])
df_h2_system['Country'] = df_h2_system['Node_production'].str[:3]
df_h2_system['H2_system'] = df_h2_system['Node_production']+'-'+df_h2_system['Source']+'-'+df_h2_system['Technology']

