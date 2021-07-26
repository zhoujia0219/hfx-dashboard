import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
from app import flask_server
from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from apps.menu import dash_app as menu_app
from apps.sales_bymonth import dash_app as sales_app


@flask_server.route('/')
@flask_server.route('/hello')
def hello():
    return 'hello world!'


@flask_server.route('/sales/')
def render_dashboard():
    return flask.redirect('/dash1')


@flask_server.route('/menus/')
def render_reports():
    return flask.redirect('/dash2')


app = DispatcherMiddleware(flask_server, {
    '/dash1': menu_app.server,
    '/dash2': sales_app.server
})

run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content')
# ])


# @app.callback(Output('page-content', 'children'),
#               Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/apps/sales_bymonth':
#         return sales_bymonth.layout
#     elif pathname == '/apps/menu':
#         return menu.layout
#     else:
#         return menu.layout

#
# if __name__ == '__main__':
#     app.run_server(port=8056, debug=True, dev_tools_hot_reload=True)
