import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
from apps import load_data
import plotly.graph_objects as go

from apps import functions
from apps import load_data


# ------------------------------------------------------------------------------
# Load data

lst_selection = ['Region_export','Region_import','Country_import','Country_export','Transport_international','Transport_national']
lst_year = load_data.lst_year

df_data = functions.fct_load_results_supply()

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 5, 'offset': 1},
                    ),
            dbc.Col(html.H3('Selection'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Slider(
                                id='page_sankey_slider_year',
                                min=lst_year[0],
                                max=lst_year[-1],
                                step=10,
                                value=lst_year[0],
                                marks=dict(zip(lst_year, lst_year)),
                                ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_sankey_drop_selection",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_selection],
                                 multi=True,
                                 value=['Region_export','Region_import'],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_sankey_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    Output(component_id='page_sankey_graph', component_property='figure'),
    [Input(component_id='page_sankey_drop_selection', component_property='value'),
     Input(component_id='page_sankey_slider_year', component_property='value')],
)
def page_sankey_update_graph(slct_selection, slct_year):

    print(slct_selection)
    print(slct_year)

    #slct_year = int(slct_year)

    #slct_year = 2020
    #slct_selection = ['Region_export','Country_export','Region_import']

    df_slct = df_data.copy()
    df_slct = df_slct[df_slct['Year']==slct_year]

    [data, layout] = functions.genSankey(df_slct, cat_cols=slct_selection, value_cols='Volume', title='Sankey Diagram')

    fig = go.Figure(data=[go.Sankey(data)])

    #fig.show()

    return fig
