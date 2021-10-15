import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import numpy as np
import plotly.express as px

###############
# 数据
###############

from services.srv_cdp import df_md_pm

df_md_pm_db = df_md_pm[['门店名', '营业额排名', '净利润排名']]
df_md_pm_db = df_md_pm_db.melt(
    id_vars='门店名', 
    value_vars=['营业额排名', '净利润排名'], 
    var_name='排名类别', 
    value_name='排名'
)

df_cs = pd.DataFrame({
    '城市': ['自贡市','绵阳市','拉萨市','成都市','南充市','戍都市','广安市','贵阳市','丽江市','眉山市','乐山市'],
    '个数': [30,3,2,2,1,1,1,1,1,1,1]
    })

df_qy = pd.DataFrame({
    '区域': ['市辖区', '县', '县级市', '镇'],
    '个数': [44,4,1,1]
})

df_md = pd.DataFrame({
    '数据范围': ['前20家门店', '前50家门店'],
    '房租': [8032, 7382],
    '人工': [14000, 13000],
    '季度营业额': [300000, 320000],
    '月均营业额': [100000, 110000],
    '净利润月': [20000, 19000],
    '净利润年': [240000, 221000],
    '投资回报周期': [6.3, 7.7],
})

df_tz = pd.DataFrame({
    '区域': ['成都市', '县级市', '其他市', '县', '镇'],
    '周期': [9.6, 4.8, 9.2, 6.4, 7.4]
})

###############
# 图
###############

# 城市分布图
fig_cs = px.bar(
    df_cs,
    x='城市', 
    y='个数', 
    text='个数', 
    title='城市分布',
    template='plotly_white', 
)
fig_cs.update_layout(margin=dict(l=20, r=0, t=40, b=20), title_x=0.5)
fig_cs.update_traces(texttemplate='%{text:.0f}', textposition='outside',)
fig_cs.update_xaxes(title=None)
fig_cs.update_yaxes(title=None)

# 区域属性图
fig_qy = px.bar(
    df_qy,
    x='区域', 
    y='个数', 
    text='个数', 
    title='区域属性（门店数）',
    template='plotly_white', 
)
fig_qy.update_layout(margin=dict(l=20, r=0, t=40, b=20), title_x=0.5)
fig_qy.update_traces(texttemplate='%{text:.0f}', textposition='outside',)
fig_qy.update_xaxes(title=None)
fig_qy.update_yaxes(title=None)

# 区域属性图2
fig_qy2 = px.pie(
    df_qy, 
    names='区域', 
    values='个数'
)
fig_qy2.update_traces(textposition='outside')
fig_qy2.update_layout(
    legend={'x': 0.15, 'y': 1.2, 'orientation': 'h'},
    margin=dict(l=20, r=0, t=40, b=20),
)

# 投资回报周期图
fig_tz = px.bar(
    df_tz,
    x='区域', 
    y='周期', 
    text='周期', 
    title='投资回报周期（月）',
    template='plotly_white', 
)
fig_tz.update_traces(texttemplate='%{text:.0f}', textposition='outside',)
fig_tz.update_layout(title_x=0.5, margin=dict(l=20, r=0, t=40, b=20),)
fig_tz.update_xaxes(title=None)
fig_tz.update_yaxes(title=None)

# 门店排名对比图
fig_md_pm = px.bar(
    data_frame = df_md_pm_db,
    x = '门店名',
    y = '排名',
    color = '排名类别',
    barmode = 'group',
    text = '排名',
    template = 'plotly_white',
    title = '营业额&净利润排名对比'
)
fig_md_pm.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig_md_pm.update_layout(
    legend={'x': 0.45, 'y': -0.5, 'orientation': 'h', 'title': ''},
    title_x=0.5,
    margin=dict(l=20, r=0, t=45, b=10)
)
fig_md_pm.update_xaxes(title=None)
fig_md_pm.update_yaxes(title=None)

###############
# 表
###############

# 门店表
table_md = dash_table.DataTable(
    id='table_1',
    data=df_md.to_dict('records'),
    columns=[{'name': i, 'id': i} for i in df_md.columns],
)

# 门店排名表
table_md_pm = dash_table.DataTable(
    id='table_2',
    data=df_md_pm.to_dict('records'),
    columns=[{'name': i, 'id': i} for i in df_md_pm.columns],
        style_data_conditional=[
        {
            'if': {
                'column_id': '营业额排名',
                'filter_query': '{营业额排名} <= 20',
                },
            'backgroundColor': 'pink'
        },
        {
            'if': {
                'column_id': '净利润排名',
                'filter_query': '{净利润排名} <= 20',
                },
            'backgroundColor': 'yellow'
        },
    ]
)

###############
# 卡片
###############

# 城市分布卡片
card_cs = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='fig_cs_loading',
            type='circle',
            children=[
                dcc.Graph(id="fig_cs_bar", figure=fig_cs)
            ],
        )
    ])
])

# 区域属性卡片
card_qy = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='fig_qy_loading',
            type='circle',
            children=[
                dcc.Graph(id="fig_qy_bar", figure=fig_qy)
            ],
        )
    ])
])

# 门店卡片
card_md = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='table_md_loading',
            type='circle',
            children=[
                table_md
            ],
        )
    ])
])

# 门店排名卡片
card_md_pm = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='table_md_pm_loading',
            type='circle',
            children=[
                table_md_pm
            ],
        )
    ])
])

# 区域属性2卡片
card_qy2 = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='pie_qy_loading',
            type='circle',
            children=[
                dcc.Graph(id='fig_qy2_pie', figure=fig_qy2)
            ],
        )
    ])
])

# 投资回报周期卡片
card_tz = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='fig_tz_loading',
            type='circle',
            children=[
                dcc.Graph(id="fig_tz_bar", figure=fig_tz)
            ],
        )
    ])
])

# 门店排名对比卡片
card_md_pm_db = dbc.Card([
    dbc.CardBody([
        dcc.Loading(
            id='fig_md_pm_db_loading',
            type='circle',
            children=[
                dcc.Graph(id="fig_md_pm_db_bar", figure=fig_md_pm)
            ],
        )
    ])
])

###############
# content
###############

sidebar = html.Div([])

content = html.Div(
            [    
                dbc.Row([
                    dbc.Col([card_cs], width=6),
                    dbc.Col([card_qy], width=6)
                ], className='mb-2, mt-2'),
                dbc.Row([
                    dbc.Col([card_md], width=12)
                ], className='mb-2, mt-2'),
                dbc.Row([
                    dbc.Col([card_qy2], width=6),
                    dbc.Col([card_tz], width=6)
                ], className='mb-2, mt-2'),
                dbc.Row([
                    dbc.Col([card_md_pm_db], width=12)
                ], className='mb-2, mt-2'),
                dbc.Row([
                    dbc.Col([card_md_pm], width=12)
                ], className='mb-2, mt-2'),
            ], className='mb-2, mt-2'
)

# layout = html.Div([
#     sidebar,
#     content
# ])

