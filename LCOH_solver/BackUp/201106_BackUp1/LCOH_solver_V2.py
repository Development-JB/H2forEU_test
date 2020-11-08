import pandas as pd
import numpy as np

import LCOH_main
import LCOH_Tools






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
                arr_opt2[i_y,i_x] = fct_lcoh(i_x, i_y, x_range_temp, y_range_temp)
            else:
                arr_opt2[i_y, i_x] = fct_lcoh(i_x, i_y, x_range_temp, y_range_temp)

    return arr_opt2



def fct_optimize_cell_system(x_range_init, y_range_init):

    i_init = 0
    difference = 1000
    while difference > LCOH_main.tolerance:

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

    return lcoh_optimum, x_optimium, y_optimium


def fct_lcoh(i_x, i_y, x_range_temp, y_range_temp):
    x_temp = x_range_temp[i_x]
    y_temp = y_range_temp[i_y]

    total_cost = x_temp * LCOH_main.i_annulized_pv + y_temp * LCOH_main.i_annulized_onshore + LCOH_main.i_annulized_electrolyser

    total_electricity = np.where((LCOH_main.arr_pv * x_temp + LCOH_main.arr_onshore * y_temp) > 1, 1,
                                 (LCOH_main.arr_pv * x_temp + LCOH_main.arr_onshore * y_temp)).sum()

    total_hydrogen = total_electricity * LCOH_main.i_efficiency_electrolyser * 1000 / 33.33

    lcoh = total_cost / total_hydrogen

    return lcoh