import dash
from flask_login import login_required

from conf.hfx_dashboard import BOOTSTRAP_THEME
from conf.router_conts import URL_SALES_BYMONTH
from apps.html_string.base_html_string_index import base_html_string_index


def register_sales_app(app):
    from apps.layouts.app_sales_bymonth_layout import layout
    from apps.callbacks.app_sales_by_month_callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                         server=app,
                         update_title="数据载入中...",
                         suppress_callback_exceptions=True,
                         # assets_url_path="assets",
                         url_base_pathname=URL_SALES_BYMONTH,
                         meta_tags=[meta_viewport],
                         external_stylesheets=[BOOTSTRAP_THEME],
                         index_string=base_html_string_index  # todo
                         )

    with app.app_context():
        dash_app.title = '门店月度销售分析'
        dash_app.layout = layout
        # dash_app.layout = html.Div(
        #     children=[
        #         html.H6(children="总销售额1", style={"color": "red", "whiteSpace": "pre"}),
        #
        #     ]
        # )
        register_callbacks(dash_app)
    # _protect_dash_views(dash_app)

def _protect_dash_views(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.url_base_pathname):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
