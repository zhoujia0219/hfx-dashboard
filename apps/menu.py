import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from conts import router_conts
from core.flask_app import flask_server

###############
# dash
###############
menu_app = dash.Dash(__name__,
                     server=flask_server,
                     title="菜单",
                     update_title="数据载入中...",
                     suppress_callback_exceptions=True,
                     url_base_pathname=router_conts.MENUS,
                     external_stylesheets=[dbc.themes.PULSE])

menu_app.layout = html.Div([
    html.H3('菜单'),
    dcc.Link('月度销售分析', href='/sales/')
])
