import pandas as pd
import numpy as np
import time

import LCOH_settings
import LCOH_tools

def fct_find_minimum_sector(arr_init, x_range_init):

    dim_col = len(x_range_init)

    arr_min = np.empty(shape=[dim_col - 1])

    for i_col in list(range(0, dim_col - 1, 1)):

        arr_min[i_col] = arr_init[i_col:i_col + 2].sum()

    pos_min = np.argmin(arr_min, axis=0)

    #print(arr_min)
    #print(pos_min)
    if (pos_min < 3):
        #print('E1')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]

        x1_new = arr_init[0]
        xend_new = arr_init[dim_col-2]

    elif (pos_min > 2):
        #print('E2')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]

        x1_new = arr_init[1]
        xend_new = arr_init[dim_col-1]


    arr_opt = np.empty(shape=[dim_col])
    arr_opt[0] = x1_new
    arr_opt[dim_col-1] = xend_new

    x_range_temp = np.linspace(x_min_temp,x_max_temp,dim_col)

    return arr_opt, x_range_temp



def fct_find_minimum_quadrant(arr_init, x_range_init, y_range_init):

    dim_col = len(x_range_init)
    dim_row= len(y_range_init)

    arr_min = np.empty(shape=[dim_row-1, dim_col-1])

    for i_row in list(range(0,dim_row-1,1)):

        for i_col in list(range(0,dim_col-1,1)):

            arr_min[i_row,i_col] = arr_init[i_row:i_row+2,i_col:i_col+2].sum()

            pos_min = np.unravel_index(arr_min.argmin(), arr_min.shape)


    if (pos_min[0] < (dim_row-1.5)/2) & (pos_min[1] < (dim_col-1.5)/2):
        #print('Q1')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,0]
        xend_y1_new = arr_init[0,dim_col-2]
        xend_yend_new = arr_init[dim_row-2,dim_col-2]
        x1_yend_new = arr_init[dim_row-2,0]

    elif (pos_min[0] < (dim_row-1.5)/2) & (pos_min[1] > (dim_col-1.5)/2):
        #print('Q2')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,1]
        xend_y1_new = arr_init[0,dim_col-1]
        xend_yend_new = arr_init[dim_row-2,dim_col-1]
        x1_yend_new = arr_init[dim_row-2,1]

    elif (pos_min[0] > (dim_row-1.5)/2) & (pos_min[1] > (dim_col-1.5)/2):
        #print('Q3')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[1]
        y_max_temp = y_range_init[-1]

        x1_y1_new = arr_init[1,1]
        xend_y1_new = arr_init[1,dim_col-1]
        xend_yend_new = arr_init[dim_row-1,dim_col-1]
        x1_yend_new = arr_init[dim_row-1,1]

    elif (pos_min[0] > (dim_row-1.5)/2) & (pos_min[1] < (dim_col-1.5)/2):
        #print('Q4')
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


def fct_fill_lcoh_vector(i_init, df_data_input, arr_res, x_range_temp, arr_opt = None):

    dim_col = len(x_range_temp)

    if arr_opt is None:
        arr_opt = np.empty(shape=[dim_col])

    lst_pos_x = list(range(0, dim_col, 1))

    for i_x in lst_pos_x:
        if (i_init == 0) & ~(i_x == 0) & ~(i_x == lst_pos_x[-1]):
            arr_opt[i_x] = LCOH_tools.fct_lcoh_1d(df_data_input, arr_res, x_range_temp[i_x])
        else:
            arr_opt[i_x] = LCOH_tools.fct_lcoh_1d(df_data_input, arr_res, x_range_temp[i_x])

    #print(arr_opt)
    #print(arr_opt)

    return arr_opt



def fct_fill_lcoh_matrix(i_init, df_data_input, arr_pv, arr_onshore, x_range_temp, y_range_temp, arr_opt = None):

    dim_col = len(x_range_temp)
    dim_row = len(y_range_temp)

    if arr_opt is None:
        arr_opt = np.empty(shape=[dim_row, dim_col])

    lst_pos_x = list(range(0, dim_col, 1))
    lst_pos_y = list(range(0, dim_row, 1))

    for i_y in lst_pos_y:
        for i_x in lst_pos_x:

            if (i_init == 0) & ~((i_x == 0) & (i_y == 0)) & ~((i_x == lst_pos_x[-1]) & (i_y == 0)) & ~((i_x == lst_pos_x[-1]) & (i_y == lst_pos_y[-1])) & ~((i_x == 0) & (i_y == lst_pos_y[-1])):
                arr_opt[i_y, i_x] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_range_temp[i_x], y_range_temp[i_y])
            else:
                arr_opt[i_y, i_x] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_range_temp[i_x], y_range_temp[i_y])

    return arr_opt


def fct_optimize_system_2d(df_data_input, arr_pv, arr_onshore):

    i_init = 0
    difference = 1000
    while difference > LCOH_settings.tolerance:

        i_init += 1
        #print(i_init)

        if i_init == 1:
            x_range_temp = LCOH_settings.x_range_init
            y_range_temp = LCOH_settings.y_range_init
            arr_opt_2d = fct_fill_lcoh_matrix(i_init, df_data_input, arr_pv, arr_onshore, x_range_temp, y_range_temp)

        else:
            arr_opt_2d = fct_fill_lcoh_matrix(i_init, df_data_input, arr_pv, arr_onshore, x_range_temp, y_range_temp, arr_opt_2d)

        [arr_opt_2d, x_range_temp, y_range_temp] = fct_find_minimum_quadrant(arr_opt_2d, x_range_temp, y_range_temp)

        difference = min((x_range_temp[-1]-x_range_temp[0]),(y_range_temp[-1]-y_range_temp[0]))

    pos_min = np.unravel_index(arr_opt_2d.argmin(), arr_opt_2d.shape)
    lcoh_optimum = arr_opt_2d[pos_min[0],pos_min[1]]
    x_optimium = x_range_temp[pos_min[1]]
    y_optimium = y_range_temp[pos_min[0]]

    return lcoh_optimum, x_optimium, y_optimium


def fct_optimize_system_1d(df_data_input, arr_res):

    i_init = 0
    difference = 1000
    while difference > LCOH_settings.tolerance:

        i_init += 1

        if i_init == 1:
            x_range_temp = LCOH_settings.x_range_1d_init
            arr_opt_new = fct_fill_lcoh_vector(i_init, df_data_input, arr_res, x_range_temp)

        else:
            arr_opt_new = fct_fill_lcoh_vector(i_init, df_data_input, arr_res, x_range_temp, arr_opt)


        [arr_opt, x_range_temp] = fct_find_minimum_sector(arr_opt_new, x_range_temp)

        difference = (x_range_temp[-1]-x_range_temp[0])


    pos_min = np.argmin(arr_opt)
    lcoh_optimum = arr_opt[pos_min]
    x_optimium = x_range_temp[pos_min]

    return lcoh_optimum, x_optimium


