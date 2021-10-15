import pandas
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.figure_factory as ff

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


# 定义方法： 门店销售时段&平均销售额
def fig_time_bar_method():
    date = ['11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00',
            '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00']
    values = [104, 131, 107, 154, 220, 240, 259, 279, 246, 233, 219]
    fig = go.Figure(data=[go.Bar(
        x=date,
        y=values,
        name='门店销售时段*平均销售额',
        text=values,
        textposition='outside',
        textfont_size=12,
        #marker_color='rgb(55, 83, 109)'
    )])
    fig.update_layout(
        #xaxis_tickangle=-45,
        template='plotly_white',
        # 柱状图模式
        barmode='group',
        # 组间距离
        bargap=0.5,
        # 组内距离
        bargroupgap=0.2,
        font=dict(family='arial',
                  color='#000000',
                  size=12),
        # 显示文本/数值
        uniformtext_mode='show',
        # 文本/数值显示的大小
        uniformtext_minsize=8,
        title_text='门店销售时段*平均销售额',
        # margin=dict(t=5, l=5, b=5, r=5)
    )
    # fig.update_traces(hoverinfo='label+percent',    # 设置鼠标悬浮上去时显示的文本
    #                   textfont_size=20,
    #                  )
    return fig


# 定义方法： （13家）日均时段销售额
def fig_sales_bar_method():
    date = ['00:00-01:00', '01:00-02:00', '02:00-03:00', '03:00-04:00', '04:00-05:00', '05:00-06:00', '06:00-07:00',
            '07:00-08:00', '08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00',
            '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00', '20:00-21:00',
            '21:00-22:00', '22:00-23:00', '23:00-00:00']
    values = [48.79, 20.56, 11.04, 0.31, 0.15, 6.55, 9.44, 0.03, 0.09, 1.37, 30.65, 147.23, 191.06, 157.79, 217.31,
              315.91, 367.04, 400.01, 424.90, 405.58, 381.62, 347.57, 252.39, 143.21]
    fig = go.Figure(data=[go.Bar(
        x=date,
        y=values,
        name='kkk',
        text=values,
        textposition='outside',
        textfont_size=25
        # marker_color='rgb(55, 83, 109)'
    )])
    fig.update_layout(
        # X坐标轴标签倾斜度数
        xaxis_tickangle=-45,
        # 背景颜色
        template='plotly_white',
        # 柱状图模式
        barmode='group',
        # 组间距离
        bargap=0.2,
        # 组内距离
        bargroupgap=0.2,
        # 字体样式、颜色、大小设置
        font=dict(family='arial',
                  color='#000000',
                  size=12),
        # 显示文本/数值
        uniformtext_mode='show',
        # 文本/数值显示的大小
        uniformtext_minsize=11,
        # margin=dict(t=5, l=5, b=5, r=5)
    )
    # fig.update_traces(hoverinfo='label+percent',    # 设置鼠标悬浮上去时显示的文本
    #                   textfont_size=20,
    #                  )
    return fig


# 定义方法：  销售占比统计table
def fig_sales_table_method():
    fig = go.Figure(data=[go.Table(
        # 列属性的顺序
        columnorder=[1, 2, 3, 4, 5, 6],
        # 列属性中元素所占单元格整体大小
        columnwidth=[350, 950, 350, 350, 350, 350],
        header=dict(values=['编号', '门店名', '堂食占比', '外卖占比', '营业额排名', '净利润排名'],
                    line_color='darkslategray',
                    fill_color='white',
                    align='center'),
        cells=dict(values=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, " "],
                           ['蔡大胖炸洋芋（华商店）', '蔡大胖炸洋芋（火炮街店）', '蔡大胖炸洋芋（拉萨金马店）',
                            '蔡大胖炸洋芋（华熙528店）', '蔡大胖炸洋芋（中央华城店）','蔡大胖炸洋芋（南充高坪中学店）',
                            '蔡大胖炸洋芋（川师成龙校区店）', '蔡大胖炸洋芋（九里晴川店）', '蔡大胖炸洋芋（滨江和城店）',
                            '蔡大胖炸洋芋（花果园店）','蔡大胖炸洋芋（天府逸家店）', '蔡大胖炸洋芋（华润时光里店）',
                            '蔡大胖炸洋芋（广安北街店）', '平均占比'],
                           [0.8, 0.5, 0.2, 0.4, 0.3, 0.4, 0.4, 0.3, 0.5, 0.3, 0.3, 0.3, 0.3, 0.4],
                           [0.2, 0.5, 0.8, 0.6, 0.7, 0.6, 0.6, 0.7, 0.5, 0.7, 0.7, 0.7, 0.7, 0.6],
                           [1, 8, 12, 9, 11, 5, 2, 6, 19, 3, 13, 10, 18, " "],
                           [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 20, " "]
                           ],
                   line_color=['#000000', ],
                   fill=dict(color=[
                       ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white',
                        'white', 'white', 'white', 'white'],
                       ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white',
                        'white', 'white', 'white', 'white'],
                       ['pink', 'pink', 'white', 'pink', 'white', 'pink', 'pink', 'white', 'pink', 'white', 'white',
                        'white', 'white', 'white'],
                       ['white', 'white', 'paleturquoise', 'white', 'paleturquoise', 'white', 'white', 'paleturquoise',
                        'white', 'paleturquoise', 'paleturquoise', 'paleturquoise', 'paleturquoise', 'white'],
                       ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white',
                        'white', 'white', 'white', 'white'],
                       ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white',
                        'white', 'white', 'white', 'white']
                   ]),
                   align=('center','left','center'),
                   height=28,
                   font=dict(family='Microsoft Yahei')
                   ))
    ])
    fig.update_layout(margin=dict(t=5, l=5, b=5, r=5),
                      height=450)
    # fig.update_traces(
    #     columnwidth=100,
    #     hoverlabel_namelength=15,
    # #   header_line_width=8, #表格第一行边框厚度
    #     cells_fill_color='white',
    #     cells_font_family="PT Sans Narrow"
    # )
    return fig

# 定义方法： 时段门店数量table
def fig_stores_table_method():
    fig = go.Figure(data=[go.Table(
        # 列属性的顺序
        columnorder=[1, 2, 3, 4, 5, 6, 7, 8],
        # 列属性中元素所占单元格整体大小
        columnwidth=[500, 500, 500, 500, 500, 500, 500, 500],
        header=dict(values=['时段', '门店数', '时段', '门店数', '时段', '门店数', '时段', '门店数'],
                    line_color='darkslategray',
                    fill_color='white',
                    align='center'),
        cells=dict(values=[
            ['00:00-01:00', '01:00-02:00', '02:00-03:00', '03:00-04:00', '04:00-05:00', '05:00-06:00', '06:00-07:00',
             '07:00-08:00'],
            [65, 26, 19, 7, 9, 8, 10, 20],
            ['08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '13:00-14:00', '14:00-15:00',
             '15:00-16:00'],
            [137, 161, 166, 166, 166, 166, 166, 166],
            ['16:00-17:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', '18:00-19:00', '19:00-20:00',
             '20:00-21:00'],
            [166, 166, 166, 166, 166, 166, 166, 166],
            ['21:00-22:00', '22:00-23:00', '23:00-00:00'],
            [166, 159, 119]
        ],
                   line_color=['#000000', ],
                   fill=dict(color=['white', 'white']),
                   align='center',
                   height=28,
                   font=dict(family='Microsoft Yahei')
                   ))
    ])
    fig.update_layout(margin=dict(t=5, l=5, b=5, r=5),
                      height=300)
    return fig


# 门店销售时段&平均销售额bar图
module_ave_sales_bar = dbc.Card(
    children=dbc.CardBody(
        children=[
            dbc.Row([
                dbc.Col(
                    children=[
                        # 用户选项
                        html.Div(
                            [
                                html.H5(
                                    id='time_bar',
                                    children=' ',
                                    className='media-body'
                                ),
                                html.Hr(),
                                # 图
                                html.Div(
                                    children=[
                                        dcc.Loading(id='time_bar_loading',
                                                    type='circle',
                                                    children=[
                                                        dcc.Graph(figure=fig_time_bar_method(),
                                                                  config={
                                                                        #隐藏浮动工具栏
                                                                        'displayModeBar': False
                                                                  }
                                                                  )
                                                    ],
                                                    style={'width': 120}
                                                    ),
                                    ],
                                    #设置固定高度，增加页面体验效果
                                    style={"height":"450px"}
                                )
                            ]
                        )
                    ]
                )
            ])
        ]
    )
)

# （13家）日均时段销售额bar图
module_time_sales_bar = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(
                        id='sales_bar',
                        children=' ',
                        className='media-body'
                    ),
                    html.Hr(),
                    # 图
                    html.Div(
                        children=[
                            dcc.Loading(id='sales_bar_loading',
                                        type='circle',
                                        children=[
                                            dcc.Graph(figure=fig_sales_bar_method(),
                                                      config={
                                                            #隐藏浮动工具栏
                                                            'displayModeBar': False
                                                      }
                                                      )
                                        ],
                                        style={'width': 120}
                                        ),
                        ],
                        style={"height":"450px"}
                    )
                ]
            )
        ]
    )
)

# 销售占比统计table
module_sales_tot_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(
                        id='sales_table',
                        children=' ',
                        className='media-body'
                    ),
                    html.Hr(),
                    # 图
                    html.Div(
                        children=[
                            dcc.Loading(id='sales_table_loading',
                                        type='circle',
                                        children=[
                                            dcc.Graph(
                                                figure=fig_sales_table_method(),
                                                config={
                                                    # 隐藏浮动工具栏
                                                    'displayModeBar': False
                                                }
                                            )
                                        ],
                                        style={'width': 120}
                                        ),
                        ],
                        style={"height":"450px"}
                    )
                ]
            )
        ]
    )
)

#销售时间段统计（门店数量）tbale
module_stores_count_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(
                        id='stores_table',
                        children=' ',
                        className='media-body'
                    ),
                    html.Hr(),
                    # 图
                    html.Div(
                        children=[
                            dcc.Loading(id='stores_table_loading',
                                        type='circle',
                                        children=[
                                            dcc.Graph(figure=fig_stores_table_method(),
                                                      config={
                                                          # 隐藏浮动工具栏
                                                          'displayModeBar': False
                                                      }
                                                      )
                                        ],
                                        style={'width': 120}
                                        ),
                        ],
                        # style={"height":"200px"}
                    )
                ]
            )
        ]
    )
)

# 销售占比统计
module_sales_tot_three_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 用户选项
            html.Div(
                [
                    html.H5(
                        id='sales_table',
                        children=' ',
                        className='media-body'
                    ),
                    html.Hr(),
                    # 图
                    html.Div(
                        children=[
                            dcc.Loading(id='sales_table_loading',
                                        type='circle',
                                        children=[
                                            dcc.Graph(
                                                figure=fig_sales_table_method(),
                                                config={
                                                    # 隐藏浮动工具栏
                                                    'displayModeBar': False
                                                }
                                            )
                                        ],
                                        style={'width': 120}
                                        ),
                        ],
                        style={"height":"450px"}
                    )
                ]
            )
        ]
    )
)

# 整体布局
content = html.Div(
    className='content-style',
    children=[
        dbc.Row(
            children=[
                dbc.Col(module_ave_sales_bar),
            ],
            className='mt-3'
        ),
        dbc.Row(
            children=[
                dbc.Col(module_time_sales_bar),
            ],
            className='mt-3'
        ),
        dbc.Row(
            children=[
                dbc.Col(module_sales_tot_table),
                dbc.Col()
            ],
            className='mt-3'),
        dbc.Row(
            children=[
                dbc.Col(module_stores_count_table),
            ],
            className='mt-3'),
    ],
)

# 页面布局
layout = html.Div(
    children=[
        content,
        dcc.Store(id='signal')
    ],
    style={"width": "100%"}
)
