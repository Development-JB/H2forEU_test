import pandas as pd
import numpy as np
import time

import LCOH_settings
import LCOH_tools


def fct_find_optimum_sector(arr_init, x_range_init, optimization_objective=None):

    dim_col = len(x_range_init)

    arr_opt = np.empty(shape=[dim_col - 1])


    for i_col in list(range(0, dim_col - 1, 1)):

        arr_opt[i_col] = np.amax(arr_init[i_col:i_col + 2])

    arr_opt = np.round(arr_opt,3)

    arr_opt_flip = np.flip(arr_opt, axis=0)

    if optimization_objective == 'maximize':
        pos_opt_reverse = np.argmax(arr_opt_flip, axis=0)
    else:
        pos_opt_reverse = np.argmin(arr_opt_flip, axis=0)

    pos_opt = len(arr_opt)-pos_opt_reverse-1

    if (pos_opt < 3):
        #print('E1')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]

        x1_new = arr_init[0]
        xend_new = arr_init[dim_col-2]

    elif (pos_opt > 2):
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


def fct_find_optimum_quadrant(arr_init, x_range_init, y_range_init, optimization_objective=None):

    dim_col = len(x_range_init)
    dim_row= len(y_range_init)

    arr_opt = np.empty(shape=[dim_row-1, dim_col-1])

    for i_row in list(range(0,dim_row-1,1)):

        for i_col in list(range(0,dim_col-1,1)):

            if optimization_objective == 'maximize':
                arr_opt[i_row, i_col] = np.amax(arr_init[i_row:i_row + 2, i_col:i_col + 2])
            else:
                arr_opt[i_row, i_col] = np.amin(arr_init[i_row:i_row + 2, i_col:i_col + 2])

    arr_opt = np.round(arr_opt,3)

    arr_opt_flip = np.flip(arr_opt, axis=0)
    arr_opt_flip = np.flip(arr_opt_flip, axis=1)

    if optimization_objective == 'maximize':
        pos_opt_reverse = np.unravel_index(arr_opt_flip.argmax(), arr_opt_flip.shape)
    else:
        pos_opt_reverse = np.unravel_index(arr_opt_flip.argmin(), arr_opt_flip.shape)

    pos_opt = np.array([0,0])
    pos_opt[0] = len(arr_opt)-pos_opt_reverse[0]-1
    pos_opt[1] = len(arr_opt)-pos_opt_reverse[1]-1

    if (pos_opt[0] < (dim_row-1.5)/2) & (pos_opt[1] < (dim_col-1.5)/2):
        #print('Q1')
        x_min_temp = x_range_init[0]
        x_max_temp = x_range_init[-2]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,0]
        xend_y1_new = arr_init[0,dim_col-2]
        xend_yend_new = arr_init[dim_row-2,dim_col-2]
        x1_yend_new = arr_init[dim_row-2,0]

    elif (pos_opt[0] < (dim_row-1.5)/2) & (pos_opt[1] > (dim_col-1.5)/2):
        #print('Q2')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[0]
        y_max_temp = y_range_init[-2]

        x1_y1_new = arr_init[0,1]
        xend_y1_new = arr_init[0,dim_col-1]
        xend_yend_new = arr_init[dim_row-2,dim_col-1]
        x1_yend_new = arr_init[dim_row-2,1]

    elif (pos_opt[0] > (dim_row-1.5)/2) & (pos_opt[1] > (dim_col-1.5)/2):
        #print('Q3')
        x_min_temp = x_range_init[1]
        x_max_temp = x_range_init[-1]
        y_min_temp = y_range_init[1]
        y_max_temp = y_range_init[-1]

        x1_y1_new = arr_init[1,1]
        xend_y1_new = arr_init[1,dim_col-1]
        xend_yend_new = arr_init[dim_row-1,dim_col-1]
        x1_yend_new = arr_init[dim_row-1,1]

    elif (pos_opt[0] > (dim_row-1.5)/2) & (pos_opt[1] < (dim_col-1.5)/2):
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


def fct_fill_vector(optimization, df_data_input, df_data_input_landuse, i_system, arr_res, x_range_temp):

    dim_col = len(x_range_temp)

    arr_opt = np.empty(shape=[dim_col])

    lst_pos_x = list(range(0, dim_col, 1))

    val_h2_selling_price = LCOH_settings.val_h2_selling_price

    for i_x in lst_pos_x:

        [val_lcoh, val_vol] = LCOH_tools.fct_lcoh_1d(df_data_input, arr_res, x_range_temp[i_x])

        if optimization == 'Lcoh':

            arr_opt[i_x] = val_lcoh

            arr_opt[np.isnan(arr_opt)] = 0
            arr_opt[np.isinf(arr_opt)] = 100

        elif optimization == 'Profit':

            val_unit = LCOH_tools.fct_unit_1d(df_data_input_landuse, i_system, x_range_temp[i_x])

            # Calculate profit for assumed selling price
            arr_opt[i_x] = val_unit * val_vol * (val_h2_selling_price - val_lcoh) / 1000
            arr_opt[np.isnan(arr_opt)] = 0

        elif optimization == 'Volume':

            val_unit = LCOH_tools.fct_unit_1d(df_data_input_landuse, i_system, x_range_temp[i_x])

            # Calculate total volumes
            arr_opt[i_x] = val_unit * val_vol
            arr_opt[np.isinf(arr_opt)] = 0

    return arr_opt


def fct_fill_matrix(optimization, df_data_input, df_data_input_landuse, arr_pv, arr_onshore, x_range_temp, y_range_temp):

    dim_col = len(x_range_temp)
    dim_row = len(y_range_temp)

    arr_matrix_opti = np.empty(shape=[dim_row, dim_col])

    lst_pos_x = list(range(0, dim_col, 1))
    lst_pos_y = list(range(0, dim_row, 1))

    val_h2_selling_price = LCOH_settings.val_h2_selling_price

    for i_y in lst_pos_y:
        for i_x in lst_pos_x:

            [val_lcoh, val_vol] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore,x_range_temp[i_x], y_range_temp[i_y])
            # Correct LCOH when above threshold
            val_lcoh = np.where(val_lcoh > val_h2_selling_price, val_h2_selling_price, val_lcoh)

            if optimization == 'Lcoh':

                arr_matrix_opti[i_y, i_x] = val_lcoh

                arr_matrix_opti[np.isnan(arr_matrix_opti)] = 0
                arr_matrix_opti[np.isinf(arr_matrix_opti)] = 100

            elif optimization == 'Profit':

                val_unit = LCOH_tools.fct_unit_2d(df_data_input_landuse, x_range_temp[i_x], y_range_temp[i_y])

                # Calculate profit for assumed selling price
                arr_matrix_opti[i_y, i_x] = val_unit * val_vol * (val_h2_selling_price - val_lcoh) / 1000

                arr_matrix_opti[np.isnan(arr_matrix_opti)] = 0

            elif optimization == 'Volume':

                val_unit = LCOH_tools.fct_unit_2d(df_data_input_landuse, x_range_temp[i_x], y_range_temp[i_y])
                #Calculate total volumes
                if (x_range_temp[i_x] == 0) & (y_range_temp[i_y] == 0):
                    arr_matrix_opti[i_y, i_x] = 0
                else:
                    arr_matrix_opti[i_y, i_x] = val_unit * val_vol

                # arr_matrix_opti[np.isinf(arr_matrix_opti)] = 1000000

    return arr_matrix_opti


def fct_optimize_system_2d(optimization, df_data_input, df_data_input_landuse, arr_pv, arr_onshore):

    if optimization in ['Lcoh']:
        optimization_objective = 'minimize'
    elif optimization in ['Volume', 'Profit']:
        optimization_objective = 'maximize'

    i_init = 0
    difference = 1000
    while difference > LCOH_settings.tolerance:

        i_init += 1

        if i_init == 1:
            x_range_temp = LCOH_settings.x_range_init
            y_range_temp = LCOH_settings.y_range_init

        arr_opt_2d = fct_fill_matrix(optimization, df_data_input, df_data_input_landuse, arr_pv, arr_onshore, x_range_temp, y_range_temp)

        [arr_opt_2d, x_range_temp, y_range_temp] = fct_find_optimum_quadrant(arr_opt_2d, x_range_temp, y_range_temp, optimization_objective)

        difference = min((x_range_temp[-1]-x_range_temp[0]),(y_range_temp[-1]-y_range_temp[0]))


    if optimization_objective == 'maximize':
        pos_opt = np.unravel_index(arr_opt_2d.argmax(), arr_opt_2d.shape)
    else:
        pos_opt = np.unravel_index(arr_opt_2d.argmin(), arr_opt_2d.shape)


    x_optimum = x_range_temp[pos_opt[1]]
    y_optimum = y_range_temp[pos_opt[0]]

    [val_lcoh_optimum, val_vol_optimum] = LCOH_tools.fct_lcoh_2d(df_data_input, arr_pv, arr_onshore, x_optimum, y_optimum)

    val_unit_optimum = LCOH_tools.fct_unit_2d(df_data_input_landuse, x_optimum, y_optimum)

    return x_optimum, y_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum


def fct_optimize_system_1d(df_data_input, df_data_input_landuse, i_system, arr_res, optimization):

    if optimization in ['Lcoh']:
        optimization_objective = 'minimize'
    elif optimization in ['Volume', 'Profit']:
        optimization_objective = 'maximize'

    i_init = 0
    difference = 1000
    while difference > LCOH_settings.tolerance:

        i_init += 1

        if i_init == 1:
            x_range_temp = LCOH_settings.x_range_1d_init

        arr_opt_new = fct_fill_vector(optimization, df_data_input, df_data_input_landuse, i_system, arr_res, x_range_temp)

        [arr_opt, x_range_temp] = fct_find_optimum_sector(arr_opt_new, x_range_temp, optimization_objective)

        difference = (x_range_temp[-1]-x_range_temp[0])

    if optimization_objective == 'maximize':
        pos_opt = np.argmax(arr_opt)
    else:
        pos_opt = np.argmin(arr_opt)

    val_x_optimum = x_range_temp[pos_opt]

    if val_x_optimum == 0:
        val_unit_optimum = 0
        val_lcoh_optimum = 1000
        val_vol_optimum = 0

    else:
        [val_lcoh_optimum, val_vol_optimum] = LCOH_tools.fct_lcoh_1d(df_data_input, arr_res, val_x_optimum)
        val_unit_optimum = LCOH_tools.fct_unit_1d(df_data_input_landuse, i_system, val_x_optimum)

    return val_x_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum






