import logging
from importlib import import_module
from os import path

from flask import Flask, url_for
from flask_caching import Cache

# 引入dash应用实例
from redis import StrictRedis

from apps.app_sales_by_real_time import register_real_time_sales_app
from apps.app_sales_bymonth_index import register_sales_app
from apps.app_store_inspection import register_store_inspection_app
from apps.app_self_checking_index import register_self_checking_app
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


class Config(object):
    DEBUG = True
    SECRET_KEY = 'nNYMkDHH+uleYRxSpizW6HEDEp2KfwcggXLW3ikWGE7VmgDWfIC2k271rwejEKDX'  # 设置全局唯一的密钥，主要是为后面的session

    # Redis 的配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # Session保存配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 开启session签名,是否被加密签名
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_PERMANENT = True  # 设置是否过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 设置过期时间，两天

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG

def create_app():
    app = Flask(__name__, static_folder='./apps/base/static', template_folder='./apps/base/templates')
    app.config.from_object(Config)  # 加载配置
    # 注册dash应用实例
    register_sales_app(app)
    register_real_time_sales_app(app)  # 实时销售页面的dash对象的注册
    register_store_inspection_app(app)
    # 自检
    register_self_checking_app(app)
    # # 数据传输
    # register_data_transfe_app(app)
    # 集成插件
    register_extensions(app)
    # 注册 路由
    register_blueprints(app)
    # 注册样式
    apply_themes(app)
    return app

