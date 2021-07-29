from werkzeug.serving import run_simple

from apis import api_routers

run_simple('0.0.0.0', 8080, api_routers.app, use_reloader=True, use_debugger=True)
