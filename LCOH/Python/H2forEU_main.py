# Main File

import H2forEU_tools_write_gdx


lst_gdx = [
           'YEAR',
           'TIMESTEP_HOUR',
           'ENERGY_TYPE',
           'TECHNOLOGY',
           'p_wind_profile',
           'p_solar_profile',
           'p_test'
          ]



lst_para = [s for s in lst_gdx if 'p_' in s]
H2forEU_tools_write_gdx.fct_write_gdx_parameters(lst_para)

lst_set = [s for s in lst_gdx if 'p_' not in s]
H2forEU_tools_write_gdx.fct_write_gdx_sets(lst_set)




