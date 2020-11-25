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

from apps import load_data
from apps import functions


# ------------------------------------------------------------------------------
# Load data

lst_year = load_data.lst_year

json_nuts2 = functions.fct_load_json_file()
df_data = functions.fct_load_capacity_utilitzation_result()

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
                                id='page_map_system_capacity_utilization_slider_year',
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
            dbc.Col(dcc.Graph(id='page_map_system_capacity_utilization_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_map_system_capacity_utilization_graph', component_property='figure'),
    [Input(component_id='page_map_system_capacity_utilization_slider_year', component_property='value')],
)
def page_lcoh_update_graph(slct_year):

    #print(slct_year)
    slct_year = 2020

    df_slct = df_data.copy()
    df_slct = df_slct[df_slct['Year'] == slct_year]

    df_slct = df_slct.rename(columns={'Node_production':'Cell_node'})
    df_slct = df_slct.rename(columns={'Cell_node':'NUTS_ID'})

    fig = go.Figure(data=[go.Choropleth(geojson=json_nuts2,
                                        locations=df_slct['NUTS_ID'],
                                        z=df_slct['Ratio_capacity_utilization']
                                        #autocolorscale=True,
                                        #colorscale=colorscale
                                        )
                          ]
                    )

    fig.update_layout(height=800)
    fig.update_geos(fitbounds='locations',
                    visible=False,
                    showframe=False,
                    scope='world')

    fig.show()

    return fig