# Sets and parameter

def TIMESTEP_HOUR():

    # Import packages
    import pandas as pd

    # Import files
    import H2forEU_config_time

    df_gdx = H2forEU_config_time.df_time_link[['Timestep_hour']]
    df_gdx.columns = ['TIMESTEP_HOUR']

    gdx_name = 'TIMESTEP_HOUR'
    gdx_dimensions = df_gdx.columns.tolist()
    gdx_data = df_gdx

    return gdx_name, gdx_dimensions, gdx_data
