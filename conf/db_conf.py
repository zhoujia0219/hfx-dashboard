###############
# Greenplum 配置
###############
HOST = "192.168.1.174"
PORT = "5432"
USERNAME = "gpadmin"
PASSWORD = "gpadmin"
POOL_MIN_CONN = 10
POOL_MAX_CONN = 200

###############
# Redis 配置
###############
# url
REDIS_URL = "redis://192.168.2.182:6379"
# 缓存过期时间
REDIS_CACHE_DEFAULT_TIMEOUT = 5*60
