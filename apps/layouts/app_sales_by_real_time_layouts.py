from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas
from dateutil.relativedelta import relativedelta
import plotly.express as px

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from services import srv_sales_real_time
from services.srv_comm_dim import get_day_hour, get_week_map
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

###############
# sidebar
###############

# 侧边栏
sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4(children="门店月度销售分析"),
        html.Hr(),
        # html.P(children="可通过条件筛选过滤数据，也可以改变维度和图形样式", className="small", style={'color': 'gray'}),
        # html.Div([
        #     filter_date_range.filter_month_range(date_range, start_month, stop_month),
        #     filter_city_level.filter_city_level(),
        #     filter_channels.filter_channels(),
        #     filter_store_age.filter_store_age(),
        #     filter_store_area.filter_store_area(),
        #     filter_store_star.filter_store_star(),
        #     dbc.Button(children='重新计算', id='f_submit', color="primary", className="mt-3", block=True),
        # ]),
    ],
)

###############
# content
###############
card_list = [
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    html.H6(children="总销售额"),
                    html.H4(
                        children=[
                            html.Span(children='￥'),
                            html.Span(children=['0.00'], id='total_sales'),
                            html.Span(children='M')
                        ],
                        id='total_sale_title',
                        style={"color": "darkred"}
                    ),
                    html.Label(
                        children=[
                            html.Span(
                                children=[start_month],
                                id="total_sales_start_month"
                            ),
                            html.Span(children=" - "),
                            html.Span(
                                children=[stop_month],
                                id="total_sales_stop_month"
                            ),
                        ],
                        id="total_sale_label"
                    ),
                ]
            ),
            className='title-card'
        ),
        className='title-col mr-2'
    ),
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    html.H6(children="上月销售额"),
                    html.H4(
                        children=[
                            html.Span(children='￥'),
                            html.Span(children=['0.00'], id='last_month_sales'),
                            html.Span(children='M')],
                        id='last_month_title',
                        style={"color": "darkred"}
                    ),
                    html.Label(
                        children=[
                            html.Span(children="同比: "),
                            html.Span(children=['0.00%'], id="last_month_tb"),
                            html.Span(children="  环比： "),
                            html.Span(children=['0.00%'], id="last_month_hb")
                        ],
                        id="last_month_label"
                    ),
                ]
            ),
            className='title-card'
        ),
        className='title-col mr-2'
    ),
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    html.H6(
                        children=[
                            html.Span(children="本月销售额"),
                            html.Span(children="("),
                            html.Span(children=[stop_month], id="current_month_sign"),
                            html.Span(children=")")
                        ]
                    ),

                    html.H4(
                        children=[
                            html.Span(children='￥'),
                            html.Span(children=['0.00'], id="current_month_sales"),
                            html.Span(children='M')
                        ],
                        id='current_month_title',
                        style={"color": "darkred"}
                    ),

                    html.Label(
                        children=[
                            html.Span(children="增长率："),
                            html.Span(children=["0.00%"], id="growth_rate")
                        ],
                        id="current_month_label"
                    ),
                ]
            ),
            className='title-card'
        ),
        className='title-col mr-2'
    ),
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    html.H6(
                        children=[
                            html.Span(children="近12月销售趋势"),
                            html.Span(children="("),
                            html.Span(children=[start_month], id="group_start_month"),
                            html.Span(children=" - "),
                            html.Span(children=[stop_month], id="group_end_month"),
                            html.Span(children=")")
                        ],
                        id="month_group_title"
                    ),
                    dcc.Graph(id='graph_month_group', style={"height": "60px"}),
                ]
            ),
            className='title-card'
        ),
        className='title-col col-5',
        style={'paddingRight': 15}
    ),
]


def sale_day_fig(data_x, data_y):
    """
    销售日数据
    :param data_x:
    :param data_y:
    :param data_sum: pic_dff.sum()
    :return:
    """
    pic = srv_sales_real_time.sales_day()
    if len(pic) < 1:
        return dash.no_update
    if data_x == data_y:
        return dash.no_update
    pic_dff = pic.groupby([data_x], as_index=False)['sale'].sum()
    empty_pic = pandas.DataFrame(get_day_hour(), columns=["times", "sale"])
    pic_dff = pandas.concat([empty_pic, pic_dff])
    fig = px.bar(
        pic_dff,
        x=data_x,
        y='sale',
        color='sale',
        barmode='group',
        template='plotly_white',
        labels={'sale': '总销售额', 'times': '时间点'},
    )
    fig.update_traces(textposition='inside')
    axis = [i for i in range(1, 24)]
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=axis,
            ticktext=axis
        ))
    return fig


left_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    dbc.Row(  # 顶上日期
                        dbc.Col(
                            html.Span(children="{}".format(
                                datetime.now().strftime("%Y-%m-%d") + " " + get_week_map()[
                                    datetime.now().isoweekday()])),
                            style={"color": "#dcdcdc"},
                            width=6
                        )),
                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="本日销售额"
                            ),
                            width=6
                        ),
                        dbc.Col(
                            html.H4(
                                children="门店总数"
                            ),
                            width=3
                        )]),
                    dbc.Row([
                        dbc.Col(
                            html.H3(
                                children="￥200000000",
                                style={"color": "red"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            html.H3(
                                children="3500",
                                style={"color": "red"}
                            ),
                            width=3
                        )]),
                    html.Hr(),  # todo 中间一点点的空白多了一根横线
                    dbc.Row([  # 第一个带有图的
                        dbc.Col(
                            [dbc.Row(dbc.Col(html.H5(
                                children="本周累计销售额/计划"
                            ))),

                                dbc.Row(dbc.Col(html.H5(
                                    children="￥200000000/￥200000000",
                                    style={"color": "red"}
                                )))],
                            width=6
                        ),

                        dbc.Col(
                            html.H5(  # 图
                                children="画图"
                            ),
                            width=6
                        ),
                    ], style={"backgroundColor": "#dcdcdc"}),
                    html.Hr(),  # todo 中间一点点的空白多了一根横线
                    dbc.Row([  # 第二个带有图的
                        dbc.Col(
                            [dbc.Row(dbc.Col(html.H5(
                                children="本月累计销售额/计划"
                            ))),

                                dbc.Row(dbc.Col(html.H5(
                                    children="￥200000000/￥200000000",
                                    style={"color": "red"}
                                )))],
                            width=6
                        ),

                        dbc.Col(
                            html.H5(  # 图
                                children="画图"
                            ),
                            width=6
                        ),
                    ], style={"backgroundColor": "#dcdcdc"}),

                    # 表格
                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children=""
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="昨日同期"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="今日"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="上升/下降"
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="销售总数"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="90000"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="99999"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="+10%",
                                style={"backgroundColor": "red"}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="店均销售"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="3000"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="3300"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="+1%",
                                style={"backgroundColor": "red"}

                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="客单量"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="300"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="280"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="-10%",
                                style={"backgroundColor": "green"}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="客单价"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="34.5"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="34.5"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="0%"
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="销售毛利"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="450.0"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="460"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="5%",
                                style={"backgroundColor": "red"}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="毛利率"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="12%"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="11%"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="-5%",
                                style={"backgroundColor": "green"}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H4(
                                children="门店数"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="3500",
                                style={"color": "#dcdcdc"}
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="3500"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H4(
                                children="+2%",
                                style={"backgroundColor": "red"}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),
                    # todo
                ],
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
        ]
    ),
    style={"width": "100%"}
)

# 本日本月销售分布
c_fig_sales_day_month = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(
                        children='销售分布',
                        className='media-body',
                        style={'min-width': '150px'}
                    ),
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            html.H6(
                children='本日销售分析',
                className='media-body',
                style={'min-width': '150px'}
            ),
            html.Div([
                dcc.Dropdown(
                    id="x_choice_3",
                    style={'width': 120},
                    options=[{'label': '5-12', 'value': 'time1'},
                             {'label': '12-18', 'value': 'time1'},
                             {'label': '18-5', 'value': 'time2'}],
                    value='time1',
                    searchable=False,
                    clearable=False
                ),
            ],
                className='media-left block-inline'),
            # 画图 - 日销售分布
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            id='loading_sales_day',
                            type='circle',
                            children=[
                                dcc.Graph(
                                    id='sales_day',
                                    figure=sale_day_fig("times", "sale"),  # 画图
                                    style={'height': '400px', 'width': '1200px'}
                                )
                            ], ), ), ),
            ], ),
            html.H6(children='本月销售分析', className='media-body', style={'min-width': '150px'}),
            # 用户选项
            html.Div(
                children=[
                    # 单选框
                    dcc.RadioItems(
                        id="total_avg_mid",
                        options=[{'label': '总额', 'value': 'ZE'},
                                 {'label': '平均数', 'value': 'PJS'},
                                 {'label': '中位数', 'value': 'ZWS'}],
                        value='ZE',
                    ),
                    # 下拉框
                    html.Div([
                        dcc.Dropdown(
                            id="range_choice",
                            style={'width': 120},
                            options=[
                                {'label': '本月', 'value': 'by'},
                                {'label': '最近30天', 'value': 'zj'}
                            ],
                            value='by',
                            searchable=False,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id="map_index2",
                            style={'width': 120},
                            options=[{'label': "图形样式：柱状图", 'value': "b"}],
                            value='b',
                            searchable=False,
                            clearable=False
                        ),
                    ], className='media-right block-inline'
                    ),
                ], className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            dbc.Row([
                dbc.Col(html.Div(
                    dcc.Loading(
                        id='loading_sales_month',
                        type='circle',
                        children=[
                            dcc.Graph(  # 月销售分布图
                                id='sales_month',
                                style={'height': '400px', 'width': '1200px'}
                            )
                        ], ), ), ),
            ], ),

            html.Hr(),
            html.Div([
                html.Div(children='最近更新: 2021-07-23 12:30:00',
                         className='media-body'),
                html.Div(children=dbc.Button(
                    children='立即刷新',
                    color='secondary',
                    className='mr-1',
                    size='sm',
                    id='map_update_button3',
                    n_clicks=0
                )
                ),
            ],
                className='media flex-wrap align-items-center'
            ),
        ]
    ),
    style={"width": "100%"}
)

content = html.Div(
    className='content-style',
    children=[
        # dbc.Row(id="card_data", children=card_list),
        dbc.Row(
            children=[
                dbc.Col(left_table, width=4),

                dbc.Col(
                    children=[
                        dbc.Row(children=c_fig_sales_day_month, className='mt-3'),  # 本日本月的销售分布
                    ],
                    width=8  # 控制整个块的区域
                ),
            ],
            className='mt-3'),
    ],
)

###############
# 页面布局
###############

layout = html.Div(
    children=[
        sidebar,
        content,
        # signal value to trigger callbacks
        dcc.Store(id='signal')
    ],
    style={"width": "100%"}
)
