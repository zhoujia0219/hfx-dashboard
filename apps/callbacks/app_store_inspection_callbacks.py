import datetime
import plotly.express as px
import pandas as pd
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

    # 巡检情况完成率趋势——折线图
    @dash_app.callback(
        Output('graph_inspection_line', 'figure'),
        [Input('area_choice', 'value'),Input('year_choice', 'value')]
    )
    def build_fig_inspect_finish_line(filter_values,year_value):
        """
        巡检情况完成率趋势折线图
        :param df: 数据
        :return: 返回图形
        """
        # 调用方法--巡检情况完成率
        inspection_current = srv_store_inspection.find_store_inspect_finish_rate(filter_values,year_value).values
        if len(inspection_current) < 1:
            return dash.no_update

        # def get_month_range():
        #     end_day = datetime.datetime.now()
        #     start_day = datetime.datetime.strptime(
        #         str(int(end_day.year) - 1) + "-" + str(end_day.month) + "-" + str(end_day.day), '%Y-%m-%d').date()
        #     months = (end_day.year - start_day.year) * 12 + end_day.month - start_day.month
        #     month_range = [str('%s-%s' % (start_day.year + mon // 12, mon % 12 + 1))
        #                    for mon in range(start_day.month - 1, start_day.month + months)]
        #     return month_range
        nameLink = []
        oneLink = []
        twoLink = []
        for i in inspection_current:
            nameLink.append(i[1])
            oneLink.append(i[3])
            twoLink.append(i[4])

        fig = go.Figure(data=[
            go.Scatter(
                name='巡检门店完成率',
                x=nameLink,
                y=oneLink,
                marker={
                    "color": "#FFA488",# 线条的颜色_橙色
                    "line": {
                        "width": 10,  # 线条上点的大小
                        "color": "rgba(1, 170, 118, 0.3)",  # 点的颜色
                    }
                }
            ),
            go.Scatter(
                name='巡检次数完成率',
                x=nameLink,
                y=twoLink,
                marker={
                    "color": "#99BBFF", # 线条的颜色_浅蓝色
                    "line": {
                        "width": 10,  # 线条上点的大小
                        "color": "rgba(1, 170, 118, 0.3)", # 点的颜色
                    }
                }
            )
        ])

        fig.update_layout(
            # showlegend=False,
            plot_bgcolor='white',
            # template='plotly_white',
            height=400,
            # margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig


    # 01_bar直方图 巡检情况完成率
    @dash_app.callback(
        Output('graph_finish_bar', 'figure'),
        [Input('sort_choice_01', 'value'), Input('finish_fig_month_choice', 'value')]
    )
    def update_graph_bar_01(val1, val2):
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
            marker={
                "color": "#FFDDAA",
            },
            # 指定为水平方向即可
            orientation="h"
        )
        fig = go.Figure(data=[trace0])
        fig.update_layout(
            height=300,
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig


    # 02_bar直方图 巡检情况合格率
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
            marker={
                "color": "#FFDDAA",
            },
            name="巡检门店合格率",
            # 指定为水平方向即可
            orientation="h"
        )
        fig = go.Figure(data=[trace0])
        fig.update_layout(
            height=300,
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig


    # 03_bar直方图 巡检情况整改率
    @dash_app.callback(
        Output('graph_rectify_bar', 'figure'),
        [Input('sort_choice_03', 'value'), Input('rectify_fig_month_choice', 'value')]
    )
    def update_graph_bar_03(val1, val2):
        # # 调用方法--巡检情况完成率
        inspection_current = srv_store_inspection.find_store_inspect_rectify_rate_01(val2, val1).values
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
            marker={
                "color": "#FFDDAA",
            },
            name="巡检门店整改率",
            # 指定为水平方向即可
            orientation="h"
        )
        fig = go.Figure(data=[trace0])
        fig.update_layout(
            height=300,
            showlegend=False,
            plot_bgcolor='white',
            margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig


    # 折线图—实现标题回调（区域）
    @dash_app.callback(
        Output('area_choice_title', 'children'),Input('area_choice', 'value')
    )
    def update_line_title(value):
        return value+" "+"巡检完成率趋势"

    # 定义方法，实现三个直方图的标题回调（月份）
    def concat_str(value, str_):
        """拼接字符串
        param：value:回调函数的值
               str_：最后拼接的字符串
        """
        return (value.replace('0', "") if value[0:1] == "0" else value) + '月份 {}'.format(str_)

    # 图一 调用方法，完成率_直方图—实现标题回调（月份）
    @dash_app.callback(
        Output('month_choice_bar_finish_title', 'children'), Input('finish_fig_month_choice', 'value')
    )
    def update_bar_title(value):
        """图一 完成率_直方图—实现标题回调（月份）"""
        return concat_str(value, "巡检完成率排名")

    # 图二 调用方法，合格率_直方图—实现标题回调（月份）
    @dash_app.callback(
        Output('month_choice_bar_regular_title', 'children'), Input('regular_fig_month_choice', 'value')
    )
    def update_bar_title(value):
        """图二 合格率_直方图—实现标题回调（月份）"""
        return concat_str(value, '巡检合格率排名')

    # 图三 调用方法，整改率_直方图—实现标题回调（月份）
    @dash_app.callback(
        Output('month_choice_bar_rectify_title', 'children'), Input('rectify_fig_month_choice', 'value')
    )
    def update_bar_title(value):
        """图三 整改率_直方图—实现标题回调（月份）"""
        return concat_str(value, '巡检整改率排名')


    # 门店巡检项合格率—甜甜圈图
    @dash_app.callback(
        Output('graph_inspect_item_pie','figure'),
        Input('inspect_item_area_choice','value')
    )
    def pie_inspect_item_rate(filter_values):
        """
        门店巡检项合格率——饼图
        """
        inspect_item_rate_data = srv_store_inspection.find_inspect_style_regular_pie(filter_values)
        # index = 1 if inspect_rate == "finish" else 0
        if len(inspect_item_rate_data) < 1:
            return " "
        else:
            colors = ['#FFC573','#99BBFF','#FF9DB5','#FFCCCC','#5599FF']
            item_regular_name = []
            item_regular = []
            for item in inspect_item_rate_data:
                item_regular_name.append(item[1])
                item_regular.append(item[4])
            fig = go.Figure(data=[go.Pie(
                labels=item_regular_name,
                # labels={'text-align': 'right','value':'item_regular_name'},
                values=item_regular,
                hole=0.6,
                text=item_regular_name,
                marker=dict(colors=colors, line=dict(color='white', width=2)),
                # showlegend=False,
                textinfo='percent',
                hoverinfo="label+percent", )])
            fig.update_layout(
                height=320,
                paper_bgcolor="#FFFFFF",
                # showlegend=False,
                margin=dict(t=5, l=5, b=5, r=5),
            #     legend_orientation="h",
            #     legend=dict(
            #         font=dict(
            #             # family="sans-serif",
            #             size=10,
            #         )
            #     )
            )
            return fig


    # 不合格门店巡检类型分布—雷达图
    @dash_app.callback(
        Output('graph_inspect_style_radar', 'figure'),
        Input('inspect_style_area_choice', 'value')
    )
    def inspect_item_radar(val):
        """
        不合格
        巡检项类型分布雷达图
        :return:
        """
        store_inspect_style_rate_data = srv_store_inspection.find_store_inspect_style_rate(val)
        title_data = []
        bl_data = []
        for idata in store_inspect_style_rate_data:
            title_data.append(idata[1])
            bl_data.append(idata[3])
        # df = pd.DataFrame(dict(
        #     r=bl_data,
        #     theta=title_data
        # ))
        # fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=bl_data,
            theta=title_data,
            fill='toself',
            name='ProductA'
        ))
        fig.update_layout(
            height=320,
            showlegend=False,
            margin=dict(t=1, l=5, b=1, r=5),
            polar=dict(
                radialaxis=dict(
                    visible=True
                )
            )
        )
        return fig


    # 合格巡检项类型分布—树状图
    @dash_app.callback(
        Output('graph_inspect_style_tree', 'figure'),
        Input('inspect_tree_area_choice', 'value')
    )
    def build_inspect_tree(val):
        """
        合格巡检类别treemap
        :return:
        """
        regular_data = srv_store_inspection.find_inspect_style_regular(val)
        # area = regular_data[0][0]
        # inspect_category = regular_data[0][1]
        # regular_value = regular_data[0][2]
        # fig = px.treemap(regular_data, path=[area, inspect_category], values=regular_value)
        all_data = []
        for idata in regular_data:
            da = []
            # da.append(idata[0])
            da.append(idata[1])
            da.append(idata[2])
            da.append(idata[3])
            all_data.append(da)
        df = pd.DataFrame(all_data, columns=['inspect_category', 'inspect_item', 'usm'])
        df["all"] = "inspect_category"  # in order to have a single root node
        fig = px.treemap(df,
                         path=['inspect_category', 'inspect_item'],  # 层级顺序
                         values='usm',  # 面积大小用usm字段决定
                         color_continuous_scale='Geyser'
                         )
        # fig.show()
        fig.update_layout(
            height=320,
            showlegend=False,
            margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig







