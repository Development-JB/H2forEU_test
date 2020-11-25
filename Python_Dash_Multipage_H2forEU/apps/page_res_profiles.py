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
import plotly.graph_objects as go
from app import app

from apps import load_data
from apps import functions


# ------------------------------------------------------------------------------
# Load data

lst_res_selection = ['PV load factor','Onshore load factor','Correlation']

json_nuts2 = functions.fct_load_json_file()
[df_res_information, df_colorscale_load_factor] = functions.fct_load_res_information()

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    dbc.Row([
            dbc.Col(html.H2('Selection'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="page_res_profiles_drop_selection",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_res_selection],
                                 multi=False,
                                 value=lst_res_selection[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_res_profiles_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_res_profiles_graph', component_property='figure'),
    [Input(component_id='page_res_profiles_drop_selection', component_property='value')],
)
def page_res_profiles_update_graph(slct_selection):

    #print(slct_system)
    #print(slct_electrolyser)
    #print(slct_year)

    df_slct = df_res_information.copy()


    if slct_selection == 'PV load factor':
        df_slct = df_slct[['NUTS_ID','PV']]
        df_slct = df_slct.rename(columns={'PV':'Value'})
        val_min = df_slct['Value'].min().round(3)
        val_max = df_slct['Value'].max().round(3)
        arr_colorscale = [[0,df_colorscale_load_factor.loc[val_min,'Rgb']],[1,df_colorscale_load_factor.loc[val_max,'Rgb']]]

    elif slct_selection == 'Onshore load factor':
        df_slct = df_slct[['NUTS_ID','Wind']]
        df_slct = df_slct.rename(columns={'Wind':'Value'})
        val_min = df_slct['Value'].min().round(3)
        val_max = df_slct['Value'].max().round(3)
        # arr_colorscale = np.empty(shape=[2,2], dtype=object)
        # arr_colorscale[0,:] = [1,df_colorscale_load_factor.loc[val_max,'Rgb']]
        # arr_colorscale[1,:] = [0,df_colorscale_load_factor.loc[val_min,'Rgb']]
        arr_colorscale = [[0,df_colorscale_load_factor.loc[val_min,'Rgb']],[1,df_colorscale_load_factor.loc[val_max,'Rgb']]]


    elif slct_selection == 'Correlation':
        df_slct = df_slct[['NUTS_ID','Correlation']]
        df_slct = df_slct.rename(columns={'Correlation':'Value'})
        val_min = df_slct['Value'].min().round(3)
        val_max = df_slct['Value'].max().round(3)
        # arr_colorscale = np.empty(shape=[2,2], dtype=object)
        # arr_colorscale[0,:] = [1,'rgb(0,255,0)']
        # arr_colorscale[1,:] = [0,'rgb(255,0,0)']
        arr_colorscale = [[0,'rgb(255,0,0)'],[1,'rgb(0,255,0)']]



    fig = go.Figure(data=[go.Choropleth(geojson=json_nuts2,
                                        locations=df_slct['NUTS_ID'],
                                        z=df_slct['Value'],
                                        colorscale=arr_colorscale
                                        )
                          ])

    fig.update_geos(fitbounds='locations', visible=False)
    #fig.show()

    return fig