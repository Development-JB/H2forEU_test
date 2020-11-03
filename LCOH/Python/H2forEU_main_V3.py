import time
start_time = time.time()

# Import packages
import gdxpds
import pandas as pd
from gams import *
import glob
import os

# Import files
import H2forEU_settings
import H2forEU_config_time
import H2forEU_tools_write_gdx


ws = GamsWorkspace(working_directory=H2forEU_settings.path_folder_gams_working_directory)


# Load all data
df_data = H2forEU_settings.df_data

df_capex = df_data.loc[pd.IndexSlice['Technology', :,'Capex', :], :]
df_capex = df_capex.reset_index()
df_capex = df_capex[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_capex', df_capex, ['YEAR', 'TECHNOLOGY', 'Value'],
                                                       H2forEU_settings.path_folder_gdx)

df_opex = df_data.loc[pd.IndexSlice['Technology', :,'Opex', :], :]
df_opex = df_opex.reset_index()
df_opex = df_opex[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_opex', df_opex, ['YEAR', 'TECHNOLOGY', 'Value'],
                                                       H2forEU_settings.path_folder_gdx)

df_lifetime = df_data.loc[pd.IndexSlice['Technology', :,'Lifetime', :], :]
df_lifetime = df_lifetime.reset_index()
df_lifetime = df_lifetime[['Year', 'Data_category2', 'Value']]
H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_lifetime', df_lifetime, ['YEAR', 'TECHNOLOGY', 'Value'],
                                                       H2forEU_settings.path_folder_gdx)

var_decimals = 2

df_result = pd.DataFrame()
for i_cell in H2forEU_settings.lst_cells:
    print(i_cell)

    i_country = i_cell[:3]
    #print(i_country)

    df_wacc_temp = df_data.loc[pd.IndexSlice['Financing', 'Wacc', i_country, :], :]
    df_wacc_temp = df_wacc_temp.reset_index()
    df_wacc_temp = df_wacc_temp[['Year','Value']]
    H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_wacc', df_wacc_temp, ['YEAR','Value'], H2forEU_settings.path_folder_gdx)



    for i_system in H2forEU_settings.lst_system:
        print(i_system)
        df_res_profile = pd.DataFrame([])

        lst_energy_type = []
        lst_energy_type = H2forEU_settings.df_system.loc[:,i_system].tolist()
        lst_energy_type = [x for x in lst_energy_type if x == x]

        if 'PV' in lst_energy_type:
            df_res_profile_temp = pd.DataFrame()
            df_res_profile_temp = pd.read_csv(H2forEU_settings.path_folder_res_profiles + "\\PV\\" + i_cell + "_PV.csv")
            df_res_profile_temp['Timestamp'] = pd.to_datetime(df_res_profile_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_temp = pd.merge(df_res_profile_temp,H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',on=['Timestamp'])
            df_res_profile_temp['Energy_type'] = 'PV'
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)
        else:
            df_res_profile_temp = pd.DataFrame()
            df_res_profile_temp = H2forEU_config_time.df_time_link[['Timestep_hour']]
            df_res_profile_temp['Energy_type'] = 'PV'
            df_res_profile_temp['Value'] = 0
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)

        if 'Onshore' in lst_energy_type:
            df_res_profile_temp = pd.DataFrame()
            df_res_profile_temp = pd.read_csv(H2forEU_settings.path_folder_res_profiles+"\\Onshore\\"+i_cell+"_Wind.csv")
            df_res_profile_temp['Timestamp'] = pd.to_datetime(df_res_profile_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_temp = pd.merge(df_res_profile_temp,H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',on=['Timestamp'])
            df_res_profile_temp['Energy_type'] = 'Onshore'
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)
        else:
            df_res_profile_temp = pd.DataFrame()
            df_res_profile_temp = H2forEU_config_time.df_time_link[['Timestep_hour']]
            df_res_profile_temp['Energy_type'] = 'Onshore'
            df_res_profile_temp['Value'] = 0
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)

        df_res_profile['Value'] = df_res_profile['Value'].round(var_decimals)
        df_res_profile = pd.pivot_table(data=df_res_profile, index=['Timestep_hour'], columns=['Energy_type'], values='Value')
        df_res_profile = df_res_profile.groupby(['PV','Onshore']).size().reset_index(name='Weighting')
        df_res_profile['Timestep'] = list(range(1,len(df_res_profile)+1,1))

        df_res_profile_stack = df_res_profile[['Timestep','PV','Onshore']].set_index(['Timestep']).stack().reset_index(name='Value')
        df_res_profile_stack.columns = ['Timestep','Energy_type','Value']

        # Timesteps
        H2forEU_tools_write_gdx.fct_write_gdx_single_set('TIMESTEP',df_res_profile[['Timestep']],['Timestep'], H2forEU_settings.path_folder_gdx)
        H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_profile',df_res_profile_stack,['Timestep','ENERGY_TYPE','Value'], H2forEU_settings.path_folder_gdx)
        H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_timestep_weighting',df_res_profile[['Timestep','Weighting']],['TIMESTEP','Value'], H2forEU_settings.path_folder_gdx)
        H2forEU_tools_write_gdx.fct_write_gdx_single_set('ENERGY_TYPE', pd.DataFrame(lst_energy_type), ['ENERGY_TYPE'], H2forEU_settings.path_folder_gdx)


        for i_electrolyser in H2forEU_settings.lst_electrolyser:
            #print(i_electrolyser)

            H2forEU_tools_write_gdx.fct_write_gdx_single_set('ELECTROLYSER', pd.DataFrame([i_electrolyser]), ['TECHNOLOGY'],H2forEU_settings.path_folder_gdx)
            lst_technology = lst_energy_type + [i_electrolyser]
            H2forEU_tools_write_gdx.fct_write_gdx_single_set('TECHNOLOGY', pd.DataFrame(lst_technology), ['TECHNOLOGY'],H2forEU_settings.path_folder_gdx)


            for i_year in H2forEU_settings.lst_year:
                #print(i_year)

                H2forEU_tools_write_gdx.fct_write_gdx_single_set('YEAR',pd.DataFrame([i_year]),['YEAR'], H2forEU_settings.path_folder_gdx)

                t1 = ws.add_job_from_file(H2forEU_settings.path_file_gms)
                t1.run()
                del t1

                # # Prepare outputs
                df_gdx = gdxpds.to_dataframes(H2forEU_settings.path_folder_gdx + '\\' + '00_results.gdx')

                df_result_temp = pd.DataFrame([[i_cell, i_system, i_electrolyser]], columns=['Cell','System','Electrolyser'])

                df_capacity_temp = df_gdx['p_capacity'].set_index(['ENERGY_TYPE'])
                if 'PV' in df_capacity_temp.index.tolist():
                    df_result_temp['PV'] = df_capacity_temp.loc['PV','Value']
                else:
                    df_result_temp['PV'] = 0

                if 'Onshore' in df_capacity_temp.index.tolist():
                    df_result_temp['Onshore'] = df_capacity_temp.loc['Onshore','Value']
                else:
                    df_result_temp['Onshore'] = 0

                df_result_temp['LCOH'] = df_gdx['p_LCOH'].iloc[0,0]

                df_result = df_result.append(df_result)

                print('Done')


    for i_file in glob.glob(H2forEU_settings.path_folder_gams_working_directory + "_gams_py_gjo*.lst"):
        os.remove(i_file)
    for i_file in glob.glob(H2forEU_settings.path_folder_gams_working_directory + "_gams_py_gdb*.gdx"):
        os.remove(i_file)

df_result.to_csv("C:\\Users\\Johannes\\Desktop\\LCOH_result.csv", index=False)

end_time = time.time()
print(end_time - start_time)





