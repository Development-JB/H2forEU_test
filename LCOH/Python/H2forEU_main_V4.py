import time
start_time = time.time()

# Import packages
import gdxpds
import pandas as pd
import numpy as np
from gams import *
import glob
import os

# Import files
import H2forEU_settings
import H2forEU_config_time
import H2forEU_tools_write_gdx

var_decimals = 2
ws = GamsWorkspace(working_directory=H2forEU_settings.path_folder_gams_working_directory)


# Preparation
df_cell = pd.DataFrame(H2forEU_settings.lst_cell, columns=['Cell'])
df_cell['Country'] = df_cell['Cell'].str[:3]
df_year = pd.DataFrame(H2forEU_settings.lst_year, columns=['Year'])
df_system = pd.DataFrame(H2forEU_settings.lst_system, columns=['System'])
df_electrolyser = pd.DataFrame(H2forEU_settings.lst_electrolyser, columns=['Electrolyser'])
df_template = pd.merge(df_cell.assign(A=1), df_year.assign(A=1), on='A')
df_template = pd.merge(df_template, df_system.assign(A=1), on='A')
df_template = pd.merge(df_template, df_electrolyser.assign(A=1), on='A')
df_template = df_template.drop(['A'], axis=1)
df_template['Key_scenario'] = df_template['Cell']+'_'+df_template['Year'].astype(str)+'_'+df_template['System']+'_'+df_template['Electrolyser']
df_template['Iteration'] = list(range(1,len(df_template)+1,1))
# GDX creation

#LINKS
df_link_iteration_key = df_template[['Iteration','Key_scenario']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_ITERATION_KEY', df_link_iteration_key, ['ITERATION','KEY_SCENARIO'],H2forEU_settings.path_folder_gdx)
df_link_key_cell = df_template[['Key_scenario','Cell']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_CELL', df_link_key_cell, ['KEY_SCENARIO','CELL'],H2forEU_settings.path_folder_gdx)
df_link_key_country = df_template[['Key_scenario','Country']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_COUNTRY', df_link_key_country, ['KEY_SCENARIO','COUNTRY'],H2forEU_settings.path_folder_gdx)
df_link_key_year = df_template[['Key_scenario','Year']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_YEAR', df_link_key_year, ['KEY_SCENARIO','YEAR'],H2forEU_settings.path_folder_gdx)
df_link_key_system = df_template[['Key_scenario','System']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_SYSTEM', df_link_key_system, ['KEY_SCENARIO','SYSTEM'],H2forEU_settings.path_folder_gdx)
df_link_key_electrolyser = df_template[['Key_scenario','Electrolyser']]
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_ELECTROLYSER', df_link_key_electrolyser, ['KEY_SCENARIO','ELECTROLYSER'],H2forEU_settings.path_folder_gdx)

df_system2 = H2forEU_settings.df_system.copy()
df_system2 = df_system2.stack().reset_index()
df_system2.columns = ['Index','System','Energy_type']
df_system2 = df_system2[['System','Energy_type']]
df_link_key_energy_type = pd.merge(df_link_key_system,df_system2, how='left', on=['System'])
df_link_key_energy_type = df_link_key_energy_type.drop(['System'], axis=1)
del df_system2
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_ENERGY_TYPE', df_link_key_energy_type, ['KEY_SCENARIO','ENERGY_TYPE'],H2forEU_settings.path_folder_gdx)

df_link_key_technology1 = df_link_key_energy_type.copy()
df_link_key_technology1 = df_link_key_technology1.rename(columns={'Energy_type':'Technology'})
df_link_key_technology2 = df_link_key_electrolyser.copy()
df_link_key_technology2 = df_link_key_technology2.rename(columns={'Electrolyser':'Technology'})
df_link_key_technology = df_link_key_technology1.append(df_link_key_technology2).sort_values(['Key_scenario'])
del df_link_key_technology1, df_link_key_technology2
H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_TECHNOLOGY', df_link_key_technology, ['KEY_SCENARIO','TECHNOLOGY'],H2forEU_settings.path_folder_gdx)

# SET ITERATION
lst_iteration = df_template['Iteration'].tolist()
H2forEU_tools_write_gdx.fct_write_gdx_single_set('ITERATION', pd.DataFrame(lst_iteration), ['ITERATION'],
                                                 H2forEU_settings.path_folder_gdx)
# SET YEAR
H2forEU_tools_write_gdx.fct_write_gdx_single_set('YEAR', pd.DataFrame(H2forEU_settings.lst_year), ['YEAR'],
                                                 H2forEU_settings.path_folder_gdx)

# SET KEY_SCENARIO
lst_key = df_template['Key_scenario'].tolist()
H2forEU_tools_write_gdx.fct_write_gdx_single_set('KEY_SCENARIO', pd.DataFrame(lst_key), ['KEY_SCENARIO'],
                                                 H2forEU_settings.path_folder_gdx)
# SET COUNTRY
lst_country = df_template['Country'].drop_duplicates(keep='first').tolist()
H2forEU_tools_write_gdx.fct_write_gdx_single_set('COUNTRY', pd.DataFrame(lst_country), ['COUNTRY'],
                                                 H2forEU_settings.path_folder_gdx)
# SET CELL
H2forEU_tools_write_gdx.fct_write_gdx_single_set('CELL', pd.DataFrame(H2forEU_settings.lst_cell), ['CELL'],
                                                 H2forEU_settings.path_folder_gdx)

# SET ENERGY_TYPE
lst_energy_type = H2forEU_settings.df_system.stack().unique().tolist()
H2forEU_tools_write_gdx.fct_write_gdx_single_set('ENERGY_TYPE', pd.DataFrame(lst_energy_type), ['ENERGY_TYPE'],
                                                 H2forEU_settings.path_folder_gdx)
# SET ELECTROLYSER
H2forEU_tools_write_gdx.fct_write_gdx_single_set('ELECTROLYSER', pd.DataFrame(H2forEU_settings.lst_electrolyser), ['ELECTROLYSER'],
                                                 H2forEU_settings.path_folder_gdx)
# SET TECHNOLOGY
lst_technology = df_link_key_technology['Technology'].tolist()
H2forEU_tools_write_gdx.fct_write_gdx_single_set('TECHNOLOGY', pd.DataFrame(lst_technology), ['TECHNOLOGY'],
                                                 H2forEU_settings.path_folder_gdx)

# SET SYSTEM
H2forEU_tools_write_gdx.fct_write_gdx_single_set('SYSTEMS', pd.DataFrame(H2forEU_settings.lst_system), ['SYSTEMS'],
                                                 H2forEU_settings.path_folder_gdx)

del df_year, df_cell, df_electrolyser

# Load all data
df_data = H2forEU_settings.df_data

# parameter wacc
df_wacc_temp = df_data.loc[pd.IndexSlice['Financing', 'Wacc', :, :], :]
df_wacc_temp = df_wacc_temp.reset_index()
df_wacc_temp = df_wacc_temp.iloc[:,2:]
df_wacc_temp.columns = ['Country','Year','Value']
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_wacc', df_wacc_temp[['Year','Country','Value']], ['YEAR','COUNTRY','Value'],H2forEU_settings.path_folder_gdx)
del df_wacc_temp

# Parameter capex
df_capex = df_data.loc[pd.IndexSlice['Technology', :,'Capex', :], :]
df_capex = df_capex.reset_index()
df_capex = df_capex[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_capex', df_capex, ['YEAR', 'TECHNOLOGY', 'Value'],H2forEU_settings.path_folder_gdx)
del df_capex

# Parameter opex
df_opex = df_data.loc[pd.IndexSlice['Technology', :,'Opex', :], :]
df_opex = df_opex.reset_index()
df_opex = df_opex[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_opex', df_opex, ['YEAR', 'TECHNOLOGY', 'Value'],H2forEU_settings.path_folder_gdx)
del df_opex

# Parameter lifetime
df_lifetime = df_data.loc[pd.IndexSlice['Technology', :,'Lifetime', :], :]
df_lifetime = df_lifetime.reset_index()
df_lifetime = df_lifetime[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_lifetime', df_lifetime, ['YEAR', 'TECHNOLOGY', 'Value'],H2forEU_settings.path_folder_gdx)
del df_lifetime

# Parameter efficiency
df_efficiency = df_data.loc[pd.IndexSlice['Technology', :,'Efficiency', :], :]
df_efficiency = df_efficiency.reset_index()
df_efficiency = df_efficiency[df_efficiency['Data_category2'].isin(H2forEU_settings.lst_electrolyser)]
df_efficiency = df_efficiency[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_efficiency', df_efficiency, ['YEAR', 'ELECTROLYSER', 'Value'],H2forEU_settings.path_folder_gdx)
del df_efficiency

df_result = pd.DataFrame([])
for i_cell in H2forEU_settings.lst_cell:
    print(i_cell)

    df_res_profile = pd.DataFrame([])
    df_res_profile_weighting = pd.DataFrame([])
    for i_system in H2forEU_settings.lst_system:
        print(i_system)

        lst_energy_type = []
        lst_energy_type = H2forEU_settings.df_system.loc[:, i_system].tolist()
        lst_energy_type = [x for x in lst_energy_type if x == x]

        df_res_profile_system = pd.DataFrame([])
        if 'PV' in lst_energy_type:
            df_res_profile_system_temp = pd.DataFrame()
            df_res_profile_system_temp = pd.read_csv(H2forEU_settings.path_folder_res_profiles + "\\Solar\\" + i_cell + "_PV.csv")
            df_res_profile_system_temp['Timestamp'] = pd.to_datetime(df_res_profile_system_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_system_temp = pd.merge(df_res_profile_system_temp,
                                           H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',
                                           on=['Timestamp'])
            df_res_profile_system_temp['Energy_type'] = 'PV'
            df_res_profile_system_temp = df_res_profile_system_temp[['Timestep_hour', 'Energy_type', 'Load_factor']]
            df_res_profile_system = df_res_profile_system.append(df_res_profile_system_temp)
        else:
            df_res_profile_system_temp = pd.DataFrame()
            df_res_profile_system_temp = H2forEU_config_time.df_time_link[['Timestep_hour']]
            df_res_profile_system_temp['Energy_type'] = 'PV'
            df_res_profile_system_temp['Load_factor'] = 0
            df_res_profile_system_temp = df_res_profile_system_temp[['Timestep_hour', 'Energy_type', 'Load_factor']]
            df_res_profile_system = df_res_profile_system.append(df_res_profile_system_temp)

        if 'Onshore' in lst_energy_type:
            df_res_profile_system_temp = pd.DataFrame()
            df_res_profile_system_temp = pd.read_csv(
                H2forEU_settings.path_folder_res_profiles + "\\Wind\\" + i_cell + "_Wind_130m.csv")
            df_res_profile_system_temp['Wind_speed'] = df_res_profile_system_temp['Wind_speed'].round(1)
            df_power_curve = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\Wind_power_curve.csv")
            df_power_curve = df_power_curve[df_power_curve['Turbine_type'] == H2forEU_settings.val_turbine_type]
            df_res_profile_system_temp = pd.merge(df_res_profile_system_temp, df_power_curve[['Wind_speed','Load_factor']], how='left', on=['Wind_speed'])
            df_res_profile_system_temp.to_csv("C:\\Users\\Johannes\\Desktop\\LCOH_result.csv", index=False)
            del df_power_curve
            df_res_profile_system_temp['Timestamp'] = pd.to_datetime(df_res_profile_system_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_system_temp = df_res_profile_system_temp.drop(['Wind_speed'], axis=1)
            df_res_profile_system_temp = pd.merge(df_res_profile_system_temp,
                                           H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',
                                           on=['Timestamp'])
            df_res_profile_system_temp['Energy_type'] = 'Onshore'
            df_res_profile_system_temp = df_res_profile_system_temp[['Timestep_hour', 'Energy_type', 'Load_factor']]
            df_res_profile_system = df_res_profile_system.append(df_res_profile_system_temp)
        else:
            df_res_profile_system_temp = pd.DataFrame()
            df_res_profile_system_temp = H2forEU_config_time.df_time_link[['Timestep_hour']]
            df_res_profile_system_temp['Energy_type'] = 'Onshore'
            df_res_profile_system_temp['Load_factor'] = 0
            df_res_profile_system_temp = df_res_profile_system_temp[['Timestep_hour', 'Energy_type', 'Load_factor']]
            df_res_profile_system = df_res_profile_system.append(df_res_profile_system_temp)

        df_res_profile_system['Cell'] = i_cell
        df_res_profile_system['System'] = i_system

        df_res_profile_system['Load_factor'] = df_res_profile_system['Load_factor'].round(var_decimals)
        df_res_profile_system = pd.pivot_table(data=df_res_profile_system, index=['Timestep_hour', 'Cell', 'System'],columns=['Energy_type'], values='Load_factor')
        df_res_profile_system = df_res_profile_system.groupby(['Cell', 'System', 'PV', 'Onshore']).size().reset_index(name='Weighting')

        df_res_profile_system['Timestep'] = list(range(1, len(df_res_profile_system) + 1, 1))

        df_res_profile_system_stack = df_res_profile_system[['Timestep', 'Cell', 'System', 'PV', 'Onshore']].set_index(['Timestep', 'Cell', 'System']).stack().reset_index(name='Load_factor')
        df_res_profile_system_stack.columns = ['Timestep', 'Cell', 'System', 'Energy_type', 'Load_factor']


        df_res_profile = df_res_profile.append(df_res_profile_system_stack)
        del df_res_profile_system_stack
        df_res_profile_weighting = df_res_profile_weighting.append(df_res_profile_system[['Timestep', 'Cell', 'System','Weighting']])
        del df_res_profile_system, df_res_profile_system_temp



    # Timesteps
    H2forEU_tools_write_gdx.fct_write_gdx_single_set('TIMESTEP', df_res_profile[['Timestep']].drop_duplicates(keep='first'), ['TIMESTEP'], H2forEU_settings.path_folder_gdx)
    H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_profile', df_res_profile,
                                                           ['TIMESTEP','CELL','SYSTEM','ENERGY_TYPE', 'Value'],
                                                           H2forEU_settings.path_folder_gdx)

    H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_timestep_weighting',
                                                           df_res_profile_weighting[['Timestep','Cell','System', 'Weighting']],['TIMESTEP','CELL','SYSTEM','Value'], H2forEU_settings.path_folder_gdx)
    del df_res_profile_weighting

    df_link_key_timestep = pd.merge(df_res_profile[['Cell','System','Timestep']], df_template[['Key_scenario','Cell','System']], how='left', on=['Cell','System'])
    H2forEU_tools_write_gdx.fct_write_gdx_single_set('LINK_KEY_TIMESTEP',
                                                           df_link_key_timestep[['Key_scenario','Timestep']],['KEY_SCENARIO','TIMESTEP'], H2forEU_settings.path_folder_gdx)
    del df_link_key_timestep, df_res_profile

    t1 = ws.add_job_from_file(H2forEU_settings.path_file_gms)
    t1.run()
    del t1

    # Prepare outputs
    df_gdx = gdxpds.to_dataframes(H2forEU_settings.path_folder_gdx + '\\' + '00_results.gdx')

    df_result_temp_capacity = df_gdx['r_capacity']
    df_result_temp_capacity.columns = ['Key_scenario','Energy_type','Capacity']
    df_result_temp_capacity = df_result_temp_capacity.set_index(['Key_scenario','Energy_type']).unstack(['Energy_type']).droplevel(level=0, axis=1)
    df_result_temp_LCOH = df_gdx['r_LCOH']
    df_result_temp_LCOH.columns = ['Key_scenario', 'LCOH']
    df_result_temp_LCOH = df_result_temp_LCOH.set_index(['Key_scenario'])
    df_result_temp_h2_production = df_gdx['r_TotalProductionH2']
    df_result_temp_h2_production.columns = ['Key_scenario','H2_production']
    df_result_temp_h2_production = df_result_temp_h2_production.set_index(['Key_scenario'])

    df_result_temp = df_template.copy()
    df_result_temp['LCOH'] = np.nan
    df_result_temp['H2_production'] = np.nan
    for i_energy_type in lst_energy_type:
        df_result_temp[i_energy_type] = np.nan
    df_result_temp = df_result_temp.set_index('Key_scenario')

    df_result_temp = df_result_temp.combine_first(df_result_temp_LCOH)
    df_result_temp = df_result_temp.combine_first(df_result_temp_h2_production)
    df_result_temp = df_result_temp.combine_first(df_result_temp_capacity)

    df_result = df_result.append(df_result_temp)

    print('Done')

    for i_file in glob.glob(H2forEU_settings.path_folder_gams_working_directory + "_gams_py_gjo*.lst"):
        os.remove(i_file)
    for i_file in glob.glob(H2forEU_settings.path_folder_gams_working_directory + "_gams_py_gdb*.gdx"):
        os.remove(i_file)

end_time = time.time()
print(end_time - start_time)