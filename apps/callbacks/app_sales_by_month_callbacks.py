import math
import time
import json

import dash
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from flask import g
from pandas import DataFrame

from services import srv_sales_bymonth

###############
# 回调
###############
from services.srv_comm_dim import get_ZE_PJS_ZWS
from utils.thread_one_interface import MyThread
from utils.tools import user_login_data


def register_callbacks(dash_app):
    ###############
    # 页面内容构建刷新函数
    ###############

    # 顶部 12月趋势图
    def build_group_sales_fig(df: DataFrame):

        """
        12个月销售趋势图
        :param df: 包含月份和销售额的dataframe 数据
        :return 返回图形
        """

        time_start = time.time()
        fig = px.bar(df, x="month_group", y="dealtotal", width=200, height=60)
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            margin=dict(t=10, l=10, b=10, r=10)
        )

        time_end = time.time()
        print('build_group_sales_fig: Running time:{} seconds'.format(time_end - time_start))
        return fig

    # 战区排名
    def build_top_graph(order_value: int, month_value: str, filter_values: dict):
        """

        构建排名图
        :param order_value: 排序
        :param month_value:
        :param filter_values:
        :return:
        """

        time_start = time.time()
        fig_df = srv_sales_bymonth.calculate_top_graph(filter_values, month_value, order_value)
        if len(fig_df) > 0:
            fig = px.bar(fig_df, x="dealtotal", y="areaname3", color='month_group', orientation='h', height=300,
                         category_orders={'areaname3': [c for c in fig_df['areaname3']]},
                         hover_name='month_group',
                         labels={'month_group': '销售额环比', 'dealtotal': '销售额', 'areaname3': '战区'},
                         text=[str(round(math.fabs(c) / srv_sales_bymonth.trans_num, 2)) + "M" for c in
                               fig_df["dealtotal"]],
                         template="plotly_white")

            # todo 添加显示标签

            time_end = time.time()
            print('build_top_graph: Running time:{} seconds'.format(time_end - time_start))
            return fig
        else:
            return {}

    # 销售分析
    def build_sales_graph(filter_values, val_graph, val_cate, val_agg):
        """

        :param filter_values:
        :param val_graph:
        :param val_cate:
        :param val_agg:
        :return:
        """
        time_start = time.time()
        df = srv_sales_bymonth.calculate_graph_data(filter_values)
        if len(df) < 1:
            return dash.no_update
        if val_graph == 'px.bar':
            dff = df.groupby(['month', val_cate], as_index=False)['dealtotal']
            dff = eval(val_agg)
            dff_line = dff.groupby('month', as_index=False)['dealtotal'].mean()

            fig = go.Figure([
                                go.Bar(name=lab,
                                       x=dff[dff[val_cate] == lab]['month'],
                                       y=dff[dff[val_cate] == lab]['dealtotal'], )
                                for lab in dff[val_cate].unique()] +
                            [go.Scatter(name='平均值', x=dff_line['month'], y=dff_line['dealtotal'], mode="lines")])
            fig.update_layout(barmode='group', template='plotly_white')

            time_end = time.time()
            print('build_sales_graph: Running time:{} seconds'.format(time_end - time_start))
            return fig
        else:
            dff = df.groupby(['month', val_cate], as_index=False)['dealtotal']
            dff = eval(val_agg)
            fig = eval(val_graph)(
                dff,
                x='month',
                y='dealtotal',
                color=val_cate,
                labels={'month': '月份', 'dealtotal': '总销售额'},
                title='销售额分析',
                template='plotly_white'
            )

            time_end = time.time()
            print('build_sales_graph: Running time:{} seconds'.format(time_end - time_start))
            return fig

    # 所属城市级别
    def build_city_graph(filter_values, val_x, val_cate, val_agg):
        """

        :param filter_values:
        :param val_x:
        :param val_cate:
        :param val_agg:
        :return:
        """
        time_start = time.time()
        df = srv_sales_bymonth.calculate_graph_data(filter_values)
        if len(df) < 1:
            return dash.no_update
        if val_x == val_cate:
            return dash.no_update
        else:
            dff = df.groupby([val_x, val_cate], as_index=False)['dealtotal']
            dff = eval(val_agg)
            fig = px.bar(
                dff,
                x=val_x,
                y='dealtotal',
                color=val_cate,
                labels={'dealtotal': '总销售额'},
                title='销售额分析',
                barmode='group',
                text='dealtotal',
                template='plotly_white'
            )
            fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
            time_end = time.time()
            print('build_city_graph: Running time:{} seconds'.format(time_end - time_start))
            return fig

    # 不同维度间销售额分析
    def build_allsale_graph(filter_values, data_x, data_y, data_sum):
        """
        :param filter_values:
        :param data_x:
        :param data_y:
        :param data_sum: pic_dff.sum()
        :return:
        """

        pic = srv_sales_bymonth.calculate_graph_allsale(filter_values)
        if len(pic) < 1:
            return dash.no_update
        if data_x == data_y:
            return dash.no_update
        else:
            pic_dff = pic.groupby([data_x], as_index=False)['dealtotal']
            pic_dff = eval(data_sum)
            if data_x == "city_level":
                fig = px.bar(
                    pic_dff,
                    x=data_x,
                    y='dealtotal',
                    color='dealtotal',
                    barmode='group',
                    template='plotly_white',
                    labels={'dealtotal': '总销售额', 'city_level': '城市等级'},
                )
                fig.update_layout(
                    xaxis=dict(
                        tickmode='array',
                        tickvals=[2, 3],
                        ticktext=['城市等级2', '城市等级3']

                    )
                )
            elif data_x == "areasize":
                pic_dff = pic.groupby(['areasize_bins'], as_index=False)['dealtotal'].sum()
                fig = px.pie(
                    pic_dff,
                    names='areasize_bins',
                    values='dealtotal',
                    color_discrete_sequence=px.colors.sequential.Bluyl,
                    labels={'dealtotal': '总销售额', 'areasize_bins': '门店面积类型'},
                )
            elif data_x == 'star':
                fig = px.bar(
                    pic_dff,
                    x=data_x,
                    y='dealtotal',
                    color='dealtotal',
                    barmode='group',
                    template='plotly_white',
                    labels={'dealtotal': '总销售额', 'star': '门店星级'},
                )
                fig.update_layout(
                    xaxis=dict(
                        tickmode='array',
                        tickvals=[1, 2, 3, 4, 5],
                        ticktext=['门店星级1', '门店星级2', '门店星级3', '门店星级4', '门店星级5', ]
                    )
                )

            else:
                fig = px.bar(
                    pic_dff,
                    x=data_x,
                    y='dealtotal',
                    color='dealtotal',
                    barmode='group',
                    template='plotly_white',
                    labels={'dealtotal': '总销售额', 'areaname4': '战区', 'businessname': '销售渠道', 'vctype': '门店类型'},
                )
                fig.update_traces(textposition='inside')
            return fig

    # 销售单价与销售数量分析气泡图
    def build_trademoney_scatter(filter_values, d_x, d_y, d_d):
        """
        :param filter_values:
        :param d_x:
        :param d_y:
        :param d_d:
        :return:
        """
        trade_data = srv_sales_bymonth.calculate_graph_scatter(filter_values)
        if len(trade_data) < 1:
            return dash.no_update
        if d_x == d_y:
            return dash.no_update
        trade_data_group = trade_data.groupby([d_d, d_x], as_index=False)[['dealtotal', d_y]].sum()
        fig = px.scatter(
            trade_data_group,
            x=d_x,
            y=d_y,
            color='county_name',
            size='dealtotal',  # 点的大小
            log_x=True,  # 对数变换
            size_max=60,  # 点的最大值
            # hover_name=,       #悬停信息
            # animation_frame='',   #将**作为播放按钮
            labels={'price': '客单价', 'billcount': '客单量', 'county_name': '城区', 'dealtotal': '总销售额', 'areasize': '面积'}
        )
        return fig

    # 地理图
    def build_map_graph(filter_values, map_name, map_value):
        """
        :param filter_values:
        :param map_one:
        :param map_two:
        :param map_other:
        :return:
        """
        map_data = srv_sales_bymonth.find_mapdata_list(filter_values)
        with urlopen('https://cdn.huanggefan.cn/geojson/china.json') as f:
            provinces_map = json.load(f)
        map_datas = map_data.groupby('ad_name', as_index=False)['sales'].sum()
        # print(map_datas)
        fig = px.choropleth_mapbox(
            map_datas,
            geojson=provinces_map,
            color=map_value,
            locations=map_name,
            # 地理数据json文件中的省份名称的键名
            featureidkey="properties.name",
            mapbox_style="white-bg",
            # 不同程度的颜色参数
            color_continuous_scale=[
                [0, '#FFFAF0'],
                [1. / 30000, '#FFE4B5'],
                [1. / 300, '#F4A460'],
                [1. / 30, '#F08080'],
                [1 / 3, '#FA8072'],
                [1., '#FF4500']],
            # 中心经纬度
            center={"lat": 37.110573, "lon": 106.493924},
            zoom=3,
            hover_name="ad_name",
            hover_data=["sales"],
            labels={
                'ad_name': '省份名称',
                'sales': '销售总额'
            }
        )
        return fig

    @dash_app.callback(
        Output('signal', 'data'),
        [
            Input("f_submit", "n_clicks"),
            # 日期筛选
            State('f_begin_month', 'value'),
            State('f_end_month', 'value'),
            # 城市筛选
            State('f_cities', 'value'),
            # 渠道筛选
            State('f_channels', 'value'),
            # 店龄筛选
            State('f_store_age', 'value'),
            # 门店面积筛选
            State('f_store_area', 'value'),
            # 门店星级筛选
            State('f_store_star', 'value'),
        ]
    )
    # @user_login_data
    def compute_value(n_clicks, begin_month, end_month, city_level, channel, store_age, store_area, store_star):
        """
        点击提交按钮后，保存筛选值到signal
        :param n_clicks 提交按钮点击次数
        :param begin_month 结束日期
        :param end_month 开始日期
        :param city_level  城市级别
        :param channel 渠道
        :param store_age 店龄
        :param store_area 店面积
        :param store_star 门店星级
        :return 返回筛选的所有选中值（用于取缓存）

        """
        # user = g.user
        # print(user, 44555666777889)
        filter_values = {'begin_month': begin_month, 'end_month': end_month,
                         'city_level': city_level, 'channel': channel,
                         'store_age': store_age, 'store_area': store_area, 'store_star': store_star}
        # compute value and send a signal when done
        srv_sales_bymonth.global_store(filter_values)
        return filter_values

    @dash_app.callback(
        [
            Output('total_sales', 'children'),
            Output('total_sales_start_month', 'children'),
            Output('total_sales_stop_month', 'children'),
            Output('last_month_sales', 'children'),
            Output('last_month_tb', 'children'),
            Output('last_month_hb', 'children'),
            Output('current_month_sign', 'children'),
            Output('current_month_sales', 'children'),
            Output('growth_rate', 'children'),
            Output('group_start_month', 'children'),
            Output('group_end_month', 'children'),
            Output('graph_month_group', 'figure'),
        ],
        [Input('signal', 'data')])
    def update_card_group_month_graph(filter_values):
        """
        更新 12个月趋势图卡片
        :param filter_values:
        :return:
        """
        # 获取基础数据
        df = srv_sales_bymonth.global_store(filter_values)
        begin_month = filter_values["begin_month"]
        end_month = filter_values["end_month"]
        # 计算卡片数据
        card_df = srv_sales_bymonth.calculate_card_data(df, end_month)
        graph_df = srv_sales_bymonth.calculate_card_graph(df)
        return [[card_df["total_sale"]], [begin_month], [end_month],
                [card_df["last_month_total"]], [card_df["tb_percentage"]], [card_df["hb_percentage"]],
                [end_month], [card_df["c_month_total_sale"]], [card_df["m_growth_rate"]],
                [begin_month], [end_month], build_group_sales_fig(graph_df)]

    @dash_app.callback(
        Output('graph_top', 'figure'),
        [
            Input('choices_top_order', 'value'),
            Input('choices_top_month', 'value'),
            Input('signal', 'data'),
        ])
    def update_top_graph(order_value, month_value, filter_values):
        """
        更新排名图
        :param order_value: 1: 正序， 2： 倒序
        :param month_value: 月份值
        :param filter_values:  筛选值->全局缓存key
        """

        return build_top_graph(order_value, month_value, filter_values)

    @dash_app.callback(
        Output('choices_top_month', 'value'),
        Input('f_end_month', 'value'),
    )
    def update_choices_top_month_value(month_value):
        """
        更新排名月份选项值 -- 用于页面初始化时，默认展示排名月份的展示
        :param month_value : 过滤结束月份时间
        :return  返回 筛选结束月份的值
        """
        return month_value

    # graph_out_qs
    @dash_app.callback(
        Output('graph_out_qs', 'figure'),
        [
            Input('btn_sales_update', 'n_clicks'),
            Input('cate_choice', 'value'),
            Input('agg_choice', 'value'),
            Input('graph_choice', 'value'),
            Input('signal', 'data'),
        ],
    )
    def update_sales_graph(n_clicks, val_cate, val_agg, val_graph, filter_values):
        """

        :param n_clicks
        :param val_cate:
        :param val_agg:
        :param val_graph:
        :param filter_values:
        :return:
        """
        return build_sales_graph(filter_values, val_graph, val_cate, val_agg)

    # graph_out_wd
    @dash_app.callback(
        Output('graph_out_wd', 'figure'),
        [
            Input('btn_city_update', 'n_clicks'),
            Input('x_choice_2', 'value'),
            Input('cate_choice_2', 'value'),
            Input('agg_choice_2', 'value'),
            Input('signal', 'data'),
        ],
    )
    def update_city_graph(n_clicks, val_x, val_cate, val_agg, filter_values):
        """

        :param n_clicks
        :param val_x:
        :param val_cate:
        :param val_agg:
        :param filter_values:
        :return:
        """
        return build_city_graph(filter_values, val_x, val_cate, val_agg)

    # graph_out_dy
    @dash_app.callback(
        Output('graph_out_dy', 'figure'),
        [
            Input('btn_sales_update', 'n_clicks'),
            Input('x_choice_1', 'value'),
            Input('cate_choice_1', 'value'),
            Input('agg_choice_1', 'value'),
            Input('signal', 'data'),
        ],
    )
    def update_my_graph(n_clicks, val_x, val_cate, val_agg, filter_values):
        """

        :param n_clicks
        :param val_x:
        :param val_cate:
        :param val_agg:
        :param filter_values:
        :return:
        """

        return build_city_graph(filter_values, val_x, val_cate, val_agg)

    @dash_app.callback(
        [
            Output('graph_out_one', 'figure'),
            Output('graph_out_two', 'figure'),
            Output('graph_out_three', 'figure'),
            Output('graph_out_four', 'figure'),
        ],
        Input('x_choice_3', 'value'),
    )
    def updata_out_four(updata_out_list):
        # fig_list = []
        # for j in updata_out_list:
        #     fig_list.append(build_allsale_graph(updata_out_list, j, 'dealtotal', 'pic_dff.sum()'))
        #     if len(fig_list) == 4:
        #         break
        # if len(fig_list) < 4:
        #     for a in range(4 - len(fig_list)):
        #         fig_list.append("")
        # return fig_list[0], fig_list[1], fig_list[2], fig_list[3]

        a1 = time.time()
        fig_list1 = []
        thread_list = []  # 多线程对象保存列表
        if len(updata_out_list) > 4:
            updata_out_list = updata_out_list[:4]  # 多选不会多返回fig
        for i in updata_out_list:
            t = MyThread(build_allsale_graph, args=(updata_out_list, i, 'dealtotal', 'pic_dff.sum()'))
            thread_list.append(t)
            t.start()
        for j in thread_list:
            j.join()  # 开启等待全部线程运行完，否则某些线程未跑完返回None
            fig_list1.append(j.get_result())
        if len(fig_list1) < 4:
            for i in range(4 - len(fig_list1)):
                fig_list1.append("")
        b1 = time.time()
        print("测试代码：", b1 - a1)
        return fig_list1[0], fig_list1[1], fig_list1[2], fig_list1[3]

    @dash_app.callback(
        Output('graph_billcount', 'figure'),
        [
            Input('option_x', 'value'),
            Input('option_y', 'value'),
            Input('option_other', 'value'),
        ]
    )
    def updata_graph_scatter(d_x, d_y, d_d):
        """
         :param filter_values
         :param d_x:
         :param d_y:
         :param d_d:
         :return:
         """
        scatter_list = build_trademoney_scatter("", d_x, d_y, d_d)
        return scatter_list

    @dash_app.callback(
        Output('map_graph', 'figure'),
        [
            Input('map_limits', 'value'),
            Input('map_index', 'value'),
        ]
    )
    def updata_graph_map(map_name, map_value):
        """
        销售分布的本日、本月的回调函数
        :param total_avg_mid: 单选框
        :return:sales_day:本日销售分布图
                sales_month:本月销售分布图
        """
        return build_map_graph("", map_name, map_value)
