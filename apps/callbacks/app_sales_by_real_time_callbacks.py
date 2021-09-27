import copy
import json
import math
from urllib.request import urlopen

import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html

import dash
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

from analog_data import today_area_sale_, yesterday_area_sale_, pie_key_category_sale_pie_today, \
    pie_key_category_sale_pie_yesterday, area_sale_rank_bar_today, area_sale_rank_bar_yesterday, china_data
from services import srv_sales_real_time

###############
# 回调
###############
from services.srv_comm_dim import get_ZE_PJS_ZWS
from services.srv_sales_real_time import get_all_areaname, sale_total
from utils.date_util import get_day_hour
from utils.tools import big_number_conduct


def register_callbacks(dash_app):
    ###############
    # 页面内容构建刷新函数
    ###############
    # 今日昨日销售额
    def sale_month_callback(data_x, data_y, data_sum, range_choice):
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
        layout = go.Layout(
            xaxis=dict(title="日期"),
            yaxis=dict(title="销售额（元/1M=1百万）"),
        )
        fig = go.Figure(data, layout=layout)
        fig.update_layout(
            barmode='group',
            template='plotly_white',
            width=1130
        )

        return fig

    def sale_day_fig(data_x, data_y, x_choice_time):
        """
        销售日数据
        :param data_x:
        :param data_y:
        :param data_sum: pic_dff.sum()
        :return:
        """
        day_hour_arang, all_time_list = get_day_hour(x_choice_time)
        today_data, yesterday_data = srv_sales_real_time.sales_day(all_time_list)  #
        if data_x == data_y:
            return ''
        pic_dff_today = today_data.groupby([data_x], as_index=False)['sale'].sum()  # 今日数据的聚合
        pic_dff_yesterday = yesterday_data.groupby([data_x], as_index=False)['sale'].sum()  # 昨日数据的聚合
        empty_pic = pd.DataFrame(day_hour_arang, columns=["times", "sale"])  # 所有时间点的dataframe
        pic_dff = pd.concat([pic_dff_today, pic_dff_yesterday])  # 拼接两天数据
        pic_dff = pd.concat([pic_dff, empty_pic])  # 拼接所有时间点
        pic_dff.drop_duplicates(subset=['times'], keep='first', inplace=True)  # 去重
        pic_dff = pic_dff.sort_values('times', ascending=True, inplace=False)  # 排序

        # 对颜色处理
        color_time_list = sorted(all_time_list[0] + all_time_list[1])
        # 按照显示的效果将颜色设置好
        color_list = ["darkgrey" if i in all_time_list[0] else '#44cef6' for i in color_time_list]
        trace = go.Bar(
            name="小时销售",
            x=pic_dff[data_x],
            y=pic_dff['sale'],
            marker=dict(color=color_list)
        )
        layout = go.Layout(
            xaxis=dict(title="时间（/小时）"),
            yaxis=dict(title="销售额（元/1M=1百万）"),
        )
        trace_avg = go.Scatter(  # 均值线
            x=pic_dff[data_x],
            y=[pic_dff['sale'].sum() / len(day_hour_arang) for _ in day_hour_arang],
            name="平均线",
            mode='lines',
            line=dict(color='blue', dash='dash')
        )
        fig = go.Figure(data=[trace, trace_avg], layout=layout)
        fig.update_layout(
            barmode='group',
            template='plotly_white',
            width=1130
        )
        fig.update_layout(
            showlegend=False,
            margin=dict(t=5, l=5, b=5, r=5)
        )
        return fig

    @dash_app.callback(
        Output('sales_real_time_day', 'figure'),
        [Input('x_choice_time', 'value'),
         Input("graph-update", "n_intervals")]
    )
    def sale_day_day_callback(x_choice_time, n):
        """
        销售日分布
        """
        fig_sales_day = sale_day_fig("times", "sale", x_choice_time),  # 画图
        return fig_sales_day[0]

    def day_area_sale_list(level_area):
        """
        销售日数据
        :param data_x:
        :param data_y:
        :return:
        """
        map_area = {"level_1": "area1", "level_2": "area2"}  # 根据选择确定对相应的列聚合
        group_name = map_area[level_area]  # 得出要分组列的name
        day_hour_arang, all_time_list = get_day_hour('1-24')
        today_data, yesterday_data = pd.DataFrame(today_area_sale_), pd.DataFrame(yesterday_area_sale_)  #
        # today_data, yesterday_data = srv_sales_real_time.sales_day(all_time_list)  #
        # if data_x == data_y:
        #     return ''

        pic_dff = pd.concat([today_data, yesterday_data])  # 聚合两天数据
        data = pic_dff.groupby([group_name])

        # map_area = {"level_1": "area1", "level_2": "area2"}  # 根据选择确定对相应的列聚合
        # group_name = map_area[level_area]  # 得出要分组列的name
        # day_hour_arang, all_time_list = get_day_hour('1-24')
        # today_data, yesterday_data = pd.DataFrame(today_area_sale_), pd.DataFrame(yesterday_area_sale_)  #
        # # today_data, yesterday_data = srv_sales_real_time.sales_day(all_time_list)  #
        # # if data_x == data_y:
        # #     return ''
        #
        # pic_dff = pd.concat([today_data, yesterday_data])  # 聚合两天数据
        # fig_number = 0
        # data = pic_dff.groupby([group_name])
        # for i, j in data:
        #     fig_number += 1
        # width_height = {  # 通过图形的数量动态的改变宽度和长度
        #     1: [360, 150], 2: [720, 150], 3: [1080, 150],
        #     4: [1080, 300], 5: [1080, 300], 6: [1080, 300],
        #     7: [1080, 450], 8: [1080, 450], 9: [1080, 450]
        # }
        # color_list = ["darkgrey" if str(i) in all_time_list[0] else '#44cef6' for i in pic_dff["times"]]
        # print(color_list, 53)
        # fig = px.bar(
        #     pic_dff,
        #     x='times',
        #     y="dealtotal",
        #     barmode="group",  # 柱状图模式取值
        #     facet_col='%s' % group_name,  # 列元素取值
        #     facet_col_wrap=3,
        #     # color=color_list,
        #     width=width_height[fig_number][0],
        #     height=width_height[fig_number][1],
        # )
        # fig.update_layout(
        #     showlegend=False,
        #     margin=dict(t=5, l=5, b=5, r=5),
        #     template='plotly_white',
        #
        # )
        # return fig
        trace_name = []
        for i, j in data:
            trace_name.append(i)
        fig = make_subplots(rows=3,  # 将画布分为3行
                            cols=3,  # 将画布分为3列
                            subplot_titles=trace_name,  # 子图的标题
                            )
        flag = 1  # 标记只能有9个
        for i, j in data:
            if flag < 9:
                # 分组之后的每个战区名字，每组数据
                area_name = i
                times_list = []  # 时间列表，x轴
                times_groupby = j.groupby("times")
                for a, b in times_groupby:
                    times_list.append(a)
                y_dealtotal = times_groupby.sum()["dealtotal"]
                # 对颜色处理
                color_time_list = sorted(all_time_list[0] + all_time_list[1])
                # 按照显示的效果将颜色设置好
                color_list = ["darkgrey" if i in all_time_list[0] else '#44cef6' for i in color_time_list]
                trace = go.Bar(
                    name="{}".format(area_name),
                    x=times_list,
                    y=y_dealtotal,
                    marker=dict(color=color_list),
                )
                # 对位置的添加
                fig.append_trace(trace, math.ceil(flag / 3), flag % 3 if flag % 3 != 0 else 3)
            else:
                break
            flag += 1
        fig.update_layout(
            showlegend=False,
            margin=dict(t=22, l=5, b=5, r=5)
        )
        return fig
        # fig_list = []
        # flag = 1  # 标记只能有9个
        # for i, j in data:
        #     if flag < 9:
        #         # 分组之后的每个战区名字，每组数据
        #         area_name = i
        #         times_list = []  # 时间列表，x轴
        #         times_groupby = j.groupby("times")
        #         for a, b in times_groupby:
        #             times_list.append(a)
        #         y_dealtotal = times_groupby.sum()["dealtotal"]
        #
        #         # 对颜色处理
        #         color_time_list = sorted(all_time_list[0] + all_time_list[1])
        #         # 按照显示的效果将颜色设置好
        #         color_list = ["darkgrey" if i in all_time_list[0] else '#44cef6' for i in color_time_list]
        #         trace = go.Bar(
        #             name="{}".format(area_name),
        #             x=times_list,
        #             y=y_dealtotal,
        #             marker=dict(color=color_list),
        #             xaxis='x'+str(i), #
        #             yaxis='y'+str(i)
        #         )
        #         layout = go.Layout(
        #             xaxis=dict(title="{}".format(area_name)),
        #         )
        #         fig = go.Figure(data=[trace, ], layout=layout)
        #         fig.update_layout(
        #             showlegend=False,
        #             margin=dict(t=5, l=5, b=5, r=5)
        #         )
        #         fig_list.append(fig)
        #     else:
        #         break
        #     flag += 1
        # if len(fig_list) < 9:  # 数据量不足
        #     for i in range(9 - len(fig_list)):
        #         fig_list.append("")
        # return fig_list

    @dash_app.callback(
        Output("day_area_fig_bar", "figure"),
        Input('area_level', 'value')
    )
    def day_area_sale_callback(value):
        """
        各区域本日销售分布
        """
        return day_area_sale_list(value)

    # @dash_app.callback(
    #     Output('sales_real_time_month', 'figure'),
    #     [
    #         Input('total_avg_mid', 'value'),
    #         Input('range_choice', 'value'),
    #         # Input("graph-update", "n_intervals")
    #
    #     ]
    # )
    # def sale_day_month(total_avg_mid, range_choice):
    #     """
    #     销售月分布
    #     """
    #     fig_sales_month = sale_month_fig("day", "dealtotal", get_ZE_PJS_ZWS()[total_avg_mid], range_choice)
    #     return fig_sales_month

    @dash_app.callback(
        Output("total_sale", "children"),
        Input("table_update", "n_intervals")
    )
    def update_total_sale_callback(n):
        """
        对销售总额的定时刷新
        """
        sale_total_form = sale_total()
        return [
            dbc.Col(
                html.H5(
                    children="销售总额"
                ),
                width=3
            ),
            dbc.Col(
                html.H5(
                    children="{}".format(big_number_conduct(sale_total_form[1], 2))
                ),
                width=3
            ),
            dbc.Col(
                html.H5(
                    children="{}".format(big_number_conduct(sale_total_form[0], 2))
                ),
                width=3
            ),
            dbc.Col(
                html.H5(
                    children="0%" if sale_total_form[0] == sale_total_form[1] else (
                            ("+" if sale_total_form[0] > sale_total_form[1] else "-") + "{}%".format(
                        round(sale_total_form[0] / sale_total_form[1] / 100, 2))),
                    style={
                        "backgroundColor": "red" if sale_total_form[0] > sale_total_form[1] else "green"} if
                    sale_total_form[0] != sale_total_form[1] else {}
                ),
                width=3
            )
        ]

    @dash_app.callback(
        Output("pie_key_category_sale_fig", "figure"),
        [
            Input("key_category_sale_pie1", "value"),
            Input("key_category_sale_pie2", "value")
        ]
    )
    def pie_key_category_sale_callback(value1, value2):
        """
        重点商品品类的销售情况饼图
        """
        if value2 == 'today':
            data = pd.DataFrame(pie_key_category_sale_pie_today)
        else:
            data = pd.DataFrame(pie_key_category_sale_pie_yesterday)

        # trace = go.Pie(labels=data['category_name'], values=data['dealtotal'], textfont=dict(size=15), )
        # layout = go.Layout(
        #     xaxis=dict(title="{}".format(1)),
        # )
        # fig = go.Figure(data=[trace, ], layout=layout)
        # fig.update_layout(
        #     showlegend=False,
        #     margin=dict(t=2, l=5, b=5, r=5)
        # )
        # fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=20,
        #                   # marker=dict(line=dict(color='#000000', width=2))
        #                   )
        # return fig
        fig = px.pie(data, values='dealtotal', names='category_name',
                     width=600
                     )
        fig.update_traces(textposition='outside', textinfo='percent+label', )
        fig.update_layout(
            showlegend=True,
            margin=dict(t=5, l=5, b=5, r=5),
            legend_orientation="h",  # 将颜色条放下面
            width=600
        )
        return fig

    @dash_app.callback(
        Output("key_category_sale_bar_fig", "figure"),
        Input("graph-update_3", "n_intervals")
    )
    def key_category_sale_bar_callback(n):
        """
        重点品类商品的横向条形图
        """
        today_data = pd.DataFrame(pie_key_category_sale_pie_today)
        yesterday_data = pd.DataFrame(pie_key_category_sale_pie_yesterday)
        data = today_data["dealtotal"] - yesterday_data["dealtotal"]
        color_list = ["red" if i < 0 else "#00bc12" for i in data]
        fig_list = [
            go.Bar(
                x=data,
                y=today_data['category_name'],
                text=[i if i < 0 else "+" + str(i) for i in data],
                orientation='h',
                marker=dict(color=color_list),
            ),
        ]
        layout = go.Layout(
            title='今日昨日销售数据比对', height=620, width=510, )

        fig = go.Figure(data=fig_list, layout=layout)
        fig.update_layout(
            barmode='group',
            template='plotly_white',
        )
        fig.update_traces(textposition='outside')  # 条形显示数据
        return fig

    @dash_app.callback(
        Output("area_sale_rank_fig", "figure"),
        [
            Input("area_sale_1", "value"),
            Input("area_sale_2", "value")
        ]
    )
    def area_sale_rank_bar_callback(value1, value2):
        """
        区域销售排名横向对比条形图
        """
        # if value2 == "one":
        #     area = 'area1'
        # else:
        #     area = 'area2'
        # today_data = pd.DataFrame(today_area_sale_).groupby(area)
        # yesterday_data = pd.DataFrame(yesterday_area_sale_).groupby(area)
        # y_axis = []
        # for i,j in today_data:
        #     y_axis.append(i)
        # today_sum_data = today_data.sum()
        # yesterday_sum_data = yesterday_data.sum()
        # data = today_sum_data["dealtotal"] - yesterday_sum_data["dealtotal"]
        # color_list = ["red" if i < 0 else "#00bc12" for i in data]
        # fig_list = [
        #     go.Bar(
        #         x=data,
        #         y=y_axis,
        #         text=[i if i < 0 else "+" + str(i) for i in data],
        #         orientation='h',
        #         marker=dict(color=color_list),
        #     ),
        # ]
        # layout = go.Layout(
        #     title='', height=850, width=510, )
        #
        # fig = go.Figure(data=fig_list, layout=layout)
        # fig.update_layout(
        #     barmode='group',
        #     template='plotly_white',
        # )
        # fig.update_traces(textposition='outside',texttemplate='%{text:.2s}')  # 条形显示数据
        # return fig
        # if value2 == "one":
        area = 'area1'
        # else:
        #     area = 'area2'
        today_data = pd.DataFrame(area_sale_rank_bar_today).groupby(area)
        yesterday_data = pd.DataFrame(area_sale_rank_bar_yesterday).groupby(area)
        y_axis = []
        for i, j in today_data:
            y_axis.append(i)
        today_sum_data = today_data.sum()
        yesterday_sum_data = yesterday_data.sum()
        data = today_sum_data["dealtotal"] - yesterday_sum_data["dealtotal"]

        color_list = ["red" if i < 0 else "#00bc12" for i in data]
        fig_list = [
            go.Bar(
                x=data,
                y=y_axis,
                text=[i if i < 0 else "+" + str(i) for i in data],
                orientation='h',
                marker=dict(color=color_list),
            ),
        ]
        layout = go.Layout(
            title='', height=480, width=380, )

        fig = go.Figure(data=fig_list, layout=layout)
        fig.update_layout(
            barmode='group',
            template='plotly_white',
            # showlegend=False,
            margin=dict(t=5, l=5, b=5, r=5)
        )
        fig.update_traces(textposition='outside')  # 条形显示数据
        return fig

    @dash_app.callback(
        Output("area_sale_distribute_fig", "figure"),
        Input("area_sale_distribute_option", "value")
    )
    def area_sale_distribute_callback(value):
        """
        区域销售分布，地理图
        """
        with urlopen('https://cdn.huanggefan.cn/geojson/china.json') as f:
            provinces_map = json.load(f)
        map_datas = pd.DataFrame(china_data)

        # map_datas = map_data.groupby('ad_name', as_index=False)['sales'].sum()
        fig = px.choropleth_mapbox(
            map_datas,
            geojson=provinces_map,
            color='sales',
            locations='ad_name',
            # 地理数据json文件中的省份名称的键名
            featureidkey="properties.name",
            mapbox_style="white-bg",
            # 不同程度的颜色参数
            # color_continuous_scale=[
            #     [0, 'lightcoral'],  # 这个必须要写，否则会出错
            #     [1. / 3000, 'indianred'],
            #     [1. / 300, 'brown'],
            #     [1. / 30, 'firebrick'],
            #     [1 / 3, 'maroon'],
            #     [1., 'darkred']],
            color_continuous_scale='Viridis',
            range_color=(0, 10000000),
            # 中心经纬度
            center={"lat": 37.110573, "lon": 106.493924},
            width=550,
            zoom=2,  # 地图缩小值（0-12）
            hover_name="ad_name",
            hover_data=["sales"],
            labels={
                'ad_name': '省份名称',
                'sales': '销售总额',
                'normal': {"show": True}
            }
        )
        fig.update_layout(coloraxis_showscale=False)  # 去掉颜色条

        layout = go.Layout(
            title='', height=620, width=550, )
        fig = go.Figure(data=fig, layout=layout)
        # fig.update_traces(text="fwfwfwgwgegwgw",visible=True)
        return fig
