import pandas as pd
import numpy as np

df_nuts2 = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\05WorkingData\\201112_NUTS2EU_Table_Area_V0.csv")
df_lcoh = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH_solver\\201111_Results_LCOH_CentralEurope.csv")
df_nuts2_codes_fr = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")


val_landuse_availability = 0.15
val_land_utilisation = 0.0067
df_nuts2['Area'] = df_nuts2['Area']/10**6
df_nuts2['Area_available'] = df_nuts2['Area']*val_landuse_availability
df_nuts2['Area_utilisable'] = df_nuts2['Area_available']*val_land_utilisation
df_nuts2= df_nuts2.rename(columns={'NUTS_ID':'Nuts2_code2016'})
df_nuts2 = pd.merge(df_nuts2[['Nuts2_code2016','Area_utilisable']], df_nuts2_codes_fr, how='left', on=['Nuts2_code2016'])
df_nuts2['Nuts2_code'] = df_nuts2['Nuts2_code2013'].combine_first(df_nuts2['Nuts2_code2016'])
df_nuts2 = df_nuts2.drop(['Nuts2_code2013','Nuts2_code2016'], axis=1)

df_lcoh['Nuts2_code'] = df_lcoh['Cell'].str[4:]
df_lcoh = pd.merge(df_lcoh,df_nuts2, how='left', on=['Nuts2_code'])
df_lcoh_selected = df_lcoh[df_lcoh['Sensitivity']=='Default']
df_lcoh_selected = df_lcoh_selected[df_lcoh_selected['Year']==2020]
df_lcoh_selected = df_lcoh_selected[df_lcoh_selected['Electrolyser']=='Alkaline']



val_energy_density_pv = 170
val_land_dedication_pv = 0.03
val_energy_density_onshore = 5
val_land_dedication_onshore = 1

df_lcoh_selected['Units'] = np.nan
df_lcoh_selected['Units'] = np.where((df_lcoh_selected['PV'] == 0) & (df_lcoh_selected['Onshore'] != 0), df_lcoh_selected['Area_utilisable']/(df_lcoh_selected['Onshore']/(val_energy_density_onshore*val_land_dedication_onshore)), df_lcoh_selected['Units'])
df_lcoh_selected['Units'] = np.where((df_lcoh_selected['PV'] != 0) & (df_lcoh_selected['Onshore'] == 0), df_lcoh_selected['Area_utilisable']/(df_lcoh_selected['PV']/(val_energy_density_pv*val_land_dedication_pv)), df_lcoh_selected['Units'])
df_lcoh_selected['Units'] = np.where((df_lcoh_selected['PV'] != 0) & (df_lcoh_selected['Onshore'] != 0), df_lcoh_selected['Area_utilisable']/(df_lcoh_selected['PV']/(val_energy_density_pv*val_land_dedication_pv)+df_lcoh_selected['Onshore']/(val_energy_density_onshore*val_land_dedication_onshore)), df_lcoh_selected['Units'])

val_lcoh_max = df_lcoh_selected['Lcoh'].max()

df_lcoh_selected['Revenues'] = df_lcoh_selected['Units']*val_lcoh_max*df_lcoh_selected['H2_volume']
df_lcoh_selected['Profit'] = df_lcoh_selected['Units']*(val_lcoh_max-df_lcoh_selected['Lcoh'])*df_lcoh_selected['H2_volume']
df_lcoh_selected['Total_h2_volume'] = df_lcoh_selected['Units']*df_lcoh_selected['H2_volume']
