

def fct_calculate_lcoh(dict_data_input, i_technology):

    # Calculate annualization factor
    #var_annualization_factor = dict_data_input['Wacc'] / (1 - (1 + dict_data_input['Wacc']) ** (-dict_data_input['Lifetime']))

    # 1/CFR = sum_t (1/(1+Wacc)^t)
    val_cfr = dict_data_input['Wacc']/(1-(1+dict_data_input['Wacc'])**(-dict_data_input['Lifetime']))


    # Calculate actualized annual hydrogen production
    val_h2_volume = dict_data_input['Load_factor']*8760/0.03333/val_cfr



    # Calculate individual costs
    val_capex = dict_data_input['Capex']/val_h2_volume
    val_fixed_om = dict_data_input['Fixed_om']/val_h2_volume/val_cfr

    ### Input_side
    #val_variable_om = (dict_data_input['Load_factor']*8760*dict_data_input['Efficiency']*dict_data_input['Variable_om'])/val_h2_volume/val_cfr
    #val_feedstock_cost = (dict_data_input['Load_factor']*8760*dict_data_input['Fuel_price'])/val_h2_volume/val_cfr

    #val_co2_cost = (dict_data_input['Load_factor']*8760*dict_data_input['Emission_factor']*(1-dict_data_input['Capture_rate'])*dict_data_input['Co2_price'])/val_h2_volume/val_cfr
    #val_co2_td_cost = (dict_data_input['Load_factor']*8760*dict_data_input['Emission_factor']*dict_data_input['Capture_rate']*dict_data_input['Co2_td_price'])/val_h2_volume/val_cfr
    #val_by_product_sale = (dict_data_input['Load_factor']*8760*dict_data_input['Efficiency']*dict_data_input['By_product_volume']*dict_data_input['By_product_price'])//val_h2_volume/val_cfr

    #val_by_product_sale = (dict_data_input['Load_factor']*8760*dict_data_input['Efficiency']*dict_data_input['By_product_volume']*dict_data_input['By_product_price'])/val_h2_volume/val_cfr


    ### Output_side
    val_variable_om = (dict_data_input['Load_factor']*8760*dict_data_input['Variable_om'])/val_h2_volume/val_cfr
    val_feedstock_cost = (dict_data_input['Load_factor']*8760*dict_data_input['Fuel_price']/dict_data_input['Efficiency'])/val_h2_volume/val_cfr

    val_co2_cost = (dict_data_input['Load_factor']*8760/dict_data_input['Efficiency']*dict_data_input['Emission_factor']*(1-dict_data_input['Capture_rate'])*dict_data_input['Co2_price'])/val_h2_volume/val_cfr
    if i_technology == 'Pyrolysis':
        val_co2_td_cost = 0
    else:
        val_co2_td_cost = (dict_data_input['Load_factor']*8760/dict_data_input['Efficiency']*dict_data_input['Emission_factor']*dict_data_input['Capture_rate']*dict_data_input['Co2_td_price'])/val_h2_volume/val_cfr


    print(dict_data_input['By_product_volume'])
    print(dict_data_input['By_product_price'])
    val_by_product_sale = (dict_data_input['Load_factor']*8760*dict_data_input['By_product_volume']*dict_data_input['By_product_price'])/val_h2_volume/val_cfr


    # Calculate lcoh
    val_lcoh = val_capex + val_fixed_om + val_variable_om + val_feedstock_cost + val_co2_cost + val_co2_td_cost - val_by_product_sale

    return val_lcoh, val_capex, val_fixed_om, val_variable_om, val_feedstock_cost, val_co2_cost, val_co2_td_cost, val_by_product_sale





def fct_load_input_data(i_ctry, i_technology, i_year, i_sensitivity):

    import LCOH_NG_settings

    dict_data_input = {}

    i_energy_type = LCOH_NG_settings.df_link_energy_type_technology.loc[i_technology,'Energy_type']

    try:
        dict_data_input['Capex'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'Capex', i_year), 'Value']
    except:
        dict_data_input['Capex'] = 0


    try:
        dict_data_input['Fixed_om'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'Fixed_om', i_year), 'Value']
    except:
        dict_data_input['Fixed_om'] = 0


    try:
        dict_data_input['Variable_om'] = LCOH_NG_settings.df_data.loc[(i_sensitivity, 'Technology', i_technology, 'Variable_om', i_year), 'Value']
    except:
        dict_data_input['Variable_om'] = 0


    try:
        dict_data_input['Lifetime'] = LCOH_NG_settings.df_data.loc[(i_sensitivity, 'Technology', i_technology, 'Lifetime', i_year), 'Value']
    except:

        dict_data_input['Lifetime'] = 0


    try:
        dict_data_input['Efficiency'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'Efficiency', i_year), 'Value']
    except:
        dict_data_input['Efficiency'] = 0


    try:
        dict_data_input['Capture_rate'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'Capture_rate', i_year), 'Value']
    except:
        dict_data_input['Capture_rate'] = 1


    try:
        dict_data_input['Emission_factor'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', i_energy_type, 'Emission_factor', i_year), 'Value']
    except:
        dict_data_input['Emission_factor'] = 0


    try:
        dict_data_input['Load_factor'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'Load_factor', i_year), 'Value']
    except:
        dict_data_input['Load_factor'] = 0


    try:
        dict_data_input['Wacc'] = LCOH_NG_settings.df_data.loc[(i_sensitivity, 'Financing', 'Wacc', i_ctry, i_year), 'Value']
    except:
        dict_data_input['Wacc'] = LCOH_NG_settings.df_data.loc[(i_sensitivity, 'Financing', 'Wacc', 'Default', i_year), 'Value']


    try:
        dict_data_input['Fuel_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', i_energy_type+'_price', i_ctry, i_year), 'Value']
    except:
        dict_data_input['Fuel_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', i_energy_type+'_price', 'Default', i_year), 'Value']


    try:
        dict_data_input['Co2_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', 'Co2_price', i_ctry, i_year), 'Value']
    except:
        dict_data_input['Co2_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', 'Co2_price', 'Default', i_year), 'Value']


    try:
        dict_data_input['Co2_td_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', 'Co2_td_price', i_ctry, i_year), 'Value']
    except:
        dict_data_input['Co2_td_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Other', 'Co2_td_price', 'Default', i_year), 'Value']


    try:
        dict_data_input['By_product_volume'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'By_product_volume', i_year), 'Value']
    except:
        dict_data_input['By_product_volume'] = 0


    try:
        dict_data_input['By_product_price'] = LCOH_NG_settings.df_data.loc[(i_sensitivity,'Technology', i_technology, 'By_product_price', i_year), 'Value']
    except:
        dict_data_input['By_product_price'] = 0


    return dict_data_input