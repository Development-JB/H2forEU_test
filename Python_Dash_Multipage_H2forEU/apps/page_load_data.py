import gdxpds
import pandas as pd
import numpy as np
import json

path_gdx = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\SupplyChain_Optimization\\GAMS\\gdx\\"
df_gdx_results = gdxpds.to_dataframes(path_gdx + "00_results.gdx")


### Sets
# YEAR
df_gdx = gdxpds.to_dataframes(path_gdx + "YEAR.gdx")
df_gdx = df_gdx['YEAR']
lst_year = df_gdx['YEAR'].tolist()
del df_gdx

# COUNTRY
df_gdx = gdxpds.to_dataframes(path_gdx + "COUNTRY.gdx")
df_gdx = df_gdx['COUNTRY']
lst_country = df_gdx['COUNTRY'].tolist()
del df_gdx

# COUNTRY_IMPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "COUNTRY_IMPORT.gdx")
df_gdx = df_gdx['COUNTRY_IMPORT']
lst_country_import = df_gdx['COUNTRY'].tolist()
del df_gdx

# COUNTRY_EXPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "COUNTRY_EXPORT.gdx")
df_gdx = df_gdx['COUNTRY_EXPORT']
lst_country_export = df_gdx['COUNTRY'].tolist()
del df_gdx

# NODE_PRODUCTION
df_gdx = gdxpds.to_dataframes(path_gdx + "NODE_PRODUCTION.gdx")
df_gdx = df_gdx['NODE_PRODUCTION']
lst_node_production = df_gdx['NODE_PRODUCTION'].tolist()
del df_gdx

# NODE_EXPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "NODE_EXPORT.gdx")
df_gdx = df_gdx['NODE_EXPORT']
lst_node_export = df_gdx['NODE_EXPORT'].tolist()
del df_gdx

# NODE_IMPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "NODE_IMPORT.gdx")
df_gdx = df_gdx['NODE_IMPORT']
lst_node_import = df_gdx['NODE_IMPORT'].tolist()
del df_gdx

# ENERGY_TYPE
df_gdx = gdxpds.to_dataframes(path_gdx + "ENERGY_TYPE.gdx")
df_gdx = df_gdx['ENERGY_TYPE']
lst_energy_type = df_gdx['ENERGY_TYPE'].tolist()
del df_gdx

# TECHNOLOGY
df_gdx = gdxpds.to_dataframes(path_gdx + "TECHNOLOGY.gdx")
df_gdx = df_gdx['TECHNOLOGY']
lst_technology = df_gdx['TECHNOLOGY'].tolist()
del df_gdx

# TRANSPORT_CONVERSION
df_gdx = gdxpds.to_dataframes(path_gdx + "TRANSPORT_CONVERSION.gdx")
df_gdx = df_gdx['TRANSPORT_CONVERSION']
lst_transport_conversion = df_gdx['TRANSPORT_CONVERSION'].tolist()
del df_gdx

# TRANSPORT_NATIONAL
df_gdx = gdxpds.to_dataframes(path_gdx + "TRANSPORT_NATIONAL.gdx")
df_gdx = df_gdx['TRANSPORT_NATIONAL']
lst_transport_national = df_gdx['TRANSPORT_NATIONAL'].tolist()
del df_gdx

# TRANSPORT_INTERNATIONAL
df_gdx = gdxpds.to_dataframes(path_gdx + "TRANSPORT_INTERNATIONAL.gdx")
df_gdx = df_gdx['TRANSPORT_INTERNATIONAL']
lst_transport_international = df_gdx['TRANSPORT_INTERNATIONAL'].tolist()
del df_gdx

# SOURCE
df_gdx = gdxpds.to_dataframes(path_gdx + "SOURCE.gdx")
df_gdx = df_gdx['SOURCE']
lst_source = df_gdx['SOURCE'].tolist()
del df_gdx

# SOURCE_NON_VRES
df_gdx = gdxpds.to_dataframes(path_gdx + "SOURCE_NON_VRES.gdx")
df_gdx = df_gdx['SOURCE_NON_VRES']
lst_source_non_vres = df_gdx['SOURCE_NON_VRES'].tolist()
del df_gdx

# SOURCE_VRES
df_gdx = gdxpds.to_dataframes(path_gdx + "SOURCE_VRES.gdx")
df_gdx = df_gdx['SOURCE_VRES']
lst_source_vres = df_gdx['SOURCE_VRES'].tolist()
del df_gdx

# H2_system
df_gdx = gdxpds.to_dataframes(path_gdx + "H2_SYSTEM.gdx")
df_gdx = df_gdx['H2_SYSTEM']
lst_h2_system = df_gdx['H2_SYSTEM'].tolist()
del df_gdx

# LINK_REGION_COUNTRY
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_REGION_COUNTRY.gdx")
df_gdx = df_gdx['LINK_REGION_COUNTRY']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Region','Country']
df_link_region_country = df_gdx
del df_gdx

# LINK_COUNTRY_NODE_PRODUCTION
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_COUNTRY_NODE_PRODUCTION.gdx")
df_gdx = df_gdx['LINK_COUNTRY_NODE_PRODUCTION']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Country','Node_production']
df_link_country_node_production = df_gdx
del df_gdx

# LINK_H2_SYSTEM_COUNTRY
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_H2_SYSTEM_COUNTRY.gdx")
df_gdx = df_gdx['LINK_H2_SYSTEM_COUNTRY']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['H2_system','Country']
df_h2_system_country = df_gdx
del df_gdx

# LINK_H2_SYSTEM_ENERGY_TYPE
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_H2_SYSTEM_ENERGY_TYPE.gdx")
df_gdx = df_gdx['LINK_H2_SYSTEM_ENERGY_TYPE']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['H2_system','Energy_type']
df_h2_system_energy_type = df_gdx
del df_gdx

# LINK_H2_SYSTEM_NODE_PRODUCTION
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_H2_SYSTEM_NODE_PRODUCTION.gdx")
df_gdx = df_gdx['LINK_H2_SYSTEM_NODE_PRODUCTION']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['H2_system','Node_production']
df_h2_system_node_production = df_gdx
del df_gdx

# LINK_H2_SYSTEM_SOURCE
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_H2_SYSTEM_SOURCE.gdx")
df_gdx = df_gdx['LINK_H2_SYSTEM_SOURCE']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['H2_system','Source']
df_h2_system_source = df_gdx
del df_gdx

# LINK_H2_SYSTEM_TECHNOLOGY
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_H2_SYSTEM_TECHNOLOGY.gdx")
df_gdx = df_gdx['LINK_H2_SYSTEM_TECHNOLOGY']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['H2_system','Technology']
df_h2_technology = df_gdx
del df_gdx

# LINK_PATH_NODE_EXPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_NODE_EXPORT.gdx")
df_gdx = df_gdx['LINK_PATH_NODE_EXPORT']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Node_export']
df_path_node_export = df_gdx
del df_gdx

# LINK_PATH_NODE_IMPORT
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_NODE_IMPORT.gdx")
df_gdx = df_gdx['LINK_PATH_NODE_IMPORT']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Node_import']
df_path_node_import = df_gdx
del df_gdx

# LINK_PATH_NODE_PRODUCTION
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_NODE_PRODUCTION.gdx")
df_gdx = df_gdx['LINK_PATH_NODE_PRODUCTION']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Node_production']
df_path_node_production = df_gdx
del df_gdx

# LINK_PATH_TRANSPORT_INTERNATIONAL
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_TRANSPORT_INTERNATIONAL.gdx")
df_gdx = df_gdx['LINK_PATH_TRANSPORT_INTERNATIONAL']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Transport_international']
df_path_transport_international = df_gdx
del df_gdx

# LINK_PATH_TRANSPORT_NATIONAL
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_TRANSPORT_NATIONAL.gdx")
df_gdx = df_gdx['LINK_PATH_TRANSPORT_NATIONAL']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Transport_national']
df_path_transport_national = df_gdx
del df_gdx

# LINK_PATH_CONVERSION
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_PATH_CONVERSION.gdx")
df_gdx = df_gdx['LINK_PATH_CONVERSION']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Path','Transport_conversion']
df_link_path_conversion = df_gdx
del df_gdx

# LINK_SOURCE_ENERGY_TYPE
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_SOURCE_ENERGY_TYPE.gdx")
df_gdx = df_gdx['LINK_SOURCE_ENERGY_TYPE']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Source','Energy_type']
df_source_energy_type = df_gdx
del df_gdx

# LINK_SOURCE_TECHNOLOGY
df_gdx = gdxpds.to_dataframes(path_gdx + "LINK_SOURCE_TECHNOLOGY.gdx")
df_gdx = df_gdx['LINK_SOURCE_TECHNOLOGY']
df_gdx = df_gdx.iloc[:,:-1]
df_gdx.columns = ['Source','Technology']
df_source_technology = df_gdx
del df_gdx

### Results
# Path
df_path = df_gdx_results['r_Path']
df_path.columns = ['Year', 'Path', 'Node_production','Transport_national', 'Node_export', 'Transport_international', 'Node_import', 'Volume_transport']

#Production at node
df_production_node = df_gdx_results['r_ProductionNode']
df_production_node.columns = ['Year', 'Node_production','Volume_production_node']

#H2_system
df_h2_system = df_gdx_results['r_H2_system']
df_h2_system.columns = ['Year', 'H2_system', 'Country', 'Node_production','Source','Energy_type', 'Technology','Volume_production_system']

df_supply = pd.merge(df_h2_system, df_production_node, how='left', on=['Year', 'Node_production'])
df_supply = pd.merge(df_supply, df_path, how='left', on=['Year', 'Node_production'])

df_supply['Volume'] = df_supply['Volume_production_system']/df_supply['Volume_production_node']*df_supply['Volume_transport']


df_supply = df_supply[['Year', 'H2_system', 'Path', 'Country', 'Source', 'Technology', 'Node_production',
                      'Transport_national', 'Node_export', 'Transport_international', 'Node_import', 'Volume']]



### p_demand_eu
df_gdx = gdxpds.to_dataframes(path_gdx + "p_demand_eu.gdx")
df_gdx = df_gdx["p_demand_eu"]
df_gdx.columns = ['Year','Demand_eu']
p_demand_eu = df_gdx
del df_gdx

### p_production_area_available_node
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_area_available_node.gdx")
df_gdx = df_gdx["p_production_area_available_node"]
df_gdx.columns = ['Node_production','Production_area_available_node']
df_production_area_available_node = df_gdx
del df_gdx

### p_production_capacity
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_capacity.gdx")
df_gdx = df_gdx["p_production_capacity"]
df_gdx.columns = ['Year','H2_system','Energy_type','Production_capacity']
df_production_capacity = df_gdx
del df_gdx

### Lcoh - p_production_cost
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_cost.gdx")
df_gdx = df_gdx["p_production_cost"]
df_gdx.columns = ['Year', 'H2_system','Production_cost']
df_production_cost = df_gdx
del df_gdx

### p_production_energy_density
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_energy_density.gdx")
df_gdx = df_gdx["p_production_energy_density"]
df_gdx.columns = ['Energy_type','Production_energy_density']
df_production_energy_density = df_gdx
del df_gdx

### p_production_land_dedication
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_land_dedication.gdx")
df_gdx = df_gdx["p_production_land_dedication"]
df_gdx.columns = ['Energy_type','Production_land_dedication']
df_production_land_dedication = df_gdx
del df_gdx

### p_production_limit_capacity_node
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_limit_capacity_node.gdx")
df_gdx = df_gdx["p_production_limit_capacity_node"]
df_gdx.columns = ['Year','Node_production','Production_limit_capacity_node']
df_production_limit_capacity_node = df_gdx
del df_gdx

### p_production_limit_country
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_limit_country.gdx")
df_gdx = df_gdx["p_production_limit_country"]
df_gdx.columns = ['Year','Country','Energy_type','Production_limit_country']
df_production_limit_country = df_gdx
del df_gdx

### p_production_limit_node
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_limit_node.gdx")
df_gdx = df_gdx["p_production_limit_node"]
df_gdx.columns = ['Year','Country','Energy_type','Production_limit_node']
df_production_limit_node = df_gdx
del df_gdx

### p_production_limit_volume_node
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_limit_volume_node.gdx")
df_gdx = df_gdx["p_production_limit_volume_node"]
df_gdx.columns = ['Year','Country','Energy_type','Production_limit_volume_node']
df_production_limit_volume_node = df_gdx
del df_gdx

### p_production_volume
df_gdx = gdxpds.to_dataframes(path_gdx + "p_production_volume.gdx")
df_gdx = df_gdx["p_production_volume"]
df_gdx.columns = ['Year','H2_system','Production_volume']
df_production_volume = df_gdx
del df_gdx

### p_transport_conversion_cost
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_conversion_cost.gdx")
df_gdx = df_gdx["p_transport_conversion_cost"]
df_gdx.columns = ['Year','Transport_conversion','Transport_conversion_cost']
df_transport_conversion_cost = df_gdx
del df_gdx

### p_transport_international_capacity
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_capacity.gdx")
df_gdx = df_gdx["p_transport_international_capacity"]
df_gdx.columns = ['Year','Node_export','Node_import','Transport_international','Transport_international_capacity']
df_transport_international_capacity = df_gdx
del df_gdx

### p_transport_international_cost_fixed
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_cost_fixed.gdx")
df_gdx = df_gdx["p_transport_international_cost_fixed"]
df_gdx.columns = ['Year','Transport_international','Transport_international_cost_fixed']
df_transport_international_cost_fixed = df_gdx
del df_gdx

### p_transport_international_cost_variable
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_cost_variable.gdx")
df_gdx = df_gdx["p_transport_international_cost_variable"]
df_gdx.columns = ['Year','Transport_international','Transport_international_cost_variable']
df_transport_international_cost_variable = df_gdx
del df_gdx

### p_transport_international_distance
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_distance.gdx")
df_gdx = df_gdx["p_transport_international_distance"]
df_gdx.columns = ['Node_export','Node_import','Transport_international','Transport_international_distance']
df_transport_international_distance = df_gdx
del df_gdx

### p_transport_international_import_capacity
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_international_import_capacity.gdx")
df_gdx = df_gdx["p_transport_international_import_capacity"]
df_gdx.columns = ['Year','Node_Export','Transport_international','Transport_international_import_capacity']
df_transport_international_import_capacity = df_gdx
del df_gdx

### p_transport_national_cost_fixed
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_national_cost_fixed.gdx")
df_gdx = df_gdx["p_transport_national_cost_fixed"]
df_gdx.columns = ['Year','Transport_national','Transport_national_cost_fixed']
df_transport_national_cost_fixed = df_gdx
del df_gdx

### p_transport_national_cost_variable
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_national_cost_variable.gdx")
df_gdx = df_gdx["p_transport_national_cost_variable"]
df_gdx.columns = ['Year','Transport_national','Transport_national_cost_variable']
df_transport_national_cost_variable = df_gdx
del df_gdx

### p_transport_national_distance
df_gdx = gdxpds.to_dataframes(path_gdx + "p_transport_national_distance.gdx")
df_gdx = df_gdx["p_transport_national_distance"]
df_gdx.columns = ['Node_production','Node_export','Transport_national','Transport_national_distance']
df_transport_national_distance = df_gdx
del df_gdx



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

    ### Lcoh
    df_results = pd.merge(df_supply,df_production_cost, how='left', on=['Year','H2_system'])

    ### Transport national
    df_results = pd.merge(df_results,df_transport_national_cost_fixed, how='left', on=['Year','Transport_national'])
    df_results = pd.merge(df_results,df_transport_national_cost_variable, how='left', on=['Year','Transport_national'])
    df_results = pd.merge(df_results,df_transport_national_distance, how='left', on=['Node_production','Node_export','Transport_national'])

    df_results['Transport_national_cost'] = df_results['Transport_national_cost_variable']+df_results['Transport_national_cost_fixed']*df_results['Transport_national_distance']

    ### Transport international
    df_results = pd.merge(df_results,df_transport_international_cost_fixed, how='left', on=['Year','Transport_international'])
    df_results = pd.merge(df_results,df_transport_international_cost_variable, how='left', on=['Year','Transport_international'])
    df_results = pd.merge(df_results,df_transport_international_distance, how='left', on=['Node_export','Node_import','Transport_international'])

    df_results['Transport_international_cost'] = df_results['Transport_international_cost_variable']+df_results['Transport_international_cost_fixed']*df_results['Transport_international_distance']


    ### Transport conversion cost
    df_transport_conversion_cost = pd.merge(df_link_path_conversion, df_transport_conversion_cost, how='left', on=['Transport_conversion'])
    df_transport_conversion_cost = df_transport_conversion_cost.groupby(['Year','Path']).agg({'Transport_conversion_cost':'sum'}).reset_index()

    df_results = pd.merge(df_results, df_transport_conversion_cost, how='left', on=['Year','Path'])

    ### Total cost per kg H2
    df_results['Lcoh'] = df_results['Production_cost']
    df_results['Lcoh_fob'] = df_results['Lcoh']+df_results['Transport_national_cost']
    df_results['Lcoh_cif'] = df_results['Lcoh_fob']+df_results['Transport_international_cost']+df_results['Transport_conversion_cost']

    ### Add link regions and countries
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