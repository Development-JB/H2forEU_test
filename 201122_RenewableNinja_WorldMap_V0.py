import requests
import pandas as pd
import json
import os
import numpy as np
import TOOLS
import time

from datetime import date

### Settings
date_today = date.today().strftime('%y%m%d')


df_centroids_init = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\201122_WordGrid_3DegreeCountriesCentroid_V2.csv")
df_centroids = df_centroids_init.copy()

#North name
df_centroids['Longitude_help'] = abs(df_centroids['Longitude'])
df_centroids['Longitude_name1'] = df_centroids['Longitude_help'].astype(str).str.split('.').str[0].str.zfill(3)
df_centroids['Longitude_name2'] = df_centroids['Longitude_help'].astype(str).str.split('.').str[1].str[:5]
df_centroids['Longitude_name'] = np.where(df_centroids['Longitude']>0,df_centroids['Longitude_name1']+'E'+df_centroids['Longitude_name2'],df_centroids['Longitude_name1']+'W'+df_centroids['Longitude_name2'])
df_centroids = df_centroids.drop(['Longitude_help','Longitude_name1','Longitude_name2'], axis=1)
#South name
df_centroids['Latitude_help'] = abs(df_centroids['Latitude'])
df_centroids['Latitude_name1'] = df_centroids['Latitude_help'].astype(str).str.split('.').str[0].str.zfill(3)
df_centroids['Latitude_name2'] = df_centroids['Latitude_help'].astype(str).str.split('.').str[1].str[:5]
df_centroids['Latitude_name'] = np.where(df_centroids['Latitude']>0,df_centroids['Latitude_name1']+'N'+df_centroids['Latitude_name2'],df_centroids['Latitude_name1']+'S'+df_centroids['Latitude_name2'])
df_centroids = df_centroids.drop(['Latitude_help','Latitude_name1','Latitude_name2'], axis=1)

# Optimal tilt angle
df_centroids = TOOLS.fct_calculate_optimal_tilt_angle_PV(df_centroids)


lst_ctry_not = ['DZA','TUN','RUS','UKR','AZE','EGY','QAT','ARE','ISR','JOR','KWT','MAR','OMN','YEM','TUR','ATA']
lst_ctry = df_centroids['Ctry_iso3'][~df_centroids['Ctry_iso3'].isin(lst_ctry_not)].drop_duplicates(keep='first').tolist()

token = '22b57f75700ebd2eab76caf2a453f9c87b5e74ac'
api_base = 'https://www.renewables.ninja/api/'

s = requests.session()
# Send token header with each request
s.headers = {'Authorization': 'Token ' + token}


year = 2017
lst_energy_group = ['Solar','Wind']

path_folder_save_results = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\ResNinja_World"


df_error = pd.DataFrame([])
for i_ctry in lst_ctry[:]:
    print(i_ctry)

    df_centroids_temp = df_centroids[df_centroids['Ctry_iso3']==i_ctry]
    df_locations = df_centroids_temp.copy()

    #df_locations = df_locations.set_index(df_locations.iloc[:,0])
    for i_location in df_locations.index.tolist()[:]:
        print(i_location)

        df_profile_res_temp = pd.DataFrame([])
        df_profile_res_temp['Timestamp'] = pd.date_range(start=str(year) + '-01-01 00:00',
                                                         end=str(year) + '-12-31 23:00',
                                                         freq='H')

        df_profile_solar_temp = pd.DataFrame([])
        df_profile_wind_temp = pd.DataFrame([])

        var_lat = df_locations.loc[i_location,'Latitude']
        print(var_lat)
        var_lon = df_locations.loc[i_location,'Longitude']
        print(var_lon)

        var_lat_name = df_locations.loc[i_location,'Latitude_name']
        var_lon_name = df_locations.loc[i_location,'Longitude_name']

        try:
            if 'Solar' in lst_energy_group:

                var_pv_capacity = 1000
                var_pv_loss = 0.1
                var_pv_tracking = 0
                var_pv_tilt = abs(df_locations.loc[i_location,'Tilt'])

                if var_lat >= 0:
                    var_pv_azim = 180
                else:
                    var_pv_azim = 0

                url_temp = api_base + 'data/pv'

                args = {
                    'lat': var_lat,
                    'lon': var_lon,
                    'date_from': str(year)+'-01-01',
                    'date_to': str(year)+'-12-31',
                    'dataset': 'merra2',
                    'capacity': var_pv_capacity,
                    'system_loss': var_pv_loss,
                    'tracking': var_pv_tracking,
                    'tilt': var_pv_tilt,
                    'azim': var_pv_azim,
                    'raw': True,
                    'format': 'json'
                }

                r = s.get(url_temp, params=args)

                # Parse JSON to get a pandas.DataFrame of data and dict of metadata
                parsed_response = json.loads(r.text)

                df_profile_solar_temp = pd.read_json(json.dumps(parsed_response['data']), orient='index')
                #metadata = parsed_response['metadata']
                df_profile_solar_temp = df_profile_solar_temp.reset_index()
                df_profile_solar_temp = df_profile_solar_temp.rename(columns={'index':'Timestamp',
                                                                        'electricity':'Generation',
                                                                        'irradiance_diffuse':'Irradiance_diffuce',
                                                                        'irradiance_direct':'Irradiance_direct',
                                                                        'temperature':'Temperature'})
                df_profile_solar_temp['Load_factor_pv'] = df_profile_solar_temp['Generation']/var_pv_capacity
                df_profile_solar_temp['Timestamp'] = pd.to_datetime(df_profile_solar_temp['Timestamp'],format='%Y-%m-%d %H:%M:%S')
                df_profile_solar_temp = df_profile_solar_temp[['Timestamp','Irradiance_diffuce','Irradiance_direct','Temperature','Load_factor_pv']]

                df_profile_res_temp = pd.merge(df_profile_res_temp,df_profile_solar_temp, how='left', on=['Timestamp'])

                # if not os.path.exists(path_folder_save_results+'\\Solar'):
                #     os.makedirs(path_folder_save_results+'\\Solar')
                # df_profile_solar_temp.to_csv(path_folder_save_results+'\\Solar\\'+i_location+'_PV.csv',index=False)

                if len(lst_energy_group)+len(df_locations.index.tolist()) > 6:
                    print(df_profile_solar_temp.head())
                    time.sleep(72)

            if 'Wind' in lst_energy_group:

                var_wind_capacity = 1000
                var_wind_loss = 0.1
                var_wind_height = 100
                var_wind_turbine = 'Vestas V80 2000'

                url_temp = api_base + 'data/wind'

                args = {
                    'lat': var_lat,
                    'lon': var_lon,
                    'date_from':
                        str(year)+'-01-01',
                    'date_to': str(year)+'-12-31',
                    'dataset': 'merra2',
                    'capacity': var_wind_capacity,
                    'height': var_wind_height,
                    'raw': True,
                    'turbine': var_wind_turbine,
                    'format': 'json'
                }

                r = s.get(url_temp, params=args)

                # Parse JSON to get a pandas.DataFrame of data and dict of metadata
                parsed_response = json.loads(r.text)

                df_profile_wind_temp = pd.read_json(json.dumps(parsed_response['data']), orient='index')
                #metadata = parsed_response['metadata']
                df_profile_wind_temp = df_profile_wind_temp.reset_index()
                df_profile_wind_temp = df_profile_wind_temp.rename(columns={'index':'Timestamp',
                                                                        'electricity':'Generation',
                                                                        'wind_speed':'Wind_speed'})
                df_profile_wind_temp['Load_factor_wind'] = df_profile_wind_temp['Generation']/var_wind_capacity
                df_profile_wind_temp['Timestamp'] = pd.to_datetime(df_profile_wind_temp['Timestamp'],format='%Y-%m-%d %H:%M:%S')
                df_profile_wind_temp = df_profile_wind_temp[['Timestamp','Wind_speed','Load_factor_wind']]

                df_profile_res_temp = pd.merge(df_profile_res_temp,df_profile_wind_temp, how='left', on=['Timestamp'])

                # if not os.path.exists(path_folder_save_results+'\\Wind'):
                #     os.makedirs(path_folder_save_results+'\\Wind')
                # df_profile_wind_temp.to_csv(path_folder_save_results+'\\Wind\\'+i_location+'_Wind_'+str(var_wind_height)+'m.csv',index=False)

                if len(lst_energy_group) + len(df_locations.index.tolist()) > 6:
                    print(df_profile_wind_temp.head())
                    time.sleep(72)

            # if not os.path.exists(path_folder_save_results+'\\Wind'):
            #     os.makedirs(path_folder_save_results+'\\Wind')
            df_profile_res_temp.to_csv(path_folder_save_results+'\\'+i_ctry+'-C_'+var_lon_name+'_'+var_lat_name+'.csv',index=False)

        except:
            df_error_temp = pd.DataFrame([[i_ctry, var_lon, var_lat, var_lon_name, var_lat_name]], columns=['Country_iso3','Longitude','Latitude','Longitude_name','Latitude_name'])
            df_error = df_error.append(df_error_temp)
            print('Error')

df_error.to_csv(path_folder_save_results+'\\'+str(date_today)+'Error_file_v2.csv',index=False)
