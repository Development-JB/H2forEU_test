
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to main app.py file
from app import app

lst_dashboards = [
                    'page_lcoh',
                    'page_system',
                    'page_res_profiles',
                    'page_map_source_results',
                    'page_merit_curve',
                    'marco_dummy'
                   ]

# Connect to your app pages
for i_dashboards in lst_dashboards:
    print(i_dashboards)
    exec ('from apps import %s ' % (i_dashboards))


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dbc.Nav([
                dbc.NavItem(dbc.NavLink('Map LCOH', href='/apps/page_lcoh')),
                dbc.NavItem(dbc.NavLink('Map RES system', href='/apps/page_system')),
                dbc.NavItem(dbc.NavLink('Map RES profiles', href='/apps/page_res_profiles')),
                dbc.NavItem(dbc.NavLink('Map source results', href='/apps/page_map_source_results')),
                dbc.NavItem(dbc.NavLink('Merit curve', href='/apps/page_merit_curve')),
            ]),

    html.Div(id='page-content', children=[]),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page\
                (pathname):

   if ('marco_load' in lst_dashboards) and (pathname == '/apps/marco_load'):
       return marco_load.layout
   elif ('page_lcoh' in lst_dashboards) and (pathname == '/apps/page_lcoh'):
       return page_lcoh.layout
   elif ('page_system' in lst_dashboards) and (pathname == '/apps/page_system'):
       return page_system.layout
   elif ('page_res_profiles' in lst_dashboards) and (pathname == '/apps/page_res_profiles'):
       return page_res_profiles.layout
   elif ('page_map_source_results' in lst_dashboards) and (pathname == '/apps/page_map_source_results'):
       return page_map_source_results.layout
   elif ('page_merit_curve' in lst_dashboards) and (pathname == '/apps/page_merit_curve'):
       return page_merit_curve.layout
   else:
       return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
