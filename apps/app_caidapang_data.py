import dash
from flask_login import login_required

from apps.html_string.base_html_string_index import base_html_string_index
from conf.hfx_dashboard import BOOTSTRAP_THEME
from conf.router_conts import URL_CAIDAPANG_DATA


def register_caidapang_data_app(app):
    from apps.layouts.app_caidapang_data_layout import layout
    # from apps.callbacks.app_common_checking_callbacks import register_callbacks
    import dash_html_components as html
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                         server=app,
                         update_title="数据载入中...",
                         suppress_callback_exceptions=True,
                         url_base_pathname=URL_CAIDAPANG_DATA,
                         meta_tags=[meta_viewport],
                         external_stylesheets=[BOOTSTRAP_THEME],
                         index_string=base_html_string_index  # todo
                         )

    with app.app_context():
        dash_app.title = '门店数据模型'
        dash_app.layout = layout
        # register_callbacks(dash_app)


def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
