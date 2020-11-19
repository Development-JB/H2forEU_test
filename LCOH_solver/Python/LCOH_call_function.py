import numpy as np
import pandas as pd

import LCOH_settings
import LCOH_tools
import LCOH_solver


def fct_run_optimization(i_sensitivity, i_country, i_cell, i_system, i_electrolyser, i_year, i_optimization, arr_pv, arr_onshore):

    df_data_input_temp = LCOH_tools.fct_prepare_input_data(i_sensitivity, i_country,i_system,i_electrolyser,i_year)
    df_data_input_landuse_temp = LCOH_tools.fct_prepare_input_data_landuse(i_sensitivity, i_cell, i_year)

    if i_system == 'PV':
        [val_pv_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum] = LCOH_solver.fct_optimize_system_1d(df_data_input_temp, df_data_input_landuse_temp, i_system, arr_pv, i_optimization)
        val_onshore_optimum = 0

    elif i_system == 'Onshore':
        [val_onshore_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum] = LCOH_solver.fct_optimize_system_1d(df_data_input_temp, df_data_input_landuse_temp, i_system, arr_onshore, i_optimization)
        val_pv_optimum = 0

    elif i_system == 'Hybrid':
        [val_pv_optimum, val_onshore_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum] = LCOH_solver.fct_optimize_system_2d(i_optimization, df_data_input_temp, df_data_input_landuse_temp, arr_pv, arr_onshore)

    return val_pv_optimum, val_onshore_optimum, val_lcoh_optimum, val_vol_optimum, val_unit_optimum


def fct_check_results(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, var_optimization, df_result):
    df_result = df_result.set_index(['Sensitivity', 'Country', 'Cell', 'System', 'Electrolyser', 'Year', 'Optimization'])

    df_data_input_check = LCOH_tools.fct_prepare_input_data(var_sensitivity, var_country, var_system, var_electrolyser, var_year)
    df_data_input_landuse_check = LCOH_tools.fct_prepare_input_data_landuse(var_sensitivity, var_cell, var_year)

    if var_system == 'Hybrid':
        x_optimum_check = df_result.loc[(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, var_optimization), 'PV'].mean()
        if round(x_optimum_check,4) == 0:
            x_range_check = np.linspace(0, 1, LCOH_settings.check_steps)
        else:
            x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)

        y_optimum_check = df_result.loc[(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, var_optimization), 'Onshore'].mean()
        if round(y_optimum_check,0) == 0:
            y_range_check = np.linspace(0, 1, LCOH_settings.check_steps)
        else:
            y_range_check = np.linspace(y_optimum_check * 0.5, y_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_pv_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_pv_check = df_profile_pv_check[['Load_factor']].to_numpy()
        df_profile_onshore_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_Onshore_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_onshore_check = df_profile_onshore_check[['Load_factor']].to_numpy()

        arr_matrix_check = LCOH_solver.fct_fill_matrix(var_optimization, df_data_input_check, df_data_input_landuse_check, arr_pv_check, arr_onshore_check, x_range_check, y_range_check)

        if var_optimization in ['Lcoh']:
            arr_matrix_check = np.where(arr_matrix_check > 20, np.nan, arr_matrix_check)
        elif var_optimization in ['Volume', 'Profit']:
            val_opt = np.amax(arr_matrix_check)
            arr_matrix_check = arr_matrix_check/val_opt

        LCOH_tools.fct_plot_check_2d(arr_matrix_check, x_range_check, y_range_check, x_optimum_check,y_optimum_check)


    elif var_system == 'PV':

        x_optimum_check = df_result.loc[(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, var_optimization), 'PV'].mean()

        x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_pv_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_res = df_profile_pv_check[['Load_factor']].to_numpy()

        arr_vector_check = LCOH_solver.fct_fill_vector(var_optimization, df_data_input_check, df_data_input_landuse_check, var_system, arr_res, x_range_check)

        if var_optimization in ['Lcoh']:
            arr_vector_check = np.where(arr_vector_check > 20, np.nan, arr_vector_check)

        elif var_optimization in ['Volume', 'Profit']:
            val_opt = np.amax(arr_vector_check)
            arr_vector_check = arr_vector_check/val_opt

        LCOH_tools.fct_plot_check_1d(arr_vector_check, x_range_check, x_optimum_check)

    elif var_system == 'Onshore':

        x_optimum_check = df_result.loc[(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, var_optimization), 'Onshore'].mean()

        x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_onshore_check = pd.read_csv(
            LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_Onshore_" + str(
                LCOH_settings.val_reference_year) + ".csv")
        arr_res = df_profile_onshore_check[['Load_factor']].to_numpy()

        arr_vector_check = LCOH_solver.fct_fill_vector(var_optimization, df_data_input_check, df_data_input_landuse_check, var_system, arr_res, x_range_check)

        if var_optimization in ['Lcoh']:
            arr_vector_check = np.where(arr_vector_check > 20, np.nan, arr_vector_check)

        elif var_optimization in ['Volume', 'Profit']:
            val_opt = np.amax(arr_vector_check)
            arr_vector_check = arr_vector_check / val_opt

        LCOH_tools.fct_plot_check_1d(arr_vector_check, x_range_check, x_optimum_check)

