import math
import time
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from conf.hfx_dashboard import BOOTSTRAP_THEME
from conf.router_conts import URL_SALES_BYMONTH
from flask_app import flask_server
from services import srv_sales_bymonth, srv_comm_dim
from utils import date_util

###############
# dash
###############

sales_app = dash.Dash(__name__,
                      server=flask_server,
                      title="门店月度销售分析",
                      update_title="数据载入中...",
                      suppress_callback_exceptions=True,
                      url_base_pathname=URL_SALES_BYMONTH,
                      external_stylesheets=[BOOTSTRAP_THEME])

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
# 页面内容构建刷新函数
###############

# 顶部 12月趋势图
def build_group_sales_fig(df: DataFrame):
    """
    12个月销售趋势图
    :param df: 包含月份和销售额的dataframe 数据
    :return 返回图形
    """

    time_start = time.time()
    fig = px.bar(df, x="month_group", y="dealtotal", width=200, height=60)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10, l=10, b=10, r=10)
    )

    time_end = time.time()
    print('build_group_sales_fig: Running time:{} seconds'.format(time_end - time_start))
    return fig


# 战区排名
def build_top_graph(order_value: int, month_value: str, filter_values: dict):
    """

    构建排名图
    :param order_value: 排序
    :param month_value:
    :param filter_values:
    :return:
    """

    time_start = time.time()
    fig_df = srv_sales_bymonth.calculate_top_graph(filter_values, month_value, order_value)
    if len(fig_df) > 0:
        fig = px.bar(fig_df, x="dealtotal", y="areaname3", color='month_group', orientation='h', height=300,
                     category_orders={'areaname3': [c for c in fig_df['areaname3']]},
                     hover_name='month_group',
                     labels={'month_group': '销售额环比', 'dealtotal': '销售额', 'areaname3': '战区'},
                     text=[str(round(math.fabs(c) / srv_sales_bymonth.trans_num, 2)) + "M" for c in
                           fig_df["dealtotal"]],
                     template="plotly_white")

        # todo 添加显示标签

        time_end = time.time()
        print('build_top_graph: Running time:{} seconds'.format(time_end - time_start))
        return fig
    else:
        return {}


# 销售分析
def build_sales_graph(filter_values, val_graph, val_cate, val_agg):
    """

    :param filter_values:
    :param val_graph:
    :param val_cate:
    :param val_agg:
    :return:
    """
    time_start = time.time()
    df = srv_sales_bymonth.calculate_graph_data(filter_values)
    if len(df) < 1:
        return dash.no_update
    if val_graph == 'px.bar':
        dff = df.groupby(['month', val_cate], as_index=False)['dealtotal']
        dff = eval(val_agg)
        dff_line = dff.groupby('month', as_index=False)['dealtotal'].mean()

        fig = go.Figure([
                            go.Bar(name=lab,
                                   x=dff[dff[val_cate] == lab]['month'],
                                   y=dff[dff[val_cate] == lab]['dealtotal'], )
                            for lab in dff[val_cate].unique()] +
                        [go.Scatter(name='平均值', x=dff_line['month'], y=dff_line['dealtotal'], mode="lines")])
        fig.update_layout(barmode='group', template='plotly_white')

        time_end = time.time()
        print('build_sales_graph: Running time:{} seconds'.format(time_end - time_start))
        return fig
    else:
        dff = df.groupby(['month', val_cate], as_index=False)['dealtotal']
        dff = eval(val_agg)
        fig = eval(val_graph)(
            dff,
            x='month',
            y='dealtotal',
            color=val_cate,
            labels={'month': '月份', 'dealtotal': '总销售额'},
            title='销售额分析',
            template='plotly_white'
        )

        time_end = time.time()
        print('build_sales_graph: Running time:{} seconds'.format(time_end - time_start))
        return fig


# 所属城市级别
def build_city_graph(filter_values, val_x, val_cate, val_agg):
    """

    :param filter_values:
    :param val_x:
    :param val_cate:
    :param val_agg:
    :return:
    """
    time_start = time.time()
    df = srv_sales_bymonth.calculate_graph_data(filter_values)
    if len(df) < 1:
        return dash.no_update
    if val_x == val_cate:
        return dash.no_update
    else:
        dff = df.groupby([val_x, val_cate], as_index=False)['dealtotal']
        dff = eval(val_agg)
        fig = px.bar(
            dff,
            x=val_x,
            y='dealtotal',
            color=val_cate,
            labels={'dealtotal': '总销售额'},
            title='销售额分析',
            barmode='group',
            text='dealtotal',
            template='plotly_white'
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        time_end = time.time()
        print('build_city_graph: Running time:{} seconds'.format(time_end - time_start))
        return fig


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

sales_app.layout = html.Div([
    sidebar,
    content,
    # signal value to trigger callbacks
    dcc.Store(id='signal')
])


###############
# 回调
###############

@sales_app.callback(
    Output('signal', 'data'),
    [
        Input("f_submit", "n_clicks"),
        # 日期筛选
        State('f_begin_month', 'value'),
        State('f_end_month', 'value'),
        # 城市筛选
        State('f_cities', 'value'),
        # 渠道筛选
        State('f_channels', 'value'),
        # 店龄筛选
        State('f_store_age', 'value'),
        # 门店面积筛选
        State('f_store_area', 'value'),
        # 门店星级筛选
        State('f_store_star', 'value'),
    ]
)
def compute_value(n_clicks, begin_month, end_month, city_level, channel, store_age, store_area, store_star):
    """
    点击提交按钮后，保存筛选值到signal
    :param n_clicks 提交按钮点击次数
    :param begin_month 结束日期
    :param end_month 开始日期
    :param city_level  城市级别
    :param channel 渠道
    :param store_age 店龄
    :param store_area 店面积
    :param store_star 门店星级
    :return 返回筛选的所有选中值（用于取缓存）

    """
    filter_values = {'begin_month': begin_month, 'end_month': end_month,
                     'city_level': city_level, 'channel': channel,
                     'store_age': store_age, 'store_area': store_area, 'store_star': store_star}
    # compute value and send a signal when done
    srv_sales_bymonth.global_store(filter_values)
    return filter_values


@sales_app.callback(
    [
        Output('total_sales', 'children'),
        Output('total_sales_start_month', 'children'),
        Output('total_sales_stop_month', 'children'),
        Output('last_month_sales', 'children'),
        Output('last_month_tb', 'children'),
        Output('last_month_hb', 'children'),
        Output('current_month_sign', 'children'),
        Output('current_month_sales', 'children'),
        Output('growth_rate', 'children'),
        Output('group_start_month', 'children'),
        Output('group_end_month', 'children'),
        Output('graph_month_group', 'figure'),
    ],
    [Input('signal', 'data')])
def update_card_group_month_graph(filter_values):
    """
    更新 12个月趋势图卡片
    :param filter_values:
    :return:
    """
    # 获取基础数据
    df = srv_sales_bymonth.global_store(filter_values)
    begin_month = filter_values["begin_month"]
    end_month = filter_values["end_month"]
    # 计算卡片数据
    card_df = srv_sales_bymonth.calculate_card_data(df, end_month)
    graph_df = srv_sales_bymonth.calculate_card_graph(df)
    return [[card_df["total_sale"]], [begin_month], [end_month],
            [card_df["last_month_total"]], [card_df["tb_percentage"]], [card_df["hb_percentage"]],
            [end_month], [card_df["c_month_total_sale"]], [card_df["m_growth_rate"]],
            [begin_month], [end_month], build_group_sales_fig(graph_df)]


@sales_app.callback(
    Output('graph_top', 'figure'),
    [
        Input('choices_top_order', 'value'),
        Input('choices_top_month', 'value'),
        Input('signal', 'data'),
    ])
def update_top_graph(order_value, month_value, filter_values):
    """
    更新排名图
    :param order_value: 1: 正序， 2： 倒序
    :param month_value: 月份值
    :param filter_values:  筛选值->全局缓存key
    """

    return build_top_graph(order_value, month_value, filter_values)


@sales_app.callback(
    Output('choices_top_month', 'value'),
    Input('f_end_month', 'value'),
)
def update_choices_top_month_value(month_value):
    """
    更新排名月份选项值 -- 用于页面初始化时，默认展示排名月份的展示
    :param month_value : 过滤结束月份时间
    :return  返回 筛选结束月份的值
    """
    return month_value


# graph_out_qs
@sales_app.callback(
    Output('graph_out_qs', 'figure'),
    [
        Input('btn_sales_update', 'n_clicks'),
        Input('cate_choice', 'value'),
        Input('agg_choice', 'value'),
        Input('graph_choice', 'value'),
        Input('signal', 'data'),
    ],
)
def update_sales_graph(n_clicks, val_cate, val_agg, val_graph, filter_values):
    """

    :param n_clicks
    :param val_cate:
    :param val_agg:
    :param val_graph:
    :param filter_values:
    :return:
    """
    return build_sales_graph(filter_values, val_graph, val_cate, val_agg)


# graph_out_wd
@sales_app.callback(
    Output('graph_out_wd', 'figure'),
    [
        Input('btn_city_update', 'n_clicks'),
        Input('x_choice_2', 'value'),
        Input('cate_choice_2', 'value'),
        Input('agg_choice_2', 'value'),
        Input('signal', 'data'),
    ],
)
def update_city_graph(n_clicks, val_x, val_cate, val_agg, filter_values):
    """

    :param n_clicks
    :param val_x:
    :param val_cate:
    :param val_agg:
    :param filter_values:
    :return:
    """
    return build_city_graph(filter_values, val_x, val_cate, val_agg)


# graph_out_dy
@sales_app.callback(
    Output('graph_out_dy', 'figure'),
    [
        Input('btn_sales_update', 'n_clicks'),
        Input('x_choice_1', 'value'),
        Input('cate_choice_1', 'value'),
        Input('agg_choice_1', 'value'),
        Input('signal', 'data'),
    ],
)
def update_my_graph(n_clicks, val_x, val_cate, val_agg, filter_values):
    """

    :param n_clicks
    :param val_x:
    :param val_cate:
    :param val_agg:
    :param filter_values:
    :return:
    """

    return build_city_graph(filter_values, val_x, val_cate, val_agg)
