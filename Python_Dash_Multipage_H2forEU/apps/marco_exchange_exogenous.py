import pathlib
import gdxpds
import pandas as pd



import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app

# ------------------------------------------------------------------------------
# MARCO Data

# Import gdx pre-load
from apps import marco_load_gdx

# gdx preparation
df_gdx_exchange_exogenous = marco_load_gdx.fct_load_gdx_exchange_exogenous()


# ------------------------------------------------------------------------------
# App layout
layout = html.Div([

    html.H1("Zonal load", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_marco_exchange_exo_zone",
                 options=[
                     {"label": "DE_North1", "value": "DE_North1"},
                     {"label": "DE_South", "value": "DE_South"},
                     {"label": "AT", "value": "AT"}],
                 multi=True,
                 value=["DE_South"],
                 style={'width': "40%"}
                 ),

    dcc.Graph(id='marco_exchange_exo_graph_line', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='marco_exchange_exo_graph_line', component_property='figure'),
    [Input(component_id='slct_marco_exchange_exo_zone', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    #container = "The chosen zones are: {}".format(option_slctd)

    df_slct = df_gdx_exchange_exogenous.copy()
    df_slct = df_slct[df_slct['Zone'].isin(option_slctd)]
    df_slct = df_slct[df_slct['Mode'] == 'Export']

    fig = px.line(
        data_frame=df_slct,
        x='Timestep_hour',
        y='Value'
    )

    return fig