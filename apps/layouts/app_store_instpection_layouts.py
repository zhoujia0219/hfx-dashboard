import pandas as pd
import random
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go
import plotly.express as px


from services.srv_store_inspection import find_all_store_inspect, find_store_inspect_regular, find_store_table,find_inspect_style_regular
from services.srv_comm_dim import get_store_area, get_store_sort, get_store_month,get_year

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


def pie_store_inspection_rate():
    """
    门店巡检任务——饼图
    """
    # index = 1 if inspect_rate == "finish" else 0
    night_colors = ['rgb(56, 75, 126)', 'rgb(18, 36, 37)', 'rgb(34, 53, 101)',
                    'rgb(36, 55, 57)', 'rgb(6, 4, 4)']
    sunflowers_colors = ['rgb(177, 127, 38)', 'rgb(205, 152, 36)', 'rgb(99, 79, 37)',
                         'rgb(129, 180, 179)', 'rgb(124, 103, 37)']
    irises_colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
                     'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
    cafe_colors = ['rgb(146, 123, 21)', 'rgb(177, 180, 34)', 'rgb(206, 206, 40)',
                   'rgb(175, 51, 21)', 'rgb(35, 36, 21)']
    colors = ['#FFC573', '#FF9DB5']
    fig = go.Figure(data=[go.Pie(
        labels=['巡检已完成:', '巡检未完成:'],
        values=[task_rate, 1 - task_rate],
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        showlegend=False,
        textinfo='label+percent',
        hoverinfo="label+percent",
        # marker_colors=irises_colors
    )])
    fig.update_layout(
        width=200, height=200,
        paper_bgcolor="#FFFFFF",
        # showlegend=False,
        margin=dict(t=5, l=5, b=5, r=5)
    )
    return fig


# 巡检任务完成率——饼图
left_body_01 = dbc.Card(children=dbc.CardBody(children=[
    dbc.Row([
        dbc.Col(children=[
            html.P(children="任务完成率",
                   style={"padding-bottom": "2px", "font-size": "20px", "font-weight": "bold", "color": "black"}),
            html.P(children="总门店数：900",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="巡检门店数：789",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="计划巡检频次：2",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="实际巡检频次：1.5",
                   style={"color": "black", "font-size": "15px"}),
        ]),
        dbc.Col(
            html.Div(
                children=[
                    dcc.Graph(  # 本月累计销售额/计划的饼图
                    figure=pie_store_inspection_rate(),
                    style={"width": "200px", "height": "200px"})
                ],style={"height": "200px"}
        ))
    ])
]))

#表格图
def fig_five_table():
    fig = go.Figure(data=[go.Table(

        columnorder=[1, 2, 3, 4, 5, 6, 7, 8],  # 列属性的顺序
        columnwidth=[800, 800, 950, 800, 800, 800, 800, 800],  # 列属性中元素所占单元格整体大小

        header=dict(values=['区域', '总门店数', '计划/实际巡店数', '任务完成率', '任务合格率', '任务整改率'],
                    line_color='#DCDCDC',
                    fill_color='#DCDCDC',
                    align='center'),

        cells=dict(values=[["湖南>长沙", "湖南>株洲", "湖北>武汉", "湖北>荆州", "江苏>南京", "北京>北京", "广东>广州", "四川>成都"],
                           [300, 300, 300, 300, 300, 300, 300, 300],
                           ["300/220", "300/220", "300/255", "300/200", "300/280", "300/267", "300/285", "300/245"],
                           ["80%", "80%", "84%", "70%", "95%", "88%", "90%", "76%"],
                           ["75%", "78%", "82%", "90%", "88%", "62%", "72%", "65%"],
                           ["75%", "78%", "82%", "90%", "88%", "62%", "70%", "66%"]
                           ],
                   line_color=['white'],
                   fill=dict(color=['white', 'white']),
                   align='center'
                   ))
    ])
    # fig.update_layout(margin=dict(t=5, l=5, b=5, r=5))
    return fig

# bar对比条形图（完成率、合格率、整改率）
def fig_six_compare_bar():
    df = pd.DataFrame([
                {"area": "武汉运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "武汉运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "武汉运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "杭州运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "杭州运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "杭州运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "南京运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "南京运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "南京运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "长沙运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "长沙运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "长沙运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "广州运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "广州运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "广州运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "福州运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "福州运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "福州运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "上海运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "上海运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "上海运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "成都运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "成都运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "成都运营中心", "name": "整改数", "value": random.randint(0, 15)},

                {"area": "重庆运营中心", "name": "完成数", "value": random.randint(0, 100)},
                {"area": "重庆运营中心", "name": "合格数", "value": random.randint(0, 50)},
                {"area": "重庆运营中心", "name": "整改数", "value": random.randint(0, 15)},
            ])

    fig = px.bar(df, x="value", y="area", color="name",
                         hover_data=["area", "name"],
                         color_discrete_map={
                             '完成数': 'rgb(92,176,254)',
                             '合格数': 'rgb(78,203,115)',
                             '整改数': '#FF8C00',
                         },
                         template="simple_white"
                         )
    # fig.update_layout(margin=dict(t=5, l=5, b=5, r=5))
    return fig

# 巡检情况完成率趋势——折线图
left_body_02 = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(
                        id='area_choice_title',
                        children=' ',
                        className='media-body'
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id='year_choice',
                                options=get_year(),
                                value='2020',
                                searchable=False,
                                clearable=False,
                                style={'width': 85}
                            ),
                            dcc.Dropdown(
                                id='area_choice',
                                options=get_store_area(),
                                value='武汉运营中心',
                                searchable=False,
                                clearable=False,
                                style={'width': 120}
                            )
                        ],className='media-right block-inline'
                    )
                ],
                className='media flex-wrap ',
                style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            html.Div(
                children=[
                    dcc.Loading(id='inspection_line_loading',
                                type='circle',
                                children=[
                                    dcc.Graph(id="graph_inspection_line")
                                ],
                                style={'width': 120}),
                    ],style={'height':'450px'}
            )
        ]
    )
)


def pie_store_regular_rate(store_regular):
    """
    本周本月的销售额/计划销售额饼图
    param week_month:week表示本周，month表示本月
    """
    index = 1 if store_regular == "s_regular" else 0
    colors = ['#FFC573', '#FF9DB5']
    fig = go.Figure(data=[go.Pie(
        labels=['巡检合格:', '巡检不及格:'],
        values=[regular_rate, 1 - regular_rate],
        hole=0.5,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        # showlegend=False,
        textinfo='label+percent',
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
                   style={"padding-bottom": "2px", "font-size": "20px", "font-weight": "bold", "color": "black"}),
            html.P(children="总巡检次数：789",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="合格次数：721",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="平均分之上：62%",
                   style={"color": "black", "font-size": "15px"}),
            html.P(children="平均分之下：37%",
                   style={"color": "black", "font-size": "15px"}),
        ]),
        dbc.Col(
            html.Div(
                children=[
                    dcc.Graph(
                    figure=pie_store_regular_rate("s_regular"),
                    style={"width": "200px", "height": "200px"})
                ],style={"height": "200px"}
            )
        )
    ])
]))


#合并table和compara_bar图
module_table_and_bar = dbc.Card(
    children=dbc.CardBody(
        children=[
            dbc.Row([
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Loading(
                                id='store_table_loading',
                                type='circle',
                                children=[
                                    dcc.Graph(
                                        figure=fig_five_table()
                                    )
                                ],
                            ),
                        ],
                        # style={"height":"px"}
                    )
                ),
                dbc.Col(children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                figure=fig_six_compare_bar(),
                            )
                            , ], ),

                ],
                    # style={"width":"600px"}
                ),


            ],
                # style={"height": "400px"}
            )
        ],

    ),
    style={"width": "100%"}
)


# 巡检项评估占比
build_inspect_item_fig = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                children=[
                    html.H5(
                        id='inspect_item_pie_title',
                        children='巡检项评估占比 ',
                        className='media-body'
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id='inspect_item_area_choice',
                                options=get_store_area(),
                                value='长沙运营中心',
                                searchable=False,
                                clearable=False,
                                style={'width': 120}
                            ),
                        ],
                        className='media-right block-inline'
                    )
                ],className='media flex-wrap ',
                  style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            html.Div(
                children=[
                    dcc.Loading(
                        id='inspection_item_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_inspect_item_pie")
                        ],
                        style={'width': '460px', 'height': '380px'}
                    ),
                ],style={'height': '380px'}
            )
        ]
    )
)

# 巡检不合格类别雷达图
build_inspect_style_unqualified_radar_fig = dbc.Card(
    children=dbc.CardBody(
        children=[
            #用户选项
            html.Div(
                children=[
                    html.H5(
                        id='inspect_style_radar_title',
                        children='不合格巡检项类别分布 ',
                        className='media-body'
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id='inspect_style_area_choice',
                                options=get_store_area(),
                                value='武汉运营中心',
                                searchable=False,
                                clearable=False,
                                style={'width': 120}
                            ),
                        ],
                        className='media-right block-inline'
                    )
                ],className='media flex-wrap ',
                  style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            html.Div(
                children=[
                    dcc.Loading(
                        id='inspection_style_loading',
                        type='circle',
                        children=[
                            dcc.Graph(id="graph_inspect_style_radar")
                        ],
                        style={'width': '460px', 'height': '380px'}
                    ),
                ],style={'height': '380px'}
            )
        ]
    )
)

# 合格巡检项树状图
build_inspect_style_unqualified_tree_fig = dbc.Card(
    children=dbc.CardBody(
        children=[
            #用户选项
            html.Div(
                children=[
                    html.H5(
                        id='inspect_style_tree_title',
                        children='合格巡检项类别分布 ',
                        className='media-body'
                    ),
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id='inspect_tree_area_choice',
                                options=get_store_area(),
                                value='武汉运营中心',
                                searchable=False,
                                clearable=False,
                                style={'width': 120}
                            ),
                        ],
                        className='media-right block-inline'
                    )
                ],className='media flex-wrap ',
                  style={'alignItems': 'flex-end'}
            ),
            html.Hr(),
            # 图
            html.Div(
                children=[
                    dcc.Loading(
                        id='inspection_regular_tree_loading',
                        type='circle',
                        children=[
                            dcc.Graph(
                                id='graph_inspect_style_tree'
                                # figure=build_inspect_tree("i_tree")
                            )
                        ],
                        style={'width': '460px', 'height': '380px'}
                    ),
                ],style={'height': '380px'}
            )
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
                dbc.Col(module_table_and_bar,width=12),

            ]),
        dbc.Row(
            children=[
                dbc.Col(build_inspect_item_fig,width=4),
                dbc.Col(build_inspect_style_unqualified_radar_fig,width=4),
                dbc.Col(build_inspect_style_unqualified_tree_fig,width=4)
            ],
            className='mt-3'
        )
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
