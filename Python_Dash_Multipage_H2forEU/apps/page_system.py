import pathlib
import gdxpds
import pandas as pd
import numpy as np





import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
from app import app
from apps import page_load_data


# ------------------------------------------------------------------------------
# MARCO Data

# Import gdx pre-load
#from apps import marco_load_gdx

# gdx preparation
#df_gdx_load = marco_load_gdx.fct_load_gdx_load()

lst_system = ['PV','Onshore','Hybrid']
lst_optimization = ['Lcoh','Volume','Profit']
lst_electrolyser = ['PEM','Alkaline']
lst_year = [2020,2030,2040]


json_nuts2 = page_load_data.fct_load_json_file()
df_system = page_load_data.fct_load_system_result()
df_colorbar = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Slider(
                                id='page_system_slider_year',
                                min=lst_year[0],
                                max=lst_year[-1],
                                step=10,
                                value=lst_year[0],
                                marks=dict(zip(lst_year, lst_year)),
                                ),
                    width={'size': 4, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_system_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_system_graph', component_property='figure'),
    [Input(component_id='page_system_slider_year', component_property='value')],
)
def page_lcoh_update_graph(slct_year):

    #print(slct_year)
    slct_year = 2020

    df_slct = df_system.copy()
    df_slct = df_slct[df_slct['Year'] == slct_year]
    df_slct = df_slct[df_slct['Optimization'] == 'Lcoh']
    df_slct = df_slct[df_slct['System'] == 'Hybrid']
    df_slct = df_slct[df_slct['Electrolyser'] == 'Alkaline']

    colorscale = df_colorbar[['Ratio_hybrid','Rgb']].to_numpy()
    #colorscale = [[0,'rgb(255,0,0)'],[1,'rgb(0,0,255)']]

    # fig = px.choropleth(df_slct, locations='NUTS_ID', geojson=json_nuts2, color='Pth2_system')
    # fig.update_geos(fitbounds='locations', visible=False)

    fig = go.Figure(data=[go.Choropleth(geojson=json_nuts2,
                                        locations=df_slct['NUTS_ID'],
                                        z=df_slct['Ratio_hybrid'],
                                        #autocolorscale=True,
                                        colorscale=colorscale)])
    fig.update_geos(fitbounds='locations', visible=False)
    #fig.show()
    return fig