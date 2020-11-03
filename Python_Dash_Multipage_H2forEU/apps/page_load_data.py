import geopandas as gpd
import pandas as pd
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