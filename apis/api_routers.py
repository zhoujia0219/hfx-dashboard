import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from apps.menu import menu_app
from apps.sales_bymonth import sales_app
from conts import router_conts
from core.flask_app import flask_server


@flask_server.route('/')
def hello():
    return flask.redirect(router_conts.SALES_BY_MONTH)


@flask_server.route(router_conts.MENUS)
def render_reports():
    return flask.redirect('/dash1')


# 将dash应用绑定到flask
app = DispatcherMiddleware(flask_server, {
    '/dash1': menu_app.server,
    '/dash2': sales_app.server
})
