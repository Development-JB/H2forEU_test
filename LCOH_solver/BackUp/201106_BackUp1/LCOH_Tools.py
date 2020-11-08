import numpy as np
import LCOH_main


def fct_calculated_annualized_cost(var_capex, var_opex, var_lifetime, var_wacc):

    var_annualization_factor = (var_wacc/100)/(1-(1+var_wacc/100)**(-var_lifetime))
    var_annualized_cost = var_capex*var_annualization_factor+var_opex

    return var_annualized_cost


def fct_lcoh(i_x, i_y, x_range_temp, y_range_temp):
    x_temp = x_range_temp[i_x]
    y_temp = y_range_temp[i_y]

    total_cost = x_temp * LCOH_main.i_annulized_pv + y_temp * LCOH_main.i_annulized_onshore + LCOH_main.i_annulized_electrolyser

    total_electricity = np.where((LCOH_main.arr_pv * x_temp + LCOH_main.arr_onshore * y_temp) > 1, 1,
                                 (LCOH_main.arr_pv * x_temp + LCOH_main.arr_onshore * y_temp)).sum()

    total_hydrogen = total_electricity * LCOH_main.i_efficiency_electrolyser * 1000 / 33.33

    lcoh = total_cost / total_hydrogen

    return lcoh

