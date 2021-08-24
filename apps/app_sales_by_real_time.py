import dash
from flask_login import login_required

from apps.html_string.base_html_string_real_time import base_html_string_real_time
from conf.hfx_dashboard import BOOTSTRAP_THEME
from conf.router_conts import URL_REAL_TIME_SALE


def register_real_time_sales_app(app):
    from apps.layouts.app_sales_by_real_time_layouts import layout
    from apps.callbacks.app_sales_by_real_time_callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
    import dash_html_components as html

    dash_app = dash.Dash(__name__,
                         server=app,
                         update_title="数据载入中...",
                         suppress_callback_exceptions=True,
                         url_base_pathname=URL_REAL_TIME_SALE,
                         meta_tags=[meta_viewport],
                         external_stylesheets=[BOOTSTRAP_THEME],
                         index_string=base_html_string_real_time  # todo
                         )

    with app.app_context():
        dash_app.title = '门店实时销售分析'
        dash_app.layout = layout
        register_callbacks(dash_app)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
