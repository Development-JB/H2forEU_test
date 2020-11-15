import pandas as pd

# Load and prepare color scheme energy type
df_energy_type_color = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Data\\01Input\\General_data_color_scheme_energy_type.csv")
df_energy_type_color['Rgb'] = 'rgb('+df_energy_type_color['Red'].astype(str)+','+df_energy_type_color['Green'].astype(str)+','+df_energy_type_color['Blue'].astype(str)+')'
ser_energy_type_color = pd.Series(df_energy_type_color['Rgb'].tolist(), index=df_energy_type_color['Energy_type'].tolist())
dict_energy_type_color = ser_energy_type_color.to_dict()
del df_energy_type_color, ser_energy_type_color

# Order Energy_type
df_energy_type_order = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Data\\01Input\\General_data_order_energy_type.csv")


# Grid lines
var_grid_line = 'rgb(240,240,240)'

# Country ColorCode
df_link_country_color_code = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper1\\Data\\00Templates\\Template_ColorCodeCountry.csv")

