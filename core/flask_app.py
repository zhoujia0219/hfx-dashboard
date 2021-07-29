import flask
from flask_caching import Cache

from conf import config

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
    'CACHE_REDIS_URL': config.REDIS_URL,
    'CACHE_DEFAULT_TIMEOUT': config.REDIS_CACHE_DEFAULT_TIMEOUT
}
cache.init_app(flask_server, config=CACHE_CONFIG)
