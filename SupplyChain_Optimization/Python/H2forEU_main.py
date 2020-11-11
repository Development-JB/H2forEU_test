# Main File

import H2forEU_tools_write_gdx


lst_gdx = [
            'ITERATION',
            'YEAR',
            'LINK_ITERATION_YEAR',
            'COUNTRY',
            'NODE_PRODUCTION',
            'NODE_EXPORT',
            'NODE_IMPORT',
            'PATH',
            'SOURCE',
            'SOURCE_VRES',
            'SOURCE_NON_VRES',
            'ENERGY_TYPE',
            'TECHNOLOGY',
            'H2_SYSTEM',
            'TRANSPORT_NATIONAL',
            'TRANSPORT_INTERNATIONAL',
            'TRANSPORT_CONVERSION',
            'LINK_SOURCE_ENERGY_TYPE',
            'LINK_SOURCE_TECHNOLOGY',
            'LINK_H2_SYSTEM_ENERGY_TYPE',
            'LINK_H2_SYSTEM_TECHNOLOGY',
            'LINK_H2_SYSTEM_SOURCE',
            'LINK_H2_SYSTEM_COUNTRY',
            'LINK_H2_SYSTEM_NODE_PRODUCTION',
            'LINK_COUNTRY_NODE_PRODUCTION',
            'LINK_PATH_NODE_PRODUCTION',
            'LINK_PATH_NODE_EXPORT',
            'LINK_PATH_NODE_IMPORT',
            'LINK_PATH_TRANSPORT_NATIONAL',
            'LINK_PATH_TRANSPORT_INTERNATIONAL',
            'LINK_PATH_CONVERSION',
            'p_production_limit_country',
            'p_production_limit_node',
            'p_production_area_available_node',
            'p_production_energy_density',
            'p_production_land_dedication',
            'p_production_volume',
            'p_production_cost',
            'p_production_capacities',
            'p_transport_national_cost_fixed',
            'p_transport_national_cost_variable',
            'p_transport_national_distance',
            #'p_transport_national_capacity',
            'p_transport_international_cost_fixed',
            'p_transport_international_cost_variable',
            'p_transport_international_capacity',
            'p_transport_international_import_capacity',
            'p_transport_international_distance',
            'p_transport_conversion_cost'
            #'LINK_NODE_PRODUCTION_EXPORT',
            #'LINK_NODE_EXPORT_IMPORT'
            # 'p_test'
          ]



lst_para = [s for s in lst_gdx if 'p_' in s]
H2forEU_tools_write_gdx.fct_write_gdx_parameters(lst_para)

lst_set = [s for s in lst_gdx if 'p_' not in s]
H2forEU_tools_write_gdx.fct_write_gdx_sets_individually(lst_set)




