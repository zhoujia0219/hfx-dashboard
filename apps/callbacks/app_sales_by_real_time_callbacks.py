import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html

import dash
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from analog_data import today_area_sale_, yesterday_area_sale_
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
        color_list = ["darkgrey" if i in all_time_list[0] else 'blue' for i in color_time_list]
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
    def sale_day_day(x_choice_time, n):
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
        fig_list = []
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
                color_list = ["darkgrey" if i in all_time_list[0] else 'blue' for i in color_time_list]
                trace = go.Bar(
                    name="{}".format(area_name),
                    x=times_list,
                    y=y_dealtotal,
                    marker=dict(color=color_list)
                )
                layout = go.Layout(
                    xaxis=dict(title="{}".format(area_name)),
                )
                fig = go.Figure(data=[trace, ], layout=layout)
                fig.update_layout(
                    showlegend=False,
                    margin=dict(t=5, l=5, b=5, r=5)
                )
                fig_list.append(fig)
            else:
                break
            flag += 1
        if len(fig_list) < 9:  # 数据量不足
            for i in range(9 - len(fig_list)):
                fig_list.append("")
        return fig_list

    @dash_app.callback(
        [Output("day_area_fig" + str(i), 'figure') for i in range(9)],
        Input('area_level', 'value')
    )
    def day_area_sale(value):
        """各区域本日销售分布"""
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
    def update_total_sale(n):
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
