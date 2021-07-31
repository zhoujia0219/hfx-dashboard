import math
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
# 默认筛选值
default_filter_values = {'begin_month': start_month, 'end_month': stop_month,
                         'city_level': default_city_values, 'channel': default_channel_values,
                         'store_age': default_age_values, 'store_area': default_area_values,
                         'store_star': default_star_values}

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

def build_layout_title_cards(filter_values: dict):
    """
    头部卡片
    @param filter_values: 筛选值
    @return
    """
    # 封装结果数据
    datas = srv_sales_bymonth.calculate_cards(filter_values)

    total_sale = datas["total_sale"] if datas else '0'
    begin_month = filter_values["begin_month"] if filter_values else ''
    end_month = filter_values["end_month"] if filter_values else ''
    last_month_total = datas["last_month_total"] if datas else '0'

    tb_percentage = datas["tb_percentage"] if datas else '0'
    hb_percentage = datas["hb_percentage"] if datas else '0'
    c_month_total_sale = datas["c_month_total_sale"] if datas else '0'
    m_growth_rate = datas["m_growth_rate"] if datas else '0'
    group_sales = datas["group_sales"] if datas else []
    fig = build_group_sales_fig(group_sales) if len(group_sales) > 0 else {}

    return [
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("总销售额"),
            html.H4(['￥', total_sale, 'M'], id='title_1', style={"color": "darkred"}),
            html.Label(begin_month + " - " + end_month),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("上月销售额"),
            html.H4(['￥', last_month_total, 'M'], id='title_2', style={"color": "darkred"}),
            html.Label("同比:" + tb_percentage + "  环比：" + hb_percentage),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6(["本月销售额", "(", end_month, ")"]),
            html.H4(['￥', c_month_total_sale, 'M'], id='title_3', style={"color": "darkred"}),
            html.Label("增长率：" + m_growth_rate),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6(["近12月销售趋势", "(", begin_month + " - " + end_month, ")"]),
            dcc.Graph(id='title_4', figure=fig, style={"height": "60px"}),
        ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
    ]


# 顶部 12月趋势图
def build_group_sales_fig(df: DataFrame):
    """
    12个月销售趋势图
    """
    fig = px.bar(df, x="month_group", y="dealtotal", width=200, height=60)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10, l=10, b=10, r=10)
    )
    return fig


# 战区排名
def build_top_graph(order_value: int, month_value: str, filter_values: dict):
    """
    构建排名图
    @param: order_value
    @param: month_value
    @param: filter_values
    """

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

        return fig
    else:
        return {}


# 销售分析
def build_sales_graph(filter_values, val_graph, val_cate, val_agg):
    df = srv_sales_bymonth.calculate_graph_data(filter_values)
    if len(df) < 1:
        return {}
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
        return fig


# 所属城市级别
def build_city_graph(filter_values, val_x, val_cate, val_agg):
    df = srv_sales_bymonth.calculate_graph_data(filter_values)
    if len(df) < 1:
        return {}
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
        return fig


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
    dcc.Graph(id="graph_out_qs", figure=build_sales_graph(default_filter_values, "px.bar", "areaname3", "dff.sum()")),

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
    dcc.Graph(id="graph_out_dy", figure=build_sales_graph(default_filter_values, "px.bar", "areaname3", "dff.sum()")),
    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
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
    dcc.Graph(id='graph_out_wd',
              figure=build_city_graph(default_filter_values, 'businessname', 'areaname3', 'dff.sum()')),
    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

# 战区排名
c_fig_03 = dbc.Card(dbc.CardBody([
    # 用户选项
    html.Div([
        html.H5('销售额-战区排名', className='media-body'),
        html.Div([
            dcc.Dropdown(id='top_choices_order', options=order_types, value=2, searchable=False,
                         clearable=False,
                         style={'width': 120}),
            dcc.Dropdown(id='top_choices_month', options=[{"label": x, "value": x} for x in date_range],
                         value=stop_month, searchable=False, clearable=False,
                         style={'width': 100}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(id="graph_top", figure=build_top_graph(1, stop_month, default_filter_values)),
    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

content = html.Div(
    className='content-style',
    children=[
        dbc.Row(id="card_data",
                children=build_layout_title_cards(default_filter_values)),
        dbc.Row([
            dbc.Col([
                dbc.Row(c_fig_01),
                dbc.Row(c_fig_02, className='mt-3'),
            ], width=8),
            dbc.Col(c_fig_03, width=4),
        ], className='mt-3'),
    ],
)

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
    @param n_clicks 提交按钮点击次数
    @param begin_month 结束日期
    @param end_month 开始日期
    @param city_level  城市级别
    @param channel 渠道
    @param store_age 店龄
    @param store_area 店面积
    @param store_star 门店星级
    @return 返回筛选的所有选中值（用于取缓存）

    """
    filter_values = {'begin_month': begin_month, 'end_month': end_month,
                     'city_level': city_level, 'channel': channel,
                     'store_age': store_age, 'store_area': store_area, 'store_star': store_star}
    # compute value and send a signal when done
    srv_sales_bymonth.global_store(filter_values)
    return filter_values


@sales_app.callback(Output('card_data', 'children'), Input('signal', 'data'))
def update_card_data(filter_values):
    """
    更新card数值
    @param filter_values: 筛选值
    @return  返回顶部的card
    """
    return build_layout_title_cards(filter_values)


@sales_app.callback(
    Output('graph_top', 'figure'),
    [
        Input('top_choices_order', 'value'),
        Input('top_choices_month', 'value'),
        Input('signal', 'data'),
    ])
def update_top_graph(order_value, month_value, filter_values):
    """
    更新排名图
    @param order_value: 1: 正序， 2： 倒序
    @param month_value: 月份值
    @param filter_values:  筛选值->全局缓存key
    """

    return build_top_graph(order_value, month_value, filter_values)


@sales_app.callback(
    Output('top_choices_month', 'value'),
    Input('f_end_month', 'value'),
)
def update_top_choices_month_value(month_value):
    """
    更新排名月份选项值 -- 用于页面初始化时，默认展示排名月份的展示
    @param month_value : 过滤结束月份时间
    @return  返回 筛选结束月份的值
    """
    return month_value


# graph_out_qs
@sales_app.callback(
    Output('graph_out_qs', 'figure'),
    [
        Input('cate_choice', 'value'),
        Input('agg_choice', 'value'),
        Input('graph_choice', 'value'),
        Input('signal', 'data'),
    ],
)
def update_sales_graph(val_cate, val_agg, val_graph, filter_values):
    """

    """
    return build_sales_graph(filter_values, val_graph, val_cate, val_agg)


# graph_out_wd
@sales_app.callback(
    Output('graph_out_wd', 'figure'),
    [
        Input('x_choice_2', 'value'),
        Input('cate_choice_2', 'value'),
        Input('agg_choice_2', 'value'),
        Input('signal', 'data'),
    ],
)
def update_city_graph(val_x, val_cate, val_agg, filter_values):
    """

    """
    return build_city_graph(filter_values, val_x, val_cate, val_agg)


# graph_out_dy
@sales_app.callback(
    Output('graph_out_dy', 'figure'),
    [
        Input('x_choice_1', 'value'),
        Input('cate_choice_1', 'value'),
        Input('agg_choice_1', 'value'),
        Input('signal', 'data'),
    ],
)
def update_my_graph(val_x, val_cate, val_agg, filter_values):
    """

    """
    return build_city_graph(filter_values, val_x, val_cate, val_agg)
