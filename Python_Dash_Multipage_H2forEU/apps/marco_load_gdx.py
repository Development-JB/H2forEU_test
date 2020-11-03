import gdxpds
import pandas as pd
import numpy as np

## Load sets
path_gdx = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Tools\\MARCO\\GAMS\\gdx\\"

df_gdx_sets = gdxpds.to_dataframes(path_gdx + "sets.gdx")
df_gdx_results = gdxpds.to_dataframes(path_gdx + "00_results.gdx")

# Iterations
lst_iterations = df_gdx_sets['ITERATION']['ITERATION'].tolist()
# Zones
lst_zone = df_gdx_sets['ZONE']['ZONE'].tolist()
# Countries
lst_country = df_gdx_sets['COUNTRY']['COUNTRY'].tolist()
# Timestep_week
lst_timestep_week = df_gdx_sets['TIMESTEP_WEEK']['TIMESTEP_WEEK'].tolist()
# Energy_type
lst_energy_type = df_gdx_sets['ENERGY_TYPE']['ENERGY_TYPE'].tolist()


# Link_iteration_week
df_link_iteration_month = df_gdx_sets['LINK_ITERATION_MONTH'][['ITERATION','TIMESTEP_MONTH']]
df_link_iteration_month.columns = ['Iteration','Timestep_month']
# Link_iteration_week
df_link_iteration_week = df_gdx_sets['LINK_ITERATION_WEEK'][['ITERATION','TIMESTEP_WEEK']]
df_link_iteration_week.columns = ['Iteration','Timestep_week']
# Link_iteration_day
df_link_iteration_day = df_gdx_sets['LINK_ITERATION_DAY'][['ITERATION','TIMESTEP_DAY']]
df_link_iteration_day.columns = ['Iteration','Timestep_day']
# Link_iteration_hour
df_link_iteration_hour = df_gdx_sets['LINK_ITERATION_HOUR'][['ITERATION','TIMESTEP_HOUR']]
df_link_iteration_hour.columns = ['Iteration','Timestep_hour']

# Weeks
lst_timestep_week_scn = df_link_iteration_week['Timestep_week'].drop_duplicates().tolist()


# Link_hour_month
df_link_hour_year = df_gdx_sets['LINK_HOUR_YEAR'][['TIMESTEP_HOUR','YEAR']]
df_link_hour_year.columns = ['Timestep_hour','Year']
# Link_hour_week
df_link_hour_week = df_gdx_sets['LINK_HOUR_WEEK'][['TIMESTEP_HOUR','TIMESTEP_WEEK']]
df_link_hour_week.columns = ['Timestep_hour','Timestep_week']
# Link_hour_day
df_link_hour_day = df_gdx_sets['LINK_HOUR_DAY'][['TIMESTEP_HOUR','TIMESTEP_DAY']]
df_link_hour_day.columns = ['Timestep_hour','Timestep_day']


# Link_plant_type_country
df_link_plant_key_country = df_gdx_sets['LINK_PLANT_KEY_COUNTRY'][['PLANT_KEY','COUNTRY']]
df_link_plant_key_country.columns = ['Plant_key','Country']
# Link_plant_type_zone
df_link_plant_key_zone = df_gdx_sets['LINK_PLANT_KEY_ZONE'][['PLANT_KEY','ZONE']]
df_link_plant_key_zone.columns = ['Plant_key','Zone']
# Link_plant_type_energy_type
df_link_plant_key_energy_type = df_gdx_sets['LINK_PLANT_KEY_ENERGY_TYPE'][['PLANT_KEY','ENERGY_TYPE']]
df_link_plant_key_energy_type.columns = ['Plant_key','Energy_type']
# Link_plant_type_energy_technology
df_link_plant_key_technology = df_gdx_sets['LINK_PLANT_KEY_TECHNOLOGY'][['PLANT_KEY','TECHNOLOGY']]
df_link_plant_key_technology.columns = ['Plant_key','Technology']
# Link_plant_type_energy_class
df_link_plant_key_class = df_gdx_sets['LINK_PLANT_KEY_CLASS'][['PLANT_KEY','CLASS']]
df_link_plant_key_class.columns = ['Plant_key','Class']
# Link_plant_type_controlability
df_link_plant_key_controlability = df_gdx_sets['LINK_PLANT_KEY_CONTROLABILITY'][['PLANT_KEY','CONTROLABILITY']]
df_link_plant_key_controlability.columns = ['Plant_key','Controlability']

# Link_country_zone
df_link_country_zone = df_gdx_sets['LINK_COUNTRY_ZONE'][['COUNTRY','ZONE']]
df_link_country_zone.columns = ['Country','Zone']



## Load load
def fct_load_gdx_load():

    df_gdx = gdxpds.to_dataframes(path_gdx+"p_load.gdx")

    df_gdx_load = df_gdx['p_load']
    del df_gdx
    df_gdx_load = df_gdx_load.rename(columns={'TIMESTEP_HOUR':'Timestep_hour',
                                              'COUNTRY':'Zone'})
    df_gdx_load = pd.merge(df_gdx_load,df_link_hour_week, how = 'left', on = ['Timestep_hour'])
    df_gdx_load = pd.merge(df_gdx_load,df_link_iteration_hour, how = 'left', on = ['Timestep_hour'])
    df_gdx_load = df_gdx_load.sort_values(['Iteration','Timestep_week','Timestep_hour','Zone'])
    df_gdx_load = df_gdx_load[['Iteration','Timestep_week','Timestep_hour','Zone','Value']]

    return df_gdx_load


## Load exchange exogenous
def fct_load_gdx_exchange_exogenous():

    df_gdx_export = gdxpds.to_dataframes(path_gdx+"p_power_exports.gdx")
    df_gdx_export = df_gdx_export['p_power_exports']
    df_gdx_export = df_gdx_export.rename(columns={'TIMESTEP_HOUR':'Timestep_hour',
                                                  'ZONE':'Zone'})
    df_gdx_export['Mode'] = 'Export'
    df_gdx_export['Value'] = -1*df_gdx_export['Value']

    df_gdx_import = gdxpds.to_dataframes(path_gdx+"p_power_imports.gdx")
    df_gdx_import = df_gdx_import['p_power_imports']
    df_gdx_import = df_gdx_import.rename(columns={'TIMESTEP_HOUR':'Timestep_hour',
                                                  'ZONE':'Zone'})
    df_gdx_import['Mode'] = 'Import'

    df_gdx_exchange_exogenous = df_gdx_export.append(df_gdx_import)
    del df_gdx_import, df_gdx_export
    df_gdx_exchange_exogenous = df_gdx_exchange_exogenous.sort_values(['Timestep_hour','Zone'])

    return df_gdx_exchange_exogenous


def fct_load_gdx_generation_day_ahead():

    from apps import marco_settings

    df_gdx_generation_dispatch = df_gdx_results['r_v_GenerationDispatch'][['TIMESTEP_HOUR', 'PLANT_KEY_DISPATCH', 'Value']]
    df_gdx_generation_dispatch.columns = ['Timestep_hour', 'Plant_key', 'Value']

    df_gdx_generation_res = df_gdx_results['r_v_GenerationRes'][['TIMESTEP_HOUR', 'PLANT_KEY_RES', 'Value']]
    df_gdx_generation_res.columns = ['Timestep_hour', 'Plant_key', 'Value']

    df = df_gdx_generation_res.append(df_gdx_generation_dispatch)
    del df_gdx_generation_res, df_gdx_generation_dispatch

    df = pd.merge(df, df_link_hour_year, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_week, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_day, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_iteration_hour, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_plant_key_country, how='left', on=['Plant_key'])
    df = pd.merge(df, df_link_plant_key_zone, how='left', on=['Plant_key'])
    df = pd.merge(df, df_link_plant_key_energy_type, how='left', on=['Plant_key'])
    df = pd.merge(df, df_link_plant_key_technology, how='left', on=['Plant_key'])
    df = pd.merge(df, df_link_plant_key_controlability, how='left', on=['Plant_key'])
    df = pd.merge(df, df_link_plant_key_class, how='left', on=['Plant_key'])
    df = pd.merge(df, marco_settings.df_energy_type_order, how='left', on=['Energy_type'])

    df = df[['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Zone', 'Energy_type_order','Energy_type','Technology', 'Controlability', 'Class', 'Plant_key', 'Value']]
    df = df.sort_values(['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Energy_type_order','Energy_type','Technology', 'Controlability', 'Class', 'Plant_key','Country', 'Zone'])

    return df


def fct_load_gdx_generation_historical():

    from apps import marco_settings

    df = gdxpds.to_dataframes(path_gdx+"p_generation_historical.gdx")
    df = df['p_generation_historical']
    df.columns = ['Timestep_hour', 'Country','Energy_type','Mode', 'Value']

    df = pd.merge(df, df_link_hour_year, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_week, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_day, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_iteration_hour, how='left', on=['Timestep_hour'])
    df = pd.merge(df, marco_settings.df_energy_type_order, how='left', on=['Energy_type'])

    df = df[['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Energy_type_order','Energy_type', 'Mode', 'Value']]
    df = df.sort_values(['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country','Energy_type_order','Energy_type', 'Mode'])

    return df

def fct_load_gdx_prices_day_ahead():

    from apps import marco_settings

    df = df_gdx_results['r_v_MarketPrice']
    df.columns = ['Timestep_hour', 'Zone', 'Value']

    df = pd.merge(df, df_link_hour_year, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_week, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_day, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_iteration_hour, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_country_zone, how='left', on=['Zone'])

    df = df[['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Zone', 'Value']]
    df = df.sort_values(['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Zone', 'Value'])

    return df


def fct_load_gdx_prices_historical():

    from apps import marco_settings

    df = gdxpds.to_dataframes(path_gdx+"p_prices_historical.gdx")
    df = df['p_prices_historical']
    df.columns = ['Timestep_hour', 'Country', 'Currency', 'Value']

    df = pd.merge(df, df_link_hour_year, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_week, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_hour_day, how='left', on=['Timestep_hour'])
    df = pd.merge(df, df_link_iteration_hour, how='left', on=['Timestep_hour'])

    df = df[['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Value']]
    df = df.sort_values(['Iteration', 'Year', 'Timestep_week', 'Timestep_day', 'Timestep_hour', 'Country', 'Value'])

    return df


def fct_prepare_color_code():

    from apps import marco_settings

    df_link_country_color_code = marco_settings.df_link_country_color_code[['Country','Red','Green','Blue']]
    df_link_country_color_code = df_link_country_color_code[df_link_country_color_code['Country'].isin(lst_country)]
    df_link_country_color_code = df_link_country_color_code.set_index(['Country'])
    df_link_country_color_code['Color_code_rgb'] = 'rgb(' + df_link_country_color_code['Red'].astype(str) + ',' + \
                                                   df_link_country_color_code['Green'].astype(str) + ',' + \
                                                   df_link_country_color_code['Blue'].astype(str) + ')'

    df_link_zone_color_code = df_link_country_zone.copy()
    df_link_zone_color_code['Color_code_rgb'] = np.nan
    df_link_zone_color_code= df_link_zone_color_code.set_index(['Country','Zone'])

    ser_zones_per_country = df_link_country_zone['Country'].value_counts()
    for i_country in lst_country:
        print(i_country)

        var_sign = -1

        for i_counter_zone in range(1,ser_zones_per_country.loc[i_country]+1,1):

            lst_zone_temp = df_link_country_zone['Zone'][df_link_country_zone['Country']==i_country].tolist()
            i_zone = lst_zone_temp[i_counter_zone-1]
            print(i_zone)

            if ser_zones_per_country.loc[i_country] == 1:
                df_link_zone_color_code.loc[(i_country,i_zone),'Color_code_rgb'] = df_link_country_color_code.loc[i_country,'Color_code_rgb']

            else:

                var_sign = var_sign*-1

                var_red = max(min(df_link_country_color_code.loc[i_country,'Red']+round(i_counter_zone/2+0.49)*var_sign*25,255),0)
                var_green = max(min(df_link_country_color_code.loc[i_country,'Green']+round(i_counter_zone/2+0.49)*var_sign*25,255),0)
                var_blue = max(min(df_link_country_color_code.loc[i_country,'Blue']+round(i_counter_zone/2+0.49)*var_sign*25,255),0)

                df_link_zone_color_code.loc[(i_country,i_zone),'Color_code_rgb'] = 'rgb('+str(var_red)+','+str(var_green)+','+str(var_blue)+')'

    df_link_country_color_code = df_link_country_color_code.reset_index()
    df_link_country_color_code = df_link_country_color_code[['Country','Color_code_rgb']]

    df_link_zone_color_code = df_link_zone_color_code.reset_index()
    df_link_zone_color_code = df_link_zone_color_code[['Zone','Color_code_rgb']]

    return df_link_country_color_code, df_link_zone_color_code

