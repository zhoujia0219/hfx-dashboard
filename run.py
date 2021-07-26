import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app import flask_server
from apps.menu import dash_app as menu_app
from apps.sales_bymonth import dash_app as sales_app


@flask_server.route('/')
def hello():
    return flask.redirect('/sales')


@flask_server.route('/menus/')
def render_reports():
    return flask.redirect('/dash2')


app = DispatcherMiddleware(flask_server, {
    '/dash1': menu_app.server,
    '/dash2': sales_app.server
})

run_simple('0.0.0.0', 8080, app, use_reloader=True, use_debugger=True)
