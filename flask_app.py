from importlib import import_module
from os import path

from flask import Flask, url_for
from flask_caching import Cache

from apps.app_sales_bymonth_index import register_sales_app
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


def apply_themes(app):
    """
    Add support for themes.

    If DEFAULT_THEME is set then all calls to
      url_for('static', filename='')
      will modfify the url to include the theme name

    The theme parameter can be set directly in url_for as well:
      ex. url_for('static', filename='', theme='')

    If the file cannot be found in the /static/<theme>/ location then
      the url will not be modified and the file is expected to be
      in the default /static/ location
    """

    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint.endswith('static'):
            themename = values.get('theme', None) or \
                        app.config.get('DEFAULT_THEME', None)
            if themename:
                theme_file = "{}/{}".format(themename, values.get('filename', ''))
                if path.isfile(path.join(app.static_folder, theme_file)):
                    values['filename'] = theme_file
        return url_for(endpoint, **values)


def create_app():
    app = Flask(__name__, static_folder='base/static')
    register_sales_app(app)
    register_extensions(app)
    register_blueprints(app)

    apply_themes(app)
    return app
