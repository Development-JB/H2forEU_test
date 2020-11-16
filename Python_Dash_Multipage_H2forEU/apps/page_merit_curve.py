import pathlib
import gdxpds
import pandas as pd


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import page_load_data
import plotly.graph_objects as go


# ------------------------------------------------------------------------------
# Load data

lst_color = ['Region_export','Region_import','H2_color']
lst_year = [2030,2040,2050]

df_data = page_load_data.fct_load_results_supply()

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
                                id='page_merit_curve_slider_year',
                                min=lst_year[0],
                                max=lst_year[-1],
                                step=10,
                                value=lst_year[0],
                                marks=dict(zip(lst_year, lst_year)),
                                ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_merit_curve_drop_selection",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_color],
                                 multi=False,
                                 value=lst_color[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='page_merit_curve_graph',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    Output(component_id='page_merit_curve_graph', component_property='figure'),
    [Input(component_id='page_merit_curve_drop_selection', component_property='value'),
     Input(component_id='page_merit_curve_slider_year', component_property='value')],
)
def page_merit_curve_update_graph(slct_color, slct_year):

    #print(slct_color)
    #print(slct_year)

    slct_year = 2020
    slct_color = 'H2_color'

    df_slct = df_data.copy()
    df_slct = df_slct[df_slct['Year']==slct_year]

    df_color_region = pd.DataFrame([['North_africa','rgb(150,0,0)'],
                                    ['Middle_east','rgb(0,150,0)'],
                                    ['Russia','rgb(0,0,150)']], columns=['Region','Color'])

    df_color_h2 = pd.DataFrame([['Hybrid','rgb(0,200,0)'],
                                ['PV', 'rgb(0,200,0)'],
                                ['Onshore', 'rgb(0,200,0)'],
                                ['Biomass', 'rgb(0,100,0)'],
                                ['Gas','rgb(0,0,150)']], columns=['Source','Rgb_code'])

    if slct_color == 'H2_color':
        print('yes')
        df_slct = pd.merge(df_slct,df_color_h2, how='left', on=['Source'])


    df_slct = df_slct[['Volume','Lcoh_cif','Rgb_code']].sort_values(['Lcoh_cif'])

    fig = go.Figure()

    x_start = 0
    for i_entry in df_slct.index:


        x_end = x_start+df_slct.loc[i_entry,'Volume']

        fig.add_trace(go.Scatter(x=[x_start,x_end],
                                 y=[df_slct.loc[i_entry,'Lcoh_cif'],df_slct.loc[i_entry,'Lcoh_cif']],
                                 fill='tozeroy',
                                 fillcolor=df_slct.loc[i_entry,'Rgb_code'],
                                 mode = 'lines',
                                 line = dict(color=df_slct.loc[i_entry,'Rgb_code']),
                                 showlegend=False
                                 ))

        x_start = x_end

    #fig.show()

    return fig