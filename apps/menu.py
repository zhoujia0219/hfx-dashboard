import dash_core_components as dcc
import dash_html_components as html
from app import app

###############
# 更新标题
###############
app.title = "门店月度销售分析"
app.update_title = "数据载入中..."


layout = html.Div([
    html.H3('菜单'),
    dcc.Link('月度销售分析', href='/apps/sales_bymonth')
])
