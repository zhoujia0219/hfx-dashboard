import math
import random
import time
import json

import dash
from urllib.request import urlopen

import numpy as np
import pandas as pd
from pandas import DataFrame

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
from services import srv_sales_bymonth

###############
# 回调
###############
from services.srv_comm_dim import get_ZE_PJS_ZWS
from utils.thread_one_interface import MyThread


def register_callbacks(dash_app):
    ###############
    # 页面内容构建刷新函数
    ###############

    @dash_app.callback(
        Output('graph_close_rate', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_close_rate(signal_data):
        df = pd.DataFrame([{"label": "已完成", "value": 2000},
                           {"label": "未完成", "value": 1500}])
        fig = px.pie(df, values='value', names='label', width=220, height=220, hole=0.5, template="simple_white")
        fig.update(layout_showlegend=False)
        return fig

    @dash_app.callback(
        Output('graph_pending_rate', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_pending_rate(signal_data):
        df = pd.DataFrame([{"label": "已完成", "value": 500},
                           {"label": "未完成", "value": 3000}])
        fig = px.pie(df, values='value', names='label', width=220, height=220, hole=0.5, template="simple_white")
        fig.update(layout_showlegend=False)
        return fig

    @dash_app.callback(
        Output('graph_not_yet_rate', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_not_yet_rate(signal_data):
        df = pd.DataFrame([{"label": "已完成", "value": 0},
                           {"label": "未完成", "value": 3500}])
        fig = px.pie(df, values='value', names='label', width=220, height=220, hole=0.5, template="simple_white")
        fig.update(layout_showlegend=False)
        return fig

    @dash_app.callback(
        [
            Output('month_finish_report_count', 'children'),
            Output('month_finished', 'children'),
            Output('month_finished_process', 'children'),
            Output('month_finished_process', 'value'),

            Output('month_remarks_report_count', 'children'),
            Output('month_remarks_rate', 'children'),
            Output('month_remarks_rate_process', 'children'),
            Output('month_remarks_rate_process', 'value'),

            Output('month_remarks_report_count_2', 'children'),
            Output('month_remarks_report_pass_count', 'children'),
            Output('month_remarks_report_no_pass_count', 'children'),
            Output('month_remarks_report_pass_process', 'children'),
            Output('month_remarks_report_pass_process', 'value'),
        ],
        [
            Input('signal', 'data'),
        ])
    def update_month_remarks_values(signal_data):
        # 应完成报告数
        month_finish_report_count = 71730
        # 已完成
        month_finished = 66450
        # 完成率 = 已完成报告数/应完成报告数
        month_finished_process = month_finished / month_finish_report_count

        # 点评报告数
        remarks_report_count = 33809
        # 点评率 = 点评报告数 / 已完成报告数
        month_remarks_rate = remarks_report_count / month_finished

        # 合格数
        remarks_report_pass_count = 43000
        # 不合格数
        remarks_report_no_pass_count = 12000
        # 合格率 = 合格数 /（合格数+不合格数）
        remarks_report_pass_process = (remarks_report_pass_count /
                                       (remarks_report_no_pass_count + remarks_report_pass_count))

        return [
            month_finish_report_count,
            month_finished,
            '{:.2%}'.format(month_finished_process),
            '{:.2f}'.format(month_finished_process * 100),

            remarks_report_count,
            '{:.2%}'.format(month_remarks_rate),
            '{:.2%}'.format(month_remarks_rate),
            '{:.2f}'.format(month_remarks_rate * 100),

            remarks_report_count,
            remarks_report_pass_count,
            remarks_report_no_pass_count,
            '{:.2%}'.format(remarks_report_pass_process),
            '{:.2f}'.format(remarks_report_pass_process * 100)
        ]

    @dash_app.callback(
        Output('graph_month_finish', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_month_finish_graph(signal_data):
        fig = go.Figure(go.Funnelarea(
            text=["应完成", "已完成", "点评数", "合格数"],
            values=[60000, 45000, 35000, 30000],
            showlegend=False
        ))
        # fig.update_layout(textposition="outside", showlegend=False)
        return fig

    @dash_app.callback(
        Output('graph_area_detail', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_area_detail_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "武汉运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "武汉运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "武汉运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "杭州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "杭州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "杭州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "杭州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "南京运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "南京运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "南京运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "南京运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "长沙运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "长沙运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "长沙运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "长沙运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "广州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "广州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "广州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "广州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "福州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "福州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "福州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "福州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "上海运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "上海运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "上海运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "上海运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "成都运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "成都运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "成都运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "成都运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "重庆运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "重庆运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "重庆运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "重庆运营中心", "name": "未完成", "value": random.randint(0, 50)},
        ])
        fig = px.bar(df, x="value", y="area", color="name",
                     hover_data=["area", "name"],
                     color_discrete_map={
                         '合格数': 'rgb(92,176,254)',
                         '不合格数': 'rgb(78,203,115)',
                         '未点评': 'rgb(251,212,55)',
                         '未完成': 'rgb(67,81,136)',

                     },
                     template="simple_white"
                     )
        return fig

    @dash_app.callback(
        Output('graph_task_1', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_task1_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "武汉运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "武汉运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "武汉运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "杭州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "杭州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "杭州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "杭州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "南京运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "南京运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "南京运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "南京运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "长沙运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "长沙运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "长沙运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "长沙运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "广州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "广州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "广州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "广州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "福州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "福州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "福州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "福州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "上海运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "上海运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "上海运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "上海运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "成都运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "成都运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "成都运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "成都运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "重庆运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "重庆运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "重庆运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "重庆运营中心", "name": "未完成", "value": random.randint(0, 50)},
        ])
        fig = px.bar(df, x="area", y="value", color="name",
                     color_discrete_map={
                         '合格数': 'rgb(92,176,254)',
                         '不合格数': 'rgb(78,203,115)',
                         '未点评': 'rgb(251,212,55)',
                         '未完成': 'rgb(67,81,136)',

                     },
                     template="simple_white")
        return fig

    @dash_app.callback(
        Output('graph_task_2', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_task2_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "武汉运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "武汉运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "武汉运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "杭州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "杭州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "杭州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "杭州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "南京运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "南京运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "南京运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "南京运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "长沙运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "长沙运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "长沙运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "长沙运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "广州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "广州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "广州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "广州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "福州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "福州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "福州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "福州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "上海运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "上海运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "上海运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "上海运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "成都运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "成都运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "成都运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "成都运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "重庆运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "重庆运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "重庆运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "重庆运营中心", "name": "未完成", "value": random.randint(0, 50)},
        ])
        fig = px.bar(df, x="area", y="value", color="name",
                     color_discrete_map={
                         '合格数': 'rgb(92,176,254)',
                         '不合格数': 'rgb(78,203,115)',
                         '未点评': 'rgb(251,212,55)',
                         '未完成': 'rgb(67,81,136)',

                     },
                     template="simple_white"
                     )
        return fig

    @dash_app.callback(
        Output('graph_task_3', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_task3_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "武汉运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "武汉运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "武汉运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "杭州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "杭州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "杭州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "杭州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "南京运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "南京运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "南京运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "南京运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "长沙运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "长沙运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "长沙运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "长沙运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "广州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "广州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "广州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "广州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "福州运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "福州运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "福州运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "福州运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "上海运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "上海运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "上海运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "上海运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "成都运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "成都运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "成都运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "成都运营中心", "name": "未完成", "value": random.randint(0, 50)},

            {"area": "重庆运营中心", "name": "合格数", "value": random.randint(0, 100)},
            {"area": "重庆运营中心", "name": "不合格数", "value": random.randint(0, 50)},
            {"area": "重庆运营中心", "name": "未点评", "value": random.randint(0, 30)},
            {"area": "重庆运营中心", "name": "未完成", "value": random.randint(0, 50)},
        ])
        fig = px.bar(df, x="area", y="value", color="name",
                     color_discrete_map={
                         '合格数': 'rgb(92,176,254)',
                         '不合格数': 'rgb(78,203,115)',
                         '未点评': 'rgb(251,212,55)',
                         '未完成': 'rgb(67,81,136)',

                     },
                     template="simple_white"
                     )
        return fig

    @dash_app.callback(
        Output('graph_indicator_trend', 'figure'),
        [
            Input('signal', 'data'),
        ]
    )
    def update_indicator_trend_graph(data):
        df = pd.DataFrame([
            {"month": "2020年10月", "name": "完成率", "value": 100},
            {"month": "2020年10月", "name": "点评率", "value": 95},
            {"month": "2020年10月", "name": "合格率", "value": 85},
            {"month": "2020年11月", "name": "完成率", "value": 90},
            {"month": "2020年11月", "name": "点评率", "value": 88},
            {"month": "2020年11月", "name": "合格率", "value": 80},
            {"month": "2020年12月", "name": "完成率", "value": 98},
            {"month": "2020年12月", "name": "点评率", "value": 89},
            {"month": "2020年12月", "name": "合格率", "value": 80},
            {"month": "2021年01月", "name": "完成率", "value": 95},
            {"month": "2021年01月", "name": "点评率", "value": 90},
            {"month": "2021年01月", "name": "合格率", "value": 88},
            {"month": "2021年02月", "name": "完成率", "value": 100},
            {"month": "2021年02月", "name": "点评率", "value": 91},
            {"month": "2021年02月", "name": "合格率", "value": 82},
            {"month": "2021年03月", "name": "完成率", "value": 80},
            {"month": "2021年03月", "name": "点评率", "value": 75},
            {"month": "2021年03月", "name": "合格率", "value": 68},
            {"month": "2021年04月", "name": "完成率", "value": 91},
            {"month": "2021年04月", "name": "点评率", "value": 81},
            {"month": "2021年04月", "name": "合格率", "value": 72},
            {"month": "2021年05月", "name": "完成率", "value": 100},
            {"month": "2021年05月", "name": "点评率", "value": 96},
            {"month": "2021年05月", "name": "合格率", "value": 84},
            {"month": "2021年06月", "name": "完成率", "value": 97},
            {"month": "2021年06月", "name": "点评率", "value": 85},
            {"month": "2021年06月", "name": "合格率", "value": 78},
            {"month": "2021年07月", "name": "完成率", "value": 100},
            {"month": "2021年07月", "name": "点评率", "value": 93},
            {"month": "2021年07月", "name": "合格率", "value": 89},
        ])
        fig = px.line(df, x='month', y='value', color='name',
                      labels={'month': '月份', 'value': '比例', 'name': '指标'},
                      template="simple_white")
        return fig

    @dash_app.callback(
        Output('graph_area_item_trend', 'figure'),
        [
            Input('signal', 'data'),
        ]
    )
    def update_area_item_trend_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "武汉运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "武汉运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "武汉运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "武汉运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "武汉运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "武汉运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "武汉运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "武汉运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "武汉运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "武汉运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "武汉运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "武汉运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "武汉运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "武汉运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "武汉运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "武汉运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "武汉运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "武汉运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "武汉运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "武汉运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "武汉运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "武汉运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "武汉运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "武汉运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "武汉运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "武汉运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "武汉运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "武汉运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "武汉运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "杭州运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "杭州运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "杭州运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "杭州运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "杭州运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "杭州运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "杭州运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "杭州运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "杭州运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "杭州运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "杭州运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "杭州运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "杭州运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "杭州运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "杭州运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "杭州运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "杭州运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "杭州运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "杭州运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "杭州运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "杭州运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "杭州运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "杭州运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "杭州运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "杭州运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "杭州运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "杭州运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "杭州运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "杭州运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "杭州运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "南京运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "南京运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "南京运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "南京运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "南京运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "南京运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "南京运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "南京运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "南京运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "南京运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "南京运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "南京运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "南京运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "南京运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "南京运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "南京运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "南京运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "南京运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "南京运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "南京运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "南京运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "南京运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "南京运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "南京运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "南京运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "南京运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "南京运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "南京运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "南京运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "南京运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "长沙运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "长沙运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "长沙运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "长沙运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "长沙运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "长沙运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "长沙运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "长沙运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "长沙运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "长沙运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "长沙运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "长沙运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "长沙运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "长沙运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "长沙运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "长沙运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "长沙运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "长沙运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "长沙运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "长沙运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "长沙运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "长沙运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "长沙运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "长沙运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "长沙运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "长沙运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "长沙运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "长沙运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "长沙运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "长沙运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "广州运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "广州运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "广州运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "广州运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "广州运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "广州运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "广州运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "广州运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "广州运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "广州运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "广州运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "广州运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "广州运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "广州运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "广州运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "广州运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "广州运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "广州运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "广州运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "广州运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "广州运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "广州运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "广州运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "广州运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "广州运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "广州运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "广州运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "广州运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "广州运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "广州运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "福州运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "福州运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "福州运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "福州运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "福州运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "福州运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "福州运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "福州运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "福州运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "福州运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "福州运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "福州运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "福州运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "福州运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "福州运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "福州运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "福州运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "福州运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "福州运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "福州运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "福州运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "福州运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "福州运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "福州运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "福州运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "福州运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "福州运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "福州运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "福州运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "福州运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "上海运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "上海运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "上海运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "上海运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "上海运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "上海运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "上海运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "上海运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "上海运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "上海运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "上海运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "上海运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "上海运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "上海运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "上海运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "上海运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "上海运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "上海运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "上海运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "上海运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "上海运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "上海运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "上海运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "上海运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "上海运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "上海运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "上海运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "上海运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "上海运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "上海运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "成都运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "成都运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "成都运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "成都运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "成都运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "成都运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "成都运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "成都运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "成都运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "成都运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "成都运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "成都运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "成都运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "成都运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "成都运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "成都运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "成都运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "成都运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "成都运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "成都运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "成都运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "成都运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "成都运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "成都运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "成都运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "成都运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "成都运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "成都运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "成都运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "成都运营中心", "month": "2021年07月", "name": "合格率", "value": 89},

            {"area": "重庆运营中心", "month": "2020年10月", "name": "完成率", "value": 100},
            {"area": "重庆运营中心", "month": "2020年10月", "name": "点评率", "value": 95},
            {"area": "重庆运营中心", "month": "2020年10月", "name": "合格率", "value": 85},
            {"area": "重庆运营中心", "month": "2020年11月", "name": "完成率", "value": 90},
            {"area": "重庆运营中心", "month": "2020年11月", "name": "点评率", "value": 88},
            {"area": "重庆运营中心", "month": "2020年11月", "name": "合格率", "value": 80},
            {"area": "重庆运营中心", "month": "2020年12月", "name": "完成率", "value": 98},
            {"area": "重庆运营中心", "month": "2020年12月", "name": "点评率", "value": 89},
            {"area": "重庆运营中心", "month": "2020年12月", "name": "合格率", "value": 80},
            {"area": "重庆运营中心", "month": "2021年01月", "name": "完成率", "value": 95},
            {"area": "重庆运营中心", "month": "2021年01月", "name": "点评率", "value": 90},
            {"area": "重庆运营中心", "month": "2021年01月", "name": "合格率", "value": 88},
            {"area": "重庆运营中心", "month": "2021年02月", "name": "完成率", "value": 100},
            {"area": "重庆运营中心", "month": "2021年02月", "name": "点评率", "value": 91},
            {"area": "重庆运营中心", "month": "2021年02月", "name": "合格率", "value": 82},
            {"area": "重庆运营中心", "month": "2021年03月", "name": "完成率", "value": 80},
            {"area": "重庆运营中心", "month": "2021年03月", "name": "点评率", "value": 75},
            {"area": "重庆运营中心", "month": "2021年03月", "name": "合格率", "value": 68},
            {"area": "重庆运营中心", "month": "2021年04月", "name": "完成率", "value": 91},
            {"area": "重庆运营中心", "month": "2021年04月", "name": "点评率", "value": 81},
            {"area": "重庆运营中心", "month": "2021年04月", "name": "合格率", "value": 72},
            {"area": "重庆运营中心", "month": "2021年05月", "name": "完成率", "value": 100},
            {"area": "重庆运营中心", "month": "2021年05月", "name": "点评率", "value": 96},
            {"area": "重庆运营中心", "month": "2021年05月", "name": "合格率", "value": 84},
            {"area": "重庆运营中心", "month": "2021年06月", "name": "完成率", "value": 97},
            {"area": "重庆运营中心", "month": "2021年06月", "name": "点评率", "value": 85},
            {"area": "重庆运营中心", "month": "2021年06月", "name": "合格率", "value": 78},
            {"area": "重庆运营中心", "month": "2021年07月", "name": "完成率", "value": 100},
            {"area": "重庆运营中心", "month": "2021年07月", "name": "点评率", "value": 93},
            {"area": "重庆运营中心", "month": "2021年07月", "name": "合格率", "value": 89},
        ])

        fig = px.line(df, x="month", y="value", color='name', facet_col="area", facet_col_wrap=3,
                      labels={'month': '月份', 'name': '指标', 'value': '比例'},
                      template="simple_white")

        return fig

    @dash_app.callback(
        Output('graph_indicator_relevance', 'figure'),
        [
            Input('signal', 'data'),
        ])
    def update_indicator_relevance_graph(signal_data):
        df = pd.DataFrame([
            {"area": "武汉运营中心", "month": "2020年10月",
             "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2020年10月",
             "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2020年10月",
             "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2020年10月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2020年11月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2020年12月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年01月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年02月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年03月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年04月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年05月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年06月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年07月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

            {"area": "武汉运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "杭州运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "南京运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "长沙运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "广州运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "福州运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "上海运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "成都运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},
            {"area": "重庆运营中心", "month": "2021年08月", "finish": random.randint(0, 100), "pass": random.randint(0, 98),
             "remarks": random.randint(0, 95), "total": random.randint(1000, 5000)},

        ])
        fig = px.scatter(df, x="pass", y="finish",
                         size="total", color="area", hover_name="area",
                         log_x=True, size_max=60,
                         labels={
                             'pass': '合格率',
                             'finish': '完成率',
                             'total': '门店数量',
                             'area': '区域',
                         },
                         template="simple_white")

        return fig

    @dash_app.callback(
        Output('question_distribution_graph', 'figure'),
        [
            Input('choices_item_category', 'value'),
            Input('choices_item_date', 'value'),
            Input('signal', 'data'),
        ])
    def update_question_distribution_graph(category_value, date_value, signal_data):
        df = pd.DataFrame([
            {"category": "Q-物料来源", "item": "物料来源巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "Q-物料来源", "item": "物料来源巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "Q-物料来源", "item": "物料来源巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "Q-物料来源", "item": "物料来源巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "Q-物料来源", "item": "物料来源巡检项5",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "Q-物料来源", "item": "物料来源巡检项6",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项5",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "备料管控", "item": "备料管控巡检项6",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "水果管控", "item": "水果管控巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "水果管控", "item": "水果管控巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "水果管控", "item": "水果管控巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "水果管控", "item": "水果管控巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "水果管控", "item": "水果管控巡检项5",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "开封原料", "item": "开封原料巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "开封原料", "item": "开封原料巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "开封原料", "item": "开封原料巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "效期管理", "item": "效期管理巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "效期管理", "item": "效期管理巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "效期管理", "item": "效期管理巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "效期管理", "item": "效期管理巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "储藏管理", "item": "储藏管理巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "储藏管理", "item": "储藏管理巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "储藏管理", "item": "储藏管理巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "储藏管理", "item": "储藏管理巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "交叉感染", "item": "交叉感染巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "交叉感染", "item": "交叉感染巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "交叉感染", "item": "交叉感染巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "否决项/重点项", "item": "否决项/重点项巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "否决项/重点项", "item": "否决项/重点项巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "OP操作", "item": "OP操作巡检项1",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "OP操作", "item": "OP操作巡检项2",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "OP操作", "item": "OP操作巡检项3",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "OP操作", "item": "OP操作巡检项4",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
            {"category": "OP操作", "item": "OP操作巡检项5",
             "noPassCount": random.randint(0, 500), "checkCount": random.randint(100, 1000)},
        ])

        dff = df[df["category"] == category_value] if category_value and category_value != '' else df
        fig = px.sunburst(dff,
                          path=['category', 'item'], values='noPassCount',
                          color='checkCount', hover_data=['category', 'noPassCount'],
                          labels={
                              'checkCount': '巡检次数',
                              'category': '类别',
                              'item': '巡检项',
                              'noPassCount': '不合格次数',
                          },
                          color_continuous_scale='RdBu',
                          color_continuous_midpoint=np.average(df['checkCount'], weights=df['noPassCount'])
                          )
        return fig

    @dash_app.callback(
        [
            Output('question_diff_tab', 'children'),
            # Output('question_diff_tab_graph', 'figure'),
            Output('question_diff_bar_graph', 'figure'), ],
        [
            Input('choices_diff_category', 'value'),
            Input('choices_diff_month', 'value'),
            Input('signal', 'data'),
        ])
    def update_question_diff_graph(category_value, month_value, signal_data):
        table_data = [
            # ['类别', '上月检查次数', '不合格次数', '本月检查次数', '本月不合格次数'],
            ['Q-物料来源', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['备料管控', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['水果管控', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['开封原料', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['效期管理', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['储藏管理', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['交叉感染', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['否决项/重点项', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)],
            ['OP操作', random.randint(1, 1000), random.randint(1, 100), random.randint(1, 1000),
             random.randint(1, 100)]
        ]

        tab_df = pd.DataFrame(table_data, columns=['类别', '上月检查次数', '不合格次数', '本月检查次数', '本月不合格次数'])
        tab_dff = tab_df[tab_df["类别"] == category_value] if category_value else tab_df

        ths = []
        for h in tab_dff.columns:
            ths.append(html.Th(children=h, style={}))

        table_header = [
            html.Thead(html.Tr(ths))
        ]
        rows = []
        for t in tab_dff.values:
            tds = []
            for v in t:
                tds.append(html.Td(children=v))
            rows.append(html.Tr(children=tds))

        table_body = [html.Tbody(children=rows)]

        table = [
            dbc.Table(children=table_header + table_body, responsive=True, style={'width': '200px'})
        ]
        # tab_fig = ff.create_table(table_data, height_constant=40)

        bar_df = pd.DataFrame([
            {"name": "Q-物料来源", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "备料管控", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "水果管控", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "开封原料", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "效期管理", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "储藏管理", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "交叉感染", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "否决项/重点项", "month": "2021年9月", "rate": random.randint(1, 100)},
            {"name": "OP操作", "month": "2021年9月", "rate": random.randint(1, 100)},

            {"name": "Q-物料来源", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "备料管控", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "水果管控", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "开封原料", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "效期管理", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "储藏管理", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "交叉感染", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "否决项/重点项", "month": "2021年8月", "rate": -(random.randint(1, 100))},
            {"name": "OP操作", "month": "2021年8月", "rate": -(random.randint(1, 100))},

        ])
        bar_dff = bar_df[bar_df["name"] == category_value] if category_value else bar_df

        bar_fig = px.bar(bar_dff, x="rate", y="name", color='month', orientation='h',
                         category_orders={'name': [c for c in bar_dff['name']]},
                         hover_name='month',
                         labels={'month': '月份', 'rate': '数量', 'name': '问题项'},
                         text=[str(math.fabs(c)) for c in bar_dff["rate"]],
                         template="plotly_white")
        bar_fig.update()

        return [table, bar_fig]
