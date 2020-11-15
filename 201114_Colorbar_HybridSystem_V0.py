import pandas as pd
import numpy as np
import plotly.graph_objs as go

val_steps = 101
lst_range_steps = np.linspace(0,1,val_steps)
lst_range_steps = np.round(lst_range_steps, 2)
df_colorbar = pd.DataFrame([])
df_colorbar['Ratio_hybrid'] = lst_range_steps
df_colorbar = df_colorbar.set_index(['Ratio_hybrid'])
df_colorbar['Red'] = np.nan
df_colorbar['Green'] = np.nan
df_colorbar['Blue'] = np.nan

## PV
df_colorbar.loc[0,'Red'] = 255
df_colorbar.loc[0,'Green'] = 255
df_colorbar.loc[0,'Blue'] = 102

# df_colorbar.loc[0,'Red'] = 252
# df_colorbar.loc[0,'Green'] = 236
# df_colorbar.loc[0,'Blue'] = 104

# Onshore
df_colorbar.loc[1,'Red'] = 60
df_colorbar.loc[1,'Green'] = 120
df_colorbar.loc[1,'Blue'] = 255

# df_colorbar.loc[1,'Red'] = 200
# df_colorbar.loc[1,'Green'] = 229
# df_colorbar.loc[1,'Blue'] = 255

df_colorbar = df_colorbar.interpolate(axis=0)
df_colorbar = df_colorbar.round(1)
df_colorbar['Rgb'] = 'rgb('+df_colorbar['Red'].astype(str)+','+df_colorbar['Green'].astype(str)+','+df_colorbar['Blue'].astype(str)+')'

df_colorbar.to_csv("C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")


fig = go.Figure()

for i_x in df_colorbar.index.tolist():
    print(i_x)

    fig.add_trace(go.Scatter(x=[i_x],
                             y=[i_x],
                             mode = 'markers',
                             showlegend=False,
                             marker=dict(size=10, color= df_colorbar.loc[i_x,'Rgb'])))

fig.show()