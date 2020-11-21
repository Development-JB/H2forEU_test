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

lst_color = ['Region_export','Region_import','H2_color','Transport_international','Transport_national']
lst_year = [2020,2030,2040,2050]

df_data = load_data.fct_load_results_supply()

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

    #slct_year = 2020
    #slct_color = 'Region_export'

    df_slct = df_data.copy()
    df_slct = df_slct[df_slct['Year']==slct_year]

    if slct_color == 'H2_color':
        df_color_h2 = pd.DataFrame([['Hybrid', 'rgb(0,200,0)'],
                                    ['PV', 'rgb(0,200,0)'],
                                    ['Onshore', 'rgb(0,200,0)'],
                                    ['Biomass', 'rgb(0,100,0)'],
                                    ['Gas', 'rgb(0,0,150)']],
                                    columns=['Source', 'Rgb_code'])
        df_slct = pd.merge(df_slct,df_color_h2, how='left', on=['Source'])
        df_slct = df_slct.rename(columns={'Source':'Category'})

    elif slct_color == 'Region_export':
        df_color_region_export = pd.DataFrame([['North_africa', 'rgb(150,0,0)'],
                                               ['Middle_east', 'rgb(0,150,0)'],
                                               ['Russia', 'rgb(0,0,150)']],
                                               columns=['Region_export', 'Rgb_code'])
        df_slct = pd.merge(df_slct, df_color_region_export, how='left', on=['Region_export'])
        df_slct = df_slct.rename(columns={'Region_export':'Category'})

    elif slct_color == 'Region_import':
        df_color_region_import = pd.DataFrame([['Southern_europe', 'rgb(150,0,0)'],
                                               ['Southestern_europe', 'rgb(150,50,0)'],
                                               ['Central_europe', 'rgb(0,150,0)'],
                                               ['Eastern_europe', 'rgb(0,150,150)'],
                                               ['Northern_europe', 'rgb(0,0,150)']],
                                               columns=['Region_import', 'Rgb_code'])
        df_slct = pd.merge(df_slct, df_color_region_import, how='left', on=['Region_import'])
        df_slct = df_slct.rename(columns={'Region_import':'Category'})

    elif slct_color == 'Transport_national':
        df_color_transport_national = pd.DataFrame([['Road_NH3', 'rgb(0,200,0)'],
                                                    ['Road_LH2', 'rgb(0,0,150)']],
                                                     columns=['Transport_national', 'Rgb_code'])
        df_slct = pd.merge(df_slct, df_color_transport_national, how='left', on=['Transport_national'])
        df_slct = df_slct.rename(columns={'Transport_national':'Category'})

    elif slct_color == 'Transport_international':
        df_color_transport_international = pd.DataFrame([['Pipeline', 'rgb(0,150,0)'],
                                                         ['Maritime_ammonia', 'rgb(150,0,0)'],
                                                         ['LH2', 'rgb(0,0,150)']],
                                                         columns=['Transport_international', 'Rgb_code'])
        df_slct = pd.merge(df_slct, df_color_transport_international, how='left', on=['Transport_international'])
        df_slct = df_slct.rename(columns={'Transport_international':'Category'})



    df_slct = df_slct[['Category','Volume','Lcoh_cif','Rgb_code']].sort_values(['Lcoh_cif'])

    fig = go.Figure()

    df_trigger_legend = pd.DataFrame([])
    df_trigger_legend['Rgb_code'] = df_slct['Rgb_code'].drop_duplicates(keep='first').tolist()
    df_trigger_legend['Trigger'] = 0
    df_trigger_legend = df_trigger_legend.set_index(['Rgb_code'])

    x_start = 0
    for i_entry in df_slct.index:

        x_end = x_start+df_slct.loc[i_entry,'Volume']

        fig.add_trace(go.Scatter(x=[x_start,x_end],
                                 y=[df_slct.loc[i_entry,'Lcoh_cif'],df_slct.loc[i_entry,'Lcoh_cif']],
                                 fill='tozeroy',
                                 fillcolor=df_slct.loc[i_entry,'Rgb_code'],
                                 mode = 'lines',
                                 line = dict(color=df_slct.loc[i_entry,'Rgb_code']),
                                 showlegend = True if df_trigger_legend.loc[df_slct.loc[i_entry,'Rgb_code'],'Trigger'] == 0 else False,
                                 name=df_slct.loc[i_entry, 'Category']
                                 ))
        x_start = x_end

        df_trigger_legend.loc[df_slct.loc[i_entry,'Rgb_code'], 'Trigger'] = 1

    fig.update_layout(xaxis=dict(range=[0,30000]),
                      yaxis=dict(range=[0,30]),
                      height=400,
                      width=1200,
                      legend=dict(x=0.01,
                                  y=0.99,
                                  xanchor='left',
                                  yanchor='top')
                      )

    #fig.show()

    return fig