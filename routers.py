import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from apps.app_sales_bymonth import sales_app
from conf.router_conts import URL_SALES_BYMONTH
from flask_app import flask_server


@flask_server.route('/')
def dev_debug():
    """
    仅用于测试
    """
    return flask.redirect(URL_SALES_BYMONTH)


# 将dash应用绑定到flask
app = DispatcherMiddleware(flask_server, {
    '/sales_bymonth': sales_app.server
})
