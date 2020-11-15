import pathlib
import gdxpds
import pandas as pd


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from app import app


# ------------------------------------------------------------------------------
# MARCO Data

# Import gdx pre-load
from apps import marco_load_gdx

# gdx preparation
df_gdx_load = marco_load_gdx.fct_load_gdx_load()

lst_system = ['PV','Onshore','Hybrid','Best']
lst_electrolyser = ['PEM','Alkaline']

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('System'),
                    width={'size': 5, 'offset': 1},
                    ),
            dbc.Col(html.H3('Electrolyser'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="h2foreu_load_drop_system",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_system],
                                 multi=True,
                                 value=[lst_system[0]],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="h2foreu_load_drop_electrolyser",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_electrolyser],
                                 multi=True,
                                 value=lst_electrolyser[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='h2foreu_load_graph_line',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='h2foreu_load_graph_line', component_property='figure'),
    [Input(component_id='h2foreu_load_drop_system', component_property='value'),
     Input(component_id='h2foreu_load_drop_electrolyser', component_property='value')],
)
def update_graph(slct_week, slct_zone):

    # df_slct = df_gdx_load.copy()
    #
    # df_slct = df_slct[df_slct['Timestep_week'].isin(slct_week)]
    #
    # df_slct = df_slct[df_slct['Zone'].isin(slct_zone)]



    fig = []

    # fig = px.line(
    #     data_frame=df_slct,
    #     x='Timestep_hour',
    #     y='Value',
    #     color='Zone'
    # )

    return fig