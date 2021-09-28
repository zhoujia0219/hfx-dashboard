from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dateutil.relativedelta import relativedelta

from apps.components import filter_channels
from apps.components import filter_city_level
from apps.components import filter_date_range
from apps.components import filter_store_age
from apps.components import filter_store_area
from apps.components import filter_store_star
from services.srv_comm_dim import get_dim_graph_agg, get_dim_graph_cate, \
    get_dim_graph_type, get_dim_order_type, get_dim_graph_four, get_dim_graph_scatter, \
    get_dim_graph_scatter_x, get_dim_graph_scatter_y, get_dim_graph_map_limits, get_dim_graph_map_index
from utils import date_util

import pandas as pd

###############
# 页面筛选初始值
###############
today = datetime.now()
# 格式化日期
today_str = today.strftime("%Y-%m-%d") + " " + date_util.get_week_day(today)

###############
# sidebar
###############

# 侧边栏


###############
# content
###############
top_cards = [
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        dbc.Row(
                            children=html.Label(children=today_str, id="total_date")),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.H6(children='本日自检报告数'),
                                        html.H4(
                                            children=[
                                                html.Span(children='5000', id="report_count"),
                                            ],
                                            id='total_report_count',
                                            style={"color": "darkred"}
                                        ),
                                    ]),
                                dbc.Col(children=[
                                    html.H6(children='月期初门店数'),
                                    html.H4(
                                        children=[
                                            html.Span(children='350', id="store_count"),
                                        ],
                                        id='total_store_count',
                                        style={"color": "darkred"}
                                    ),
                                ]),
                                dbc.Col(children=[
                                    html.H6(children='当前任务数量'),
                                    html.H4(
                                        children=[
                                            html.Span(children='3', id="task_count"),
                                        ],
                                        id='total_task_count',
                                        style={"color": "darkred"}
                                    ),
                                ]),
                            ]),
                    ]
                ),
                style={"height": "270px"}
            ),
        ],

    ),
    dbc.Col(
        children=
        dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Row(
                        children=html.Span(children="已结束",
                                           id="closed_status",
                                           className="label label-default",
                                           style={
                                               "borderRadius": "5px",
                                               "backgroundColor": "#D7D7D7",
                                               "padding": "5px"
                                           }
                                           )
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    html.P(children=["开市自检9月1日-9月30日"]),
                                    html.P(
                                        children=[
                                            html.Span(children="应完成自检数: "),
                                            html.Span(children=3500)
                                        ]),
                                    html.P(
                                        children=[
                                            html.Span(children="已完成: "),
                                            html.Span(children=2000)
                                        ]),
                                ]
                            ),
                            dbc.Col(
                                children=[
                                    dcc.Graph(id='graph_close_rate'),
                                ]
                            )
                        ]
                    )

                ]
            ),
            style={"height": "270px"}
        )
    ),
    dbc.Col(
        children=
        dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Row(
                        children=html.Span(children="进行中",
                                           id="pending_status",
                                           style={
                                               "borderRadius": "5px",
                                               "backgroundColor": "#70B603",
                                               "padding": "5px",
                                               "color": "#FFFFFF"
                                           }
                                           )
                    ),

                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    html.P(children="开市自检9月1日-9月30日"),
                                    html.P(children="应完成自检数: 3500"),
                                    html.P(children="已完成： 500"),
                                ]
                            ),

                            dbc.Col(
                                children=[
                                    dcc.Graph(id='graph_pending_rate',
                                              style={"height": "260px"}),
                                ]
                            )
                        ]
                    )

                ]),
            style={"height": "270px"}

        )
    ),
    dbc.Col(
        children=
        dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Row(
                        children=html.Span(children="未开始",
                                           id="not_yet_status",
                                           className="label label-default",
                                           style={
                                               "borderRadius": "5px",
                                               "backgroundColor": "#A9A9A9",
                                               "padding": "5px"
                                           }
                                           )
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    html.P(children="开市自检9月1日-9月30日"),
                                    html.P(children=[
                                        "应完成自检数: ", html.Code(id="", children="3500")
                                    ]),
                                    html.P(children=[
                                        "已完成：", html.Code(id="", children="0")
                                    ]),
                                ]
                            ),
                            dbc.Col(
                                children=[
                                    dcc.Graph(id='graph_not_yet_rate'),
                                ]
                            )
                        ])

                ]),
            style={"height": "270px"}
        )
    ),
]

# 月度自检完成情况
month_finish_detail_graph = [
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Graph(id="graph_month_finish")
                            ]
                        )
                    ]
                )
            )

        ]
    ),
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        html.Br(),
                        html.Br(),

                        dbc.Col(
                            children=[
                                html.H6(children=[
                                    html.Span(children="应完成报告数:"),
                                    html.Span(id="month_finish_report_count", children="10000"),
                                ]),
                                html.H6(children=[
                                    html.Span(children="已完成:"),
                                    html.Span(id="month_finished", children="10000"),
                                ]),
                                dbc.Progress(id="month_finished_process", children="35%", value=35)
                            ]
                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),

                        dbc.Col(
                            children=[
                                html.H6(children=[
                                    html.Span(children="点评报告数:"),
                                    html.Span(id="month_remarks_report_count", children="10000"),
                                ]),
                                html.H6(children=[
                                    html.Span(children="点评率:"),
                                    html.Span(id="month_remarks_rate", children="88.8%"),
                                ]),
                                dbc.Progress(id="month_remarks_rate_process", children="88.8%", value=88.8)
                            ]
                        ),

                        html.Br(),
                        html.Br(),
                        html.Br(),

                        dbc.Col(
                            children=[
                                html.H6(children=[
                                    html.Span(children="点评报告数:"),
                                    html.Span(id="month_remarks_report_count_2", children="10000"),
                                ]),
                                html.H6(children=[
                                    html.Span(children="合格数:"),
                                    html.Span(id="month_remarks_report_pass_count", children="10000"),
                                ]),
                                html.H6(children=[
                                    html.Span(children="不合格数:"),
                                    html.Span(id="month_remarks_report_no_pass_count", children="10000"),
                                ]),
                                dbc.Progress(id="month_remarks_report_pass_process", children="25%", value=25)
                            ]
                        ),

                        html.Br(),
                        html.Br(),
                        html.Br(),

                    ]
                )
            )

        ]
    ),
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Graph(id="graph_area_detail")
                            ]
                        )
                    ]
                )
            )
        ]
    )

]

# 自检任务完成情况
task_finish_detail_graph = [
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Label(children="任务名称：开市自检9月1日-9月30日", style={"color": "blue"}),
                    dbc.Row(
                        children=[
                            dbc.Col(children=[
                                html.P("执行有效期  2021-01-01 2021-01-31"),
                                html.P("重复方式  每日执行"),
                                html.P("执行者  店长、店员、加盟商"),
                                html.P("状态  进行中"),
                                html.P("执行组织  总部"),
                            ]),
                            dbc.Col(children=[
                                html.P("应自检门店  10000"),
                                html.P("应完成报告数  2000"),
                                html.P("已完成报告数  3000"),
                                html.P("点评报告数  1000 点评率：88.8%"),
                                html.P("合格数  7868 合格率：95.2%"),
                            ]),
                        ]
                    ),

                    dcc.Graph(id="graph_task_1")
                ]
            )
        ),
    ),

    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Label(children="任务名称：开市自检9月1日-9月30日", style={"color": "blue"}),
                    dbc.Row(
                        children=[
                            dbc.Col(children=[
                                html.P("执行有效期  2021-01-01 2021-01-31"),
                                html.P("重复方式  每日执行"),
                                html.P("执行者  店长、店员、加盟商"),
                                html.P("状态  进行中"),
                                html.P("执行组织  总部"),
                            ]),
                            dbc.Col(children=[
                                html.P("应自检门店  10000"),
                                html.P("应完成报告数  2000"),
                                html.P("已完成报告数  3000"),
                                html.P("点评报告数  1000 点评率：88.8%"),
                                html.P("合格数  7868 合格率：95.2%"),
                            ]),
                        ]
                    ),

                    dcc.Graph(id="graph_task_2")
                ]
            )
        ),
    ),
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Label(children="任务名称：开市自检9月1日-9月30日", style={"color": "blue"}),
                    dbc.Row(
                        children=[
                            dbc.Col(children=[
                                html.P("执行有效期  2021-01-01 2021-01-31"),
                                html.P("重复方式  每日执行"),
                                html.P("执行者  店长、店员、加盟商"),
                                html.P("状态  进行中"),
                                html.P("执行组织  总部"),
                            ]),
                            dbc.Col(children=[
                                html.P("应自检门店  10000"),
                                html.P("应完成报告数  2000"),
                                html.P("已完成报告数  3000"),
                                html.P("点评报告数  1000 点评率：88.8%"),
                                html.P("合格数  7868 合格率：95.2%"),
                            ]),
                        ]
                    ),

                    dcc.Graph(id="graph_task_3")
                ]
            )
        ),
    ),

]

# 完成率、点评率、合格率指标趋势
indicator_trend_graph = [
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Graph(id="graph_indicator_trend")
                            ]
                        ),
                        dbc.Col(
                            children=[
                                dcc.Graph(id="graph_area_item_trend", )
                            ]
                        )
                    ]
                )
            )
        ]
    )
]

# 完成率、点平率、合格率指标关联性
indicator_relevance_graph = [
    dbc.Col(
        children=[
            dbc.Card(
                children=dbc.CardBody(
                    children=[
                        # 筛选框
                        dbc.Row(
                            children=[
                                dbc.Col(width=6),
                                dbc.Col(
                                    html.Div([
                                        # x 轴
                                        dbc.Label(children="X轴"),
                                        dcc.Dropdown(
                                            id="choices_x",
                                            style={'width': 120},
                                            options=[
                                                {'label': '完成率', 'value': 'finish_rate'}
                                            ],
                                            value='finish_rate',
                                            searchable=False,
                                            clearable=False
                                        ),
                                        # 筛选框2
                                        dbc.Label(children="Y轴"),
                                        dcc.Dropdown(
                                            id="choices_y",
                                            style={'width': 120},
                                            options=[
                                                {'label': "合格率", 'value': "pass_rate"},
                                            ],
                                            value='pass_rate',
                                            searchable=False,
                                            clearable=False
                                        ),
                                        html.Br(),
                                        # 筛选框2
                                        dbc.Label(children="大小"),
                                        dcc.Dropdown(
                                            id="choices_big_small",
                                            style={'width': 120},
                                            options=[
                                                {'label': "门店数量", 'value': "store_count"},
                                            ],
                                            value='store_count',
                                            searchable=False,
                                            clearable=False
                                        ),
                                        # 筛选框2
                                        dbc.Label(children="颜色"),
                                        dcc.Dropdown(
                                            id="choices_color",
                                            style={'width': 120},
                                            options=[
                                                {'label': "运营区域", 'value': "area"},
                                            ],
                                            value='area',
                                            searchable=False,
                                            clearable=False
                                        )
                                    ],
                                        className='media-left block-inline'),
                                    width=6
                                ),
                            ]),
                        dbc.Row(children=[
                            dbc.Col(
                                children=[
                                    dcc.Graph(id="graph_indicator_relevance")
                                ]
                            )
                        ])

                    ]
                )
            )
        ]
    )
]
question_item_graph = [
    # 问题项分布图
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(width=6),
                            dbc.Col(
                                html.Div([
                                    # x 轴
                                    dbc.Label(children="类别筛选"),
                                    dcc.Dropdown(
                                        id="choices_item_category",
                                        style={'width': 120},
                                        options=[
                                            {'label': '5S定位查询', 'value': 'search'}
                                        ],
                                        value='search',
                                        searchable=False,
                                        clearable=False
                                    ),
                                    # 筛选框2
                                    dcc.Dropdown(
                                        id="choices_item_date",
                                        style={'width': 120},
                                        options=[
                                            {'label': "最近三个月", 'value': "recent_three"},
                                        ],
                                        value='recent_three',
                                        searchable=False,
                                        clearable=False
                                    ),

                                ],
                                    className='media-left block-inline'),
                                width=6
                            ),
                        ]
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dcc.Graph(id="question_distribution_graph")
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    ),

    # 问题项环比
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(width=6),
                            dbc.Col(
                                html.Div([
                                    # x 轴
                                    dbc.Label(children="类别筛选"),
                                    dcc.Dropdown(
                                        id="choices_diff_category",
                                        style={'width': 120},
                                        options=[
                                            {'label': '5S定位查询', 'value': 'search'}
                                        ],
                                        value='search',
                                        searchable=False,
                                        clearable=False
                                    ),
                                    # 基准月
                                    dbc.Label(children="基准月"),
                                    dcc.Dropdown(
                                        id="choices_diff_month",
                                        style={'width': 120},
                                        options=[
                                            {'label': "2021年9月", 'value': "2021-09"},
                                        ],
                                        value='2021-09',
                                        searchable=False,
                                        clearable=False
                                    ),
                                ],
                                    className='media-left block-inline'),
                                width=6
                            ),
                        ]
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                children=[
                                    dcc.Graph(id="question_diff_tab_graph"),
                                ]
                            ),

                            dbc.Col(
                                children=[
                                    dcc.Graph(id="question_diff_bar_graph")
                                ]
                            )
                        ]
                    )
                ]
            )
        )
    ),
]

content = html.Div(
    className='content-style',
    children=[
        dbc.Row(id="top_cards", children=top_cards, style={"height": "280px", "margin": "5px"}),
        dbc.Row(id="month_finish_detail_graph", children=month_finish_detail_graph,
                style={"margin": "5px 0px 5px 0px"}),
        dbc.Row(id="task_finish_detail_graph", children=task_finish_detail_graph, style={"margin": "5px 0px 5px 0px"}),
        dbc.Row(id="indicator_trend_graph", children=indicator_trend_graph, style={"margin": "5px 0px 5px 0px"}),
        dbc.Row(id="indicator_relevance_graph", children=indicator_relevance_graph,
                style={"margin": "5px 0px 5px 0px"}),
        dbc.Row(id="question_item_graph", children=question_item_graph, style={"margin": "5px 0px 5px 0px"}),

    ],
)

###############
# 页面布局
###############

layout = html.Div(
    children=[
        content,
        # signal value to trigger callbacks
        dcc.Store(id='signal', data={"today_str": today_str})
    ]
)
