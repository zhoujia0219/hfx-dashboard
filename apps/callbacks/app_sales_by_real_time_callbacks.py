import math
import time
import json

import dash
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from pandas import DataFrame
import pandas as pd

from services import srv_sales_real_time

###############
# 回调
###############
from services.srv_comm_dim import get_ZE_PJS_ZWS
from services.srv_sales_real_time import get_all_areaname
from utils.thread_one_interface import MyThread


def register_callbacks(dash_app):
    ###############
    # 页面内容构建刷新函数
    ###############
    def sale_month_fig(data_x, data_y, data_sum, range_choice):
        """
        销售月数据
        :param data_x:
        :param data_y:
        :param data_sum: pic_dff.sum()
        :return:
        """

        pic_data = srv_sales_real_time.sales_month(range_choice)
        if len(pic_data) < 1:
            return dash.no_update
        if data_x == data_y:
            return dash.no_update
        area_name = get_all_areaname()  # 所有战区名字
        data = list()
        fig = ""
        for i in area_name:
            pic = pic_data[pic_data["areaname3"] == i[0]]  # 对每个战区取数
            pic_dff = pic.groupby([data_x], as_index=False)['dealtotal']
            pic_dff = eval(data_sum)
            data.append(go.Scatter(
                name=i[0],
                x=pic_dff['day'],
                y=pic_dff['dealtotal'],
                mode="lines",
            ),
            )
            fig = go.Figure(data)
        return fig

    @dash_app.callback(
        Output('sales_month', 'figure'),
        [
            Input('total_avg_mid', 'value'),
            Input('range_choice', 'value')
        ]
    )
    def sale_day_month(total_avg_mid, range_choice):
        """
        销售月分布
        """
        fig_sales_month = sale_month_fig("day", "dealtotal", get_ZE_PJS_ZWS()[total_avg_mid],range_choice)
        return fig_sales_month
