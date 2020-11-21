import pathlib
import gdxpds
import pandas as pd


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import load_data
import plotly.graph_objects as go


# ------------------------------------------------------------------------------
# Load data

lst_source = load_data.lst_source
lst_year = load_data.lst_year


json_map = load_data.fct_load_json_file()
df_data = load_data.fct_load_results_supply()

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 5, 'offset': 1},
                    ),
            dbc.Col(html.H3('Source'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Slider(
                                id='page_map_source_results_slider_year',
                                min=lst_year[0],
                                max=lst_year[-1],
                                step=10,
                                value=lst_year[0],
                                marks=dict(zip(lst_year, lst_year)),
                                ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_map_source_results_drop_source",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_source],
                                 multi=False,
                                 value=lst_source[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_map_source_results_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    Output(component_id='page_map_source_results_graph', component_property='figure'),
    [Input(component_id='page_map_source_results_drop_source', component_property='value'),
     Input(component_id='page_map_source_results_slider_year', component_property='value')],
)
def page_map_source_results_update_graph(slct_source, slct_year):

    #print(slct_source)
    #print(slct_year)

    slct_year = 2020
    slct_source = 'Onshore'

    df_slct = df_data.copy()
    df_slct = df_slct[df_slct['Year']==slct_year]
    df_slct = df_slct[df_slct['Source'] == slct_source]
    df_slct = df_slct.rename(columns={'Volume':'Value'})
    df_slct = df_slct[['Node_production','Value']].groupby(['Node_production']).agg({'Value':'sum'}).reset_index()


    fig = go.Figure()
    # fig = go.Figure(data=[go.Choropleth(geojson=json_map,
    #                                     locations=df_slct['NUTS_ID'],
    #                                     z=df_slct['Value'],
    #                                     colorscale=[[0,'rgb(255,255,255)'],[1,'rgb(0,0,255)']]
    #                                     )
    #                       ])
    #
    # fig.update_geos(fitbounds='locations', visible=False)

    #fig.show()

    return fig