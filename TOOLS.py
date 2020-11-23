
def fct_replace_umlaute(df, val_column):
    
    df[val_column] = df[val_column].str.replace('ö', 'oe')
    df[val_column] = df[val_column].str.replace('ä', 'ae')
    df[val_column] = df[val_column].str.replace('ü', 'ue')
    df[val_column] = df[val_column].str.replace('Ö', 'Oe')
    df[val_column] = df[val_column].str.replace('Ä', 'Ae')
    df[val_column] = df[val_column].str.replace('Ü', 'ue')
    df[val_column] = df[val_column].str.replace('ß', 'ss')
    
    return df


def fct_clean_names(df, val_column):

    df = fct_replace_umlaute(df, val_column)

    df[val_column] = df[val_column].str.replace('(', '')
    df[val_column] = df[val_column].str.replace(')', '')
    df[val_column] = df[val_column].str.replace('-', '_')
    df[val_column] = df[val_column].str.replace(' ', '_')
    df[val_column] = df[val_column].str.replace(',', '')
    df[val_column] = df[val_column].str.replace('/', '_')
    df[val_column] = df[val_column].str.replace('&', '_')
    df[val_column] = df[val_column].str.capitalize()

    return df

def fct_harmonize_column_names(df,val_column, dict):

    df = df.replace({val_column: dict})

    return  df


def fct_read_all_files_in_folder(path):

    # e.g. Example Path
    #     path = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Data\\03RawData\\ENTSOE_Transparency\\ForecastedYearAheadTransferCapacity\\*_ForecastedYearAheadTransferCapacities.csv"

    import pandas as pd
    import glob

    df = pd.DataFrame([])
    for i_file in glob.glob(path):
        print(i_file)

        df_temp = pd.read_csv(i_file, sep='\t', encoding='utf16')
        df = df.append(df_temp)

    return df

def fct_calculate_optimal_tilt_angle_PV(df, decimals =None):

    import pandas as pd
    import numpy as np

    #Source: https://web.stanford.edu/group/efmh/jacobson/Articles/I/TiltAngles.pdf
    # See Fig1 - This study

    df['Tilt'] = np.nan
    df['Tilt'] = np.where(df['Latitude']>0,
                          1.3793+ df['Latitude'] *(1.2011 + df['Latitude']*(-0.014404 + df['Latitude']*0.000080509)),
                          -0.41657 + df['Latitude']*(1.4216 + df['Latitude']*(0.024052 + df['Latitude']*0.00021828)))

    if decimals == None:
        decimals = 2

    #df['Tilt'] = abs(df['Tilt'])
    df['Tilt'] = df['Tilt'].round(decimals)

    return df

def fct_create_power_curve_wind(df, decimals =None):

    import pandas as pd
    import numpy as np

    

    df['Tilt'] = np.nan
    df['Tilt'] = np.where(df['Latitude']>0,
                          1.3793+ df['Latitude'] *(1.2011 + df['Latitude']*(-0.014404 + df['Latitude']*0.000080509)),
                          -0.41657 + df['Latitude']*(1.4216 + df['Latitude']*(0.024052 + df['Latitude']*0.00021828)))

    if decimals == None:
        decimals = 2

    df['Tilt'] = df['Tilt'].round(decimals)

    return df