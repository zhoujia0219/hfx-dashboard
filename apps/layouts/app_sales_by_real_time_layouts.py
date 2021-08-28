from datetime import datetime
import plotly.graph_objs as go

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dateutil.relativedelta import relativedelta

from services.srv_comm_dim import get_week_map
from services.srv_sales_real_time import sale_total, shop_count, guest_orders, cost_price, dealtotal_plan_sales
from utils import date_util

###############
# 页面筛选初始值
###############
# 当前年月日
from utils.tools import big_number_conduct

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
sale_total_form = sale_total()  # 今日昨日销售额
shop_form = shop_count()  # 今日昨日门店数
guest_orders_form = guest_orders()  # 今日昨日客单量
cost_form = cost_price()  # 今日昨日的成本
sales_margin = [sale_total_form[0] - cost_form[0], sale_total_form[1] - cost_form[1]]  # 今日昨日的销售毛利
sales_margin_rate = [(sale_total_form[0] - cost_form[0]) / sale_total_form[0],
                     (sale_total_form[1] - cost_form[1]) / sale_total_form[1]]  # 今日昨日的毛利率

customer_transaction_form = [sale_total_form[0] / guest_orders_form[0],
                             sale_total_form[1] / guest_orders_form[1]]  # 今日昨日客单价

dealtotal_plan_sales_form = dealtotal_plan_sales()  # 本周本月的累计销售额/计划销售额


def pie_map_month_week(week_month):
    """
    本周本月的销售额/计划销售额饼图
    param week_month:week表示本周，month表示本月
    """
    index = 1 if week_month == "month" else 0
    fig = go.Figure(data=[go.Pie(
        labels=['完成', '计划'],
        values=[round(dealtotal_plan_sales_form[index][0], 2), round(dealtotal_plan_sales_form[index][1], 2)],
        hole=0.4,
        showlegend=False,
        textinfo='percent',
        hoverinfo="percent", )])
    fig.update_layout(
        width=120, height=80,
        paper_bgcolor="#dcdcdc",
        showlegend=False,
        margin=dict(t=5, l=5, b=5, r=5)
    )
    return fig


print(dealtotal_plan_sales_form[0][0], 333)
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
                                className="center-font",
                                children="本日销售额"
                            ),
                            width=6
                        ),
                        dbc.Col(
                            # width=6
                        ),
                        dbc.Col(
                            html.H4(
                                className="center-font",
                                children="门店总数"
                            ),
                            width=3
                        )]),
                    dbc.Row([
                        dbc.Col(
                            html.H3(
                                className="center-font",
                                children="￥{}".format(big_number_conduct(sale_total_form[0], 2)),
                                style={"color": "red"}
                            ),
                            width=6
                        ),
                        dbc.Col(
                            # width=6
                        ),
                        dbc.Col(
                            html.H3(
                                className="center-font",
                                children=" {}".format(format(shop_form[0], ',')),
                                style={"color": "red"}
                            ),
                            width=3
                        )], style={'text_align': 'center'}),
                    html.Hr(),  # todo 中间一点点的空白多了一根横线
                    dbc.Row([  # 第一个带有图的
                        dbc.Col(
                            [dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))),  # 这三个的目的是让文字不置顶
                                dbc.Row(dbc.Col(html.H4(
                                    className="center-font",
                                    children="本周累计销售额/计划"
                                ))),
                                dbc.Row(dbc.Col(html.H4(
                                    className="center-font",
                                    children="￥{}/￥{}".format(big_number_conduct(dealtotal_plan_sales_form[0][0], 2),
                                                              big_number_conduct(dealtotal_plan_sales_form[0][1], 2)
                                                              ),
                                    style={"color": "red"}
                                )))],
                            width=7
                        ),
                        dbc.Col(),
                        dbc.Col([
                            dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))),  # 这三个的目的是让图不置顶
                            dbc.Row(dbc.Col(
                                dcc.Graph(  # 本周累计销售额/计划图
                                    figure=pie_map_month_week("week"),
                                    style={"width": "100px", "height": "100px"}
                                )
                                ,
                                style={"backgroundColor": "#dcdcdc"},

                            )), ], width=4),
                    ], style={"backgroundColor": "#dcdcdc"}),
                    html.Hr(),  # todo 中间一点点的空白多了一根横线
                    dbc.Row([  # 第二个带有图的
                        dbc.Col(
                            [
                                dbc.Row(dbc.Col(html.H5(
                                    className="center-font",
                                    children="  "
                                ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))),  # 这三个的目的是让文字不置顶
                                dbc.Row(dbc.Col(html.H4(
                                    className="center-font",
                                    children="本月累计销售额/计划"
                                ))),

                                dbc.Row(dbc.Col(html.H4(
                                    className="center-font",
                                    children="￥{}/￥{}".format(big_number_conduct(dealtotal_plan_sales_form[1][0], 2),
                                                              big_number_conduct(dealtotal_plan_sales_form[1][1], 2)),
                                    style={"color": "red"}
                                )))],
                            width=7
                        ),
                        dbc.Col(
                            # width=6
                        ),
                        dbc.Col([
                            dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))), dbc.Row(dbc.Col(html.H5(
                                className="center-font",
                                children="  "
                            ))),  # 这三个的目的是让图不置顶
                            dbc.Row(dbc.Col(
                                dcc.Graph(  # 本月累计销售额/计划的饼图
                                    figure=pie_map_month_week("month"),
                                    style={"width": "100px", "height": "100px"}
                                )
                                ,
                                style={"backgroundColor": "#dcdcdc"},
                            ), ), ],
                            width=4
                        ),
                    ], style={"backgroundColor": "#dcdcdc", }),

                    # 表格
                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children=""
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="昨日同期"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="今日"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="上升/下降"
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="销售总额"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(sale_total_form[1], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(sale_total_form[0], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if sale_total_form[0] == sale_total_form[1] else (
                                        ("+" if sale_total_form[0] > sale_total_form[1] else "-") + "{}%".format(
                                    round(sale_total_form[0] / sale_total_form[1] / 100, 2))),
                                style={
                                    "backgroundColor": "red" if sale_total_form[0] > sale_total_form[1] else "green"} if
                                sale_total_form[0] != sale_total_form[1] else {}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="店均销售"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(round(sale_total_form[1] / shop_form[1], 2), 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(round(sale_total_form[0] / shop_form[0], 2), 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if round(sale_total_form[0] / shop_form[0], 2) == round(
                                    sale_total_form[1] / shop_form[1], 2) else (("+" if round(
                                    sale_total_form[0] / shop_form[0], 2) > round(sale_total_form[1] / shop_form[1],
                                                                                  2) else "-") + "{}%".format(round(
                                    round(sale_total_form[0] / shop_form[0], 2) / round(
                                        sale_total_form[1] / shop_form[1], 2) / 100, 2))),
                                style={
                                    "backgroundColor": "red" if round(sale_total_form[0] / shop_form[0], 2) > round(
                                        sale_total_form[1] / shop_form[1], 2) else "green"} if round(
                                    sale_total_form[0] / shop_form[0], 2) != round(sale_total_form[1] / shop_form[1],
                                                                                   2) else {}

                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="客单量"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(guest_orders_form[1], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(guest_orders_form[0], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if guest_orders_form[0] == guest_orders_form[1] else (
                                        ("+" if guest_orders_form[0] > guest_orders_form[1] else "-") + "{}%".format(
                                    round(guest_orders_form[0] / guest_orders_form[1] / 100, 2))),
                                style={
                                    "backgroundColor": "red" if guest_orders_form[0] > guest_orders_form[
                                        1] else "green"} if
                                guest_orders_form[0] != guest_orders_form[1] else {}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="客单价"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(round(customer_transaction_form[1], 2), 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(round(customer_transaction_form[0], 2), 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if customer_transaction_form[0] == customer_transaction_form[1] else (
                                        ("+" if customer_transaction_form[0] > customer_transaction_form[
                                            1] else "-") + "{}%".format(
                                    round(customer_transaction_form[0] / customer_transaction_form[1] / 100, 2))),
                                style={
                                    "backgroundColor": "red" if customer_transaction_form[0] >
                                                                customer_transaction_form[1] else "green"} if
                                customer_transaction_form[0] != customer_transaction_form[1] else {}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="销售毛利"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(sales_margin[1], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(big_number_conduct(sales_margin[0], 2))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if sales_margin[0] == sales_margin[1] else (
                                        ("+" if sales_margin[0] > sales_margin[1] else "-") + "{}%".format(
                                    round(sales_margin[0] / sales_margin[1] / 100, 2))),
                                style={
                                    "backgroundColor": "red" if sales_margin[0] > sales_margin[1] else "green"} if
                                sales_margin[0] != sales_margin[1] else {}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="毛利率"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}%".format(format(round(sales_margin_rate[1], 2), ','))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}%".format(format(round(sales_margin_rate[0], 2), ','))
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if sales_margin_rate[0] == sales_margin_rate[1]
                                else (
                                        ("+" if sales_margin_rate[0] > sales_margin_rate[1] else "-")
                                        + "{}%".format(round(sales_margin_rate[0] / sales_margin_rate[1] / 100, 2))),
                                style={
                                    "backgroundColor": "red" if sales_margin_rate[0] > sales_margin_rate[
                                        1] else "green"} if sales_margin_rate[0] != sales_margin_rate[1] else {}
                            ),
                            width=3
                        )
                    ]),
                    html.Hr(),

                    dbc.Row([
                        dbc.Col(
                            html.H5(
                                children="门店数"
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(format(shop_form[1], ',')),
                                style={"color": "#dcdcdc"}
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="{}".format(format(shop_form[0], ',')),
                            ),
                            width=3
                        ),
                        dbc.Col(
                            html.H5(
                                children="0%" if shop_form[0] == shop_form[1] else (
                                        ("+" if shop_form[0] > shop_form[1] else "-") + "{}%".format(
                                    round(shop_form[0] / shop_form[1] / 100, 2))),
                                style={"backgroundColor": "red" if shop_form[0] > shop_form[1] else "green"} if
                                shop_form[0] != shop_form[1] else {}
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

            html.Div(dbc.Row([
                dbc.Col(html.H5(
                    children='本日销售分析',
                    className='media-body',
                    style={'min-width': '150px'}
                ),
                    width=3
                ),
                dbc.Col(),
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id="x_choice_time",
                            style={'width': 120},
                            options=[{'label': '5-15', 'value': '5-15'},
                                     {'label': '12-18', 'value': '12-18'},
                                     {'label': '18-24', 'value': '18-24'}],
                            value='5-15',
                            searchable=False,
                            clearable=False
                        ),
                    ],
                        className='media-left block-inline'),
                    width=3
                )
            ])),

            # 画图 - 日销售分布
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            id='loading_sales_day',
                            type='circle',
                            children=[
                                dcc.Graph(  # 日销售分布图
                                    id='sales_real_time_day',
                                    style={'height': '400px', 'width': '1200px'}
                                )
                            ], ), ), ),
            ], ),

            html.Div(dbc.Row([
                dbc.Col(
                    html.H5(
                        children='本月销售分析',
                        className='media-body',
                        style={'min-width': '150px'}
                    ),
                    width=3
                ),
                dbc.Col(),

                html.Div(dbc.Row([
                    dbc.Col(
                        dcc.RadioItems(
                            id="total_avg_mid",
                            options=[{'label': '总额  ', 'value': 'ZE'},
                                     {'label': '平均数  ', 'value': 'PJS'},
                                     {'label': '中位数  ', 'value': 'ZWS'}],
                            value='ZE',
                        )
                        ,
                        width=3
                    ),
                    dbc.Col(
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
                        ],
                            className='media-left block-inline'),
                        width=3
                    ),
                    dbc.Col(dcc.Dropdown(
                        id="map_index2",
                        style={'width': 120},
                        options=[{'label': "图形样式：折线图", 'value': "b"}],
                        value='b',
                        searchable=False,
                        clearable=False
                    ))
                ])),

                # dbc.Col(
                #     html.Div(
                #         children=[
                #             # 单选框
                #             dcc.RadioItems(
                #                 id="total_avg_mid",
                #                 options=[{'label': '总额  ', 'value': 'ZE'},
                #                          {'label': '平均数  ', 'value': 'PJS'},
                #                          {'label': '中位数  ', 'value': 'ZWS'}],
                #                 value='ZE',
                #             ),
                #
                #             # 下拉框
                #             html.Div([
                #                 dcc.Dropdown(
                #                     id="range_choice",
                #                     style={'width': 120},
                #                     options=[
                #                         {'label': '本月', 'value': 'by'},
                #                         {'label': '最近30天', 'value': 'zj'}
                #                     ],
                #                     value='by',
                #                     searchable=False,
                #                     clearable=False
                #                 ),
                #                 dcc.Dropdown(
                #                     id="map_index2",
                #                     style={'width': 120},
                #                     options=[{'label': "图形样式：折线图", 'value': "b"}],
                #                     value='b',
                #                     searchable=False,
                #                     clearable=False
                #                 ),
                #             ], className='media-right block-inline'
                #             ),
                #         ], className='media flex-wrap ',
                #         style={'alignItems': 'flex-end'}
                #     ),
                #     width=3
                # )
            ])),

            # html.H5(children='本月销售分析', className='media-body', style={'min-width': '150px'}),
            # # 用户选项
            # html.Div(
            #     children=[
            #         # 单选框
            #         dcc.RadioItems(
            #             id="total_avg_mid",
            #             options=[{'label': '总额', 'value': 'ZE'},
            #                      {'label': '平均数', 'value': 'PJS'},
            #                      {'label': '中位数', 'value': 'ZWS'}],
            #             value='ZE',
            #         ),
            #         # 下拉框
            #         html.Div([
            #             dcc.Dropdown(
            #                 id="range_choice",
            #                 style={'width': 120},
            #                 options=[
            #                     {'label': '本月', 'value': 'by'},
            #                     {'label': '最近30天', 'value': 'zj'}
            #                 ],
            #                 value='by',
            #                 searchable=False,
            #                 clearable=False
            #             ),
            #             dcc.Dropdown(
            #                 id="map_index2",
            #                 style={'width': 120},
            #                 options=[{'label': "图形样式：折线图", 'value': "b"}],
            #                 value='b',
            #                 searchable=False,
            #                 clearable=False
            #             ),
            #         ], className='media-right block-inline'
            #         ),
            #     ], className='media flex-wrap ',
            #     style={'alignItems': 'flex-end'}
            # ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            id='loading_sales_month',
                            type='circle',
                            children=[
                                dcc.Graph(  # 月销售分布图
                                    id='sales_real_time_month',
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
    className='content-style ',
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
