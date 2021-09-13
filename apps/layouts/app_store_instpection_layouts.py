import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from services.srv_store_inspection import find_all_store_inspect, find_store_inspect_regular
from services.srv_comm_dim import get_store_area, get_store_sort, get_store_month

# 侧边栏
sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4(children="门店常规巡检"),
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

# 调用sql取数方法--巡检门店完成次数
change_finish_inspect_store = find_all_store_inspect()
# 计算巡检任务完成率
task_rate = change_finish_inspect_store[0][1] / change_finish_inspect_store[0][0]

# 调用sql取数方法--巡检门店合格与不合格
change_finish_inspect_regular = find_store_inspect_regular()
# 计算巡检门店合格率与不合格率
regular_rate = change_finish_inspect_regular[0][1] / change_finish_inspect_regular[0][0]

###############
# content
###############
card_list = [
    dbc.Col(
        children=dbc.Card(
            children=dbc.CardBody(
                children=[]
            )
        )
    )
]


def pie_store_inspection_rate(inspect_rate):
    """
    门店巡检任务——饼图
    """
    index = 1 if inspect_rate == "finish" else 0
    fig = go.Figure(data=[go.Pie(
        labels=['巡检任务已完成', '巡检任务未完成'],
        values=[task_rate, 1 - task_rate],
        hole=0.4,
        showlegend=False,
        textinfo='percent',
        hoverinfo="label+percent", )])
    fig.update_layout(
        width=200, height=200,
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        margin=dict(t=5, l=5, b=5, r=5)
    )
    return fig


# 巡检任务完成率——饼图
left_body_01 = dbc.Card(children=dbc.CardBody(children=[
    dbc.Row([
        dbc.Col(children=[
            html.P(children="任务完成率",
                   style={"padding-bottom": "6px", "font-size": "23px", "font-weight": "bold", "color": "black"}),
            html.P(children="总门店数：{}".format(change_finish_inspect_store[0][0], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="巡检门店数：{}".format(change_finish_inspect_store[0][1], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="计划巡检频次：{}".format(change_finish_inspect_store[0][2], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="实际巡检频次：{}".format(change_finish_inspect_store[0][3], 0),
                   style={"color": "black", "font-size": "20px"}),
        ]),
        dbc.Col(dcc.Graph(  # 本月累计销售额/计划的饼图
            figure=pie_store_inspection_rate("finish"),
            style={"width": "200px", "height": "200px"}
        ))
    ])
]))


# 巡检情况完成率趋势——折线图
left_body_02 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(id='area_choice_title',children=' ',
                            className='media-body'),
                    html.Div([
                        dcc.Dropdown(
                            id='area_choice',
                            options=get_store_area(),
                            value='武汉运营中心',
                            searchable=False,
                            clearable=False,
                            style={'width': 120}
                        ),
                    ])
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            dcc.Loading(id='inspection_line_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_inspection_line")
                        ],
                        style={'width': '460px', 'height': '450px'}),
        ]
    )
)


def pie_store_regular_rate(store_regular):
    """
    本周本月的销售额/计划销售额饼图
    param week_month:week表示本周，month表示本月
    """
    index = 1 if store_regular == "s_regular" else 0
    fig = go.Figure(data=[go.Pie(
        labels=['巡检合格', '巡检不及格'],
        values=[regular_rate, 1 - regular_rate],
        hole=0.4,
        showlegend=False,
        textinfo='percent',
        hoverinfo="label+percent", )])
    fig.update_layout(
        width=200, height=200,
        paper_bgcolor="#FFFFFF",
        showlegend=False,
        margin=dict(t=5, l=5, b=5, r=5)
    )
    return fig


# 巡检门店合格率——饼图
right_body = dbc.Card(children=dbc.CardBody(children=[
    dbc.Row([
        dbc.Col(children=[
            html.P(children="任务合格率",
                   style={"padding-bottom": "6px", "font-size": "23px", "font-weight": "bold", "color": "black"}),
            html.P(children="总巡检次数：{}".format(change_finish_inspect_regular[0][0], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="合格次数：{}".format(change_finish_inspect_regular[0][1], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="平均分之上：{}".format(change_finish_inspect_regular[0][2], 0),
                   style={"color": "black", "font-size": "20px"}),
            html.P(children="平均分之下：{}".format(change_finish_inspect_regular[0][3], 0),
                   style={"color": "black", "font-size": "20px"}),
        ]),
        dbc.Col(dcc.Graph(
            figure=pie_store_regular_rate("s_regular"),
            style={"width": "200px", "height": "200px"}
        ))
    ])
]))

#### 行3 3个直方图
# 巡检情况完成率排名——直方图01
right_body_01 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(id='month_choice_bar_finish_title',children=' ',
                            className='media-body'),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                    id='finish_fig_month_choice',
                                    options=get_store_month(),
                                    value='01',
                                    searchable=False,
                                    clearable=False,
                                    style={'width': 65}
                                    ),
                            dcc.Dropdown(
                                id='sort_choice_01',
                                options=get_store_sort(),
                                value='asc',
                                searchable=False,
                                clearable=False,
                                style={'width': 65}
                            ),
                        ],className='media-right block-inline'
                    )
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            dcc.Loading(id='inspection__finish_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_finish_bar")
                        ],
                        style={'width': '460px', 'height': '450px'}),

        ]
    )
)

# 巡检情况合格率排名——直方图02
right_body_02 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(id='month_choice_bar_regular_title',children=' ',
                            className='media-body'),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                    id='regular_fig_month_choice',
                                    options=get_store_month(),
                                    value='01',
                                    searchable=False,
                                    clearable=False,
                                    style={'width': 65}
                                    ),
                            dcc.Dropdown(
                                id='sort_choice_02',
                                options=get_store_sort(),
                                value='asc',
                                searchable=False,
                                clearable=False,
                                style={'width': 65}
                            ),
                        ],className='media-right block-inline'
                    )
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            dcc.Loading(id='inspection_regular_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_regular_bar")
                        ],
                        style={'width': '460px', 'height': '450px'}),

        ]
    )
)
# 巡检情况整改率排名——直方图03
right_body_03 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(id='month_choice_bar_rectify_title',children=' ',
                            className='media-body'),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                    id='rectify_fig_month_choice',
                                    options=get_store_month(),
                                    value='01',
                                    searchable=False,
                                    clearable=False,
                                    style={'width': 65}
                                    ),
                            dcc.Dropdown(
                                id='sort_choice_03',
                                options=get_store_sort(),
                                value='asc',
                                searchable=False,
                                clearable=False,
                                style={'width': 65}
                            ),
                        ],className='media-right block-inline'
                    )
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            dcc.Loading(id='inspection_rectify_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_rectify_bar")
                        ],
                        style={'width': '460px', 'height': '450px'}),

        ]
    )
)


content = html.Div(
    className='content-style',
    children=[
        dbc.Row(
            children=[
                dbc.Col(left_body_01, width=6),
                dbc.Col(right_body, width=6),
            ]),
        dbc.Row(
            children=[
                dbc.Col(left_body_02, width=12),
            ],
            className='mt-3'),
        dbc.Row(
            children=[
                dbc.Col(right_body_01, width=4),
                dbc.Col(right_body_02, width=4),
                dbc.Col(right_body_03, width=4),
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
