import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import flask_server

###############
# dash
###############
dash_app = dash.Dash(__name__,
                     server=flask_server,
                     title="门店月度销售分析",
                     update_title="数据载入中...",
                     suppress_callback_exceptions=True,
                     url_base_pathname='/menus/',
                     external_stylesheets=[dbc.themes.PULSE])

dash_app.layout = html.Div([
    html.H3('菜单'),
    dcc.Link('月度销售分析', href='/sales')
])
