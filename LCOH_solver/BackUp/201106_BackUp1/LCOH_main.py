import pandas as pd
import numpy as np
import time


#import LCOH_solver_V2


def fct_calculated_annualized_cost(var_capex, var_opex, var_lifetime, var_wacc):

    var_annualization_factor = (var_wacc/100)/(1-(1+var_wacc/100)**(-var_lifetime))
    var_annualized_cost = var_capex*var_annualization_factor+var_opex

    return var_annualized_cost


def fct_find_minimum_quadrant(arr_init, x_range_init, y_range_init):

    dim_row = len(x_range_init)
    dim_col= len(y_range_init)

    arr_min = np.empty(shape=[dim_row-1, dim_col-1])

    for i_row in list(range(0,dim_row-1,1)):
        #print(i_row)
        for i_col in list(range(0,dim_col-1,1)):
            #print(i_col)
            #print(arr_init[i_row:i_row+2,i_col:i_col+2])
            arr_min[i_row,i_col] = arr_init[i_row:i_row+2,i_col:i_col+2].sum()

            pos_min = np.unravel_index(arr_min.argmin(), arr_min.shape)


    if (pos_min[0] < (dim_row-1.5)/2) & (pos_min[1] < (dim_col-1.5)/2):
        print('Q1')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,0]
        xend_y1_new = arr_init[0,dim_col-2]
        xend_yend_new = arr_init[dim_row-2,dim_col-2]
        x1_yend_new = arr_init[dim_row-2,0]

    elif (pos_min[0] < (dim_row-1.5)/2) & (pos_min[1] > (dim_col-1.5)/2):
        print('Q2')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,1]
        xend_y1_new = arr_init[0,dim_col-1]
        xend_yend_new = arr_init[dim_row-2,dim_col-1]
        x1_yend_new = arr_init[dim_row-2,1]

    elif (pos_min[0] > (dim_row-1.5)/2) & (pos_min[1] > (dim_col-1.5)/2):
        print('Q3')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[1]
        y_max_temp = y_range_init[-1]

        x1_y1_new = arr_init[1,1]
        xend_y1_new = arr_init[1,dim_col-1]
        xend_yend_new = arr_init[dim_row-1,dim_col-1]
        x1_yend_new = arr_init[dim_row-1,1]

    elif (pos_min[0] > (dim_row-1.5)/2) & (pos_min[1] < (dim_col-1.5)/2):
        print('Q4')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]
        y_min_temp = y_range_init[1]
        y_max_temp = y_range_init[-1]

        x1_y1_new = arr_init[1,0]
        xend_y1_new = arr_init[1,dim_col-1]
        xend_yend_new = arr_init[dim_row-1,dim_col-1]
        x1_yend_new = arr_init[dim_row-1,0]

    arr_opt1 = np.empty(shape=[dim_row, dim_col])
    arr_opt1[0,0] = x1_y1_new
    arr_opt1[0,dim_col-1] = xend_y1_new
    arr_opt1[dim_row-1,dim_col-1] = xend_yend_new
    arr_opt1[dim_row-1,0] = x1_yend_new


    x_range_temp = np.linspace(x_min_temp,x_max_temp,dim_col)
    y_range_temp = np.linspace(y_min_temp,y_max_temp,dim_row)

    return arr_opt1, x_range_temp, y_range_temp


def fct_fill_lcoh_matrix(i_init, x_range_temp, y_range_temp, arr_opt2 = None):

    dim_row = len(x_range_temp)
    dim_col = len(y_range_temp)

    if arr_opt2 is None:
        arr_opt2 = np.empty(shape=[dim_row, dim_col])

    lst_pos_x = list(range(0, dim_col, 1))
    lst_pos_y = list(range(0, dim_row, 1))

    for i_y in lst_pos_y:
        for i_x in lst_pos_x:

            if (i_init == 0) & ~((i_x == 0) & (i_y == 0)) & ~((i_x == lst_pos_x[-1]) & (i_y == 0)) & ~((i_x == lst_pos_x[-1]) & (i_y == lst_pos_y[-1])) & ~((i_x == 0) & (i_y == lst_pos_y[-1])):
                arr_opt2[i_y,i_x] = fct_lcoh(x_range_temp[i_x], y_range_temp[i_y])
            else:
                arr_opt2[i_y, i_x] = fct_lcoh(x_range_temp[i_x], y_range_temp[i_y])

    return arr_opt2



def fct_optimize_cell_system(x_range_init, y_range_init):

    i_init = 0
    difference = 1000
    while difference > tolerance:

        i_init += 1
        print(i_init)

        if i_init == 1:
            x_range_temp = x_range_init
            y_range_temp = y_range_init
            arr_opt_new = fct_fill_lcoh_matrix(i_init, x_range_temp, y_range_temp)

        else:
            arr_opt_new = fct_fill_lcoh_matrix(i_init, x_range_temp, y_range_temp, arr_opt)


        [arr_opt, x_range_temp, y_range_temp] = fct_find_minimum_quadrant(arr_opt_new, x_range_temp, y_range_temp)

        difference = min((x_range_temp[-1]-x_range_temp[0]),(y_range_temp[-1]-y_range_temp[0]))
        print(difference)

    pos_min = np.unravel_index(arr_opt_new.argmin(), arr_opt_new.shape)
    lcoh_optimum = arr_opt_new[pos_min[0],pos_min[1]]
    x_optimium = x_range_temp[pos_min[1]]
    y_optimium = y_range_temp[pos_min[0]]

    print(arr_opt_new)

    return lcoh_optimum, x_optimium, y_optimium


def fct_lcoh(x_temp, y_temp):

    total_cost = x_temp * i_annulized_pv + y_temp * i_annulized_onshore + i_annulized_electrolyser

    total_electricity = np.where((arr_pv * x_temp + arr_onshore * y_temp) > 1, 1,
                                 (arr_pv * x_temp + arr_onshore * y_temp)).sum()

    total_hydrogen = total_electricity * i_efficiency_electrolyser * 1000 / 33.33

    lcoh = total_cost / total_hydrogen

    if (x_temp == 0) & (y_temp == 0):
        lcoh = 20

    return lcoh



time_start = time.time()
print(time_start)


global tolerance
tolerance = 0.01


x_min = 0
x_max = 10
y_min = 0
y_max = 0

if x_max > 0:
    dim_x = 4
else:
    dim_x = 1

if y_max > 0:
    dim_y = 4
else:
    dim_y = 1

x_range = np.linspace(x_min,x_max,dim_x)
y_range = np.linspace(y_min,y_max,dim_y)



lst_cell = ['AUT_AT12','AUT_AT32','AUT_AT33','AUT_AT34']
lst_cell = ['AUT_AT33']

path_folder_res_profile = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\RES_profiles\\EU_NUTS2"

df_results = pd.DataFrame([], index=lst_cell, columns=['System','Electrolyser','PV','Onshore','Lcoh'])

for i_cell in lst_cell:
    print(i_cell)

    ### Load profiles
    global arr_pv
    df_pv = pd.read_csv(path_folder_res_profile+"\\"+i_cell+"_PV_2016.csv")
    arr_pv = df_pv[['Load_factor']].to_numpy()

    global arr_onshore
    df_onshore = pd.read_csv(path_folder_res_profile+"\\"+i_cell+"_Onshore_2016.csv")
    arr_onshore = df_onshore[['Load_factor']].to_numpy()


    ### Parameter
    global i_system
    i_system = 'Hybrid'

    i_wacc = 8

    i_capex_pv = 1310000
    i_opex_pv = 39000
    i_lifetime_pv = 22

    i_capex_onshore = 830000
    i_opex_onshore = 39000
    i_lifetime_onshore = 25

    i_capex_electrolyser = 1250000
    i_opex_electrolyser = 18800
    i_lifetime_electrolyser = 20

    global i_efficiency_electrolyser
    i_efficiency_electrolyser = 0.645

    global i_annulized_pv
    i_annulized_pv = fct_calculated_annualized_cost(i_capex_pv,i_opex_pv,i_lifetime_pv,i_wacc)
    print(i_annulized_pv)
    global i_annulized_onshore
    i_annulized_onshore = fct_calculated_annualized_cost(i_capex_onshore,i_opex_onshore,i_lifetime_onshore,i_wacc)
    print(i_annulized_onshore)
    global i_annulized_electrolyser
    i_annulized_electrolyser = fct_calculated_annualized_cost(i_capex_electrolyser,i_opex_electrolyser,i_lifetime_electrolyser,i_wacc)
    print(i_annulized_electrolyser)

    [lcoh_optimum, x_optimium, y_optimium] = fct_optimize_cell_system(x_range, y_range)
    df_results.loc[i_cell,'Lcoh'] = lcoh_optimum
    df_results.loc[i_cell,'PV'] = x_optimium
    df_results.loc[i_cell,'Onshore'] = y_optimium

    time_intermediate = time.time()
    print(time_intermediate-time_start)

print(df_results)

x_test = 0.5
y_test = 1.1

cost_pv = x_test*i_annulized_pv
cost_onshore = y_test*i_annulized_onshore
cost_electrolyer = i_annulized_electrolyser
cost_total = cost_pv+cost_onshore+cost_electrolyer

generation = arr_pv*x_test + arr_onshore*y_test
generation = np.where(generation>1,1,generation)
generation_total = generation.sum()
production = generation_total*i_efficiency_electrolyser
production_total = production*1000/33.33

loch = cost_total/production_total


time_end = time.time()
print(time_end - time_start)


factor_check = 20
x_range_check = np.linspace(x_min,x_max,dim_x*factor_check)
y_range_check = np.linspace(y_min,y_max,dim_y*factor_check)



if y_max == 0:
    print('Only PV')
    arr_check = np.empty(shape=[1, dim_x * factor_check])
        for i_x in list(range(0, dim_x * factor_check, 1)):
            #print(i_x)

            x_temp = x_range_check[i_x]

            arr_check[0,i_x] = fct_lcoh(0,x_temp)


if (x_max> 0) & (y_max>0):
    arr_check = np.empty(shape=[dim_y * factor_check, dim_x * factor_check])
    for i_x in list(range(0,dim_x*factor_check,1)):
        #print(i_x)

        for i_y in list(range(0,dim_y*factor_check,1)):
            #print(i_y)

            x_temp = x_range_check[i_x]
            y_temp = y_range_check[i_y]

            arr_check[i_x,i_y] = fct_lcoh(y_temp,x_temp)

max_arr = arr_check.max()
min_arr = arr_check.min()
#
# import plotly.graph_objects as go
# import pandas as pd
#
# df_check = pd.DataFrame(arr_check, index=y_range_check, columns=x_range_check)
#
# colorscale = [[0, 'rgb(0,0,255)'], [(0.1)/max_arr, 'rgb(0,100,200)'],[1/max_arr, 'rgb(0,255,0)'], [(15-min_arr)/max_arr, 'rgb(255,0,0)'], [1, 'rgb(255,0,0)']]
# fig = go.Figure(
#     data=go.Surface(x=x_range_check, y=y_range_check, z=df_check.values, colorscale=colorscale),
#     layout=go.Layout(
#         width=800,
#         height=800,
#     ))
#
#
# fig.add_trace(go.Scatter3d(x=[x_optimium,x_optimium],y=[y_optimium,y_optimium],z=[0, 20]))
#
#
# fig.update_layout(
#     scene = dict(zaxis = dict(nticks=4, range=[5,20]),
#                  xaxis = dict(tickvals = list(range(0,dim_x*factor_check,1)),
#                               ticktext= x_range_check),
#                  yaxis = dict(tickvals = list(range(0,dim_y*factor_check,1)),
#                               ticktext = y_range_check)))
#
# #fig.update_layout(template='seaborn')
# fig.show()
