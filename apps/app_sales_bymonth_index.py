import dash

from conf.hfx_dashboard import BOOTSTRAP_THEME
from conf.router_conts import URL_SALES_BYMONTH


def register_dash_app(app):
    from apps.layouts.app_sales_bymonth_layout import layout
    from apps.callbacks.app_sales_by_month_callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dash_app = dash.Dash(__name__,
                         server=app,
                         title="门店月度销售分析",
                         update_title="数据载入中...",
                         suppress_callback_exceptions=True,
                         url_base_pathname=URL_SALES_BYMONTH,
                         meta_tags=[meta_viewport],
                         external_stylesheets=[BOOTSTRAP_THEME])

    with app.app_context():
        dash_app.title = 'Dash Example'
        dash_app.layout = layout
        register_callbacks(dash_app)
