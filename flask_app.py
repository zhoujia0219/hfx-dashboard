from importlib import import_module

from flask import Flask
from flask_caching import Cache

from apps.app_sales_bymonth_index import register_dash_app
from conf import hfx_dashboard

# #########################
# # 缓存
# #########################
cache = Cache()
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': hfx_dashboard.REDIS_URL,
    'CACHE_DEFAULT_TIMEOUT': hfx_dashboard.REDIS_CACHE_DEFAULT_TIMEOUT
}


def register_extensions(app):
    cache.init_app(app, config=CACHE_CONFIG)


def register_blueprints(app):
    module = import_module('apps.{}.routers'.format("base"))
    app.register_blueprint(module.blueprint)


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='base/static')
    app.config.from_object(config)
    if selenium:
        app.config['LOGIN_DISABLED'] = True

    register_dash_app(app)
    register_extensions(app)
    register_blueprints(app)

    return app
