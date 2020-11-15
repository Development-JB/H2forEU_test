
import pandas as pd
import numpy as np
import LCOH_settings
import LCOH_tools


def fct_prepare_input_data(i_senitivity, i_country,i_system,i_electrolyser,i_year):

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


def fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_temp, y_temp):

    ## Calculation of the LCOH based on technology costs and the producted H2 vol
    i_pv_capacity_2d = x_temp
    i_pv_cost_2d = df_data_input.loc['PV', 'Annualized_cost'].mean()
    i_pv_efficiency_2d = df_data_input.loc['PV', 'Efficiency'].mean()

    i_onshore_capacity_2d = y_temp
    i_onshore_efficiency_2d = df_data_input.loc['Onshore', 'Efficiency'].mean()
    i_onshore_cost_2d = df_data_input.loc['Onshore', 'Annualized_cost'].mean()

    i_electrolyser_capacity_2d = 1
    i_electrolyser_efficiency_2d = df_data_input.loc['Electrolyser', 'Efficiency'].mean()
    i_electrolyser_cost_2d = df_data_input.loc['Electrolyser', 'Annualized_cost'].mean()

    arr_electricity = (arr_pv * i_pv_capacity_2d * i_pv_efficiency_2d)+(arr_onshore*i_onshore_capacity_2d*i_onshore_efficiency_2d)
    val_total_electricity = np.where(arr_electricity > 1, 1, arr_electricity).sum()

    if (x_temp== 0) & (y_temp==0):
        val_vol = 0
        val_lcoh = 1000
    else:
        val_vol = val_total_electricity * i_electrolyser_efficiency_2d * 1000 / 33.33
        val_total_cost = i_pv_cost_2d * i_pv_capacity_2d + i_onshore_cost_2d * i_onshore_capacity_2d + i_electrolyser_cost_2d * i_electrolyser_capacity_2d + val_vol*LCOH_settings.val_cost_water*9/1000
        val_lcoh = val_total_cost / val_vol

    return val_lcoh, val_vol


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


def fct_lcoh_1d(df_data_input, arr_res, x_temp):

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

