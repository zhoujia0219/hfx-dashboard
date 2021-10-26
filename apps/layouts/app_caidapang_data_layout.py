import pandas as pd
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from services.srv_cdp_importData import data_month_order, data_time_allstore_avg, data_time_storecount, \
    data_sales_proport,res
import plotly.graph_objects as go
import plotly.express as px
from apps.layouts import app_cdp_layout

# 侧边栏
sidebar = html.Div(
    className='sidebar-style',
    children=[
        html.H4(children="门店月度销售分析"),
        html.Hr(),
    ],
)


# 定义方法： 门店销售时段&平均销售额
def fig_time_bar_method():
    date = data_time_allstore_avg['1_x']
    values = data_time_allstore_avg['1_y']
    fig = px.bar(
        x=date,
        y=values,
        text=values,
        title='门店销售时段●平均销售额',
        template='plotly_white',
        height=590
    )
    fig.update_layout(margin=dict(l=20, r=0, t=40, b=20), title_x=0.5,barmode='group', bargap=0.4, bargroupgap=0.2,
                      xaxis_tickangle=-45,)
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig

# 定义方法： （13家）日均时段销售额
def fig_sales_bar_method():
    date = data_month_order['1_x']
    values = data_month_order['1_y']
    fig = px.bar(
        x=date,
        y=values,
        text=values,
        title='营业额&利润排名重合门店(13家)●日均时段销售额',
        template='plotly_white',
    )
    fig.update_layout(margin=dict(l=20, r=0, t=40, b=20), title_x=0.5, barmode='group', bargap=0.2, bargroupgap=0.2,
                      xaxis_tickangle=-45, )
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside', )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig

# 时段门店数量数据
df_stores_count = pd.DataFrame({
    '时段①': res[0],
    '门店数①': res[1],
    '时段②': res[2],
    '门店数②': res[3],
    '时段③': res[4],
    '门店数③': res[5],
    '时段④': res[6],
    '门点数④': res[7],
})

# 时段门店数量table
table_stores_count = dash_table.DataTable(
    id='table_stores',
    data=df_stores_count.to_dict('records'),
    columns=[{'name': i, 'id': i} for i in df_stores_count.columns],
)

# 销售占比数据
df_sales_proports = pd.DataFrame({
    '编号': data_sales_proport[4],
    '门店名': data_sales_proport[0],
    '堂食占比': data_sales_proport['1_y'],
    '外卖占比': data_sales_proport['2_y'],
    '营业额排名': data_sales_proport[3],
    '净利润排名': data_sales_proport[4]
})

# 销售占比table
table_sales_tots = dash_table.DataTable(
    id='table_sales',
    data=df_sales_proports.to_dict('records'),
    columns=[{'name': i, 'id': i} for i in df_sales_proports.columns],
    # style_data_conditional=[
    #         {
    #             'if': {
    #                 'column_id': '堂食占比',
    #                 'filter_query': '{堂食占比} >= 0.4',
    #             },
    #             'backgroundColor': 'pink'
    #         },
    #         {
    #             'if': {
    #                 'colum_id': '堂食占比',
    #                 'filter_query': '{堂食占比[-1]}'
    #             },
    #             'backgroundColor': 'white'
    #         },
    #         {
    #             'if': {
    #                 'column_id': '外卖占比',
    #                 'filter_query': '{外卖占比} > 0.6',
    #             },
    #             'backgroundColor': 'yellow'
    #         },
    #     ]
)

# 门店销售时段&平均销售额bar图
module_ave_sales_bar = dbc.Card(
    children=dbc.CardBody(
        children=[
            html.Div(
                children=[
                    dcc.Loading(id='time_bar_loading',
                                type='circle',
                                children=[
                                    dcc.Graph(figure=fig_time_bar_method(),
                                              config={
                                                  # 隐藏浮动工具栏
                                                  'displayModeBar': False
                                              }
                                              )
                                ],
                                style={'width': 120}
                                ),
                ],
                # 设置固定高度，增加页面体验效果
                style={"height": "620px"}
            )
        ]
    )
)

# （13家）日均时段销售额bar图
module_time_sales_bar = dbc.Card(
    children=dbc.CardBody(
        children=[
            # 图
            html.Div(
                children=[
                    dcc.Loading(id='sales_bar_loading',
                                type='circle',
                                children=[
                                    dcc.Graph(figure=fig_sales_bar_method(),
                                              config={
                                                  # 隐藏浮动工具栏
                                                  'displayModeBar': False
                                              }
                                              )
                                ],
                                style={'width': 120}
                                ),
                ],
                style={"height": "450px"}
            )
        ]
    )
)

# 销售占比统计table
module_sales_tot_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            html.Div(
                children=[
                    dcc.Loading(id='sales_table_loading',
                                type='circle',
                                children=[
                                    table_sales_tots
                                ],
                                style={'width': 120}
                                ),
                ],
                style={"height":"620px"}
            )
        ]
    )
)
# 销售时间段统计（门店数量）tbale
module_stores_count_table = dbc.Card(
    children=dbc.CardBody(
        children=[
            html.Div(
                children=[
                    dcc.Loading(id='stores_table_loading',
                                type='circle',
                                children=[
                                    table_stores_count
                                ],
                                style={'width': 120}
                                ),
                ],
                # style={"height":"200px"}
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
                dbc.Col(module_stores_count_table),
            ],
            className='mt-3'
        ),
        dbc.Row(
            children=[
                dbc.Col(module_ave_sales_bar),
                dbc.Col(module_sales_tot_table)
            ],
            className='mt-3'),
        dbc.Row(
            children=[
                dbc.Col(module_time_sales_bar),
            ],
            className='mt-3'),
    ],
)

# 页面布局
content_1 = app_cdp_layout.content

layout = html.Div(
    children=[
        content_1,
        content,
        dcc.Store(id='signal')
    ],
    style={"width": "100%"}
)
