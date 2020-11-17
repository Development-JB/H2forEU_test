# Main File

import H2forEU_tools_write_gdx


lst_gdx = [
            'YEAR',
            'COUNTRY',
            'NODE_PRODUCTION',
            'NODE_EXPORT',
            'NODE_IMPORT',
            'H2_SYSTEM',
            'ENERGY_TYPE',
            'TECHNOLOGY',
            'TRANSPORT_NATIONAL',
            'TRANSPORT_INTERNATIONAL',
            'LINK_H2_SYSTEM_ENERGY_TYPE',
            'LINK_H2_SYSTEM_TECHNOLOGY',
            'LINK_COUNTRY_NODE_PRODUCTION',
            'LINK_NODE_PRODUCTION_EXPORT',
            'LINK_NODE_EXPORT_IMPORT'
            # 'p_test'
          ]



lst_para = [s for s in lst_gdx if 'p_' in s]
H2forEU_tools_write_gdx.fct_write_gdx_parameters(lst_para)

lst_set = [s for s in lst_gdx if 'p_' not in s]
H2forEU_tools_write_gdx.fct_write_gdx_sets(lst_set)




