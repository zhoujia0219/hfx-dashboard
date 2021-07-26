import random
import time
from datetime import datetime, date

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
from flask_caching import Cache
from conf import db_conf
from db import DbUtil
from app import app, cache
from utils import ToolUtil

###############
# 更新标题
###############
app.title = "门店月度销售分析"
app.update_title = "数据载入中..."

###############
# sidebar
###############
# 当前年月日
now = time.strftime("%Y-%m", time.localtime())
# 日期区间
date_range = ToolUtil.get_date_list("2020-01", "2021-07")

filter_month_range = dbc.FormGroup([
    dbc.Label('日期范围', className='sidebar-label'),
    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(
                id='begin_month',
                options=[{"label": x, "value": x} for x in date_range],
                value='2020-01',
                clearable=False,
                persistence=True,
            )),
            dbc.Col(dcc.Dropdown(
                id='end_month',
                options=[{"label": x, "value": x} for x in date_range],
                value='2021-02',
                clearable=False,
                persistence=True,
            )),
        ], no_gutters=True,
    ),
])

filter_cities = dbc.FormGroup([
    dbc.Label("门店所属城市", className='sidebar-label'),
    dbc.Checklist(
        id="f_cities",
        options=[
            {"label": "一线城市", "value": 1},
            {"label": "二线城市", "value": 2},
            {"label": "三线城市", "value": 3},
            {"label": "其它", "value": 4},
        ],
        value=[1, 2, 3, 4],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_channels = dbc.FormGroup([
    dbc.Label("销售渠道", className='sidebar-label'),
    dbc.Checklist(
        id="f_channels",
        options=[
            {"label": "堂食", "value": 1},
            {"label": "美团", "value": 2},
            {"label": "饿了么", "value": 3},
            {"label": "其它", "value": 0},
        ],
        value=[0, 1, 2, 3],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_store_age = dbc.FormGroup([
    dbc.Label("店龄", className='sidebar-label'),
    dbc.Checklist(
        id="f_store_age",
        options=[
            {"label": "新店（0-1年）", "value": 1},
            {"label": "1-2年", "value": 2},
            {"label": "2-3年", "value": 3},
            {"label": "3-5年", "value": 4},
            {"label": ">5年", "value": 5},
        ],
        value=[1, 2, 3, 4, 5],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_store_area = dbc.FormGroup([
    dbc.Label("门店面积", className='sidebar-label'),
    dbc.Checklist(
        id="f_store_area",
        options=[
            {"label": "档口店(<30㎡)", "value": 1},
            {"label": "外卖店(<30㎡)", "value": 2},
            {"label": "小店(<50㎡)", "value": 3},
            {"label": "标准店(50-70㎡)", "value": 4},
            {"label": "大店(>70㎡)", "value": 5},
        ],
        value=[1, 2, 3, 4, 5],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_store_star = dbc.FormGroup([
    dbc.Label("门店星级", className='sidebar-label'),
    dbc.Checklist(
        id="f_store_star",
        options=[
            {"label": "☆", "value": 1},
            {"label": "☆☆", "value": 2},
            {"label": "☆☆☆", "value": 3},
            {"label": "☆☆☆☆", "value": 4},
            {"label": "☆☆☆☆☆", "value": 5},
        ],
        value=[1, 2, 3, 4, 5],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_store_area1 = dbc.FormGroup([
    dbc.Label("门店面积", className='sidebar-label'),
    dbc.Checklist(
        id='',
        options=[
            {"label": "档口店(<30㎡)", "value": 1},
            {"label": "外卖店(<30㎡)", "value": 2},
            {"label": "小店(<50㎡)", "value": 3},
            {"label": "标准店(50-70㎡)", "value": 4},
            {"label": "大店(>70㎡)", "value": 5},
        ],
        value=[1, 2, 3, 4, 5],
        inline=True,
        labelStyle={'min-width': 70},
        persistence=True,
    ),
])

filter_submit = dbc.Button('重新计算', id='submit', color="primary", className="mt-3", block=True)

sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4("门店月度销售分析"),
        html.Hr(),
        html.P("可通过条件筛选过滤数据，也可以改变维度和图形样式", className="small", style={'color': 'gray'}),
        html.Div([
            filter_month_range,
            filter_cities,
            filter_channels,
            filter_store_age,
            filter_store_area,
            filter_store_star,
            filter_submit,
        ]),
    ],
)

###############
# 模拟数据
###############
test_df = pd.DataFrame({'Month': random.choices(range(1, 13), k=360),
                        'Area': random.choices(['一战区', '二战区', '三战区', '四战区', '五战区'], k=360),
                        'City': random.choices(['一线城市', '二线城市', '三线城市', '其它'], weights=[1, 2, 3, 1], k=360),
                        'Sales': np.random.randint(low=80, high=120, size=360)})
test_df_1 = test_df.groupby(['Month', 'Area']).sum()
test_df_1 = test_df_1.reset_index()
test_df_2 = test_df.groupby(['Month', 'City']).sum()
test_df_2 = test_df_2.reset_index()

test_pm = pd.DataFrame({'Group': ['一战区一组', '一战区二组', '一战区三组', '一战区四组'
    , '二战区一组', '二战区二组', '二战区三组', '二战区四组'
    , '三战区一组', '三战区二组', '三战区三组', '三战区四组'
    , '四战区一组', '四战区二组', '四战区三组', '四战区四组', ],
                        'Sales': np.random.randint(low=20, high=80, size=16)})
test_pm = test_pm.sort_values(by='Sales', axis=0, ascending=[True])

test_fig_1 = px.bar(test_df_1, x="Month", y="Sales", color='Area', height=300,
                    labels={'Month': '过去12个月', 'Sales': '销售额', 'Area': '战区'},
                    template="plotly_white")
test_fig_2 = px.line(test_df_2, x="Month", y="Sales", color='City', height=300,
                     labels={'Month': '过去12个月', 'Sales': '销售额', 'City': '城市'},
                     template="plotly_white")
# test_fig_3 = px.bar(test_pm, x="Sales", y="Group", orientation='h', labels={'Group': '战区', 'Sales': '销售额'}
#                     , height=740
#                     , template="plotly_white")
test_fig_3_df = pd.DataFrame({'Month': random.choices(['2021-02', '2021-01'], k=100),
                              'Area': random.choices(['一战区', '二战区', '三战区', '四战区', '五战区'], k=100),
                              'Sales': np.random.randint(low=10, high=100, size=100)})
test_fig_3_df = test_fig_3_df.groupby(['Month', 'Area']).sum()
test_fig_3_df = test_fig_3_df.reset_index()

test_fig_3_df.loc[test_fig_3_df['Month'] == '2021-01', 'Sales'] = test_fig_3_df[test_fig_3_df['Month'] == '2021-01'][
                                                                      'Sales'] * (-1)

test_fig_3 = px.bar(test_fig_3_df, x="Sales", y="Area", color='Month', orientation='h', height=300,
                    category_orders={'Area': ['一战区', '二战区', '三战区', '四战区', '五战区']},
                    hover_name='Month',

                    labels={'Month': '销售额环比', 'Sales': '销售额', 'Area': '战区'},
                    template="plotly_white")

###############
# content
###############

# 顶部4个card

layout_title_cards = [
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("总销售额"),
        html.H4('￥78,000,000', id='title_1', style={"color": "darkred"}),
        html.Label("2021.01 - 2021.02"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("上月销售额"),
        html.H4('￥10,000,000', id='title_2', style={"color": "darkred"}),
        html.Label("2021.01 - 2021.02"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("本月销售额"),
        html.H4('￥7,000,000', id='title_3', style={"color": "darkred"}),
        html.Label("2021.01 - 2021.02"),
    ]), className='title-card'), className='title-col mr-2'),
    dbc.Col(dbc.Card(dbc.CardBody([
        html.H6("近12月销售趋势"),
        # dcc.Graph(id='title_4'),
    ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
]


def build_group_sales_fig(df):
    fig = px.bar(df, x="month", y="dealtotal", width=200, height=70)
    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(t=10, l=10, b=10, r=10)
    )
    return fig


def build_layout_title_cards(datas: dict, values: dict):
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
            html.H4(['￥', total_sale], id='title_1', style={"color": "darkred"}),
            html.Label(begin_month + " - " + end_month),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("上月销售额"),
            html.H4(['￥', last_month_total], id='title_2', style={"color": "darkred"}),
            html.Label("同比:" + tb_percentage + "  环比：" + hb_percentage),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("本月销售额"),
            html.H4(['￥', c_month_total_sale], id='title_3', style={"color": "darkred"}),
            html.Label("增长率：" + m_growth_rate),
        ]), className='title-card'), className='title-col mr-2'),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("近12月销售趋势"),
            dcc.Graph(id='title_4', figure=fig),
        ]), className='title-card'), className='title-col col-5', style={'paddingRight': 15}),
    ]


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

# 战区分析
c_fig_01 = dbc.Card(dbc.CardBody([

    # 用户选项
    html.Div([
        html.H5('销售额-战区分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(id='dw_fig_1_1', options=index_type, value=1, searchable=False, clearable=False,
                         style={'width': 120}),
            dcc.Dropdown(id='dw_fig_1_2', options=dims, value=1, searchable=False, clearable=False,
                         style={'width': 150}),
            dcc.Dropdown(id='dw_fig_1_3', options=figure_type, value=1, searchable=False, clearable=False,
                         style={'width': 100}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(id="fig_1", figure=test_fig_1),
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
        html.H5('销售额-战区分析', className='media-body', style={'min-width': '150px'}),
        html.Div([
            dcc.Dropdown(id='dw_fig_2_1', options=index_type, value=1, searchable=False, clearable=False,
                         style={'width': 120}),
            dcc.Dropdown(id='dw_fig_2_2', options=dims, value=1, searchable=False, clearable=False,
                         style={'width': 150}),
            dcc.Dropdown(id='dw_fig_2_3', options=figure_type, value=1, searchable=False, clearable=False,
                         style={'width': 100}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(figure=test_fig_2),
    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

# 战区排名
# c_fig_03 = dbc.Card(dbc.CardBody([
#
#     # 用户选项
#     html.Div([
#         html.H5('销售额-战区排名', className='media-body'),
#         html.Div([
#             dcc.Dropdown(id='dw_fig_3_1', options=order_type, value=2, searchable=False, clearable=False,
#                          style={'width': 120}),
#         ], className='media-right block-inline')
#     ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
#     html.Hr(),
#
#     # 图
#     dcc.Graph(figure=test_fig_3),
#     html.Hr(),
#     html.Div([
#         html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
#         html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
#     ], className='media flex-wrap align-items-center'),
# ]), style={"width": "100%"})

# 战区排名2
c_fig_03 = dbc.Card(dbc.CardBody([
    # 用户选项
    html.Div([
        html.H5('销售额-战区排名', className='media-body'),
        html.Div([
            dcc.Dropdown(id='dw_fig_3_1', options=order_type, value=2, searchable=False, clearable=False,
                         style={'width': 120}),
        ], className='media-right block-inline')
    ], className='media flex-wrap ', style={'alignItems': 'flex-end'}),
    html.Hr(),

    # 图
    dcc.Graph(figure=test_fig_3),
    html.Hr(),
    html.Div([
        html.Div('最近更新: 2021-07-23 12:30:00', className='media-body'),
        html.Div(dbc.Button('立即刷新', color='secondary', className='mr-1', size='sm')),
    ], className='media flex-wrap align-items-center'),
]), style={"width": "100%"})

content = html.Div(
    className='content-style',
    children=[
        dbc.Row(id="card_data", children=layout_title_cards),
        dbc.Row([
            dbc.Col([
                dbc.Row(c_fig_01),
                dbc.Row(c_fig_02, className='mt-3'),
            ], width=8),
            dbc.Col(c_fig_03, width=4),
        ], className='mt-3'),
    ],
)

layout = html.Div([
    sidebar,
    content,
    # signal value to trigger callbacks
    dcc.Store(id='signal')
])

###########################
# 取数据缓存
###########################

default_dbname = "data_analysis"


@cache.memoize()
def global_store(values):
    """
    全局缓存
    :param values: json类型参数 { 'begin_month': begin_month, 'end_month': end_month,
                                'city':city, 'channel':channel,
                                'store_age':store_age, 'store_area':store_area, 'store_star':store_star}
    :return:
    """
    d = cache.get(str(values))
    if d:
        return d
    else:
        query_sql = """
                SELECT 
                areauid3, areaname3, areauid4, areaname4, storeuid, storename, weeks, rdate :: date, province, 
                province_name, city, city_name, county, county_name, businessname, vctype, areasize, 
                billcount, dealtotal, rebillcount, redealtotal, weather, weather_desc, temperature, wind_direction, 
                "month", "year", city_level
                FROM chunbaiwei.fact_storesale_weather
                WHERE 1 = 1
        """
        if values:
            if values["begin_month"] and values["end_month"]:
                query_sql += """  and to_char(rdate,'YYYY-MM') >= '{begin_month}'
                                  and to_char(rdate,'YYYY-MM') <= '{end_month}'
                """.format(begin_month=values["begin_month"], end_month=values["end_month"])
            if values["city"]:
                # 长度大于1 循环处理
                citys = tuple(str(c) for c in values["city"]) if len(values['city']) > 1 \
                    else "(" + str(values['city'][0]) + ")"
                query_sql += """ and city_level in {city}""".format(city=citys)
            # if values["channel"]:
            #     channels = tuple(str(c) for c in values["channel"])
            #     query_sql += """ and businessname in {channel}""".format(channel=channels)
            # if values["store_age"]:
            #     query_sql += """
            #     """

        # 从数据库查询
        data = DbUtil.query_list(query_sql, default_dbname)
        result = [{"areauid3": d[0], "areaname3": d[1], "areauid4": d[2], "areaname4": d[3], "storeuid": d[4],
                   "storename": d[5], "weeks": d[6], "rdate": datetime.strptime(str(d[7]), '%Y-%m-%d').date(),
                   "province": d[8], "province_name": d[9], "city": d[10], "city_name": d[11], "county": d[12],
                   "county_name": d[13], "businessname": d[14], "vctype": d[15], "areasize": d[16],
                   "billcount": d[17], "dealtotal": d[18], "rebillcount": d[19], "redealtotal": d[20],
                   "weather": d[21], "weather_desc": d[22], "temperature": d[23], "wind_direction": d[24],
                   "month": d[25], "year": d[26], "city_level": int(d[27])} for d in data]
        cache.set(str(values), result)
        return result


@app.callback(
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
    global_store(values)
    return values


def caculate_cards(card_datas, values):
    df = pd.DataFrame(card_datas)

    total_sale = round(df["dealtotal"].sum(), 2)
    # 假设当前月份为2021年2月份 取2021年1月份为 上月数据
    s_date = datetime.strptime('2021-01-01', '%Y-%m-%d').date()
    e_date = datetime.strptime('2021-01-31', '%Y-%m-%d').date()
    last_month_df = df[(df["rdate"] >= s_date) & (df["rdate"] < e_date)]
    last_month_total = round(last_month_df["dealtotal"].sum(), 2)

    # 同比 取去年当月数据
    tb_sdate = datetime.strptime('2020-01-01', '%Y-%m-%d').date()
    tb_edate = datetime.strptime('2020-01-31', '%Y-%m-%d').date()
    # 去年的数据
    tb_df = df[(df["rdate"] >= tb_sdate) & (df["rdate"] < tb_edate)]
    # 去年的总营业额
    tb_total_sale = round(tb_df["dealtotal"].sum(), 2)

    # 同比增长率计算 =（本期数－同期数）/同期数×100%
    tb_percentage = "%.2f%%" % round(
        ((last_month_total - tb_total_sale) / tb_total_sale * 100) if tb_total_sale > 0 else 0, 2)

    # 环比 取上月数据
    hb_sdate = datetime.strptime('2020-12-01', '%Y-%m-%d').date()
    hb_edate = datetime.strptime('2020-12-31', '%Y-%m-%d').date()

    # 上月数据
    hb_df = df[(df["rdate"] >= hb_sdate) & (df["rdate"] < hb_edate)]
    # 上月总营业额
    hb_total_sale = round(hb_df["dealtotal"].sum(), 2)

    # 环比增长率计算= （本期数-上期数）/上期数×100%。
    hb_percentage = "%.2f%%" % round(
        ((last_month_total - hb_total_sale) / hb_total_sale * 100) if hb_total_sale > 0 else 0, 2)
    # 本月销售额
    c_sdate = datetime.strptime('2021-02-01', '%Y-%m-%d').date()
    c_edate = datetime.strptime('2021-02-28', '%Y-%m-%d').date()
    c_month_df = df[(df["rdate"] >= c_sdate) & (df["rdate"] < c_edate)]
    c_month_total_sale = round(c_month_df["dealtotal"].sum(), 2)

    # 本月营业额与上月对比营业额 增长率 - 月增长率 =（本月营业额-上月营业额）/上月营业额*100%
    m_growth_rate = "%.2f%%" % round(
        ((c_month_total_sale - last_month_total) / last_month_total * 100) if last_month_total > 0 else 0, 2)

    # 近12月销售趋势
    group_df = df
    group_df["month"] = [x.strftime('%Y年%m月') for x in group_df["rdate"]]
    group_sales = pd.DataFrame(group_df.groupby(by="month", as_index=False)["dealtotal"].sum())

    # 封装结果数据
    return {"total_sale": total_sale, "last_month_total": last_month_total,
            "tb_percentage": tb_percentage, "hb_percentage": hb_percentage,
            "c_month_total_sale": c_month_total_sale, "m_growth_rate": m_growth_rate,
            "group_sales": group_sales}


@app.callback(Output('card_data', 'children'), Input('signal', 'data'))
def update_card_data(values):
    card_datas = global_store(values)
    if card_datas:
        # 封装结果数据
        result_datas = caculate_cards(card_datas, values)
        return build_layout_title_cards(result_datas, values)
    return build_layout_title_cards({}, values)


@app.callback(
    Output('fig_1', 'figure'),
    [
        Input('dw_fig_1_1', 'value'),
        Input('dw_fig_1_2', 'value'),
        Input('dw_fig_1_3', 'value'),
        Input('signal', 'data'),
    ])
def update_fig_1(index_type, dims_value, figure_type, values):
    # 获取缓存数据
    fig_datas = global_store(values)

    if fig_datas:
        df = pd.DataFrame(fig_datas)
        month_group_df = df
        month_group_df["month"] = [x.strftime('%Y年%m月') for x in month_group_df["rdate"]]
        # 默认根据战区及月份分组
        month_group_sales_df = pd.DataFrame(
            month_group_df.groupby(by=["areaname3", "month"], as_index=False)["dealtotal"].sum())
        fig = px.bar(month_group_sales_df, x="month", y="dealtotal", color="areaname3")
        if index_type == 2:
            # 添加平均线
            month_group_avg_df = pd.DataFrame(
                month_group_df.groupby(by="month", as_index=False)["dealtotal"].mean()
            )
            fig.add_trace(px.line(month_group_avg_df, x="month", y="dealtotal", line_group="areaname3"))
        elif index_type == 3:
            # 添加中位数线
            fig.add_trace()
        return fig
    return {}

# if __name__ == '__main__':
#     app.run_server(debug=True, port=8051)
