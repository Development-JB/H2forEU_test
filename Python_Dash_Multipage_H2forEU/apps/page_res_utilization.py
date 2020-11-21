import pandas as pd
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

from apps import load_data
from apps import functions


# ------------------------------------------------------------------------------
# Load data

lst_energy_type = load_data.lst_energy_type
lst_country = load_data.lst_country_export
lst_year = load_data.lst_year

df_production_h2_system = load_data.df_production_h2_system[['Year','H2_system','Production_system']]
df_production_capacity = load_data.df_production_capacity
df_result = pd.merge(df_production_h2_system,df_production_capacity, how='left', on=['Year','H2_system'])
df_limit_country = load_data.df_production_limit_country

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 3, 'offset': 1},
                    ),
            dbc.Col(html.H3('Country'),
                    width={'size': 3, 'offset': 1},
                    ),
            dbc.Col(html.H3('Energy_type'),
                    width={'size': 3, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="page_res_utilization_drop_year",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_year],
                                 multi=True,
                                 value=lst_year[:],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_res_utilization_drop_country",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_country],
                                 multi=True,
                                 value=lst_country[:],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_res_utilization_drop_energy_type",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in ['PV','Onshore']],
                                 multi=True,
                                 value=['PV','Onshore'],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 3, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_res_utilization_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_res_utilization_graph', component_property='figure'),
    [Input(component_id='page_res_utilization_drop_year', component_property='value'),
     Input(component_id='page_res_utilization_drop_country', component_property='value'),
     Input(component_id='page_res_utilization_drop_energy_type', component_property='value')],
)
def page_res_utilization_update_graph(slct_year, slct_country, slct_energy_type):

    # slct_country = ['DZA','MAR']
    # slct_energy_type = ['PV','Onshore']
    # slct_year = [2020]

    df_slct_result = df_result.copy()
    df_slct_result['Country'] = df_slct_result['H2_system'].str[:3]
    df_slct_result['Capacity'] = df_slct_result['Production_system']*df_slct_result['Production_capacity']
    df_slct_result = df_slct_result[df_slct_result['Year'].isin(slct_year)]
    df_slct_result = df_slct_result[df_slct_result['Country'].isin(slct_country)]
    df_slct_result = df_slct_result[df_slct_result['Energy_type'].isin(slct_energy_type)]
    df_slct_result = df_slct_result.groupby(['Year','Country','Energy_type']).agg({'Capacity':'sum'}).reset_index()


    df_slct_limit_country = df_limit_country.copy()
    val_capacity_max = df_limit_country['Production_limit_country'].max()
    df_slct_limit_country = df_slct_limit_country[df_slct_limit_country['Year'].isin(slct_year)]
    df_slct_limit_country = df_slct_limit_country[df_slct_limit_country['Country'].isin(slct_country)]
    df_slct_limit_country = df_slct_limit_country[df_slct_limit_country['Energy_type'].isin(slct_energy_type)]


    fig = go.Figure()

    counter = 0
    for i_energy_type in df_slct_limit_country['Energy_type'].drop_duplicates().tolist():
        #print(i_energy_type)
        counter += 1

        arr_y_utilized = df_slct_result['Capacity'][df_slct_result['Energy_type'] == i_energy_type].to_numpy().T
        arr_y_capacity = df_slct_limit_country['Production_limit_country'][df_slct_limit_country['Energy_type'] == i_energy_type].to_numpy().T
        arr_x = df_slct_limit_country[['Year','Country']][df_slct_limit_country['Energy_type'] == i_energy_type].to_numpy().T

        fig.add_trace(go.Bar(y=arr_y_capacity,
                             x=arr_x,
                             offsetgroup=counter,
                             marker_color='rgb(150,0,0)',
                             showlegend=True if counter == 1 else False,
                             text=i_energy_type,
                             textposition='outside',
                             name='Available'))

        fig.add_trace(go.Bar(y=arr_y_utilized,
                             x=arr_x,
                             offsetgroup=counter,
                             marker_color='rgb(0,0,150)',
                             showlegend=True if counter == 1 else False,
                             name='Utilized'))



    fig.update_layout(
                        boxmode='group'
                        )

    #fig.show()

    return fig