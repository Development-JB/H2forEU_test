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
from apps import marco_settings
from apps import marco_load_gdx

# gdx preparation
df_generation_day_ahead = marco_load_gdx.fct_load_gdx_generation_day_ahead()
df_generation_historical = marco_load_gdx.fct_load_gdx_generation_historical()


# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    html.H1("Gneration Day Ahead - Country", style={'text-align': 'left'}),

    dbc.Row([
            dbc.Col(html.H2('Weeks'),
                    width={'size': 2, 'offset': 1},
                    ),
            dbc.Col(html.H3('Country'),
                    width={'size': 1, 'offset': 1},
                    ),
            dbc.Col(html.H3('Energy_type'),
                    width={'size': 6, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Dropdown(id="marco_generation_day_ahead_drop_week",
                                 options=[{'label': i_week, 'value': i_week} for i_week in marco_load_gdx.lst_timestep_week_scn],
                                 multi=True,
                                 value=[marco_load_gdx.lst_timestep_week_scn[0]],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 2, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="marco_generation_day_ahead_drop_country",
                                 options=[{'label': i_country, 'value': i_country} for i_country in marco_load_gdx.lst_country],
                                 multi=False,
                                 value='DE',
                                 style={'width': "100%"}
                                 ),
                    width={'size': 1, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="marco_generation_day_ahead_drop_energy_type",
                                 options=[{'label': i_energy_type, 'value': i_energy_type} for i_energy_type in marco_load_gdx.lst_energy_type],
                                 multi=True,
                                 value=marco_load_gdx.lst_energy_type,
                                 style={'width': "100%"}
                                 ),
                    width={'size': 6, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Checklist(id="marco_generation_day_ahead_check_week",
                                  options=[{'label': 'All', 'value': 'All'}],
                                  value=[]
                                  ),
                    width={'size': 2, 'offset': 1},
                    ),

            # dbc.Col(dcc.Checklist(id="marco_generation_day_ahead_check_country",
            #                       options=[{'label': 'All', 'value': 'All'}],
            #                       value=[]
            #                       ),
            #         width={'size': 3, 'offset': 1},
            #         ),

            dbc.Col(dcc.Checklist(id="marco_generation_day_ahead_check_energy_type",
                                  options=[{'label': 'All', 'value': 'All'}],
                                  value=[]
                                  ),
                    width={'size': 1, 'offset': 3},
                    ),

            dbc.Col(dcc.Checklist(id="marco_generation_day_ahead_check_energy_type_no",
                                  options=[{'label': 'No', 'value': 'No'}],
                                  value=[]
                                  ),
                    width={'size': 1, 'offset': 0},
                    ),
            ]),

    dbc.Row([
            dbc.Col(html.H2('Marco - Day Ahead'),
                    width={'size': 'auto', 'offset': 0},
                    ),
            ]),
    dbc.Row([
            dbc.Col(dcc.Graph(id='marco_generation_day_ahead_graph_line',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

    dbc.Row([
            dbc.Col(html.H2('Historical'),
                    width={'size': 'auto', 'offset': 0},
                    ),
            ]),
    dbc.Row([
            dbc.Col(dcc.Graph(id='marco_generation_day_ahead_graph_line2',
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
    Output('marco_generation_day_ahead_drop_week', 'value'),
    [Input('marco_generation_day_ahead_check_week', 'value')],
    [State('marco_generation_day_ahead_drop_week', 'options')])
def marco_load_check_week_click(slct_week_check, options_week):
    if 'All' in slct_week_check:
        return [i['value'] for i in options_week]
    raise PreventUpdate()

@app.callback(
    Output('marco_generation_day_ahead_check_week', 'value'),
    [Input('marco_generation_day_ahead_drop_week', 'value')],
    [State('marco_generation_day_ahead_drop_week', 'options')],
    )
def marco_generation_day_ahead_drop_week_change(slct_week, options_week):
    if len(slct_week) < len(options_week):
        return []
    raise PreventUpdate()


# Country - checkbox / cropbox correction
# @app.callback(
#     Output('marco_generation_day_ahead_drop_country', 'value'),
#     [Input('marco_generation_day_ahead_check_country', 'value')],
#     [State('marco_generation_day_ahead_drop_country', 'options')])
# def marco_generation_day_ahead_check_country_click(slct_country_check, options_country):
#     if 'All' in slct_country_check:
#         return [i['value'] for i in options_country]
#     raise PreventUpdate()
#
# @app.callback(
#     Output('marco_generation_day_ahead_check_country', 'value'),
#     [Input('marco_generation_day_ahead_drop_country', 'value')],
#     [State('marco_generation_day_ahead_drop_country', 'options')],
#     )
# def marco_generation_day_ahead_drop_country_change(slct_country, options_country):
#     if len(slct_country) < len(options_country):
#         return []
#     raise PreventUpdate()



# Energy Type - checkbox / dropbox correction
# @app.callback(
#     [Output('marco_generation_day_ahead_drop_energy_type', 'value'),
#     Output('marco_generation_day_ahead_check_energy_type_no', 'value')],
#     [Input('marco_generation_day_ahead_check_energy_type', 'value')],
#     [State('marco_generation_day_ahead_drop_energy_type', 'options')]
#     )
# def marco_generation_day_ahead_check_energy_type_click(slct_energy_type_check, options_energy_type):
#     if 'All' in slct_energy_type_check:
#         return [i['value'] for i in options_energy_type],[]
#     raise PreventUpdate()\

# @app.callback(
#     Output('marco_generation_day_ahead_drop_energy_type', 'value'),
# #     Output('marco_generation_day_ahead_check_energy_type_no', 'value')],
#     [Input('marco_generation_day_ahead_check_energy_type', 'value')],
#     [State('marco_generation_day_ahead_drop_energy_type', 'options')]
#     )
# def test1(slct_energy_type_check, options_energy_type):
#     if 'All' in slct_energy_type_check:
#         return [i['value'] for i in options_energy_type]#,[]
#     raise PreventUpdate()


# @app.callback(
#     [Output('marco_generation_day_ahead_drop_energy_type', 'value'),
#      Output('marco_generation_day_ahead_check_energy_type', 'value')],
#     [Input('marco_generation_day_ahead_check_energy_type_no', 'value')]
#     )
# def marco_generation_day_ahead_check_energy_type_click_no(slct_energy_type_check_no):
#     if 'No' in slct_energy_type_check_no:
#         return [],[]
#     raise PreventUpdate()\

@app.callback(
    Output('marco_generation_day_ahead_drop_energy_type', 'value'),
#     Output('marco_generation_day_ahead_check_energy_type', 'value')],
    [Input('marco_generation_day_ahead_check_energy_type_no', 'value')]
    )
def test2(slct_energy_type_check_no):
    if 'No' in slct_energy_type_check_no:
        return []#,[]
    raise PreventUpdate()


@app.callback(
    [Output('marco_generation_day_ahead_check_energy_type', 'value'),
     Output('marco_generation_day_ahead_check_energy_type_no', 'value')],
    [Input('marco_generation_day_ahead_drop_energy_type', 'value')],
    [State('marco_generation_day_ahead_drop_energy_type', 'options')]
    )
def marco_generation_day_ahead_drop_energy_type_change(slct_energy_type, options_energy_type):
    if (len(slct_energy_type) < len(options_energy_type)) & (len(slct_energy_type)>0):
        return [],[]
    elif (len(slct_energy_type)==0):
        return [],['No']
    elif (len(slct_energy_type) == len(options_energy_type)):
        return ['All'], []

    raise PreventUpdate()



@app.callback(

    [Output(component_id='marco_generation_day_ahead_graph_line', component_property='figure'),
     Output(component_id='marco_generation_day_ahead_graph_line2', component_property='figure')],
    [Input(component_id='marco_generation_day_ahead_drop_week', component_property='value'),
     Input(component_id='marco_generation_day_ahead_drop_country', component_property='value'),
     Input(component_id='marco_generation_day_ahead_drop_energy_type', component_property='value')],
    [State(component_id='marco_generation_day_ahead_drop_week', component_property='value'),
     State(component_id='marco_generation_day_ahead_drop_country', component_property='value'),
     State(component_id='marco_generation_day_ahead_drop_energy_type', component_property='value')]
)
def update_graph(slct_week, slct_country, slct_energy_type, state_week, state_country, state_energy_type):

    # slct_week = ['01']
    # slct_country = 'DE'
    # slct_energy_type = ['Natural_gas']

    df_slct_da = df_generation_day_ahead.copy()
    df_slct_da = df_slct_da[df_slct_da['Timestep_week'].isin(slct_week)]
    df_slct_da = df_slct_da[df_slct_da['Country'] == slct_country]
    df_slct_da = df_slct_da[df_slct_da['Energy_type'].isin(slct_energy_type)]

    df_max_da = df_slct_da.groupby(['Timestep_hour']).sum()
    max_da = df_max_da['Value'].max()

    df_slct_hist = df_generation_historical.copy()
    df_slct_hist = df_slct_hist[df_slct_hist['Mode'] == 'Generation']
    df_slct_hist = df_slct_hist[df_slct_hist['Timestep_week'].isin(slct_week)]
    df_slct_hist = df_slct_hist[df_slct_hist['Country'] == slct_country]
    df_slct_hist = df_slct_hist[df_slct_hist['Energy_type'].isin(slct_energy_type)]

    df_max_hist = df_slct_hist.groupby(['Timestep_hour']).sum()
    max_hist = df_max_hist['Value'].max()

    max_y = max(max_da,max_hist)*1.1

    # Graphs
    # Day ahead
    fig_da = px.area(df_slct_da, x="Timestep_hour", y="Value", color="Energy_type", line_group="Plant_key", color_discrete_map=marco_settings.dict_energy_type_color)
    fig_da.update_layout(yaxis_range=(0,max_y))
    fig_da.layout.plot_bgcolor = 'White'
    fig_da.update_xaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)
    fig_da.update_yaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)
    # Historical
    fig_hist = px.area(df_slct_hist, x="Timestep_hour", y="Value", color="Energy_type", line_group="Energy_type", color_discrete_map=marco_settings.dict_energy_type_color)
    fig_hist.update_layout(yaxis_range=(0,max_y))
    fig_hist.layout.plot_bgcolor = 'White'
    fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)
    fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor=marco_settings.var_grid_line)

    return fig_da, fig_hist