import gdxpds
import pandas as pd
import numpy as np
import json

path_gdx = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\SupplyChain_Optimization\\GAMS\\gdx\\"
df_gdx_results = gdxpds.to_dataframes(path_gdx + "00_results.gdx")


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


def fct_load_results_supply():

    ### Supply
    df_supply = df_gdx_results['r_Supply']
    df_supply.columns = ['Year','H2_system','Path','Country','Source','Technology','Node_production','Transport_national','Node_export','Transport_international','Node_import','Volume']

    ### Lcoh
    df_lcoh = gdxpds.to_dataframes(path_gdx + "p_production_cost.gdx")
    df_lcoh = df_lcoh["p_production_cost"]
    df_lcoh.columns = ['Year','H2_system','Lcoh']
    df_results = pd.merge(df_supply,df_lcoh, how='left', on=['Year','H2_system'])

    ### Transport national
    df_transport_national_cost_fixed =  gdxpds.to_dataframes(path_gdx + "p_transport_national_cost_fixed.gdx")
    df_transport_national_cost_fixed = df_transport_national_cost_fixed["p_transport_national_cost_fixed"]
    df_transport_national_cost_fixed.columns = ['Year','Transport_national','Transport_national_cost_fixed']
    df_results = pd.merge(df_results,df_transport_national_cost_fixed, how='left', on=['Year','Transport_national'])

    df_transport_national_cost_variable =  gdxpds.to_dataframes(path_gdx + "p_transport_national_cost_variable.gdx")
    df_transport_national_cost_variable = df_transport_national_cost_variable["p_transport_national_cost_variable"]
    df_transport_national_cost_variable.columns = ['Year','Transport_national','Transport_national_cost_variable']
    df_results = pd.merge(df_results,df_transport_national_cost_variable, how='left', on=['Year','Transport_national'])

    df_transport_national_distance = gdxpds.to_dataframes(path_gdx + "p_transport_national_distance.gdx")
    df_transport_national_distance = df_transport_national_distance["p_transport_national_distance"]
    df_transport_national_distance.columns = ['Node_production','Node_export','Transport_national','Transport_national_distance']
    df_results = pd.merge(df_results,df_transport_national_distance, how='left', on=['Node_production','Node_export','Transport_national'])

    df_results['Transport_national_cost'] = df_results['Transport_national_cost_variable']+df_results['Transport_national_cost_fixed']*df_results['Transport_national_distance']

    ### Transport international
    df_transport_international_cost_fixed =  gdxpds.to_dataframes(path_gdx + "p_transport_international_cost_fixed.gdx")
    df_transport_international_cost_fixed = df_transport_international_cost_fixed["p_transport_international_cost_fixed"]
    df_transport_international_cost_fixed.columns = ['Year','Transport_international','Transport_international_cost_fixed']
    df_results = pd.merge(df_results,df_transport_international_cost_fixed, how='left', on=['Year','Transport_international'])

    df_transport_international_cost_variable =  gdxpds.to_dataframes(path_gdx + "p_transport_international_cost_variable.gdx")
    df_transport_international_cost_variable = df_transport_international_cost_variable["p_transport_international_cost_variable"]
    df_transport_international_cost_variable.columns = ['Year','Transport_international','Transport_international_cost_variable']
    df_results = pd.merge(df_results,df_transport_international_cost_variable, how='left', on=['Year','Transport_international'])

    df_transport_international_distance = gdxpds.to_dataframes(path_gdx + "p_transport_international_distance.gdx")
    df_transport_international_distance = df_transport_international_distance["p_transport_international_distance"]
    df_transport_international_distance.columns = ['Node_export','Node_import','Transport_international','Transport_international_distance']
    df_results = pd.merge(df_results,df_transport_international_distance, how='left', on=['Node_export','Node_import','Transport_international'])

    df_results['Transport_international_cost'] = df_results['Transport_international_cost_variable']+df_results['Transport_international_cost_fixed']*df_results['Transport_international_distance']


    ### Transport conversion cost
    df_transport_conversion_cost = gdxpds.to_dataframes(path_gdx + "p_transport_conversion_cost.gdx")
    df_transport_conversion_cost = df_transport_conversion_cost["p_transport_conversion_cost"]
    df_transport_conversion_cost.columns = ['Year','Transport_conversion','Transport_conversion_cost']

    df_link_path_conversion = gdxpds.to_dataframes(path_gdx + "LINK_PATH_CONVERSION.gdx")
    df_link_path_conversion = df_link_path_conversion["LINK_PATH_CONVERSION"]
    df_link_path_conversion.columns = ['Path','Transport_conversion','Value']
    df_link_path_conversion = df_link_path_conversion.drop(['Value'], axis=1)

    df_transport_conversion_cost = pd.merge(df_link_path_conversion,df_transport_conversion_cost, how='left', on=['Transport_conversion'])
    df_transport_conversion_cost = df_transport_conversion_cost.groupby(['Year','Path']).agg({'Transport_conversion_cost':'sum'}).reset_index()

    df_results = pd.merge(df_results, df_transport_conversion_cost, how='left', on=['Year','Path'])

    ### Total cost per kg H2
    df_results['Lcoh_fob'] = df_results['Lcoh']+df_results['Transport_national_cost']
    df_results['Lcoh_cif'] = df_results['Lcoh_fob']+df_results['Transport_international_cost']+df_results['Transport_conversion_cost']

    ### Add link regions and countries
    df_link_region_country = gdxpds.to_dataframes(path_gdx + 'LINK_REGION_COUNTRY.gdx')
    df_link_region_country = df_link_region_country['LINK_REGION_COUNTRY']
    df_link_region_country.columns = ['Region','Country','Value']
    df_link_region_country = df_link_region_country.drop(['Value'], axis=1)
    # Import
    df_results['Country_import'] = df_results['Node_import'].str[:3]
    df_link_region_country_import = df_link_region_country.rename(columns={'Region':'Region_import',
                                                                           'Country':'Country_import'})
    df_results = pd.merge(df_results, df_link_region_country_import, how='left', on=['Country_import'])
    # Export
    df_results['Country_export'] = df_results['Node_export'].str[:3]
    df_link_region_country_export = df_link_region_country.rename(columns={'Region':'Region_export',
                                                                           'Country':'Country_export'})
    df_results = pd.merge(df_results, df_link_region_country_export, how='left', on=['Country_export'])

    ### Additional treatment
    df_results['Year'] = df_results['Year'].astype(int)
    #df_results['Volume'] = df_results['Volume']/1000000

    return df_results


def fct_load_import_capacity():

    ### Import capacity
    df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_import_capacity.gdx")
    df_gdx = df_gdx["p_transport_international_import_capacity"]
    df_gdx.columns = ['Year','Node_import','Transport_international','Transport_international_import_capacity']
    df_gdx['Year'] = df_gdx['Year'].astype(int)

    return df_gdx