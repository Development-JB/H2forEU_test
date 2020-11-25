# Sets and parameter

def YEAR():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['Year']]
    df_gdx = df_gdx[df_gdx['Year'].astype(str) != 'nan']
    df_gdx.columns = ['YEAR']

    gdx_name = 'YEAR'
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

    df_gdx = H2forEU_settings.df_set[['Node_production']]
    df_gdx = df_gdx[df_gdx['Node_production'].astype(str) != 'nan']
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

    df_gdx = H2forEU_settings.df_set[['Node_export']]
    df_gdx = df_gdx[df_gdx['Node_export'].astype(str) != 'nan']
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

    df_gdx = H2forEU_settings.df_set[['Node_import']]
    df_gdx = df_gdx[df_gdx['Node_import'].astype(str) != 'nan']
    df_gdx.columns = ['NODE_IMPORT']

    gdx_name = 'NODE_IMPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def H2_SYSTEM():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['H2_system']]
    df_gdx = df_gdx[df_gdx['H2_system'].astype(str) != 'nan']
    df_gdx.columns = ['H2_SYSTEM']

    gdx_name = 'H2_SYSTEM'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def ENERGY_TYPE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = H2forEU_settings.df_set[['Energy_type']]
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

    df_gdx = H2forEU_settings.df_set[['Technology']]
    df_gdx = df_gdx[df_gdx['Technology'].astype(str) != 'nan']
    df_gdx.columns = ['TECHNOLOGY']

    gdx_name = 'TECHNOLOGY'
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

    df_gdx = H2forEU_settings.df_set[['Transport_international']]
    df_gdx = df_gdx[df_gdx['Transport_international'].astype(str) != 'nan']
    df_gdx.columns = ['TRANSPORT_INTERNATIONAL']

    gdx_name = 'TRANSPORT_INTERNATIONAL'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data


def LINK_H2_SYSTEM_ENERGY_TYPE():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_settings

    df_gdx = pd.read_excel(H2forEU_settings.val_path_settings, sheet_name='LINK_H2_SYSTEM_ENERGY_TYPE')
    df_gdx = df_gdx[['H2_system','Energy_type']]
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

    df_gdx = pd.read_excel(H2forEU_settings.val_path_settings, sheet_name='LINK_H2_SYSTEM_TECHNOLOGY')
    df_gdx = df_gdx[['H2_system','Technology']]
    df_gdx.columns = ['H2_SYSTEM','TECHNOLOGY']

    gdx_name = 'LINK_H2_SYSTEM_TECHNOLOGY'
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

    df_gdx = pd.read_excel(H2forEU_settings.val_path_settings, sheet_name='LINK_NODE_PRODUCTION_EXPORT')
    df_gdx = df_gdx[['Node_production','Node_export']]
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

    df_gdx = pd.read_excel(H2forEU_settings.val_path_settings, sheet_name='LINK_NODE_EXPORT_IMPORT')
    df_gdx = df_gdx[['Node_export','Node_import']]
    df_gdx.columns = ['NODE_EXPORT','NODE_IMPORT']

    gdx_name = 'LINK_NODE_EXPORT_IMPORT'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data