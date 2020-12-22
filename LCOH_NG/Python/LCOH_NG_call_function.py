

def fct_calculate_lcoh(i_ctry, i_technology, i_year, i_sensitivity):

    import numpy as np
    import pandas as pd

    import LCOH_NG_settings
    import LCOH_NG_tools


    dict_data_input = LCOH_NG_tools.fct_load_input_data(i_ctry, i_technology, i_year, i_sensitivity)

    [val_lcoh, val_capex, val_fixed_om, val_variable_om, val_feedstock_cost, val_co2_cost, val_co2_td_cost, val_by_product_sale] = LCOH_NG_tools.fct_calculate_lcoh(dict_data_input, i_technology)


    df_lcoh_result_temp = pd.DataFrame([[i_ctry, i_technology, i_year, val_lcoh, val_capex, val_fixed_om, val_variable_om, val_feedstock_cost, val_co2_cost, val_co2_td_cost, val_by_product_sale]],
                                       columns=['Ctry','Technology','Year','Lcoh', 'Part_capex', 'Part_fixed_om','Part_variable_om','Part_feedstock_cost','Part_co2_cost','Part_co2_td_cost','Part_by_product_sale'])

    return df_lcoh_result_temp
