import time

start_time = time.time()


# Import packages
import gdxpds
import pandas as pd
from gams import *

# Import files
import H2forEU_settings
import H2forEU_config_time
import H2forEU_tools_write_gdx

df_data = H2forEU_settings.df_data

path_input_res_profiles = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\"
path_gdx = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\gdx"
path_gms_file = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\H2forEU_LCOH_main.gms"

from gams import *
import os
import sys

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         ws = GamsWorkspace(system_directory = sys.argv[1], working_directory='C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\')
#     else:

working_directory = 'C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\GAMS\\'
ws = GamsWorkspace(working_directory=working_directory)


df_electrolyer_capex_final = pd.DataFrame([])

H2forEU_tools_write_gdx.fct_write_gdx_single_set('TIMESTEP_HOUR',H2forEU_config_time.df_time_link[['Timestep_hour']],['TIMESTEP_HOUR'],path_gdx)



import glob



path = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Data\\03RawData\\ENTSOE_Transparency\\ForecastedYearAheadTransferCapacity\\*_ForecastedYearAheadTransferCapacities.csv"





for i_cell in H2forEU_settings.lst_cells:

    print(i_cell)

    i_country = i_cell[:3]
    print(i_country)

    df_res_profile = pd.DataFrame([])
    for i_system in H2forEU_settings.lst_system:
        print(i_system)

        lst_energy_type = H2forEU_settings.df_system.loc[:,i_system].tolist()
        lst_energy_type = [x for x in lst_energy_type if x == x]

        if 'PV' in lst_energy_type:

            df_res_profile_temp = pd.read_csv(path_input_res_profiles + "\\PV\\" + i_cell + "_PV.csv")
            df_res_profile_temp['Timestamp'] = pd.to_datetime(df_res_profile_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_temp = pd.merge(df_res_profile_temp,H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',on=['Timestamp'])
            df_res_profile_temp['Energy_type'] = 'PV'
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)

        if 'Onshore' in lst_energy_type:

            df_res_profile_temp = pd.read_csv(path_input_res_profiles+"\\Onshore\\"+i_cell+"_Wind.csv")
            df_res_profile_temp['Timestamp'] = pd.to_datetime(df_res_profile_temp['Timestamp'], format='%Y-%m-%d %H:%M')
            df_res_profile_temp = pd.merge(df_res_profile_temp,H2forEU_config_time.df_time_link[['Timestamp', 'Timestep_hour']], how='left',on=['Timestamp'])
            df_res_profile_temp['Energy_type'] = 'Onshore'
            df_res_profile_temp = df_res_profile_temp[['Timestep_hour','Energy_type', 'Value']]
            df_res_profile = df_res_profile.append(df_res_profile_temp)

        H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_profile',df_res_profile,['TIMESTEP_HOUR','ENERGY_TYPE','Value'],path_gdx)
        df_energy_types = pd.DataFrame(lst_energy_type, columns=['Energy_type'])
        H2forEU_tools_write_gdx.fct_write_gdx_single_set('ENERGY_TYPE', df_energy_types, ['ENERGY_TYPE'], path_gdx)

        for i_year in H2forEU_settings.lst_year:
            print(i_year)

            i_wacc = pd.DataFrame([df_data.loc[('Financing', 'Wacc', i_country), i_year]])
            i_wacc = i_wacc/100
            H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_wacc', i_wacc, ['Value'], path_gdx)

            df_res_capex = pd.DataFrame()
            df_res_opex = pd.DataFrame()
            df_res_lifetime = pd.DataFrame()

            for i_energy_type in lst_energy_type:
                print(i_energy_type)

                df_res_capex_temp = pd.DataFrame([df_data.loc[('Technology', i_energy_type, 'CAPEX'), i_year]])
                df_res_capex_temp.columns = ['Value']
                df_res_capex_temp['Energy_type'] = i_energy_type
                df_res_capex = df_res_capex.append(df_res_capex_temp)

                df_res_opex_temp = pd.DataFrame([df_data.loc[('Technology', i_energy_type, 'OPEX'), i_year]])
                df_res_opex_temp.columns = ['Value']
                df_res_opex_temp['Energy_type'] = i_energy_type
                df_res_opex = df_res_opex.append(df_res_opex_temp)

                df_res_lifetime_temp = pd.DataFrame([df_data.loc[('Technology', i_energy_type, 'Lifetime'), i_year]])
                df_res_lifetime_temp.columns = ['Value']
                df_res_lifetime_temp['Energy_type'] = i_energy_type
                df_res_lifetime = df_res_lifetime.append(df_res_lifetime_temp)

            #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_capex', df_res_capex[['Energy_type','Value']], ['ENERGY_TYPE','Value'], path_gdx)
            #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_opex', df_res_opex[['Energy_type','Value']], ['ENERGY_TYPE','Value'], path_gdx)
            #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_res_lifetime', df_res_lifetime[['Energy_type','Value']], ['ENERGY_TYPE','Value'],path_gdx)


            for i_technology in H2forEU_settings.lst_technology:
                print(i_technology)

                df_electrolyer_capex = pd.DataFrame([df_data.loc[('Technology', i_technology, 'CAPEX'), i_year]])
                #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_electrolyer_capex', df_electrolyer_capex, ['Value'],path_gdx)

                df_electrolyer_opex = pd.DataFrame([df_data.loc[('Technology', i_technology, 'OPEX'), i_year]])
                #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_electrolyer_opex', df_electrolyer_opex, ['Value'],path_gdx)

                df_electrolyer_lifetime = pd.DataFrame([df_data.loc[('Technology', i_technology, 'Lifetime'), i_year]])
                #H2forEU_tools_write_gdx.fct_write_gdx_single_parameter('p_electrolyer_lifetime', df_electrolyer_lifetime, ['Value'],path_gdx)

                t1 = ws.add_job_from_file(path_gms_file)
                t1.run()
                del t1

                df_gdx = gdxpds.to_dataframes(path_gdx + '\\' + '00_results.gdx')

                df_electrolyer_capex_temp = df_gdx['p_electrolyer_capex']
                df_electrolyer_capex_temp.columns = ['Value']
                df_electrolyer_capex_final = df_electrolyer_capex_final.append(df_electrolyer_capex_temp)

                print('Done')

    path_lst_files_temp = working_directory + "_gams_py_gjo*.lst"
    for i_file in glob.glob(path_lst_files_temp):
        os.remove(i_file)
    path_gdx_files_temp = working_directory + "_gams_py_gdb*.gdx"
    for i_file in glob.glob(path_gdx_files_temp):
        os.remove(i_file)


print(df_electrolyer_capex_final)

end_time = time.time()
print(end_time - start_time)





