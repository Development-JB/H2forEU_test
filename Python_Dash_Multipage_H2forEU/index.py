
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Connect to main app.py file
from app import app

lst_dashboards = [
                    'page_lcoh',
                    'page_system',
                    'marco_dummy'
                   ]

# Connect to your app pages
for i_dashboards in lst_dashboards:
    print(i_dashboards)
    exec ('from apps import %s ' % (i_dashboards))


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    dbc.Nav([
                dbc.NavItem(dbc.NavLink('LCOH', href='/apps/page_lcoh')),
                dbc.NavItem(dbc.NavLink('RES system', href='/apps/page_system')),
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
   else:
       return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)
