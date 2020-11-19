import pandas as pd
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from app import app
from apps import page_load_data


# ------------------------------------------------------------------------------
# Load data

lst_transport_international = ['Pipeline','NH3']
lst_node_import = ['ESP01','ESP02','ITA01']
lst_year = [2020, 2030, 2040]

json_nuts2 = page_load_data.fct_load_json_file()
df_results = page_load_data.fct_load_results_supply()
df_import_capacity = page_load_data.fct_load_import_capacity()

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 3, 'offset': 1},
                    ),
            dbc.Col(html.H3('Node import'),
                    width={'size': 3, 'offset': 1},
                    ),
            dbc.Col(html.H3('Transport international'),
                    width={'size': 3, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="page_utilization_import_drop_year",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_year],
                                 multi=True,
                                 value=lst_year[:],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_utilization_import_drop_node_import",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_node_import],
                                 multi=True,
                                 value=lst_node_import[:],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_utilization_import_drop_transport_international",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_transport_international],
                                 multi=True,
                                 value=lst_transport_international[:],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_utilization_import_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_utilization_import_graph', component_property='figure'),
    [Input(component_id='page_utilization_import_drop_year', component_property='value'),
     Input(component_id='page_utilization_import_drop_node_import', component_property='value'),
     Input(component_id='page_utilization_import_drop_transport_international', component_property='value')],
)
def page_utilization_import_update_graph(slct_year, slct_node_import, slct_transport_international):

    #print(slct_year)

    #slct_node_import = ['ESP01','ESP02','ITA01']
    #slct_transport_international = ['Pipeline','NH3']
    #slct_year = [2020, 2030]

    #df_slct_result = df_results.copy()
    df_slct_result = pd.read_csv("C:\\Users\\Johannes\\Desktop\\Utilization.csv")
    df_slct_result = df_slct_result[['Year','Node_import','Transport_international','Volume']].groupby(['Year','Transport_international','Node_import']).agg({'Volume':'sum'}).reset_index()
    df_slct_result = df_slct_result[df_slct_result['Year'].isin(slct_year)]
    df_slct_result = df_slct_result[df_slct_result['Node_import'].isin(slct_node_import)]
    df_slct_result = df_slct_result[df_slct_result['Transport_international'].isin(slct_transport_international)]
    #df_slct_result['Volume'] = df_slct_result['Volume']*1000000

    #df_slct_import_capacity = df_import_capacity.copy()
    df_slct_import_capacity = pd.read_csv("C:\\Users\\Johannes\\Desktop\\Capacity.csv")
    df_slct_import_capacity = df_slct_import_capacity[['Year','Node_import','Transport_international','Transport_international_import_capacity']].groupby(['Year','Node_import','Transport_international']).agg({'Transport_international_import_capacity':'sum'}).reset_index()
    df_slct_import_capacity = df_slct_import_capacity[df_slct_import_capacity['Year'].isin(slct_year)]
    df_slct_import_capacity = df_slct_import_capacity[df_slct_import_capacity['Node_import'].isin(slct_node_import)]
    df_slct_import_capacity = df_slct_import_capacity[df_slct_import_capacity['Transport_international'].isin(slct_transport_international)]


    fig = go.Figure()

    counter = 0
    for i_node_import in df_slct_import_capacity['Node_import'].drop_duplicates().tolist():
        print(i_node_import)
        counter += 1

        arr_y_utilized = df_slct_result['Volume'][df_slct_result['Node_import'] == i_node_import].to_numpy().T
        arr_y_capacity = df_slct_import_capacity['Transport_international_import_capacity'][df_slct_import_capacity['Node_import'] == i_node_import].to_numpy().T
        arr_x = df_slct_import_capacity[['Year','Transport_international']][df_slct_import_capacity['Node_import'] == i_node_import].to_numpy().T

        fig.add_trace(go.Bar(y=arr_y_capacity,
                             x=arr_x,
                             offsetgroup=counter,
                             marker_color='rgb(150,0,0)',
                             showlegend=False,
                             text=i_node_import,
                             textposition='outside',
                             name='Available'))

        fig.add_trace(go.Bar(y=arr_y_utilized,
                             x=arr_x,
                             offsetgroup=counter,
                             marker_color='rgb(0,0,150)',
                             showlegend=False,
                             name='Utilized'))

    fig.update_layout(
                            boxmode='group'  # group together boxes of the different traces for each value of x
                        )

    #fig.show()


    return fig