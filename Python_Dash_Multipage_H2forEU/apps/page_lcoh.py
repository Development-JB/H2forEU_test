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
from apps import page_load_data


# ------------------------------------------------------------------------------
# MARCO Data

# Import gdx pre-load
#from apps import marco_load_gdx

# gdx preparation
#df_gdx_load = marco_load_gdx.fct_load_gdx_load()

lst_system = ['PV','Onshore','Hybrid','Best']
lst_electrolyser = ['PEM','Alkaline']
lst_year = [2020,2030,2040]


json_nuts2 = page_load_data.fct_load_json_file()
df_lcoh = page_load_data.fct_load_lcoh_result()

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
            dbc.Col(dcc.Dropdown(id="page_lcoh_drop_system",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_system],
                                 multi=False,
                                 value=lst_system[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 1},
                    ),

            dbc.Col(dcc.Dropdown(id="page_lcoh_drop_electrolyser",
                                 options=[{'label': i_lst, 'value': i_lst} for i_lst in lst_electrolyser],
                                 multi=False,
                                 value=lst_electrolyser[0],
                                 style={'width': "100%"}
                                 ),
                    width={'size': 4, 'offset': 2},
                    ),
            ]),

    dbc.Row([
            dbc.Col(html.H2('Year'),
                    width={'size': 5, 'offset': 1},
                    ),
            ]),

    dbc.Row([
            dbc.Col(dcc.Slider(
                                id='page_lcoh_slider_year',
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
            dbc.Col(dcc.Graph(id='page_lcoh_graph_line',
                              figure={}
                              ),
                    width={'size': True, 'offset': 0}
                    ),
            ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components




@app.callback(
    Output(component_id='page_lcoh_graph_line', component_property='figure'),
    [Input(component_id='page_lcoh_drop_system', component_property='value'),
     Input(component_id='page_lcoh_drop_electrolyser', component_property='value'),
     Input(component_id='page_lcoh_slider_year', component_property='value')],
)
def page_lcoh_update_graph(slct_system, slct_electrolyser, slct_year):

    #print(slct_system)
    #print(slct_electrolyser)
    #print(slct_year)

    df_slct = df_lcoh.copy()

    min_lcoh = df_lcoh['LCOH'].min()
    max_lcoh = 11 #df_lcoh['LCOH'].max()

    df_slct = df_slct[df_slct['Year'] == slct_year]
    if slct_system == 'Best':
        df_slct = df_slct.sort_values(['NUTS_ID','LCOH']).drop_duplicates(['NUTS_ID'], keep='first')
    else:
        df_slct = df_slct[df_slct['System'] == slct_system]
        df_slct = df_slct[df_slct['Electrolyser'] == slct_electrolyser]

    fig = px.choropleth(df_slct, locations='NUTS_ID', geojson=json_nuts2, color='LCOH', range_color =[min_lcoh,max_lcoh])
    fig.update_geos(fitbounds='locations', visible=False)
    #fig.show()

    return fig