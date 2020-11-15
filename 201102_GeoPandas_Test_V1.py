import geopandas as gpd
import pandas as pd
import json
import plotly.graph_objs as go
import plotly.express as px
#import plotly.io as pio
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot

df_nuts2 = gpd.read_file("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\QGIS\\EU_NUTS2\\Layer\\EU_NUTS2_V0.shp")
# df_nuts2.plot(cmap = 'jet', column='NUTS_ID', figsize=[10,10])
# df_nuts2.crs

path_file_json = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\Python_Dash_Multipage_H2forEU\\datasets\\EU_NUTS2_V0.json"
df_nuts2.to_file(path_file_json, driver = 'GeoJSON')

with open(path_file_json, encoding='utf-8') as geofile:
    json_nuts3 = json.load(geofile)

print(json_nuts3['features'][0].keys())
print(json_nuts3['features'][0]['properties'])

# Add unique key to every element / row
# Goes though all rows
for i_feature in json_nuts3['features']:
    print(i_feature)
    i_feature['id'] = i_feature['properties']['NUTS_ID']

print(json_nuts3['features'][0]['id'])

<

path_file_results_lcoh = "C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Tools\\LCOH\\201102_Results_LCOH_CentralEurope.csv"
df_nuts2_codes_fr = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\06Research\\Paper2\\Data\\06TreatedPreparedData\\NUTS2_France\\NUTS2_codes_FR.csv")
df_lcoh = pd.merge(df_lcoh,df_nuts2_codes_fr, how='left', on=['Nuts2_code2013'])
df_lcoh['NUTS_ID'] = df_lcoh['Nuts2_code2016'].combine_first(df_lcoh['Nuts2_code2013'])

df_lcoh = pd.read_csv(path_file_results_lcoh)
df_lcoh =df_lcoh.drop(['Alkaline','PEM'], axis=1)
df_lcoh = df_lcoh[df_lcoh['Year'] == 2020]
df_lcoh = df_lcoh[df_lcoh['System'] == 'Hybrid']
df_lcoh = df_lcoh[df_lcoh['Electrolyser'] == 'Alkaline']
df_lcoh['Nuts2_code2013'] = df_lcoh['Cell'].str[4:]




fig = px.choropleth(df_lcoh, locations='NUTS_ID', geojson=json_nuts3, color='LCOH')
fig.update_geos(fitbounds='locations', visible=False)
fig.show()

