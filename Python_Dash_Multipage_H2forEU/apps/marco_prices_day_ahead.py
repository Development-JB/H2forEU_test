import pathlib
import gdxpds
import pandas as pd


import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from app import app
from apps import marco_settings

# ------------------------------------------------------------------------------
# MARCO Data

# Import gdx pre-load
from apps import marco_load_gdx

# gdx preparation
df_gdx_prices_day_ahead = marco_load_gdx.fct_load_gdx_prices_day_ahead()
df_gdx_prices_historical = marco_load_gdx.fct_load_gdx_prices_historical()
[df_color_code_country,df_color_code_zone] = marco_load_gdx.fct_prepare_color_code()
df_color_code_country = df_color_code_country.set_index(['Country'])
df_color_code_zone = df_color_code_zone.set_index(['Zone'])

# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    #html.H1("Zonal load", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Weeks'),
                    width={'size': 5, 'offset': 1},
                    ),
            dbc.Col(html.H3('Country'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="marco_prices_drop_week",
                                 options=[{'label': i_week, 'value': i_week} for i_week in marco_load_gdx.lst_timestep_week_scn],
                                 multi=True,
                                 value=[marco_load_gdx.lst_timestep_week_scn[0]],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="marco_prices_drop_country",
                                 options=[{'label': i_country, 'value': i_country} for i_country in marco_load_gdx.lst_country],
                                 multi=True,
                                 value=marco_load_gdx.lst_country,
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Checklist(id="marco_prices_check_week",
                                  options=[{'label': 'All', 'value': 'All'}],
                                  value=[]
                                  ),
                    width={'size': 5, 'offset': 1},
                    ),

            dbc.Col(dcc.Checklist(id="marco_prices_check_country",
                                  options=[{'label': 'All', 'value': 'All'}],
                                  value=[]
                                  ),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Graph(id='marco_prices_graph_line',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

# WEEK - checkbox / cropbox correction
@app.callback(
    Output('marco_prices_drop_week', 'value'),
    [Input('marco_prices_check_week', 'value')],
    [State('marco_prices_drop_week', 'options')])
def marco_prices_check_week_click(slct_week_check, options_week):
    if 'All' in slct_week_check:
        return [i['value'] for i in options_week]
    raise PreventUpdate()

@app.callback(
    Output('marco_prices_check_week', 'value'),
    [Input('marco_prices_drop_week', 'value')],
    [State('marco_prices_drop_week', 'options')],
    )
def marco_prices_drop_country_change(slct_week, options_week):
    if len(slct_week) < len(options_week):
        return []
    raise PreventUpdate()


# ZONE - checkbox / cropbox correction
@app.callback(
    Output('marco_prices_drop_country', 'value'),
    [Input('marco_prices_check_country', 'value')],
    [State('marco_prices_drop_country', 'options')])
def marco_prices_check_country_click(slct_country_check, options_country):
    if 'All' in slct_country_check:
        return [i['value'] for i in options_country]
    raise PreventUpdate()

@app.callback(
    Output('marco_prices_check_country', 'value'),
    [Input('marco_prices_drop_country', 'value')],
    [State('marco_prices_drop_country', 'options')],
    )
def marco_prices_drop_country_change(slct_country, options_country):
    if len(slct_country) < len(options_country):
        return []
    raise PreventUpdate()



@app.callback(
    Output(component_id='marco_prices_graph_line', component_property='figure'),
    [Input(component_id='marco_prices_drop_week', component_property='value'),
     Input(component_id='marco_prices_drop_country', component_property='value')]
    )
def update_graph(slct_week, slct_country):

    fig = go.Figure()
    for i_country in slct_country:

        # Day ahead at zonal level
        for i_zone in marco_load_gdx.df_link_country_zone['Zone'][marco_load_gdx.df_link_country_zone['Country'] == i_country]:

            df_slct_da = df_gdx_prices_day_ahead.copy()
            df_slct_da = df_slct_da[df_slct_da['Timestep_week'].isin(slct_week)]
            df_slct_da = df_slct_da[df_slct_da['Zone'] == i_zone]

            fig.add_trace(go.Scatter(
                                x=df_slct_da['Timestep_hour'].drop_duplicates().tolist(),
                                y=df_slct_da['Value'].tolist(),
                                name = i_zone+'_da',
                                showlegend=True,
                                marker_color = df_color_code_zone.loc[i_zone,'Color_code_rgb']
                            ))

        # Historical prices at national level
        df_slct_hist = df_gdx_prices_historical.copy()
        df_slct_hist = df_slct_hist[df_slct_hist['Timestep_week'].isin(slct_week)]
        df_slct_hist = df_slct_hist[df_slct_hist['Country'] == i_country]

        fig.add_trace(go.Scatter(
                        x=df_slct_hist['Timestep_hour'].drop_duplicates().tolist(),
                        y=df_slct_hist['Value'].tolist(),
                        name=i_country+'_hist',
                        showlegend=True,
                        line = dict(color= df_color_code_country.loc[i_country,'Color_code_rgb'], dash = 'dash')
                        # marker_color = df_color_code_country.loc[i_country,'Color_code_rgb'],
                        # marker_s
                    ))


    fig.layout.plot_bgcolor = 'White'
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)

    return fig