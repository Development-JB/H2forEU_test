
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


def fct_calculated_annualized_cost(var_capex, var_opex, var_lifetime, var_wacc):

    var_annualization_factor = var_wacc/(1-(1+var_wacc)**(-var_lifetime))
    var_annualized_cost = var_capex*var_annualization_factor + var_opex*var_lifetime*var_annualization_factor

    return var_annualized_cost


def fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_temp, y_temp):

    total_cost = 0
    arr_res = np.empty(shape=[1,8784])
    for i_technology in df_data_input.index:

        if i_technology == 'PV':
            i_technology_capacity_2d = x_temp
            print(x_temp)
            i_technology_efficiency_2d = df_data_input.loc[i_technology, 'Efficiency'].mean()
            arr_res = arr_res + (arr_pv*i_technology_capacity_2d*i_technology_efficiency_2d)
        elif i_technology == 'Onshore':
            print(y_temp)
            i_technology_capacity_2d = y_temp
            i_technology_efficiency_2d = df_data_input.loc[i_technology, 'Efficiency'].mean()
            arr_res = arr_res + (arr_onshore*i_technology_capacity_2d*i_technology_efficiency_2d)
        elif i_technology == 'Electrolyser':
            i_technology_capacity_2d = 1
            i_electrolyser_efficiency_2d = df_data_input.loc[i_technology,'Efficiency'].mean()
        total_cost += i_technology_capacity_2d*df_data_input.loc[i_technology,'Annualized_cost']

    total_electricity = np.where(arr_res > 1, 1, arr_res)
    total_electricity = total_electricity.sum()


    total_hydrogen = total_electricity * i_electrolyser_efficiency_2d * 1000 / 33.33 + 1
    lcoh = total_cost / total_hydrogen

    #if (x_temp == 0) & (y_temp == 0):
    #    lcoh = 20
    #if lcoh > 20:
    #    lcoh = 20

    return lcoh


def fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_temp, y_temp):

    total_cost = 0

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
    total_electricity = np.where(arr_electricity > 1, 1, arr_electricity).sum()
    total_cost = i_pv_cost_2d*i_pv_capacity_2d + i_onshore_cost_2d*i_onshore_capacity_2d + i_electrolyser_cost_2d*i_electrolyser_capacity_2d


    total_hydrogen = total_electricity * i_electrolyser_efficiency_2d * 1000 / 33.33 + 1
    lcoh = total_cost / total_hydrogen

    #if (x_temp == 0) & (y_temp == 0):
    #    lcoh = 20
    #if lcoh > 20:
    #    lcoh = 20

    return lcoh


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

        total_cost += i_technology_capacity_1d*df_data_input.loc[i_technology,'Annualized_cost']

    total_electricity = np.where(arr_res > 1, 1,arr_res).sum()
    total_hydrogen = total_electricity * i_electrolyser_efficiency_1d * 1000 / 33.33 +1

    lcoh = total_cost / total_hydrogen

    #if (x_temp == 0) & (y_temp == 0):
    #    lcoh = 20
    #if lcoh > 20:
    #    lcoh = np.nan

    return lcoh


def fct_create_check_matrix(df_data_input_check, arr_pv, arr_onhsore, x_range_check, y_range_check):

    arr_check = np.empty(shape=[len(y_range_check),len(x_range_check)])

    for i_x_pos in list(range(0,len(x_range_check),1)):
        i_x_check = x_range_check[i_x_pos]
        #print(i_x_check)

        for i_y_pos in list(range(0, len(y_range_check),1)):
            i_y_check = y_range_check[i_y_pos]
            #print(i_y_check)

            arr_check[i_y_pos,i_x_pos] = LCOH_tools.fct_lcoh_2d(df_data_input_check, arr_pv, arr_onhsore, i_x_check,i_y_check)

    return arr_check


def fct_create_check_vector(df_data_input_check, arr_res, x_range_check):

    arr_check = np.empty(shape=[len(x_range_check)])

    for i_x_pos in list(range(0,len(x_range_check),1)):
        i_x_check = x_range_check[i_x_pos]
        #print(i_x_check)

        arr_check[i_x_pos] = LCOH_tools.fct_lcoh_1d(df_data_input_check, arr_res, i_x_check)

    return arr_check


def fct_plot_check_2d(arr_matrix_check, x_range_check, y_range_check, lcoh_optimum_check, x_optimum_check, y_optimum_check):

    import plotly.graph_objects as go
    import pandas as pd

    df_check = pd.DataFrame(arr_matrix_check, index=y_range_check, columns=x_range_check)

    #colorscale = [[0, 'rgb(0,0,255)'], [(0.1)/np.max(arr_matrix_check), 'rgb(0,100,200)'],[1/np.max(arr_matrix_check), 'rgb(0,255,0)'], [(15-np.max(arr_matrix_check))/np.max(arr_matrix_check), 'rgb(255,0,0)'], [1, 'rgb(255,0,0)']]
    fig = go.Figure(
        data=go.Surface(x=x_range_check, y=y_range_check, z=df_check.values,colorscale='Viridis'),
        layout=go.Layout(
            width=600,
            height=600,
        ))

    fig.add_trace(go.Scatter3d(x=[x_optimum_check,x_optimum_check],y=[y_optimum_check,y_optimum_check],z=[0, 20]))

    fig.update_layout(
        scene = dict(zaxis = dict(nticks=4, range=[5,20]),
                     xaxis = dict(tickvals = list(range(0,len(x_range_check),1)),
                                  ticktext= np.round(x_range_check,2)),
                     yaxis = dict(tickvals = list(range(0,len(y_range_check),1)),
                                  ticktext = np.round(y_range_check,2))))

    fig.show()


def fct_plot_check_1d(arr_vector_check, x_range_check, lcoh_optimum_check, x_optimum_check):
    import plotly.graph_objects as go

    fig = go.Figure(
        data=go.Scatter(x=x_range_check,
                        y=arr_vector_check,
                        mode='lines'),
        layout=go.Layout(
            width=600,
            height=600,
        ))

    fig.add_trace(go.Scatter(x=[x_optimum_check, x_optimum_check],
                             y=[5, 20],
                             mode='lines'))

    fig.update_layout(
        scene=dict(yaxis=dict(nticks=4, range=[5, 20]),
                   xaxis=dict(tickvals=list(range(0, len(x_range_check), 1)),
                              ticktext=np.round(x_range_check, 2))))

    fig.update_layout(showlegend=False)

    fig.show()