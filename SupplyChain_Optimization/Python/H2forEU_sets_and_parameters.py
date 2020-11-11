# Sets and parameter

def ITERATION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_iteration_year[['Iteration']]
    df_gdx.columns = ['ITERATION']

    gdx_name = 'ITERATION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def YEAR():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_year
    df_gdx.columns = ['YEAR']

    gdx_name = 'YEAR'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_ITERATION_YEAR():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_iteration_year[['Iteration','Year']]
    df_gdx.columns = ['ITERATION','YEAR']

    gdx_name = 'LINK_ITERATION_YEAR'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def COUNTRY():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['Country']]
    df_gdx = df_gdx[df_gdx['Country'].astype(str) != 'nan']
    df_gdx.columns = ['COUNTRY']

    gdx_name = 'COUNTRY'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def NODE_PRODUCTION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_node_production
    df_gdx.columns = ['NODE_PRODUCTION']

    gdx_name = 'NODE_PRODUCTION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def NODE_EXPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_node_export
    df_gdx.columns = ['NODE_EXPORT']

    gdx_name = 'NODE_EXPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def NODE_IMPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_node_import
    df_gdx.columns = ['NODE_IMPORT']

    gdx_name = 'NODE_IMPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def PATH():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_path = H2forEU_settings.df_transport_path
    df_gdx = df_path[['Transport_path']]
    df_gdx.columns = ['PATH']

    gdx_name = 'PATH'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def SOURCE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_source
    df_gdx = df_gdx[df_gdx['Source'].astype(str) != 'nan']
    df_gdx.columns = ['SOURCE']

    gdx_name = 'SOURCE'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def ENERGY_TYPE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_energy_type
    df_gdx = df_gdx[df_gdx['Energy_type'].astype(str) != 'nan']
    df_gdx.columns = ['ENERGY_TYPE']

    gdx_name = 'ENERGY_TYPE'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def TECHNOLOGY():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_technology
    df_gdx = df_gdx[df_gdx['Technology'].astype(str) != 'nan']
    df_gdx.columns = ['TECHNOLOGY']

    gdx_name = 'TECHNOLOGY'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def H2_SYSTEM():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_h2_system[['H2_system']]
    df_gdx.columns = ['H2_SYSTEM']

    gdx_name = 'H2_SYSTEM'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data

def LINK_H2_SYSTEM_ENERGY_TYPE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_h2_system[['H2_system','Energy_type']]
    df_gdx.columns = ['H2_SYSTEM','ENERGY_TYPE']

    gdx_name = 'LINK_H2_SYSTEM_ENERGY_TYPE'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_H2_SYSTEM_TECHNOLOGY():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_h2_system[['H2_system','Technology']]
    df_gdx.columns = ['H2_SYSTEM','TECHNOLOGY']

    gdx_name = 'LINK_H2_SYSTEM_TECHNOLOGY'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_H2_SYSTEM_NODE_PRODUCTION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_h2_system[['H2_system','Node_production']]
    df_gdx.columns = ['H2_SYSTEM','NODE_PRODUCTION']

    gdx_name = 'LINK_H2_SYSTEM_NODE_PRODUCTION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_H2_SYSTEM_COUNTRY():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_h2_system[['H2_system','Country']]
    df_gdx.columns = ['H2_SYSTEM','COUNTRY']

    gdx_name = 'LINK_H2_SYSTEM_COUNTRY'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def TRANSPORT_NATIONAL():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['Transport_national']]
    df_gdx = df_gdx[df_gdx['Transport_national'].astype(str) != 'nan']
    df_gdx.columns = ['TRANSPORT_NATIONAL']

    gdx_name = 'TRANSPORT_NATIONAL'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def TRANSPORT_INTERNATIONAL():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_international
    df_gdx.columns = ['TRANSPORT_INTERNATIONAL']

    gdx_name = 'TRANSPORT_INTERNATIONAL'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def TRANSPORT_CONVERSION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_conversion
    df_gdx.columns = ['TRANSPORT_CONVERSION']

    gdx_name = 'TRANSPORT_CONVERSION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_SOURCE_ENERGY_TYPE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_source_energy_type
    df_gdx = df_gdx[['Source','Energy_type']]
    df_gdx.columns = ['Source','ENERGY_TYPE']

    gdx_name = 'LINK_SOURCE_ENERGY_TYPE'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_SOURCE_NODE_PRODUCTION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_source_node_production
    df_gdx = df_gdx[['Source','Node_production']]
    df_gdx.columns = ['Source','NODE_PRODUCTION']

    gdx_name = 'LINK_SOURCE_NODE_PRODUCTION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_SOURCE_TECHNOLOGY():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_source_technology
    df_gdx = df_gdx[['Source','Technology']]
    df_gdx.columns = ['SOURCE','TECHNOLOGY']

    gdx_name = 'LINK_SOURCE_TECHNOLOGY'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_COUNTRY_NODE_PRODUCTION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['Node_production']]
    df_gdx = df_gdx[df_gdx['Node_production'].astype(str) != 'nan']
    df_gdx['Country'] = df_gdx['Node_production'].str[:3]
    df_gdx = df_gdx[['Country','Node_production']]
    df_gdx.columns = ['COUNTRY','NODE_production']

    gdx_name = 'LINK_COUNTRY_NODE_PRODUCTION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_NODE_PRODUCTION_EXPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_node_production_export
    df_gdx.columns = ['NODE_PRODUCTION','NODE_EXPORT']

    gdx_name = 'LINK_NODE_PRODUCTION_EXPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_NODE_EXPORT_IMPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_link_node_export_import
    df_gdx = df_gdx[['Node_export','Node_import']]
    df_gdx.columns = ['NODE_EXPORT','NODE_IMPORT']

    gdx_name = 'LINK_NODE_EXPORT_IMPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_PATH_NODE_PRODUCTION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path[['Transport_path','Node_production']]
    df_gdx.columns = ['PATH','NODE_PRODUCTION']

    gdx_name = 'LINK_PATH_NODE_PRODUCTION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_PATH_NODE_EXPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path[['Transport_path','Node_export']]
    df_gdx.columns = ['PATH','NODE_EXPORT']

    gdx_name = 'LINK_PATH_NODE_EXPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data

def LINK_PATH_NODE_IMPORT():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path[['Transport_path','Node_import']]
    df_gdx.columns = ['PATH','NODE_IMPORT']

    gdx_name = 'LINK_PATH_NODE_IMPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_PATH_TRANSPORT_NATIONAL():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path[['Transport_path','Transport_national']]
    df_gdx.columns = ['PATH','TRANSPORT_NATIONAL']

    gdx_name = 'LINK_PATH_TRANSPORT_NATIONAL'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_PATH_TRANSPORT_INTERNATIONAL():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path[['Transport_path','Transport_international']]
    df_gdx.columns = ['PATH','TRANSPORT_INTERNATIONAL']

    gdx_name = 'LINK_PATH_TRANSPORT_INTERNATIONAL'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_PATH_CONVERSION():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_transport_path
    df_gdx = df_gdx[['Transport_path']+H2forEU_settings.lst_transport_conversion]
    df_gdx = df_gdx.set_index('Transport_path').stack().reset_index(name='Value')
    df_gdx = df_gdx.drop(['Value'], axis=1)
    df_gdx.columns = ['PATH','CONVERSION']

    gdx_name = 'LINK_PATH_CONVERSION'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_production_limit_country():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_limit_country')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx.set_index(['Country','Energy_type'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_2':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Country','Energy_type','Value']]
    df_gdx.columns = ['YEAR','COUNTRY','ENERGY_TYPE','Value']

    gdx_name = 'p_production_limit_country'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_production_limit_node():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_limit_node')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx.set_index(['Node_production','Energy_type'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_2':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]
    df_gdx = df_gdx[df_gdx['Energy_type'].isin(H2forEU_settings.lst_energy_type)]
    df_gdx = df_gdx[df_gdx['Node_production'].isin(H2forEU_settings.lst_node_production)]

    df_gdx = df_gdx[['Year','Node_production','Energy_type','Value']]
    df_gdx.columns = ['YEAR','NODE_PRODUCTION','ENERGY_TYPE','Value']

    gdx_name = 'p_production_limit_node'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_production_volume():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_production_vres = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_vres')
    df_production_other = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_other')
    df_gdx = df_production_other.append(df_production_vres)
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]
    df_gdx['H2_system'] = df_gdx['Node_production']+'-'+df_gdx['Source']+'-'+df_gdx['Technology']

    df_gdx = df_gdx[['Year','H2_system','Production_volume']]
    df_gdx.columns = ['YEAR','H2_SYSTEM','Value']

    gdx_name = 'p_production_volume'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_production_cost():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_production_vres = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_vres')
    df_production_other = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_other')
    df_gdx = df_production_other.append(df_production_vres)
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]
    df_gdx['H2_system'] = df_gdx['Node_production']+'-'+df_gdx['Source']+'-'+df_gdx['Technology']

    df_gdx = df_gdx[['Year','H2_system','Production_cost']]
    df_gdx.columns = ['YEAR','H2_SYSTEM','Value']

    gdx_name = 'p_production_cost'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_production_capacities():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_production_vres = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_vres')
    df_production_other = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Production_data_other')
    df_gdx = df_production_other.append(df_production_vres)
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]
    df_gdx['H2_system'] = df_gdx['Node_production']+'-'+df_gdx['Source']+'-'+df_gdx['Technology']
    df_gdx = df_gdx[['H2_system','Year']+H2forEU_settings.lst_energy_type]
    df_gdx = df_gdx.set_index(['H2_system','Year']).stack().reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_2':'Energy_type'})
    df_gdx = df_gdx[['Year','H2_system','Energy_type','Value']]
    df_gdx.columns = ['YEAR','H2_SYSTEM','ENERGY_TYPE','Value']

    gdx_name = 'p_production_capacities'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_national_cost_fixed():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_national_cost')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx[df_gdx['Transport_national_cost_parameter']=='Fixed']
    df_gdx = df_gdx.drop(['Transport_national_cost_parameter'], axis=1)
    df_gdx = df_gdx.set_index(['Transport_national'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_1':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Transport_national','Value']]
    df_gdx.columns = ['YEAR','TRANSPORT_NATIONAL','Value']

    gdx_name = 'p_transport_national_cost_fixed'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_national_cost_variable():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_national_cost')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx[df_gdx['Transport_national_cost_parameter']=='Variable']
    df_gdx = df_gdx.drop(['Transport_national_cost_parameter'], axis=1)
    df_gdx = df_gdx.set_index(['Transport_national'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_1':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Transport_national','Value']]
    df_gdx.columns = ['YEAR','TRANSPORT_NATIONAL','Value']

    gdx_name = 'p_transport_national_cost_variable'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_national_distance():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_distance = H2forEU_settings.df_transport_national_distance
    df_link_transport_national_mode = H2forEU_settings.df_link_transport_national_mode

    df_gdx = pd.merge(df_distance,df_link_transport_national_mode, how='left', on=['Transport_national_mode'])

    df_gdx = df_gdx[['Node_production','Node_export','Transport_national','Transport_national_distance']]
    df_gdx.columns = ['NODE_PRODUCTION','NODE_EXPORT','TRANSPORT_NATIONAL','Value']

    gdx_name = 'p_transport_national_distance'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_international_distance():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_distance = H2forEU_settings.df_transport_international_distance
    df_link_transport_international_mode = H2forEU_settings.df_link_transport_international_mode

    df_gdx = pd.merge(df_distance,df_link_transport_international_mode, how='left', on=['Transport_international_mode'])

    df_gdx = df_gdx[['Node_export','Node_import','Transport_international','Transport_international_distance']]
    df_gdx.columns = ['NODE_EXPORT','NODE_IMPORT','TRANSPORT_INTERNATIONAL','Value']

    gdx_name = 'p_transport_international_distance'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_international_cost_fixed():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_international_cost')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx[df_gdx['Transport_international_cost_parameter']=='Fixed']
    df_gdx = df_gdx.drop(['Transport_international_cost_parameter'], axis=1)
    df_gdx = df_gdx.set_index(['Transport_international'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_1':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Transport_international','Value']]
    df_gdx.columns = ['YEAR','TRANSPORT_INTERNATIONAL','Value']

    gdx_name = 'p_transport_international_cost_fixed'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_international_cost_variable():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_international_cost')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx[df_gdx['Transport_international_cost_parameter']=='Variable']
    df_gdx = df_gdx.drop(['Transport_international_cost_parameter'], axis=1)
    df_gdx = df_gdx.set_index(['Transport_international'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_1':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Transport_international','Value']]
    df_gdx.columns = ['YEAR','TRANSPORT_INTERNATIONAL','Value']

    gdx_name = 'p_transport_international_cost_variable'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_national_capacity():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.DataFrame([])

    gdx_name = 'p_transport_national_capacity'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_international_capacity():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_international_capacity')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx.set_index(['Node_export','Node_import','Transport_international'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_3':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Node_export','Node_import','Transport_international','Value']]
    df_gdx.columns = ['YEAR','NODE_EXPORT','NODE_IMPORT','TRANSPORT_INTERNATIONAL','Value']

    gdx_name = 'p_transport_international_capacity'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def p_transport_international_import_capacity():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_international_capacity_import')
    df_gdx = df_gdx.drop(['Unit'], axis=1)
    df_gdx = df_gdx.set_index(['Node_export','Transport_international'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_2':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Node_export','Transport_international','Value']]
    df_gdx.columns = ['YEAR','NODE_EXPORT','TRANSPORT_INTERNATIONAL','Value']

    gdx_name = 'p_transport_international_import_capacity'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data

def p_transport_conversion_cost():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_data_general, sheet_name='Transport_conversion_cost')
    df_gdx = df_gdx.drop(['Unit','Transport_conversion_cost_parameter'], axis=1)
    df_gdx = df_gdx.set_index(['Transport_conversion'])
    df_gdx = df_gdx.interpolate(axis=1)
    df_gdx = df_gdx.stack()
    df_gdx = df_gdx.reset_index(name='Value')
    df_gdx = df_gdx.rename(columns={'level_1':'Year'})
    df_gdx = df_gdx[df_gdx['Year'].isin(H2forEU_settings.lst_year)]

    df_gdx = df_gdx[['Year','Transport_conversion','Value']]
    df_gdx.columns = ['YEAR','TRANSPORT_CONVERSION','Value']

    gdx_name = 'p_transport_conversion_cost'
    gdx_dimensions = df_gdx.columns[: -1].tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data
