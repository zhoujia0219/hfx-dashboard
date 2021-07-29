import math
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dateutil.relativedelta import relativedelta

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from conts import router_conts
from core.flask_app import flask_server
from service import sales_service
from utils import ToolUtil

###############
# dash
###############

sales_app = dash.Dash(__name__,
                      server=flask_server,
                      title="门店月度销售分析",
                      update_title="数据载入中...",
                      suppress_callback_exceptions=True,
                      url_base_pathname=router_conts.SALES_BY_MONTH,
                      external_stylesheets=[dbc.themes.PULSE])

###############
# sidebar
###############
# 当前年月日
today = datetime.now()
# 格式化现在的月份
now_month = today.strftime("%Y-%m")
# 日期区间
date_range = ToolUtil.get_date_list("2020-01", now_month)
# 默认开始日期 当前日期减去1年份取月份
start_month = (today - relativedelta(years=1)).strftime('%Y-%m')
# 默认结束日期  当前日期减去1月 取月份
stop_month = (today - relativedelta(months=1)).strftime('%Y-%m')

# 渠道信息获取
channels = sales_service.find_channel_list()
# 门店级别定义
city_levels = [
    {"label": "一线城市", "value": 1},
    {"label": "二线城市", "value": 2},
    {"label": "三线城市", "value": 3},
    {"label": "其它", "value": 4},
]
default_city_values = [1, 2, 3, 4]
# 店龄
store_ages = [
    {"label": "新店（0-1年）", "value": 1},
    {"label": "1-2年", "value": 2},
    {"label": "2-3年", "value": 3},
    {"label": "3-5年", "value": 4},
    {"label": ">5年", "value": 5},
]
default_age_values = [1, 2, 3, 4, 5]
store_areas = [
    {"label": "档口店(<30㎡)", "value": 1},
    {"label": "外卖店(<30㎡)", "value": 2},
    {"label": "小店(<50㎡)", "value": 3},
    {"label": "标准店(50-70㎡)", "value": 4},
    {"label": "大店(>70㎡)", "value": 5},
]
default_area_values = [1, 2, 3, 4, 5]
store_stars = [
    {"label": "☆", "value": 1},
    {"label": "☆☆", "value": 2},
    {"label": "☆☆☆", "value": 3},
    {"label": "☆☆☆☆", "value": 4},
    {"label": "☆☆☆☆☆", "value": 5},
]
default_star_values = [1, 2, 3, 4, 5]
# 提交
filter_submit = dbc.Button('重新计算', id='submit', color="primary", className="mt-3", block=True)
# 默认筛选值
default_filter_values = {'begin_month': start_month, 'end_month': stop_month,
                         'city': default_city_values, 'channel': [], 'store_age': [], 'store_area': [],
                         'store_star': []}

sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4("门店月度销售分析"),
        html.Hr(),
        html.P("可通过条件筛选过滤数据，也可以改变维度和图形样式", className="small", style={'color': 'gray'}),
        html.Div([
            filter_date_range.filter_month_range(date_range, start_month, stop_month),
            filter_city_level.filter_city_level("门店所属城市", city_levels, default_city_values),
            filter_channels.filter_channels("销售渠道", [{"label": c, "value": c} for c in channels], channels),
            filter_store_age.filter_store_age("店龄", store_ages, default_age_values),
            filter_store_area.filter_store_area("门店面积", store_areas, default_area_values),
            filter_store_star.filter_store_star("门店星级", store_stars, default_star_values),
            filter_submit,
        ]),
    ],
)


###############
# content
###############

# 顶部4个card
def build_layout_title_cards(values: dict):
    # 封装结果数据
    datas = sales_service.calculate_cards(values)

    total_sale = datas["total_sale"] if datas else '0'
    begin_month = values["begin_month"] if values else ''
    end_month = values["end_month"] if values else ''
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
            html.H6("本月销售额"),
            html.H4(['￥', c_month_total_sale, 'M'], id='title_3', style={"color": "darkred"}),
            html.Label("增长率：" + m_growth_rate),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6(["近12月销售趋势", "(", begin_month + " - " + end_month, ")"]),
            dcc.Graph(id='title_4', figure=fig, style={"height": "60px"}),
        ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
    ]


# 顶部 12月趋势图
def build_group_sales_fig(df):
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
def build_fig_3(order_value, month_value, values):
    # 取数据
    fig3_data = sales_service.global_store(values)
    if len(fig3_data) < 0:
        return {}

    df = pd.DataFrame(fig3_data)
    group_df = df
    # 当月数据
    c_month = datetime.strptime(month_value, "%Y-%m")
    cs_date = ToolUtil.get_month_first_day(c_month).date()
    ce_date = ToolUtil.get_month_last_day(c_month).date()
    current_month_df = group_df[(group_df["rdate"] >= cs_date) & (group_df["rdate"] < ce_date)]

    # 上月数据
    ls_date = ToolUtil.get_last_month_first_day(c_month).date()
    le_date = ToolUtil.get_last_month_last_day(c_month).date()
    last_month_df = group_df[(group_df["rdate"] >= ls_date) & (group_df["rdate"] < le_date)]
    # 本月战区分组聚合
    c_group_data = current_month_df.groupby(by=["areaname3", "month_group"], as_index=False)["dealtotal"].sum()
    c_df = pd.DataFrame(c_group_data)
    # 上月战区分组聚合
    l_group_data = last_month_df.groupby(by=["areaname3", "month_group"], as_index=False)["dealtotal"].sum()
    l_df = pd.DataFrame(l_group_data)

    l_df["dealtotal"] = l_df["dealtotal"] * (-1)
    # 根据战区分组并排序
    if order_value == 1:
        c_df.sort_values(by="dealtotal", ascending=True, inplace=False)
        l_df.sort_values(by="dealtotal", ascending=True, inplace=False)
    elif order_value == 2:
        c_df.sort_values(by="dealtotal", ascending=False, inplace=False)
        l_df.sort_values(by="dealtotal", ascending=False, inplace=False)

    # 合并数据
    fig_df = c_df.append(l_df)

    if len(fig_df) > 0:
        fig = px.bar(fig_df, x="dealtotal", y="areaname3", color='month_group', orientation='h', height=300,
                     category_orders={'areaname3': [c for c in fig_df['areaname3']]},
                     hover_name='month_group',
                     labels={'month_group': '销售额环比', 'dealtotal': '销售额', 'areaname3': '战区'},
                     text=[str(round(math.fabs(c) / sales_service.trans_num, 2)) + "M" for c in fig_df["dealtotal"]],
                     template="plotly_white")

        # todo 添加显示标签

        return fig
    else:
        return {}


# 销售分析
def build_sales_gragh(values, val_graph, val_cate, val_agg):
    df = sales_service.calculate_gragh_data(values)
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
def build_city_graph(values, val_x, val_cate, val_agg):
    df = sales_service.calculate_gragh_data(values)
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


# 常量定义

dims = [
    {'label': '维度: 门店所属战区', 'value': 1},
    {'label': '维度: 门店所属城市', 'value': 2},
    {'label': '维度: 销售渠道', 'value': 3},
    {'label': '维度: 店龄', 'value': 4},
    {'label': '维度: 门店面积', 'value': 5},
    {'label': '维度: 门店星级', 'value': 6},
]
figure_type = [
    {'label': '图: 折线图', 'value': 1},
    {'label': '图: 柱状图', 'value': 2},
]
index_type = [
    {'label': '指标: 销售总额', 'value': 1},
    {'label': '指标: 平均值', 'value': 2},
    {'label': '指标: 中位数', 'value': 3},
]
order_type = [
    {'label': '排序: 正序', 'value': 1},
    {'label': '排序: 降序', 'value': 2},
]

cate = {'维度: 渠道': 'businessname', '维度: 战区': 'areaname3', '维度: 店面积': 'areasize_bins'}
agg = {'聚合函数: 总和': 'dff.sum()', '聚合函数: 平均值': 'dff.mean()', '聚合函数: 中位数': 'dff.median()'}
graph = {'图形: 柱状图': 'px.bar', '图形: 线性图': 'px.line'}

# 战区分析 -- dengxiaohu
c_fig_01 = dbc.Card(dbc.CardBody([
    # 用户选项
    html.Div([
        html.H5('销售额分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(
                id="cate_choice",
                options=[{'label': x, 'value': y} for x, y in cate.items()],
                value='businessname',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='agg_choice',
                options=[{'label': x, 'value': y} for x, y in agg.items()],
                value='dff.sum()',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='graph_choice',
                options=[{'label': x, 'value': y} for x, y in graph.items()],
                value='px.bar',
                searchable=False, clearable=False, style={'width': 120}
            ),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(id="graph_out_qs", figure=build_sales_gragh(default_filter_values, "px.bar", "areaname3", "dff.sum()")),
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
                id="x_choice",
                options=[{'label': x, 'value': y} for x, y in cate.items()],
                value='businessname',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='cate_choice_2',
                options=[{'label': x, 'value': y} for x, y in cate.items()],
                value='areaname3',
                searchable=False, clearable=False, style={'width': 120}
            ),
            dcc.Dropdown(
                id='agg_choice_2',
                options=[{'label': x, 'value': y} for x, y in agg.items()],
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
            dcc.Dropdown(id='dw_fig_3_1', options=order_type, value=2, searchable=False, clearable=False,
                         style={'width': 120}),
            dcc.Dropdown(id='dw_fig_3_2', options=[{"label": x, "value": x} for x in date_range],
                         value=stop_month, searchable=False, clearable=False,
                         style={'width': 100}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(id="fig_3", figure=build_fig_3(1, stop_month, default_filter_values)),
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
        Input("submit", "n_clicks"),
        # 日期筛选
        State('begin_month', 'value'),
        State('end_month', 'value'),
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
def compute_value(n_clicks, begin_month, end_month, city, channel, store_age, store_area, store_star):
    values = {'begin_month': begin_month, 'end_month': end_month,
              'city': city, 'channel': channel,
              'store_age': store_age, 'store_area': store_area, 'store_star': store_star}
    # compute value and send a signal when done
    sales_service.global_store(values)
    return values


@sales_app.callback(Output('card_data', 'children'), Input('signal', 'data'))
def update_card_data(values):
    return build_layout_title_cards(values)


@sales_app.callback(
    Output('fig_3', 'figure'),
    [
        Input('dw_fig_3_1', 'value'),
        Input('dw_fig_3_2', 'value'),
        Input('signal', 'data'),
    ])
def update_fig_3(order_value, month_value, values):
    """
        更新排名图
    @param order_value: 1: 正序， 2： 倒序
    @param month_value: 月份值
    @param values:  全局缓存key
    """

    return build_fig_3(order_value, month_value, values)


@sales_app.callback(
    Output('dw_fig_3_2', 'value'),
    Input('end_month', 'value'),
)
def update_fig_3_2_value(value):
    """
    更新选项值
    """
    return value


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
def update_my_graph(val_cate, val_agg, val_graph, values):
    return build_sales_gragh(values, val_graph, val_cate, val_agg)


# graph_out_wd
@sales_app.callback(
    Output('graph_out_wd', 'figure'),
    [
        Input('x_choice', 'value'),
        Input('cate_choice_2', 'value'),
        Input('agg_choice_2', 'value'),
        Input('signal', 'data'),
    ],
)
def update_my_graph(val_x, val_cate, val_agg, values):
    return build_city_graph(values, val_x, val_cate, val_agg)
