
import pandas as pd
import numpy as np
import json


def fct_load_json_file():
    
    path_file_json = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\Python_Dash_Multipage_H2forEU\\datasets\\EU_NUTS2_V0.json"

    with open(path_file_json, encoding='utf-8') as geofile:
        json_nuts2 = json.load(geofile)

    # Add unique key to every element / row
    # Goes though all rows
    for i_feature in json_nuts2['features']:
        i_feature['id'] = i_feature['properties']['NUTS_ID']
    
    return json_nuts2

def fct_load_lcoh_result():

    path_file_results_lcoh = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\201102_Results_LCOH_CentralEurope.csv"
    df_nuts2_codes_fr = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
    df_lcoh = pd.read_csv(path_file_results_lcoh)
    df_lcoh['Nuts2_code2013'] = df_lcoh['Cell'].str[4:]
    df_lcoh = pd.merge(df_lcoh, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
    df_lcoh['NUTS_ID'] = df_lcoh['Nuts2_code2016'].combine_first(df_lcoh['Nuts2_code2013'])
    df_lcoh = df_lcoh.drop(['Nuts2_code2016','Nuts2_code2013'], axis=1)
    df_lcoh = df_lcoh.drop(['Alkaline', 'PEM'], axis=1)

    return df_lcoh

def fct_load_system_result():

    path_file_results_lcoh = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH_solver\\201115_Results_LCOH_CentralEurope.csv"
    df_nuts2_codes_fr = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
    df_colorbar = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")
    df_lcoh = pd.read_csv(path_file_results_lcoh)
    df_lcoh['Nuts2_code2013'] = df_lcoh['Cell'].str[4:]
    df_lcoh = pd.merge(df_lcoh, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
    df_lcoh['NUTS_ID'] = df_lcoh['Nuts2_code2016'].combine_first(df_lcoh['Nuts2_code2013'])
    df_lcoh['Ratio_hybrid'] = df_lcoh['Onshore']/(df_lcoh['PV']+df_lcoh['Onshore'])
    df_lcoh['Ratio_hybrid'] = df_lcoh['Ratio_hybrid'].round(2)
    df_lcoh = pd.merge(df_lcoh,df_colorbar[['Ratio_hybrid','Rgb']], how='left', on=['Ratio_hybrid'])

    df_lcoh = df_lcoh.drop(['Nuts2_code2016','Nuts2_code2013'], axis=1)

    return df_lcoh


def fct_load_res_information():

    df_res_information = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2\\201115_Summary_cells.csv")
    df_nuts2_codes_fr = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
    df_res_information['Nuts2_code2013'] = df_res_information['Id_cell'].str[4:]
    df_res_information = pd.merge(df_res_information, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
    df_res_information['NUTS_ID'] = df_res_information['Nuts2_code2016'].combine_first(df_res_information['Nuts2_code2013'])
    df_res_information = df_res_information.drop(['Nuts2_code2016','Nuts2_code2013'], axis=1)

    df_colorscale_load_factor = pd.DataFrame(range(0,1000+1,1), columns=['Load_factor'])
    df_colorscale_load_factor['Red'] = np.nan
    df_colorscale_load_factor['Green'] = np.nan
    df_colorscale_load_factor['Blue'] = np.nan
    df_colorscale_load_factor['Load_factor'] = df_colorscale_load_factor['Load_factor']/1000
    df_colorscale_load_factor = df_colorscale_load_factor.set_index(['Load_factor'])
    df_colorscale_load_factor.loc[0,'Red'] = 255
    df_colorscale_load_factor.loc[0,'Green'] = 255
    df_colorscale_load_factor.loc[0,'Blue'] = 255
    df_colorscale_load_factor.loc[0.12,'Red'] = 255
    df_colorscale_load_factor.loc[0.12,'Green'] = 255
    df_colorscale_load_factor.loc[0.12,'Blue'] = 255
    df_colorscale_load_factor.loc[0.3,'Red'] = 0
    df_colorscale_load_factor.loc[0.3,'Green'] = 0
    df_colorscale_load_factor.loc[0.3,'Blue'] = 0
    df_colorscale_load_factor.loc[1,'Red'] = 0
    df_colorscale_load_factor.loc[1,'Green'] = 0
    df_colorscale_load_factor.loc[1,'Blue'] = 0

    df_colorscale_load_factor = df_colorscale_load_factor.interpolate(axis=0).round(2)
    df_colorscale_load_factor['Rgb'] = 'rgb('+df_colorscale_load_factor['Red'].astype(str)+','+df_colorscale_load_factor['Green'].astype(str)+','+df_colorscale_load_factor['Blue'].astype(str)+')'

    return df_res_information, df_colorscale_load_factor