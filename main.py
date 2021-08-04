from werkzeug.serving import run_simple

import routers

# 启动 WSGI Web 服务器
run_simple(
    hostname='0.0.0.0',
    port=8080,
    application=routers.app,
    use_reloader=True,
    use_debugger=True,
    threaded=True
)
