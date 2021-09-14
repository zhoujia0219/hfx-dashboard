import datetime

import dash
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from services import srv_store_inspection
from apps.layouts.app_store_instpection_layouts import get_store_area


###############
# 回调
###############
# from services.srv_comm_dim import
# from services.srv_store_inspection import get_all_areaname
# from utils.date_util import get_day_hour


def register_callbacks(dash_app):
    ###############
    # 页面内容构建刷新函数
    ###############

    # 行2左边 巡检情况完成率趋势——折线图
    @dash_app.callback(
        Output('graph_inspection_line', 'figure'),
        Input('area_choice', 'value')
    )
    def build_fig_inspect_finish_line(filter_values):
        """
        巡检情况完成率趋势图
        :param df: 数据
        :return: 返回图形
        """
        # 调用方法--巡检情况完成率
        inspection_current = srv_store_inspection.find_store_inspect_finish_rate(filter_values).values
        if len(inspection_current) < 1:
            return dash.no_update

        def get_month_range():
            end_day = datetime.datetime.now()
            start_day = datetime.datetime.strptime(
                str(int(end_day.year) - 1) + "-" + str(end_day.month) + "-" + str(end_day.day), '%Y-%m-%d').date()
            months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
            month_range = [str('%s-%s' % (start_day.year + mon // 12, mon % 12 + 1))
                           for mon in range(start_day.month - 1, start_day.month + months)]
            return month_range

        oneLink = []
        twoLink = []
        for i in inspection_current:
            oneLink.append(i[2])
            twoLink.append(i[3])

        fig = go.Figure(data=[
            go.Scatter(name='巡检门店完成率', x=get_month_range(), y=oneLink),
            go.Scatter(name='巡检次数完成率', x=get_month_range(), y=twoLink)
        ])
        return fig

    # bar直方图 巡检情况完成率
    @dash_app.callback(
        Output('graph_finish_bar', 'figure'),
        [Input('sort_choice_01', 'value'), Input('finish_fig_month_choice', 'value')]

    )
    def update_graph_bar_01(val1, val2):
        # # 调用方法--巡检情况完成率
        inspection_current = srv_store_inspection.find_store_inspect_finish_rate_01(val2, val1).values
        print(inspection_current,2332322)
        if len(inspection_current) < 1:
            # return dash.no_update
            return ""
        nameiLnk = []
        oneLink = []
        twoLink = []
        for i in inspection_current:
            nameiLnk.append(i[1])
            oneLink.append(i[2])
            twoLink.append(i[3])

        trace0 = go.Bar(
            # 方向变了，所以 x 轴和 y 轴的数据也要调换位置
            y=nameiLnk,
            x=oneLink,
            name="巡检门店完成率",

            # 指定为水平方向即可
            orientation="h"
        )

        fig = go.Figure(data=[trace0])
        return fig

    # bar直方图 巡检情况合格率
    @dash_app.callback(
        Output('graph_regular_bar', 'figure'),
        [Input('sort_choice_02', 'value'), Input('regular_fig_month_choice', 'value')]

    )
    def update_graph_bar_02(val1, val2):
        # # 调用方法--巡检情况合格率
        inspection_current = srv_store_inspection.find_store_inspect_regular_rate_01(val2, val1).values
        if len(inspection_current) < 1:
            return dash.no_update
        nameiLnk = []
        oneLink = []
        twoLink = []
        for i in inspection_current:
            nameiLnk.append(i[1])
            oneLink.append(i[2])
            twoLink.append(i[3])
        trace0 = go.Bar(
            # 方向变了，所以 x 轴和 y 轴的数据也要调换位置
            y=nameiLnk,
            x=oneLink,
            name="巡检门店合格率",

            # 指定为水平方向即可
            orientation="h"
        )
        fig = go.Figure(data=[trace0])
        return fig

    # bar直方图 巡检情况整改率
    @dash_app.callback(
        Output('graph_rectify_bar', 'figure'),
        [Input('sort_choice_03', 'value'), Input('rectify_fig_month_choice', 'value')]

    )
    def update_graph_bar_03(val1, val2):
        # # 调用方法--巡检情况完成率
        inspection_current = srv_store_inspection.find_store_inspect_finish_rate_01(val2, val1).values
        if len(inspection_current) < 1:
            return dash.no_update
        nameiLnk = []
        oneLink = []
        twoLink = []
        for i in inspection_current:
            nameiLnk.append(i[1])
            oneLink.append(i[2])
            twoLink.append(i[3])
        trace0 = go.Bar(
            # 方向变了，所以 x 轴和 y 轴的数据也要调换位置
            y=nameiLnk,
            x=oneLink,
            name="巡检门店完成率",

            # 指定为水平方向即可
            orientation="h"
        )

        trace1 = go.Bar(
            y=nameiLnk,
            x=twoLink,
            name="巡检次数完成率",

            orientation="h"
        )

        fig = go.Figure(data=[trace0, trace1])
        return fig

    # 折线图—实现标题回调（区域）
    @dash_app.callback(
        Output('area_choice_title', 'children'), Input('area_choice', 'value')
    )
    def update_line_title(value):
        return value + " " + "巡检完成率趋势"

    def concat_str(value, str_):
        """拼接字符串
        param：value:回调函数的值
               str_：最后拼接的字符串
        """

        return (value.replace('0', "") if value[0:1] == "0" else value) + '月份 {}'.format(str_)

    # 图一 完成率_直方图—实现标题回调（月份）
    @dash_app.callback(
        Output('month_choice_bar_finish_title', 'children'), Input('finish_fig_month_choice', 'value')
    )
    def update_bar_title(value):
        return concat_str(value, "巡检完成率排名")

    @dash_app.callback(
        Output('month_choice_bar_regular_title', 'children'), Input('regular_fig_month_choice', 'value')
    )
    def update_bar_title(value):
        """图二 合格率_直方图—实现标题回调（月份）"""
        return concat_str(value, '巡检合格率排名')

    # 图三 整改率_直方图—实现标题回调（月份）
    @dash_app.callback(
        Output('month_choice_bar_rectify_title', 'children'), Input('rectify_fig_month_choice', 'value')
    )
    def update_bar_title(value):

        return concat_str(value, '巡检整改率排名')
