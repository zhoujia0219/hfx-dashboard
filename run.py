import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import sales_bymonth, menu

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/sales_bymonth':
        return sales_bymonth.layout
    elif pathname == '/apps/menu':
        return menu.layout
    else:
        return menu.layout


if __name__ == '__main__':
    app.run_server(port=8056, debug=True, dev_tools_hot_reload=True)
