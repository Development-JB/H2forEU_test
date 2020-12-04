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

lst_source_vres = load_data.lst_source_vres
lst_technology = load_data.lst_technology + ['Best']
lst_year = load_data.lst_year

json_data = functions.fct_load_json_file()
#df_system = functions.fct_load_system_result()
df_colorbar = pd.read_csv("C:\\Users\\Johannes\\Documents\\PhD\\07GeneralData\\Color_scheme\\Colorbar_HybridSystem.csv")

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 5, 'offset': 1},
                    ),

            dbc.Col(html.H3('Node import'),
                    width={'size': 3, 'offset': 1},
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

            dbc.Col(dcc.Dropdown(id="page_system_drop_technology",
                             options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_technology],
                             multi=True,
                             value=lst_technology[:],
                             style={'width': "100%"}
                             ),
                width={'size': 3, 'offset': 1},
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
    [Input(component_id='page_system_slider_year', component_property='value'),
     Input(component_id='page_system_drop_technology', component_property='value')],
)
def page_lcoh_update_graph(slct_year, slct_technology):

    # #print(slct_year)
    # slct_year = 2020
    # slct_technology = 'Best'

    # df_slct = df_system.copy()
    # df_slct = df_slct[df_slct['Year'] == slct_year]
    # df_slct = df_slct[df_slct['Source'] == 'Hybrid']
    #
    # if slct_technology == 'Best':
    #     df_slct = df_slct.sort_values(['Node_production','Source','Year','Production_cost'], ascending=True)
    #     df_slct = df_slct.drop_duplicates(['Node_production','Source','Year'], keep='first')
    # else:
    #     df_slct = df_slct[df_slct['Optimization'] == slct_technology]
    #
    # colorscale = df_colorbar[['Ratio_hybrid','Rgb']].to_numpy()
    #
    # df_slct = df_slct.rename(columns={'Node_production':'Cell_node'})
    # df_slct = df_slct.rename(columns={'Cell_node':'Id_cell'})

    #df_slct = pd.read_csv(r"C:\Users\Johannes\Desktop\Cells_test.csv")
    df_slct = pd.read_csv(r"C:\Users\Johannes\Documents\PhD\06Research\Paper2\Tools\LCOH_solver\201204_Results_LCOH_World.csv")
    df_slct = df_slct[df_slct['System'] == 'Hybrid']
    df_slct = df_slct[df_slct['Year'] == 2050]

    fig = go.Figure(data=[go.Choropleth(geojson=json_data,
                                        locations=df_slct['Id_cell'],
                                        z=df_slct['Lcoh']
                                        #autocolorscale=True,
                                        #colorscale=colorscale
                                        )])

    fig.update_layout(height=800)
    fig.update_geos(fitbounds='locations',
                    visible=False,
                    showframe=False,
                    scope='world')

    fig.show()

    return fig