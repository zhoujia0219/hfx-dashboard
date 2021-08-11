from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dateutil.relativedelta import relativedelta

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from services import srv_comm_dim
from utils import date_util

###############
# 页面筛选初始值
###############
# 当前年月日
today = datetime.now()
# 格式化现在的月份
now_month = today.strftime("%Y-%m")
# 日期区间
date_range = date_util.get_date_list("2020-01", now_month)
# 默认开始日期 当前日期减去1年份取月份
start_month = (today - relativedelta(years=1)).strftime('%Y-%m')
# 默认结束日期  当前日期减去1月 取月份
stop_month = (today - relativedelta(months=1)).strftime('%Y-%m')

# 渠道信息获取
channels = srv_comm_dim.get_dim_channel()
default_channel_values = [r["value"] for r in channels]
# 门店级别定义
city_levels = srv_comm_dim.get_dim_city_levels()
default_city_values = [r["value"] for r in city_levels]
# 店龄
store_ages = srv_comm_dim.get_dim_store_ages()
default_age_values = [r["value"] for r in store_ages]
# 门店面积
store_areas = srv_comm_dim.get_dim_store_areas()
default_area_values = [r["value"] for r in store_areas]
# 门店星级
store_stars = srv_comm_dim.get_dim_store_star()
default_star_values = [r["value"] for r in store_stars]


###############
# 图形维度初始值
###############
# 排序类型
order_types = srv_comm_dim.get_dim_order_type()
# 分类维度
dim_cates = srv_comm_dim.get_dim_graph_cate()
# 图形类型维度
dim_types = srv_comm_dim.get_dim_graph_type()
# 聚合函数维度
dim_aggs = srv_comm_dim.get_dim_graph_agg()



###############
# sidebar
###############

# 侧边栏
sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4("门店月度销售分析"),
        html.Hr(),
        html.P("可通过条件筛选过滤数据，也可以改变维度和图形样式", className="small", style={'color': 'gray'}),
        html.Div([
            filter_date_range.filter_month_range(date_range, start_month, stop_month),
            filter_city_level.filter_city_level("门店所属城市", city_levels, default_city_values),
            filter_channels.filter_channels("销售渠道", channels, default_channel_values),
            filter_store_age.filter_store_age("店龄", store_ages, default_age_values),
            filter_store_area.filter_store_area("门店面积", store_areas, default_area_values),
            filter_store_star.filter_store_star("门店星级", store_stars, default_star_values),
            dbc.Button('重新计算', id='f_submit', color="primary", className="mt-3", block=True),
        ]),
    ],
)

###############
# content
###############
card_list = [
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("总销售额"),
        html.H4(children=[html.Span('￥'),
                          html.Span(children=['0.00'], id='total_sales'),
                          html.Span('M')],
                id='total_sale_title',
                style={"color": "darkred"}),
        html.Label(children=[html.Span(children=[start_month], id="total_sales_start_month"),
                             " - ",
                             html.Span(children=[stop_month], id="total_sales_stop_month"), ],
                   id="total_sale_label"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("上月销售额"),
        html.H4(children=[html.Span('￥'),
                          html.Span(children=['0.00'], id='last_month_sales'),
                          html.Span('M')],
                id='last_month_title',
                style={"color": "darkred"}),
        html.Label(children=["同比: ",
                             html.Span(children=['0.00%'], id="last_month_tb"),
                             "  环比： ",
                             html.Span(children=['0.00%'], id="last_month_hb")],
                   id="last_month_label"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6(["本月销售额", "(", html.Span(children=[stop_month], id="current_month_sign"), ")"]),

        html.H4(children=[html.Span('￥'),
                          html.Span(children=['0.00'],
                                    id="current_month_sales"),
                          html.Span('M')],
                id='current_month_title',
                style={"color": "darkred"}),

        html.Label(children=["增长率：",
                             html.Span(children=["0.00%"], id="growth_rate")],
                   id="current_month_label"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6(["近12月销售趋势",
                 "(",
                 html.Span(children=[start_month], id="group_start_month"),
                 " - ",
                 html.Span(children=[stop_month], id="group_end_month"),
                 ")"],
                id="month_group_title"),
        dcc.Graph(id='graph_month_group', style={"height": "60px"}),
    ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
]

# 战区分析 -- dengxiaohu
c_fig_01 = dbc.Card(dbc.CardBody([
    # 用户选项
    html.Div([
        html.H5('销售额分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(
                id="cate_choice",
                options=[{'label': x, 'value': y} for x, y in dim_cates.items()],
                value='businessname',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='agg_choice',
                options=[{'label': x, 'value': y} for x, y in dim_aggs.items()],
                value='dff.sum()',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='graph_choice',
                options=[{'label': x, 'value': y} for x, y in dim_types.items()],
                value='px.bar',
                searchable=False, clearable=False, style={'width': 120}
            ),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Loading(id='loading-1',
                type='circle',
                children=[dcc.Graph(id="graph_out_qs")],
                style={'width': '1022px', 'height': '450px'}),

    # 用户选项
    html.Div([
        html.H5('单月分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(
                id="x_choice_1",
                options=[{'label': x, 'value': y} for x, y in dim_cates.items()],
                value='businessname',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='cate_choice_1',
                options=[{'label': x, 'value': y} for x, y in dim_cates.items()],
                value='areaname3',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='agg_choice_1',
                options=[{'label': x, 'value': y} for x, y in dim_aggs.items()],
                value='dff.sum()',
                searchable=False, clearable=False, style={'width': 120}
            ),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Loading(id='loading-2',
                type='circle',
                children=[dcc.Graph(id="graph_out_dy")],
                style={'width': '1022px', 'height': '450px'}),

    html.Hr(),
    html.Div([
        html.Div(children=[html.Span('最近更新:'),
                           html.Span('2021-07-23 12:30:00', id="sales_update_time")
                           ], className='media-body'),
        html.Div(
            dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm', id='btn_sales_update', n_clicks=0)),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

# 所属城市级别
c_fig_02 = dbc.Card(dbc.CardBody([

    # 用户选项
    html.Div([
        html.H5('销售额分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(
                id="x_choice_2",
                options=[{'label': x, 'value': y} for x, y in dim_cates.items()],
                value='businessname',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='cate_choice_2',
                options=[{'label': x, 'value': y} for x, y in dim_cates.items()],
                value='areaname3',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='agg_choice_2',
                options=[{'label': x, 'value': y} for x, y in dim_types.items()],
                value='dff.sum()',
                searchable=False, clearable=False, style={'width': 120}
            ),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Loading(id='loading-3',
                type='circle',
                children=[dcc.Graph(id='graph_out_wd')],
                style={'width': '1022px', 'height': '450px'}),

    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(
            dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm', id='btn_city_update', n_clicks=0)),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

# 战区排名
c_fig_03 = dbc.Card(dbc.CardBody([
    # 用户选项
    html.Div([
        html.H5('销售额-战区排名', className='media-body'),
        html.Div([
            dcc.Dropdown(id='choices_top_order', options=order_types, value=2, searchable=False,
                         clearable=False,
                         style={'width': 120}),
            dcc.Dropdown(id='choices_top_month', options=[{"label": x, "value": x} for x in date_range],
                         value=stop_month, searchable=False, clearable=False,
                         style={'width': 100}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Loading(id='loading-4',
                type='circle',
                children=[
                    dcc.Graph(id="graph_top")
                ],
                style={'width': '460px', 'height': '450px'}),

    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm', id='button-3', n_clicks=0)),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

content = html.Div(
    className='content-style',
    children=[
        dbc.Row(id="card_data", children=card_list),
        dbc.Row([
            dbc.Col([
                dbc.Row(c_fig_01),
                dbc.Row(c_fig_02, className='mt-3'),
            ], width=8),
            dbc.Col(c_fig_03, width=4),
        ], className='mt-3'),
    ],
)

###############
# 页面布局
###############

layout = html.Div([
    sidebar,
    content,
    # signal value to trigger callbacks
    dcc.Store(id='signal')
])
