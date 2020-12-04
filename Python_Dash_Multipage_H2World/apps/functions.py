


def genSankey(df, cat_cols=[], value_cols='', title='Sankey Diagram'):
    #https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0

    import pandas as pd

    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE', '#306998', '#FFE873', '#FFD43B', '#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp = list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))

    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]] * colorNum

    # transform df into a source-target pair
    for i in range(len(cat_cols) - 1):
        if i == 0:
            sourceTargetDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            sourceTargetDf.columns = ['source', 'target', 'count']
        else:
            tempDf = df[[cat_cols[i], cat_cols[i + 1], value_cols]]
            tempDf.columns = ['source', 'target', 'count']
            sourceTargetDf = pd.concat([sourceTargetDf, tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source', 'target']).agg({'count': 'sum'}).reset_index()

    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))

    # creating the sankey diagram
    data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(
                color="black",
                width=0.5
            ),
            label=labelList,
            color=colorList
        ),
        link=dict(
            source=sourceTargetDf['sourceID'],
            target=sourceTargetDf['targetID'],
            value=sourceTargetDf['count']
        )
    )

    layout = dict(
        title=title,
        font=dict(
            size=10
        )
    )

    return data, layout



def fct_load_json_file():

    import json
    import os

    from apps import load_data

    path_file_json = os.getcwd() + "\\datasets\\World_Grid.json"

    with open(path_file_json, encoding='utf-8') as geofile:
        json_data = json.load(geofile)

    # Add unique key to every element / row
    # Goes though all rows
    # JB!!! It is important that the feature is calles 'id' and not 'ID','Id',etc.
    for i_feature in json_data['features']:
        i_feature['id'] = i_feature['properties']['Id_cell']

    return json_data


def fct_load_lcoh_result():

    import pandas as pd

    from apps import load_data

    path_file_results_lcoh = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\201102_Results_LCOH_CentralEurope.csv"
    df_nuts2_codes_fr = pd.read_csv(
        "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
    df_lcoh = pd.read_csv(path_file_results_lcoh)
    df_lcoh['Nuts2_code2013'] = df_lcoh['Cell'].str[4:]
    df_lcoh = pd.merge(df_lcoh, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
    df_lcoh['NUTS_ID'] = df_lcoh['Nuts2_code2016'].combine_first(df_lcoh['Nuts2_code2013'])
    df_lcoh = df_lcoh.drop(['Nuts2_code2016', 'Nuts2_code2013'], axis=1)
    df_lcoh = df_lcoh.drop(['Alkaline', 'PEM'], axis=1)

    return df_lcoh


def fct_load_capacity_utilitzation_result():

    import pandas as pd

    from apps import load_data

    df_data = load_data.df_production_h2_system
    df_data = pd.merge(df_data, load_data.df_link_h2_system_energy_type, how='left', on=['H2_system'])
    df_data = pd.merge(df_data, load_data.df_production_capacity, how='left', on=['Year','H2_system','Energy_type'])
    df_data['Production_capacity_total'] = df_data['Production_system']*df_data['Production_capacity']
    df_data = df_data.groupby(['Year','Node_production']).agg({'Production_capacity_total':'sum'}).reset_index()

    df_data = pd.merge(df_data,load_data.df_production_limit_capacity_node, how='left', on=['Year','Node_production'])
    df_data['Ratio_capacity_utilization'] = df_data['Production_capacity_total']/df_data['Production_limit_capacity_node']

    return df_data




def fct_load_system_result():

    import pandas as pd

    from apps import load_data

    df_colorbar = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")

    df_h2_system = load_data.df_link_h2_system_node_production
    df_h2_system = pd.merge(df_h2_system, load_data.df_production_capacity, how='left', on=['H2_system'])
    df_h2_system = pd.merge(df_h2_system, load_data.df_link_h2_system_source, how='left', on=['H2_system'])
    df_h2_system = pd.merge(df_h2_system, load_data.df_link_h2_system_technology, how='left', on=['H2_system'])
    df_h2_system = pd.merge(df_h2_system, load_data.df_production_cost, how='left', on=['Year','H2_system'])
    df_h2_system = df_h2_system[df_h2_system['Source'].isin(load_data.lst_source_vres)]

    df_h2_system_pivot = pd.pivot_table(df_h2_system, index=['Node_production','Year','Source','Technology','Production_cost'], columns=['Energy_type'], values=['Production_capacity'])
    df_h2_system_pivot = df_h2_system_pivot.droplevel(level=0, axis=1).reset_index()

    df_h2_system_pivot['Ratio_hybrid'] = df_h2_system_pivot['Onshore'] / (df_h2_system_pivot['PV'] + df_h2_system_pivot['Onshore'])
    df_h2_system_pivot['Ratio_hybrid'] = df_h2_system_pivot['Ratio_hybrid'].round(2)
    df_h2_system_pivot = pd.merge(df_h2_system_pivot, df_colorbar[['Ratio_hybrid', 'Rgb']], how='left', on=['Ratio_hybrid'])

    return df_h2_system_pivot


# def fct_load_system_result():
#
#     import pandas as pd
#
#     from apps import load_data
#
#     path_file_results_lcoh = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH_solver\\201115_Results_LCOH_CentralEurope.csv"
#     df_nuts2_codes_fr = pd.read_csv(
#         "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
#     df_colorbar = pd.read_csv(
#         "C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")
#     df_lcoh = pd.read_csv(path_file_results_lcoh)
#     df_lcoh['Nuts2_code2013'] = df_lcoh['Cell'].str[4:]
#     df_lcoh = pd.merge(df_lcoh, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
#     df_lcoh['NUTS_ID'] = df_lcoh['Nuts2_code2016'].combine_first(df_lcoh['Nuts2_code2013'])
#     df_lcoh['Ratio_hybrid'] = df_lcoh['Onshore'] / (df_lcoh['PV'] + df_lcoh['Onshore'])
#     df_lcoh['Ratio_hybrid'] = df_lcoh['Ratio_hybrid'].round(2)
#     df_lcoh = pd.merge(df_lcoh, df_colorbar[['Ratio_hybrid', 'Rgb']], how='left', on=['Ratio_hybrid'])
#
#     df_lcoh = df_lcoh.drop(['Nuts2_code2016', 'Nuts2_code2013'], axis=1)
#
#     return df_lcoh


def fct_load_res_information():

    import pandas as pd
    import numpy as np

    from apps import load_data

    df_res_information = pd.read_csv(
        "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2\\201115_Summary_cells.csv")
    df_nuts2_codes_fr = pd.read_csv(
        "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
    df_res_information['Nuts2_code2013'] = df_res_information['Id_cell'].str[4:]
    df_res_information = pd.merge(df_res_information, df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
    df_res_information['NUTS_ID'] = df_res_information['Nuts2_code2016'].combine_first(
        df_res_information['Nuts2_code2013'])
    df_res_information = df_res_information.drop(['Nuts2_code2016', 'Nuts2_code2013'], axis=1)

    df_colorscale_load_factor = pd.DataFrame(range(0, 1000 + 1, 1), columns=['Load_factor'])
    df_colorscale_load_factor['Red'] = np.nan
    df_colorscale_load_factor['Green'] = np.nan
    df_colorscale_load_factor['Blue'] = np.nan
    df_colorscale_load_factor['Load_factor'] = df_colorscale_load_factor['Load_factor'] / 1000
    df_colorscale_load_factor = df_colorscale_load_factor.set_index(['Load_factor'])
    df_colorscale_load_factor.loc[0, 'Red'] = 255
    df_colorscale_load_factor.loc[0, 'Green'] = 255
    df_colorscale_load_factor.loc[0, 'Blue'] = 255
    df_colorscale_load_factor.loc[0.12, 'Red'] = 255
    df_colorscale_load_factor.loc[0.12, 'Green'] = 255
    df_colorscale_load_factor.loc[0.12, 'Blue'] = 255
    df_colorscale_load_factor.loc[0.3, 'Red'] = 0
    df_colorscale_load_factor.loc[0.3, 'Green'] = 0
    df_colorscale_load_factor.loc[0.3, 'Blue'] = 0
    df_colorscale_load_factor.loc[1, 'Red'] = 0
    df_colorscale_load_factor.loc[1, 'Green'] = 0
    df_colorscale_load_factor.loc[1, 'Blue'] = 0

    df_colorscale_load_factor = df_colorscale_load_factor.interpolate(axis=0).round(2)
    df_colorscale_load_factor['Rgb'] = 'rgb(' + df_colorscale_load_factor['Red'].astype(str) + ',' + \
                                       df_colorscale_load_factor['Green'].astype(str) + ',' + df_colorscale_load_factor[
                                           'Blue'].astype(str) + ')'

    return df_res_information, df_colorscale_load_factor


def fct_load_results_supply():

    import pandas as pd

    from apps import load_data

    ### Lcoh
    df_results = pd.merge(load_data.df_supply, load_data.df_production_cost, how='left', on=['Year', 'H2_system'])

    ### Transport national
    df_results = pd.merge(df_results, load_data.df_transport_national_cost_fixed, how='left', on=['Year', 'Transport_national'])
    df_results = pd.merge(df_results, load_data.df_transport_national_cost_variable, how='left',
                          on=['Year', 'Transport_national'])
    df_results = pd.merge(df_results, load_data.df_transport_national_distance, how='left',
                          on=['Node_production', 'Node_export', 'Transport_national'])

    df_results['Transport_national_cost'] = df_results['Transport_national_cost_variable'] + df_results[
        'Transport_national_cost_fixed'] * df_results['Transport_national_distance']

    ### Transport international
    df_results = pd.merge(df_results, load_data.df_transport_international_cost_fixed, how='left',
                          on=['Year', 'Transport_international'])
    df_results = pd.merge(df_results, load_data.df_transport_international_cost_variable, how='left',
                          on=['Year', 'Transport_international'])
    df_results = pd.merge(df_results, load_data.df_transport_international_distance, how='left',
                          on=['Node_export', 'Node_import', 'Transport_international'])

    df_results['Transport_international_cost'] = df_results['Transport_international_cost_variable'] + df_results[
        'Transport_international_cost_fixed'] * df_results['Transport_international_distance']

    # ### Transport conversion cost
    # df_transport_conversion_cost2 = pd.merge(df_link_path_conversion, df_transport_conversion_cost, how='left',
    #                                         on=['Transport_conversion'])
    # df_transport_conversion_cost2 = df_transport_conversion_cost2.groupby(['Year', 'Path']).agg(
    #     {'Transport_conversion_cost': 'sum'}).reset_index()
    #
    # df_results = pd.merge(df_results, df_transport_conversion_cost2, how='left', on=['Year', 'Path'])

    ### Transport conversion national_cost
    df_transport_conversion_national_cost2 = pd.merge(load_data.df_link_path_conversion_national, load_data.df_transport_conversion_cost, how='left',
                                            on=['Transport_conversion'])
    df_transport_conversion_national_cost2 = df_transport_conversion_national_cost2.groupby(['Year', 'Path']).agg(
        {'Transport_conversion_cost': 'sum'}).reset_index()
    df_transport_conversion_national_cost2 = df_transport_conversion_national_cost2.rename(columns={'Transport_conversion_cost':'Transport_conversion_national_cost'})

    df_results = pd.merge(df_results, df_transport_conversion_national_cost2, how='left', on=['Year', 'Path'])

    ### Transport conversion international_cost
    df_transport_conversion_international_cost2 = pd.merge(load_data.df_link_path_conversion_international, load_data.df_transport_conversion_cost, how='left',
                                            on=['Transport_conversion'])
    df_transport_conversion_international_cost2 = df_transport_conversion_international_cost2.groupby(['Year', 'Path']).agg(
        {'Transport_conversion_cost': 'sum'}).reset_index()
    df_transport_conversion_international_cost2 = df_transport_conversion_international_cost2.rename(columns={'Transport_conversion_cost':'Transport_conversion_international_cost'})

    df_results = pd.merge(df_results, df_transport_conversion_international_cost2, how='left', on=['Year', 'Path'])

    ### Total cost per kg H2
    df_results['Lcoh'] = df_results['Production_cost']
    df_results['Lcoh_fob'] = df_results['Lcoh'] + df_results['Transport_national_cost']+df_results['Transport_conversion_national_cost']
    df_results['Lcoh_cif'] = df_results['Lcoh_fob'] + df_results['Transport_international_cost'] + df_results['Transport_conversion_international_cost']

    ### Add link regions and countries
    # Import
    df_results['Country_import'] = df_results['Node_import'].str[:3]
    df_link_region_country_import = load_data.df_link_region_country.rename(columns={'Region': 'Region_import',
                                                                           'Country': 'Country_import'})
    df_results = pd.merge(df_results, df_link_region_country_import, how='left', on=['Country_import'])
    # Export
    df_results['Country_export'] = df_results['Node_export'].str[:3]
    df_link_region_country_export = load_data.df_link_region_country.rename(columns={'Region': 'Region_export',
                                                                           'Country': 'Country_export'})
    df_results = pd.merge(df_results, df_link_region_country_export, how='left', on=['Country_export'])

    ### Additional treatment
    df_results['Year'] = df_results['Year'].astype(int)
    # df_results['Volume'] = df_results['Volume']/1000000

    return df_results


def fct_load_import_capacity():
    import gdxpds
    import pandas as pd

    from apps import load_data


    ### Import capacity
    df_gdx = gdxpds.to_dataframes(load_data.path_gdx + "p_transport_international_import_capacity.gdx")
    df_gdx = df_gdx["p_transport_international_import_capacity"]
    df_gdx.columns = ['Year', 'Node_import', 'Transport_international', 'Transport_international_import_capacity']
    df_gdx['Year'] = df_gdx['Year'].astype(int)

    return df_gdx
