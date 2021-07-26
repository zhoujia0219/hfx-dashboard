
import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
from conf import db_conf

app = dash.Dash(__name__,
                update_title="数据载入中...",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.PULSE])
server = app.server

#########################
# 缓存
#########################

cache = Cache()
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': db_conf.REDIS_URL,
    'CACHE_DEFAULT_TIMEOUT': db_conf.REDIS_CACHE_DEFAULT_TIMEOUT
}
cache.init_app(server, config=CACHE_CONFIG)

