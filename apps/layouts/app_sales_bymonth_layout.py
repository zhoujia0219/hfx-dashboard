from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dateutil.relativedelta import relativedelta
import plotly.express as px

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from services import srv_sales_bymonth
from services.srv_comm_dim import get_dim_graph_agg, get_dim_graph_cate, \
    get_dim_graph_type, get_dim_order_type, get_dim_graph_four, get_dim_graph_scatter, \
    get_dim_graph_scatter_x, get_dim_graph_scatter_y, get_dim_graph_map_limits, get_dim_graph_map_index
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
        html.P(children="可通过条件筛选过滤数据，也可以改变维度和图形样式", className="small", style={'color': 'gray'}),
        html.Div([
            filter_date_range.filter_month_range(date_range, start_month, stop_month),
            filter_city_level.filter_city_level(),
            filter_channels.filter_channels(),
            filter_store_age.filter_store_age(),
            filter_store_area.filter_store_area(),
            filter_store_star.filter_store_star(),
            dbc.Button(children='重新计算', id='f_submit', color="primary", className="mt-3", block=True),
        ]),
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

# 战区分析 -- dengxiaohu
c_fig_01 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(children='销售额分析', className='media-body', style={'min-width': '150px'}),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="cate_choice",
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_cate().items()],
                                value='businessname',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                            dcc.Dropdown(
                                id='agg_choice',
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_agg().items()],
                                value='dff.sum()',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                            dcc.Dropdown(
                                id='graph_choice',
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_type().items()],
                                value='px.bar',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                        ],
                        className='media-right block-inline')
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 图
            dcc.Loading(id='loading-1',
                        type='circle',
                        children=[dcc.Graph(id="graph_out_qs")],
                        style={'width': '1022px', 'height': '450px'}),

            # 用户选项
            html.Div(
                children=[
                    html.H5(children='单月分析', className='media-body', style={'min-width': '150px'}),
                    html.Div(children=[
                        dcc.Dropdown(
                            id="x_choice_1",
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_cate().items()],
                            value='businessname',
                            searchable=False, clearable=False, style={'width': 120}
                        ),
                        dcc.Dropdown(
                            id='cate_choice_1',
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_cate().items()],
                            value='areaname3',
                            searchable=False, clearable=False, style={'width': 120}
                        ),
                        dcc.Dropdown(
                            id='agg_choice_1',
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_agg().items()],
                            value='dff.sum()',
                            searchable=False, clearable=False, style={'width': 120}
                        ),
                    ],
                        className='media-right block-inline')
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 图
            dcc.Loading(id='loading-2',
                        type='circle',
                        children=[dcc.Graph(id="graph_out_dy")],
                        style={'width': '1022px', 'height': '450px'}),

            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Span('最近更新:'),
                            html.Span('2021-07-23 12:30:00', id="sales_update_time")
                        ],
                        className='media-body'
                    ),
                    html.Div(
                        children=dbc.Button(children='立即刷新',
                                            color='secondary',
                                            className='mr-1',
                                            size='sm',
                                            id='btn_sales_update',
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

# 所属城市级别
c_fig_02 = dbc.Card(
    children=dbc.CardBody(
        children=[

            # 用户选项
            html.Div(
                children=[
                    html.H5(children='销售额分析', className='media-body', style={'min-width': '150px'}),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="x_choice_2",
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_cate().items()],
                                value='businessname',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                            dcc.Dropdown(
                                id='cate_choice_2',
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_cate().items()],
                                value='areaname3',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                            dcc.Dropdown(
                                id='agg_choice_2',
                                options=[{'label': x, 'value': y} for x, y in get_dim_graph_type().items()],
                                value='dff.sum()',
                                searchable=False, clearable=False, style={'width': 120}
                            ),
                        ],
                        className='media-right block-inline')
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 图
            dcc.Loading(id='loading-3',
                        type='circle',
                        children=[dcc.Graph(id='graph_out_wd')],
                        style={'width': '1022px', 'height': '450px'}),

            html.Hr(),
            html.Div(
                children=[
                    html.Div(children='最近更新: 2021-07-23 12:30:00', className='media-body'),
                    html.Div(
                        children=dbc.Button(children='立即刷新',
                                            color='secondary',
                                            className='mr-1',
                                            size='sm',
                                            id='btn_city_update',
                                            n_clicks=0)
                    ),
                ],
                className='media flex-wrap align-items-center'),
        ]
    ),
    style={"width": "100%"}
)

# 战区排名
c_fig_03 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(children='销售额-战区排名', className='media-body'),
                    html.Div([
                        dcc.Dropdown(
                            id='choices_top_order',
                            options=get_dim_order_type(),
                            value=2,
                            searchable=False,
                            clearable=False,
                            style={'width': 120}
                        ),
                        dcc.Dropdown(
                            id='choices_top_month',
                            options=[{"label": x, "value": x} for x in date_range],
                            value=stop_month,
                            searchable=False,
                            clearable=False,
                            style={'width': 100}
                        ),
                    ], className='media-right block-inline')
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 图
            dcc.Loading(id='loading-4',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_top")
                        ],
                        style={'width': '460px', 'height': '450px'}),

            html.Hr(),
            html.Div(
                children=[
                    html.Div(children='最近更新: 2021-07-23 12:30:00', className='media-body'),
                    html.Div(
                        children=dbc.Button(
                            children='立即刷新',
                            color='secondary',
                            className='mr-1',
                            size='sm',
                            id='button-3',
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

# 不同维度间销售额分析
c_fig_04 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(children='销售额分析',
                            className='media-body',
                            style={'min-width': '150px'}
                            ),
                    html.Div([
                        dcc.Dropdown(
                            id="x_choice_3",
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_four().items()],
                            value=['businessname', 'areaname4', 'areasize', 'star'],
                            multi=True,
                            searchable=False,
                            clearable=False
                        ),
                    ],
                        className='media-right block-inline')
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 画图 - 柱状图
            dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            id='loading_one',
                            type='circle',
                            children=[
                                dcc.Graph(
                                    id='graph_out_one',
                                    style={'height': '320px', 'width': '500px'}
                                )
                            ], ), ), ),
                dbc.Col(html.Div(
                    dcc.Loading(
                        id='loading_two',
                        type='circle',
                        children=[
                            dcc.Graph(
                                id='graph_out_two',
                                style={'height': '320px', 'width': '500px'}
                            )
                        ], ), ), ),
            ], ),
            dbc.Row([
                dbc.Col(html.Div(
                    dcc.Loading(
                        id='loading_three',
                        type='circle',
                        children=[
                            dcc.Graph(
                                id='graph_out_three',
                                style={'height': '320px', 'width': '500px'}
                            )
                        ], ), ), ),
                dbc.Col(html.Div(
                    dcc.Loading(
                        id='loading_four',
                        type='circle',
                        children=[
                            dcc.Graph(
                                id='graph_out_four',
                                style={'height': '320px', 'width': '500px'}
                            )
                        ], ), ), )
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
                    id='3',
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

# 销售分析气泡图
c_fig_05 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5('单月销售单价与数额之间的分析', className='media-body', style={'min-width': '150px'}),
                    html.Div([
                        dcc.Dropdown(
                            id="option_x",
                            style={'width': 120},
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_scatter_x().items()],
                            value='price',
                            searchable=False,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id="option_y",
                            style={'width': 120},
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_scatter_y().items()],
                            value='billcount',
                            searchable=False,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id="option_other",
                            style={'width': 120},
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_scatter().items()],
                            value='county_name',
                            searchable=False,
                            clearable=False
                        ),
                    ], className='media-right block-inline'
                    ),
                ], className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),

            # 画图 - 气泡图
            dcc.Loading(
                id='loading_scatter',
                type='circle',
                children=[
                    dcc.Graph(
                        id="graph_billcount"
                    )
                ],
                style={'width': '1022px', 'height': '450px'}
            ),
            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Span('最近更新:'),
                            html.Span('2021-07-23 12:30:00',
                                      id="billcount_update_time")
                        ], className='media-body'
                    ),
                    html.Div(dbc.Button(
                        children='立即刷新',
                        id='billcount_update_button',
                        color='secondary',
                        className='mr-1',
                        size='sm',
                        n_clicks=0)),
                ], className='media flex-wrap align-items-center'
            ),
        ]
    ), style={"width": "100%"}
)

# 销售分布地理图
c_fig_06 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5('销售分布地理图', className='media-body', style={'min-width': '150px'}),
                    html.Div([
                        dcc.Dropdown(
                            id="map_limits",
                            style={'width': 120},
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_map_limits().items()],
                            value='ad_name',
                            searchable=False,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id="map_index",
                            style={'width': 120},
                            options=[{'label': x, 'value': y} for x, y in get_dim_graph_map_index().items()],
                            value='sales',
                            searchable=False,
                            clearable=False
                        ),
                    ], className='media-right block-inline'
                    ),
                ], className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 画图 - 地理图
            dcc.Loading(
                id='map_loading',
                children=[
                    dcc.Graph(
                        id="map_graph"
                    )
                ],
                style={'width': '1022px', 'height': '450px'}
            ),
            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Span('最近更新:'),
                            html.Span('2021-08-20 17:00:00',
                                      id="map_update_time")
                        ], className='media-body'
                    ),
                    html.Div(dbc.Button(
                        children='立即刷新',
                        id='map_update_button',
                        color='secondary',
                        className='mr-1',
                        size='sm',
                        n_clicks=0)),
                ], className='media flex-wrap align-items-center'
            ),
        ]
    ), style={"width": "100%"}
)


def sale_day_fig(data_x, data_y):
    """
    销售日数据
    :param data_x:
    :param data_y:
    :param data_sum: pic_dff.sum()
    :return:
    """
    pic = srv_sales_bymonth.sales_day()
    if len(pic) < 1:
        return dash.no_update
    if data_x == data_y:
        return dash.no_update
    pic_dff = pic.groupby([data_x], as_index=False)['sale'].sum()

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
    return fig


# 本日本月销售分布
c_fig_sales_day_month = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 画图 - 销售分布
            html.H5('销售分布', className='media-body', style={'min-width': '150px'}),
            dbc.Row([
                html.H6(children='本日销售分布', className='media-body', style={'min-width': '150px'}),
                dbc.Col(
                    html.Div(
                        dcc.Loading(
                            id='loading_sales_day',
                            type='circle',
                            children=[
                                dcc.Graph(
                                    id='sales_day',
                                    figure=sale_day_fig("times", "sale"),  # 画图
                                    style={'height': '400px', 'width': '1000px'}
                                )
                            ], ), ), ),

                html.H6(children='本月销售分析', className='media-body', style={'min-width': '150px'}),

                # 用户选项
                html.Div(
                    children=[
                        # 标题和单选框
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
                                options=[{'label': '本月', 'value': 'by'},
                                         {'label': '最近30天', 'value': 'zj'}],
                                value='by',
                                searchable=False,
                                clearable=False
                            ),
                            dcc.Dropdown(
                                id="map_index2",
                                style={'width': 120},
                                options=[{'label': "b", 'value': "b"}],
                                value='b',
                                searchable=False,
                                clearable=False
                            ),
                        ], className='media-right block-inline'
                        ),
                    ], className='media flex-wrap ',
                    style={'alignItems': 'flex-end'}
                ),

                html.Hr(),
                dbc.Col(html.Div(
                    dcc.Loading(
                        id='loading_sales_month',
                        type='circle',
                        children=[
                            dcc.Graph(
                                id='sales_month',
                                style={'height': '400px', 'width': '1000px'}
                            )
                        ], ), ), ),
            ], ),

            html.Hr(),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Span('最近更新:'),
                            html.Span('{}'.format(str(datetime.now())[:19]),
                                      id="map_update_time2")
                        ], className='media-body'
                    ),
                    html.Div(dbc.Button(
                        children='立即刷新',
                        id='map_update_button2',
                        color='secondary',
                        className='mr-1',
                        size='sm',
                        n_clicks=0)),
                ], className='media flex-wrap align-items-center'
            ),
        ]
    ), style={"width": "100%"}
)
content = html.Div(
    className='content-style',
    children=[
        dbc.Row(id="card_data", children=card_list),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(children=c_fig_01),
                        dbc.Row(children=c_fig_02, className='mt-3'),
                        dbc.Row(children=c_fig_04, className='mt-3'),
                        dbc.Row(children=c_fig_05, className='mt-3'),
                        dbc.Row(children=c_fig_06, className='mt-3'),
                        dbc.Row(children=c_fig_sales_day_month, className='mt-3'),  # 本日本月的销售分布
                    ],
                    width=8
                ),
                dbc.Col(c_fig_03, width=4),
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
    ]
)
