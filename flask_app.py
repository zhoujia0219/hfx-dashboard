import flask
from flask_caching import Cache

from conf import hfx_dashboard

#########################
# flask
#########################
flask_server = flask.Flask(__name__)

#########################
# 缓存
#########################

cache = Cache()
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': hfx_dashboard.REDIS_URL,
    'CACHE_DEFAULT_TIMEOUT': hfx_dashboard.REDIS_CACHE_DEFAULT_TIMEOUT
}
cache.init_app(flask_server, config=CACHE_CONFIG)
