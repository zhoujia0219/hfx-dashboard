import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from services import srv_sales_real_time

###############
# 回调
###############
from services.srv_comm_dim import get_ZE_PJS_ZWS
from services.srv_sales_real_time import get_all_areaname
from utils.date_util import get_day_hour


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

    def sale_day_fig(data_x, data_y, x_choice_time):
        """
        销售日数据
        :param data_x:
        :param data_y:
        :param data_sum: pic_dff.sum()
        :return:
        """
        day_hour_arang, all_time_list = get_day_hour(x_choice_time)
        pic = srv_sales_real_time.sales_day(all_time_list)  # todo
        if data_x == data_y:
            return dash.no_update
        pic_dff = pic.groupby([data_x], as_index=False)['sale'].sum()
        empty_pic = pd.DataFrame(day_hour_arang, columns=["times", "sale"])
        print(empty_pic,'empty_pic')
        pic_dff = pd.concat([empty_pic, pic_dff])
        fig = px.bar(
            pic_dff,
            x=data_x,
            y='sale',
            color='sale',
            barmode='group',
            template='plotly_white',
            labels={'sale': '总销售额', 'times': '时间点'},
        )
        fig.update_traces(textposition='inside')
        axis = [i for i in range(1, 24)]
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=axis,
                ticktext=axis
            ))
        return fig

    @dash_app.callback(
        Output('sales_real_time_day', 'figure'),
        Input('x_choice_time', 'value'),
    )
    def sale_day_day(x_choice_time):
        """
        销售日分布
        """
        fig_sales_day = sale_day_fig("times", "sale", x_choice_time),  # 画图
        return fig_sales_day[0]

    @dash_app.callback(
        Output('sales_real_time_month', 'figure'),
        [
            Input('total_avg_mid', 'value'),
            Input('range_choice', 'value'),

        ]
    )
    def sale_day_month(total_avg_mid, range_choice):
        """
        销售月分布
        """
        fig_sales_month = sale_month_fig("day", "dealtotal", get_ZE_PJS_ZWS()[total_avg_mid], range_choice)
        return fig_sales_month
