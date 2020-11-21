
import pandas as pd
import numpy as np
import LCOH_settings
import LCOH_tools


def fct_prepare_input_data(i_senitivity, i_country, i_system, i_electrolyser, i_year):

    lst_energy_type_temp = LCOH_settings.df_system[i_system].tolist()
    lst_energy_type_temp = [x for x in lst_energy_type_temp if str(x) != 'nan']

    dict_data_input = {}
    lst_lifetime = []
    if 'PV' in lst_energy_type_temp:
        dict_data_input['PV'] = {
                                   'Capex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'PV', 'Capex', i_year), 'Value'],
                                   'Opex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'PV', 'Opex', i_year), 'Value'],
                                   'Lifetime':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'PV', 'Lifetime', i_year), 'Value'],
                                   'Efficiency':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'PV', 'Efficiency', i_year), 'Value']
                               }
        lst_lifetime = lst_lifetime +[LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'PV', 'Lifetime', i_year), 'Value']]
    if 'Onshore' in lst_energy_type_temp:
        dict_data_input['Onshore'] = {
                                   'Capex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'Onshore', 'Capex', i_year), 'Value'],
                                   'Opex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'Onshore', 'Opex', i_year), 'Value'],
                                   'Lifetime':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'Onshore', 'Lifetime', i_year), 'Value'],
                                   'Efficiency':LCOH_settings.df_data.loc[(i_senitivity,'Technology', 'Onshore', 'Efficiency', i_year), 'Value']
                               }
        lst_lifetime = lst_lifetime + [LCOH_settings.df_data.loc[(i_senitivity, 'Technology', 'Onshore', 'Lifetime', i_year), 'Value']]

    dict_data_input['Electrolyser'] = {
                               'Capex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', i_electrolyser, 'Capex', i_year), 'Value'],
                               'Opex':LCOH_settings.df_data.loc[(i_senitivity,'Technology', i_electrolyser, 'Opex', i_year), 'Value'],
                               'Lifetime':LCOH_settings.df_data.loc[(i_senitivity,'Technology', i_electrolyser, 'Lifetime', i_year), 'Value'],
                               'Efficiency':LCOH_settings.df_data.loc[(i_senitivity,'Technology', i_electrolyser, 'Efficiency', i_year), 'Value']
                           }
    lst_lifetime = lst_lifetime + [LCOH_settings.df_data.loc[(i_senitivity, 'Technology', i_electrolyser, 'Lifetime', i_year), 'Value']]

    val_wacc = LCOH_settings.df_data.loc[(i_senitivity, 'Financing', 'Wacc', i_country, i_year), 'Value']
    dict_data_input['Wacc'] = val_wacc


    # Determine system lifetime as lifetime of shortest life component (avoid replacement costs)
    val_system_lifetime = int(min(lst_lifetime))
    dict_data_input['System'] = {'Lifetime':val_system_lifetime}


    # Create series with discount factors
    df_discount = pd.DataFrame([])
    if LCOH_settings.val_overnight == 'Yes':
        df_discount['Year'] = range(0, val_system_lifetime, 1)
    elif LCOH_settings.val_overnight == 'NO':
        df_discount['Year'] = range(1, val_system_lifetime + 1, 1)
    df_discount['Value'] = (1 + val_wacc) ** df_discount['Year']
    df_discount = df_discount.set_index(['Year'])
    dict_discount = df_discount.to_dict()
    dict_data_input['Discount_factor'] = dict_discount['Value']


    if 'PV' in lst_energy_type_temp:

        #dict_data_input['PV'].append({'Residual_value':(-1 * max(0, (dict_data_input['PV']['Capex'] - dict_data_input['PV']['Capex'] / dict_data_input['PV']['Lifetime'] * val_system_lifetime) / ((1 + val_wacc) ** val_system_lifetime)))})
        dict_data_input['PV'].update({'Residual_value':(-1 * max(0, (dict_data_input['PV']['Capex'] - dict_data_input['PV']['Capex'] / dict_data_input['PV']['Lifetime'] * val_system_lifetime) / ((1 + val_wacc) ** val_system_lifetime)))})

    if 'Onshore' in lst_energy_type_temp:

        dict_data_input['Onshore'].update({'Residual_value':(-1 * max(0, (dict_data_input['Onshore']['Capex'] - dict_data_input['Onshore']['Capex'] / dict_data_input['Onshore']['Lifetime'] * val_system_lifetime) / ((1 + val_wacc) ** val_system_lifetime)))})

    dict_data_input['Electrolyser'].update({'Residual_value':(-1 * max(0, (dict_data_input['Electrolyser']['Capex'] - dict_data_input['Electrolyser']['Capex'] / dict_data_input['Electrolyser']['Lifetime'] * val_system_lifetime) / ((1 + val_wacc) ** val_system_lifetime)))})

    return dict_data_input


def fct_prepare_input_data_BackUp(i_senitivity, i_country, i_system, i_electrolyser, i_year):

    lst_energy_type_temp = LCOH_settings.df_system[i_system].tolist()
    lst_energy_type_temp = [x for x in lst_energy_type_temp if str(x) != 'nan']
    lst_technology_temp = ['Electrolyser']+lst_energy_type_temp

    i_wacc = LCOH_settings.df_data.loc[(i_senitivity, 'Financing','Wacc',i_country,i_year),'Value'].mean()


    df_data_input_temp = pd.DataFrame([], index=lst_technology_temp, columns=['Annualized_cost','Efficiency'])
    for i_technology in lst_technology_temp:

        if i_technology == 'Electrolyser':
            i_technology_query = i_electrolyser
        else:
            i_technology_query = i_technology

        i_capex = LCOH_settings.df_data.loc[(i_senitivity, 'Technology',i_technology_query,'Capex',i_year),'Value'].mean()
        i_opex = LCOH_settings.df_data.loc[(i_senitivity, 'Technology',i_technology_query,'Opex',i_year),'Value'].mean()
        i_lifetime = LCOH_settings.df_data.loc[(i_senitivity, 'Technology',i_technology_query,'Lifetime',i_year),'Value'].mean()

        df_data_input_temp.loc[i_technology,'Annualized_cost'] = LCOH_tools.fct_calculated_annualized_cost(i_capex,i_opex,i_lifetime, i_wacc)
        df_data_input_temp.loc[i_technology, 'Efficiency'] = LCOH_settings.df_data.loc[(i_senitivity, 'Technology', i_technology_query,'Efficiency',i_year),'Value'].mean()


    return df_data_input_temp


def fct_prepare_input_data_landuse(i_sensitivity, i_cell, i_year):

    i_land_available = LCOH_settings.df_data_cells.loc[i_cell,'Area_utilizable'].mean()

    df_data_input_temp = pd.DataFrame([[i_land_available]], index=['Area_utilizable'], columns=['Value'])

    return df_data_input_temp


def fct_calculated_annualized_cost(var_capex, var_opex, var_lifetime, var_wacc):

    var_annualization_factor = var_wacc/(1-(1+var_wacc)**(-var_lifetime))
    #var_annualized_cost = var_capex*var_annualization_factor + var_opex*var_lifetime*var_annualization_factor
    var_annualized_cost = var_capex*var_annualization_factor + var_opex

    return var_annualized_cost


def fct_lcoh_2d(dict_data_input, arr_pv, arr_onshore, x_temp, y_temp):

    if (x_temp== 0) & (y_temp==0):
        val_vol_annually = 0
        val_lcoh = 1000
    else:

        # Set key parameters
        val_wacc = dict_data_input['Wacc']
        val_capacity_electrolyser = 1
        val_water = 0.01

        # # Calculate total electricity generation
        arr_electricity = (arr_pv * x_temp * dict_data_input['PV']['Efficiency']) + \
                          (arr_onshore * y_temp * dict_data_input['Onshore']['Efficiency'])
        val_total_electricity = np.where(arr_electricity > val_capacity_electrolyser, val_capacity_electrolyser,arr_electricity).sum()


        # # Calculate annual hydrogen production adjusted to a year with 8760 hours
        val_vol_annually = val_total_electricity * dict_data_input['Electrolyser']['Efficiency'] * 1000 / 33.33 * (8760/len(arr_pv))

        arr_discount_factor = np.array(list(dict_data_input['Discount_factor'].values()))

        val_capex = dict_data_input['PV']['Capex'] * x_temp
        val_capex += dict_data_input['Onshore']['Capex'] * y_temp
        val_capex += dict_data_input['Electrolyser']['Capex'] * val_capacity_electrolyser

        val_opex = sum((dict_data_input['PV']['Opex'] * x_temp + dict_data_input['Onshore']['Opex'] * y_temp + dict_data_input['Electrolyser']['Opex'] * val_capacity_electrolyser) / arr_discount_factor)

        val_residual_value = - x_temp * dict_data_input['PV']['Residual_value'] - y_temp * dict_data_input['Onshore']['Residual_value']  - val_capacity_electrolyser * dict_data_input['Electrolyser']['Residual_value']

        val_vom = sum((val_vol_annually * val_water) / arr_discount_factor)
        val_vol_h2 = sum(val_vol_annually / arr_discount_factor)

        val_lcoh = (val_capex + val_opex + val_vom + val_residual_value) / val_vol_h2


    return val_lcoh, val_vol_annually


def fct_unit_2d(df_data_input_landuse, x_temp, y_temp):

    ## Calculation of profits based on available landuse
    val_area_utilizable = df_data_input_landuse.loc['Area_utilizable','Value']
    val_energy_density_pv = LCOH_settings.val_energy_density_pv
    val_land_dedication_pv = LCOH_settings.val_land_dedication_pv
    val_energy_density_onshore = LCOH_settings.val_energy_density_onshore
    val_land_dedication_onshore = LCOH_settings.val_land_dedication_onshore

    # Methode 1: Calculation of system units (Electrolyser MW) for cell where PV and onshore are competing on available land
    val_unit = val_area_utilizable / (x_temp / (val_energy_density_pv * val_land_dedication_pv) + y_temp / (val_energy_density_onshore * val_land_dedication_onshore))

    # Methode 2: Calculation of system units (Electrolyser MW) for cell where PV and onshore are not competing on available land
    # val_unit1 = val_area_utilizable / (x_temp / (val_energy_density_pv * val_land_dedication_pv))
    # val_unit2 = val_area_utilizable / (y_temp / (val_energy_density_onshore * val_land_dedication_onshore))
    # val_unit = min(val_unit1, val_unit2)

    return val_unit


def fct_lcoh_1d(dict_data_input, arr_res, x_temp):

    if (x_temp == 0):
        val_vol_annually = 0
        val_lcoh = 1000
    else:

        if 'PV' in dict_data_input.keys():
            i_res = 'PV'
        elif 'Onshore' in dict_data_input.keys():
            i_res = 'Onshore'

        # Set key parameters
        val_wacc = dict_data_input['Wacc']
        val_capacity_electrolyser = 1
        val_water = 0.01

        # # Calculate total electricity generation
        arr_electricity = (arr_res * x_temp * dict_data_input[i_res]['Efficiency'])
        val_total_electricity = np.where(arr_electricity > val_capacity_electrolyser, val_capacity_electrolyser,
                                         arr_electricity).sum()

        # # Calculate annual hydrogen production adjusted to a year with 8760 hours
        val_vol_annually = val_total_electricity * dict_data_input['Electrolyser']['Efficiency'] * 1000 / 33.33 * (
                    8760 / len(arr_res))

        arr_discount_factor = np.array(list(dict_data_input['Discount_factor'].values()))

        val_capex = dict_data_input[i_res]['Capex'] * x_temp
        val_capex += dict_data_input['Electrolyser']['Capex'] * val_capacity_electrolyser

        val_opex = sum((dict_data_input[i_res]['Opex'] * x_temp +
                        dict_data_input['Electrolyser']['Opex'] * val_capacity_electrolyser) / arr_discount_factor)

        val_residual_value = - x_temp * dict_data_input[i_res]['Residual_value'] - val_capacity_electrolyser * dict_data_input['Electrolyser']['Residual_value']

        val_vom = sum((val_vol_annually * val_water) / arr_discount_factor)
        val_vol_h2 = sum(val_vol_annually / arr_discount_factor)

        val_lcoh = (val_capex + val_opex + val_vom + val_residual_value) / val_vol_h2

    return val_lcoh, val_vol_annually


def fct_lcoh_1d_BackUp2(df_data_input, arr_res, x_temp):

    ## Calculation of the LCOH based on technology costs and the producted H2 vol
    lst_technologies = df_data_input['Data_category2'][df_data_input['Data_category1']=='Technology'].drop_duplicates().tolist()

    if 'PV' in lst_technologies:
        i_res = 'PV'
    elif 'Onshore' in lst_technologies:
        i_res = 'Onshore'

    df_data_input = df_data_input.set_index(['Data_category1','Data_category2','Data_category3'])

    # Set key parameters
    val_wacc = df_data_input.loc[('Financing', 'Wacc', slice(None)), 'Value'].mean()
    val_capacity_electrolyser = 1
    val_water = 0.01

    # Calculate total electricity generation
    arr_electricity = (arr_res * x_temp * df_data_input.loc[('Technology',i_res,'Efficiency'),'Value'])
    val_total_electricity = np.where(arr_electricity > val_capacity_electrolyser, val_capacity_electrolyser, arr_electricity).sum()

    if (x_temp== 0):
        val_vol_annually = 0
        val_lcoh = 1000
    else:

        # Calculate annual hydrogen production adjusted to a year with 8760 hours
        val_vol_annually = val_total_electricity * df_data_input.loc[('Technology','Electrolyser','Efficiency'),'Value'] * 1000 / 33.33 * (8760/len(arr_res))

        # Determine system lifetime as lifetime of shortest life component (avoid replacement costs)
        val_system_lifetime = df_data_input.loc[('Technology',slice(None),'Lifetime'),'Value'].astype(int).min()

        # Create series with discount factors
        df_discount = pd.DataFrame([])
        df_discount['Year'] = range(1, val_system_lifetime + 1, 1)
        df_discount['Factor_discount'] = (1 + val_wacc) ** df_discount['Year']
        df_discount = df_discount.set_index(['Year'])

        # Initiate financial parameters
        val_capex = 0
        val_opex = 0
        val_vom = 0
        val_residual_value = 0
        # Loop over technologies and add costs
        for i_tech in lst_technologies:
            #print(i_tech)

            if i_tech == 'PV':
                i_capacity = x_temp
            elif i_tech == 'Onshore':
                i_capacity = x_temp
            elif i_tech == 'Electrolyser':
                i_capacity = val_capacity_electrolyser

            val_capex += df_data_input.loc[('Technology', i_tech, 'Capex'), 'Value'] * i_capacity
            val_opex += sum((df_data_input.loc[('Technology', i_tech, 'Opex'), 'Value'] * i_capacity) / df_discount['Factor_discount'])
            #val_vom += sum((val_vol_annually * df_data_input.loc[('Technology', i_tech, 'Vom'), 'Value']) / df_discount['Factor_discount'])

            val_residual_value += -1 * max(0, i_capacity *
                                ((df_data_input.loc[('Technology', i_tech, 'Capex'), 'Value'] - (df_data_input.loc[('Technology', i_tech, 'Capex'), 'Value']
                                / df_data_input.loc[('Technology', i_tech, 'Lifetime'), 'Value']) * val_system_lifetime)
                                / ((1 + val_wacc) ** val_system_lifetime)))

        val_vom += sum((val_vol_annually * val_water) / df_discount['Factor_discount'])
        val_vol_h2 = sum(val_vol_annually / df_discount['Factor_discount'])

        val_lcoh = (val_capex + val_opex + val_vom + val_residual_value) / val_vol_h2

    return val_lcoh, val_vol_annually


def fct_lcoh_1d_BackUp(df_data_input, arr_res, x_temp):

    total_cost = 0
    for i_technology in df_data_input.index:

        if i_technology == 'PV':
            i_technology_capacity_1d  = x_temp
            i_technology_efficiency_1d = df_data_input.loc[i_technology, 'Efficiency'].mean()
            arr_res = arr_res*i_technology_capacity_1d*i_technology_efficiency_1d
        elif i_technology == 'Onshore':
            i_technology_capacity_1d = x_temp
            i_technology_efficiency_1d = df_data_input.loc[i_technology, 'Efficiency'].mean()
            arr_res = arr_res*i_technology_capacity_1d*i_technology_efficiency_1d
        elif i_technology == 'Electrolyser':
            i_technology_capacity_1d = 1
            i_electrolyser_efficiency_1d = df_data_input.loc[i_technology,'Efficiency'].mean()

    total_electricity = np.where(arr_res > 1, 1,arr_res).sum()
    if x_temp == 0:
        val_vol = 0
        val_lcoh = 1000
    else:
        val_vol = total_electricity * i_electrolyser_efficiency_1d * 1000 / 33.33
        total_cost += i_technology_capacity_1d * df_data_input.loc[i_technology, 'Annualized_cost'] + val_vol * LCOH_settings.val_cost_water * 9 / 1000
        val_lcoh = total_cost / val_vol

    return val_lcoh, val_vol


def fct_unit_1d(df_data_input_landuse, i_system, x_temp):

    ## Calculation of profits based on available landuse
    val_area_utilizable = df_data_input_landuse.loc['Area_utilizable','Value']

    if i_system == 'PV':
        val_energy_density_pv = LCOH_settings.val_energy_density_pv
        val_land_dedication_pv = LCOH_settings.val_land_dedication_pv

        # Calculation of system units (Electrolyser MW) for cell
        if x_temp == 0:
            val_unit = 0
        else:
            val_unit = val_area_utilizable / (x_temp / (val_energy_density_pv * val_land_dedication_pv))

    elif i_system == 'Onshore':
        val_energy_density_onshore = LCOH_settings.val_energy_density_onshore
        val_land_dedication_onshore = LCOH_settings.val_land_dedication_onshore

        # Calculation of system units (Electrolyser MW) for cell
        if x_temp == 0:
            val_unit = 0
        else:
            val_unit = val_area_utilizable / (x_temp / (val_energy_density_onshore * val_land_dedication_onshore))

    return val_unit


def fct_plot_check_2d(arr_matrix_check, x_range_check, y_range_check, x_optimum_check, y_optimum_check):

    import plotly.graph_objects as go
    import pandas as pd

    val_max = np.amax(arr_matrix_check)

    df_check = pd.DataFrame(arr_matrix_check, index=y_range_check, columns=x_range_check)

    fig = go.Figure(
        data=go.Surface(x=x_range_check, y=y_range_check, z=df_check.values,colorscale='Viridis'),
        layout=go.Layout(
            width=600,
            height=600,
        ))

    fig.add_trace(go.Scatter3d(x=[x_optimum_check,x_optimum_check],y=[y_optimum_check,y_optimum_check], z=[0,val_max+0.1]))

    fig.update_layout(
        scene = dict(zaxis = dict(nticks=4),
                     xaxis = dict(tickvals = list(range(0,len(x_range_check),1)),
                                  ticktext= np.round(x_range_check,2)),
                     yaxis = dict(tickvals = list(range(0,len(y_range_check),1)),
                                  ticktext = np.round(y_range_check,2))))

    fig.show()


def fct_plot_check_1d(arr_vector_check, x_range_check, x_optimum_check):
    import plotly.graph_objects as go

    val_max = np.amax(arr_vector_check)

    fig = go.Figure(
        data=go.Scatter(x=x_range_check,
                        y=arr_vector_check,
                        mode='lines'),
        layout=go.Layout(
            width=600,
            height=600,
        ))

    fig.add_trace(go.Scatter(x=[x_optimum_check, x_optimum_check], y=[0,val_max + 0.1],
                             mode='lines'))

    fig.update_layout(
        scene=dict(yaxis=dict(nticks=4),
                   xaxis=dict(tickvals=list(range(0, len(x_range_check), 1)),
                              ticktext=np.round(x_range_check, 2))))

    fig.update_layout(showlegend=False)

    fig.show()

