import numpy as np
import pandas as pd

import LCOH_settings
import LCOH_tools
import LCOH_solver



def run_optimization(i_sensitivity, i_country,i_system,i_electrolyser,i_year,arr_pv,arr_onshore):

    df_data_input_temp = LCOH_tools.fct_prepare_input_data(i_sensitivity, i_country,i_system,i_electrolyser,i_year)

    #print(df_data_input_temp)

    if i_system == 'Hybrid':
        [lcoh_optimum, pv_optimium, onshore_optimium, vol_optimum] = LCOH_solver.fct_optimize_system_2d(df_data_input_temp, arr_pv, arr_onshore)
    elif i_system == 'PV':
        [lcoh_optimum, pv_optimium, vol_optimum] = LCOH_solver.fct_optimize_system_1d(df_data_input_temp, arr_pv)
        onshore_optimium = 0
    elif i_system == 'Onshore':
        [lcoh_optimum, onshore_optimium, vol_optimum] = LCOH_solver.fct_optimize_system_1d(df_data_input_temp, arr_onshore)
        pv_optimium = 0

    return lcoh_optimum, pv_optimium, onshore_optimium, vol_optimum



def fct_check_results(var_sensitivity, var_country, var_cell, var_system, var_electrolyser, var_year, df_result):

    df_data_input_check = LCOH_tools.fct_prepare_input_data(var_sensitivity, var_country, var_system, var_electrolyser, var_year)

    #print(df_data_input_check)

    if var_system == 'Hybrid':
        x_optimum_check = df_result.loc[(var_country, var_cell, var_system, var_electrolyser, var_year), 'PV'].mean()
        y_optimum_check = df_result.loc[
            (var_country, var_cell, var_system, var_electrolyser, var_year), 'Onshore'].mean()
        lcoh_optimum_check = df_result.loc[
            (var_country, var_cell, var_system, var_electrolyser, var_year), 'Lcoh'].mean()

        x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)
        y_range_check = np.linspace(y_optimum_check * 0.5, y_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_pv_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_pv_check = df_profile_pv_check[['Load_factor']].to_numpy()
        df_profile_onshore_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_Onshore_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_onshore_check = df_profile_onshore_check[['Load_factor']].to_numpy()

        arr_matrix_check = LCOH_tools.fct_create_check_matrix(df_data_input_check, arr_pv_check, arr_onshore_check, x_range_check,y_range_check)
        arr_matrix_check = np.where(arr_matrix_check > 20, np.nan, arr_matrix_check)

        LCOH_tools.fct_plot_check_2d(arr_matrix_check, x_range_check, y_range_check, lcoh_optimum_check, x_optimum_check,y_optimum_check)

    elif var_system == 'PV':
        x_optimum_check = df_result.loc[(var_country, var_cell, var_system, var_electrolyser, var_year), 'PV'].mean()
        lcoh_optimum_check = df_result.loc[
            (var_country, var_cell, var_system, var_electrolyser, var_year), 'Lcoh'].mean()

        x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_pv_check = pd.read_csv(LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_PV_" + str(LCOH_settings.val_reference_year) + ".csv")
        arr_res = df_profile_pv_check[['Load_factor']].to_numpy()

        arr_vector_check = LCOH_tools.fct_create_check_vector(df_data_input_check, arr_res, x_range_check)
        arr_vector_check = np.where(arr_vector_check > 20, np.nan, arr_vector_check)

        LCOH_tools.fct_plot_check_1d(arr_vector_check, x_range_check, lcoh_optimum_check, x_optimum_check)

    elif var_system == 'Onshore':
        x_optimum_check = df_result.loc[
            (var_country, var_cell, var_system, var_electrolyser, var_year), 'Onshore'].mean()
        lcoh_optimum_check = df_result.loc[
            (var_country, var_cell, var_system, var_electrolyser, var_year), 'Lcoh'].mean()

        x_range_check = np.linspace(x_optimum_check * 0.5, x_optimum_check * 2, LCOH_settings.check_steps)

        df_profile_onshore_check = pd.read_csv(
            LCOH_settings.path_folder_res_profiles + "\\" + var_cell + "_Onshore_" + str(
                LCOH_settings.val_reference_year) + ".csv")
        arr_res = df_profile_onshore_check[['Load_factor']].to_numpy()

        arr_vector_check = LCOH_tools.fct_create_check_vector(df_data_input_check, arr_res, x_range_check)
        arr_vector_check = np.where(arr_vector_check > 20, np.nan, arr_vector_check)

        LCOH_tools.fct_plot_check_1d(arr_vector_check, x_range_check, lcoh_optimum_check, x_optimum_check)


