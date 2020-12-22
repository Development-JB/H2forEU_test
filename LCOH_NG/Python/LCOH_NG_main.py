import time
import pandas as pd

import LCOH_NG_settings
import LCOH_NG_call_function

df_lcoh_result = pd.DataFrame([])
df_lcoh_error = pd.DataFrame([])
for i_ctry in LCOH_NG_settings.lst_crty[:]:
    print(i_ctry)

    for i_technology in LCOH_NG_settings.lst_technology[:]:
        print(i_technology)

        for i_year in LCOH_NG_settings.lst_year[:]:
            print(i_year)

            for i_sensitivity in LCOH_NG_settings.lst_sensitivity[:1]:
                #print(i_sensitivity)

                try:
                    df_lcoh_result_temp = LCOH_NG_call_function.fct_calculate_lcoh(i_ctry, i_technology, i_year, i_sensitivity)
                    #print(df_lcoh_result_temp)

                    df_lcoh_result = df_lcoh_result.append(df_lcoh_result_temp)

                except:

                    df_lcoh_error_temp = pd.DataFrame([i_ctry], columns=['Ctry_iso3'])
                    df_lcoh_error = df_lcoh_error.append(df_lcoh_error_temp)

df_lcoh_result.to_csv(r"C:\Users\Johannes\Documents\PhD\06Research\Paper2\Tools\LCOH_NG\Data\02Output\201213_Results_V0.csv", index=False)
df_lcoh_error.to_csv(r"C:\Users\Johannes\Documents\PhD\06Research\Paper2\Tools\LCOH_NG\Data\02Output\201213_Errors_V0.csv", index=False)