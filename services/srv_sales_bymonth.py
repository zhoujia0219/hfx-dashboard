import time
from datetime import datetime
from typing import Dict

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from flask_app import cache
from utils import date_util
from utils import db_util
from utils.date_util import get_current_month_all_day

default_dbname = "data_analysis"


###########################
# 取数据缓存
###########################

@cache.memoize()
def global_store(filter_values: dict) -> DataFrame:
    """
    全局缓存
    @:param filter_values: 筛选值 json类型参数 { 'begin_month': begin_month, 'end_month': end_month,
                                'city_level':city_level, 'channel':channel,
                                'store_age':store_age, 'store_area':store_area, 'store_star':store_star}
    @:return:
    """
    time_start = time.time()
    df = find_sales_list(filter_values)

    time_end = time.time()
    print('global_store: Running time:{} seconds'.format(time_end - time_start))
    return df


@cache.memoize()
def global_cache(filter_values: dict) -> DataFrame:
    """
        全局缓存
        @:param filter_values: 筛选值 json类型参数 { 'businessname': businessname, 'dealtotal': dealtotal,
                                    'city_level':city_level, 'vctype':vctype,
                                    'star':star, 'areaname4':areaname4}
        @:return:
        """
    time_start = time.time()
    allsale = find_allsale_list(filter_values)

    time_end = time.time()
    print('global_cache: Running time:{} seconds'.format(time_end - time_start))
    return allsale


@cache.memoize()
def global_buffer(filter_values: dict) -> DataFrame:
    """
        全局缓存
        @:param filter_values: 筛选值 json类型参数 { 'price': price, 'amount': amount,
                                       'trademoney':trademoney,'rdate':rdate, 'classname':classname,'province_name':province_name}
        @:return:
        """
    time_start = time.time()
    scatter_data = find_trademoney_list(filter_values)

    time_end = time.time()
    print('global_buffer: Running time:{} seconds'.format(time_end - time_start))
    print(scatter_data, 789797979797979)
    return scatter_data


###########################
# 展示计算数据
###########################

# 换算单位、百万
trans_num = 100000


@cache.memoize()
def calculate_card_data(df: DataFrame, end_month: str) -> Dict:
    """
    计算头部的4个card 的数据
    :param df: 处理数据
    :param end_month: 筛选结束月份
    :return dict :
            {"total_sale": 总销售量: 浮点类型，单位百万(M),
            "last_month_total": 上月销售量：浮点类型，单位百万(M),
            "tb_percentage": 同比百分比（上月的数据比去年的数据）：字符串类型，单位%,
            "hb_percentage": 环比百分比（上月的数据比上上月的数据）：字符串类型，单位%,
            "c_month_total_sale": 本月总销售量：浮点类型，单位百万(M),
            "m_growth_rate": 增长率（本月比上月）：字符串类型，单位%}
    """
    time_start = time.time()

    # 总营业额
    total_sale = round((df["dealtotal"].sum() / trans_num), 2) if len(df) > 0 else 0.00
    # 当前月份(以时间筛选的截止日期为准)的上月数据
    ve_date = datetime.strptime(end_month, "%Y-%m")
    s_date = date_util.get_last_month_first_day(ve_date).date()
    e_date = date_util.get_last_month_last_day(ve_date).date()
    last_month_df = df[(df["rdate"] >= s_date) & (df["rdate"] < e_date)] if len(df) > 0 else []
    last_month_total = round((last_month_df["dealtotal"].sum()) / trans_num, 2) if len(last_month_df) > 0 else 0.00

    # 同比 取去年当月数据
    tb_sdate = (s_date - relativedelta(years=1))
    tb_edate = (e_date - relativedelta(years=1))
    # 去年的数据
    tb_df = df[(df["rdate"] >= tb_sdate) & (df["rdate"] < tb_edate)] if len(df) > 0 else []
    # 去年的总营业额
    tb_total_sale = round((tb_df["dealtotal"].sum() / trans_num), 2) if len(tb_df) > 0 else 0.00

    # 同比增长率计算 =（本期数－同期数）/同期数×100%
    tb_percentage = "%.2f%%" % round(
        ((last_month_total - tb_total_sale) / tb_total_sale * 100) if tb_total_sale > 0 else 0, 2)

    # 环比 取上月数据
    hb_sdate = date_util.get_last_month_first_day(s_date).date()
    hb_edate = date_util.get_last_month_last_day(e_date).date()

    # 上月数据
    hb_df = df[(df["rdate"] >= hb_sdate) & (df["rdate"] < hb_edate)] if len(df) > 0 else []
    # 上月总营业额
    hb_total_sale = round((hb_df["dealtotal"].sum() / trans_num), 2) if len(hb_df) > 0 else 0.00

    # 环比增长率计算= （本期数-上期数）/上期数×100%。
    hb_percentage = "%.2f%%" % round(
        ((last_month_total - hb_total_sale) / hb_total_sale * 100) if hb_total_sale > 0 else 0, 2)
    # 本月销售额
    c_sdate = date_util.get_month_first_day(ve_date).date()
    c_edate = date_util.get_month_last_day(ve_date).date()
    c_month_df = df[(df["rdate"] >= c_sdate) & (df["rdate"] < c_edate)] if len(df) > 0 else []
    c_month_total_sale = round((c_month_df["dealtotal"].sum() / trans_num), 2) if len(c_month_df) > 0 else 0.00

    # 本月营业额与上月对比营业额 增长率 - 月增长率 =（本月营业额-上月营业额）/上月营业额*100%
    m_growth_rate = "%.2f%%" % round(
        ((c_month_total_sale - last_month_total) / last_month_total * 100) if last_month_total > 0 else 0, 2)

    time_end = time.time()
    print('calculate_card_data: Running time:{} seconds'.format(time_end - time_start))
    # 封装结果数据
    return {"total_sale": total_sale, "last_month_total": last_month_total,
            "tb_percentage": tb_percentage, "hb_percentage": hb_percentage,
            "c_month_total_sale": c_month_total_sale, "m_growth_rate": m_growth_rate}


@cache.memoize()
def calculate_card_graph(df: DataFrame) -> DataFrame:
    """
    计算卡片图-近12月趋势图数据
    :param df:
    :return: dataframe
    """

    time_start = time.time()
    group_df = df
    month_groups = group_df.groupby(by=["month_group"], as_index=False)["dealtotal"].sum() if len(group_df) > 0 else []
    group_sales = pd.DataFrame(month_groups)

    time_end = time.time()
    print('calculate_card_graph: Running time:{} seconds'.format(time_end - time_start))
    return group_sales


# 展示图数据
@cache.memoize()
def calculate_graph_data(filter_values: dict) -> DataFrame:
    """
    计算销售图的数据
    :param filter_values: 过滤值
            { 'begin_month': 开始时间: 字符串类型，格式 YYYY-MM,
              'end_month': 结束时间: 字符串类型，格式 YYYY-MM,
              'city_level': 城市级别: List类型,
              'channel': 渠道: List类型,
              'store_age': 店龄: List类型 ,
              'store_area': 门店面积: List类型,
              'store_star': 门店星级: List类型}
    :return:
    """
    # df = global_store(filter_values)
    time_start = time.time()
    df = find_sales_list(filter_values)
    if len(df) > 0:
        # 转换0值
        df.replace(0, np.nan, inplace=True)
        df['areasize'] = df['areasize'].astype('float')
        # 新增areasize_bins
        df['areasize_bins'] = pd.cut(df['areasize'], bins=[0, 40, 72, 90, 130], labels=['小店', '中店', '大店', '超大店'])
        # 缩小渠道范围
        df = df[df['businessname'].isin(['到店销售', '开放平台-扫码点餐'])]
        # 缩小战区范围
        df = df[df['areaname3'].isin(['一战区', '二战区', '三战区', '四战区'])]
        # 变更‘rdate’类型
        df['rdate'] = pd.to_datetime(df['rdate'])
        # 去2021年的值
        df = df[df['rdate'] >= '2021-01-01']
        df = df[df['businessname'].isin(['到店销售', '开放平台-扫码点餐'])]
        df['month_str'] = df['month'].map({1: '1月', 2: '2月', 3: '3月', 4: '4月', 5: '5月'})
        df['month'] = df['month'].astype('str')
        time_end = time.time()
        print('calculate_graph_data: Running time:{} seconds'.format(time_end - time_start))
        return df

    return []


@cache.memoize()
def calculate_top_graph(filter_values: dict, month_value: str, order_value: int) -> DataFrame:
    """
    计算排名图数据
    :param filter_values:  过滤值
    :param month_value: 月份
    :param order_value: 排序
    :return: 返回一组Dataframe类型的数据
    """
    time_start = time.time()
    # 取数据
    # df = find_sales_list(filter_values)
    c_month = datetime.strptime(month_value, "%Y-%m")
    ce_date = date_util.get_month_last_day(c_month).date()

    ls_date = date_util.get_last_month_first_day(c_month).date()
    filter_values["start_date"] = ls_date
    filter_values["end_date"] = ce_date
    filter_values["order_type"] = """order by month_group asc,dealtotal asc""" if order_value == 1 \
        else """order by month_group asc, dealtotal desc"""
    df = find_top_list(filter_values)
    c_month_group = month_value.replace("-", "年") + "月"
    df.loc[df["month_group"] != c_month_group, "dealtotal"] = df[df["month_group"] != c_month_group]["dealtotal"] * (-1)
    # if len(df) > 0:
    #     group_df = df
    #     # 当月数据
    #     c_month = datetime.strptime(month_value, "%Y-%m")
    #     cs_date = date_util.get_month_first_day(c_month).date()
    #     ce_date = date_util.get_month_last_day(c_month).date()
    #     current_month_df = group_df[(group_df["rdate"] >= cs_date) &
    #                                 (group_df["rdate"] < ce_date)]
    #
    #     # 上月数据
    #     ls_date = date_util.get_last_month_first_day(c_month).date()
    #     le_date = date_util.get_last_month_last_day(c_month).date()
    #     last_month_df = group_df[(group_df["rdate"] >= ls_date) &
    #                              (group_df["rdate"] < le_date)]
    #
    #     # 本月战区分组聚合
    #     c_group_data = current_month_df.groupby(by=["areaname3", "month_group"],
    #                                             as_index=False)["dealtotal"].sum()
    #     c_df = pd.DataFrame(c_group_data)
    #
    #     # 上月战区分组聚合
    #     l_group_data = last_month_df.groupby(by=["areaname3", "month_group"],
    #                                          as_index=False)["dealtotal"].sum()
    #     l_df = pd.DataFrame(l_group_data)
    #
    #     l_df["dealtotal"] = l_df["dealtotal"] * (-1)
    #     # 根据战区分组并排序
    #     if order_value == 1:
    #         c_df.sort_values(by="dealtotal", ascending=True, inplace=False)
    #         l_df.sort_values(by="dealtotal", ascending=True, inplace=False)
    #     elif order_value == 2:
    #         c_df.sort_values(by="dealtotal", ascending=False, inplace=False)
    #         l_df.sort_values(by="dealtotal", ascending=False, inplace=False)
    #
    #     # 合并数据
    #     fig_df = c_df.append(l_df)
    #
    #     time_end = time.time()
    #     print('calculate_top_graph: Running time:{} seconds'.format(time_end - time_start))
    #     return fig_df
    time_end = time.time()
    print('calculate_top_graph: Running time:{} seconds'.format(time_end - time_start))
    return df


@cache.memoize()
def calculate_graph_allsale(filter_values: dict) -> DataFrame:
    """

    :param filter_values:
    :return:
    """
    time_start = time.time()
    allsale = find_allsale_list(filter_values)
    if len(allsale) > 0:
        allsale.replace(0, np.nan, inplace=True)
        allsale['areasize'] = allsale['areasize'].astype('float')
        allsale['areasize_bins'] = pd.cut(allsale['areasize'],
                                          bins=[1, 20, 30, 50, 70, 100],
                                          labels=['档口店', '外卖店', '小店', '标准店', '大店'])
        time_end = time.time()
        print('calculate_graph_allsale: Running time:{} seconds'.format(time_end - time_start))
        return allsale
    return []


@cache.memoize()
def calculate_graph_scatter(filter_values: dict) -> DataFrame:
    """

    :param filter_values:
    :return:
    """
    scatter_data = find_trademoney_list(filter_values)
    if len(scatter_data) > 0:
        # 转换0值
        scatter_data.replace(0, np.nan, inplace=True)
        scatter_data['rdate'] = pd.to_datetime(scatter_data['rdate'])
        scatter_data = scatter_data[scatter_data['rdate'] == '2020/12/31']
        scatter_data['price'] = scatter_data['dealtotal'] / scatter_data['billcount']
        scatter_data = scatter_data[scatter_data['city_name'] == '莆田市']
        scatter_data = scatter_data[scatter_data['dealtotal'] > 0]
        scatter_data = scatter_data[scatter_data['businessname'] == '到店销售']
        return scatter_data
    return []


###########################
# 数据库取数
###########################

def find_sales_list(filter_values: dict) -> DataFrame:
    time_start = time.time()
    query_sql = """
                   SELECT  {}
                   FROM chunbaiwei.fact_storesale_weather
                   WHERE areauid3 is not null  and areauid4 is not null and province is not null and city is not null 
                   and county is not null
           """
    query_sql = add_sub_sql(filter_values, query_sql)
    query_cols = """ areaname3,  areaname4,  storename, weeks, rdate :: date,  
                   province_name,  city_name,  county_name, businessname, vctype, areasize, 
                   billcount, dealtotal::float, rebillcount, redealtotal, weather,   
                    "month", "year", city_level, to_char(rdate,'YYYY年MM月') as month_group"""
    query_sql = query_sql.format(query_cols)
    df = db_util.read_by_pd(query_sql, default_dbname)

    time_end = time.time()
    print('find_sales_list: Running time:{} seconds'.format(time_end - time_start))
    return df


def find_channel_list() -> DataFrame:
    time_start = time.time()
    query_sql = """
        select distinct businessname as {} from  chunbaiwei.fact_storesale_weather
    """.format("channel")

    channels = db_util.read_by_pd(query_sql, default_dbname)
    time_end = time.time()
    print('find_channel_list: Running time:{} seconds'.format(time_end - time_start))
    print(channels, 353535352262)
    return channels


def find_top_list(filter_values: dict) -> DataFrame:
    time_start = time.time()
    query_sql = """
        SELECT 
            {}
        FROM chunbaiwei.fact_storesale_weather
        where  areaname3 is not null 
    """
    query_sql = add_sub_sql(filter_values, query_sql)
    query_sql += """
        group by month_group , areaname3  
    """ + filter_values["order_type"]
    query_cols = """
         to_char(rdate,'YYYY年MM月') as month_group , areaname3, sum(dealtotal) as dealtotal
    """
    query_sql = query_sql.format(query_cols)
    top_list = db_util.read_by_pd(query_sql, default_dbname)
    time_end = time.time()
    print('find_channel_list: Running time:{} seconds'.format(time_end - time_start))
    return top_list


def add_sub_sql(filter_values: dict, query_sql: str) -> str:
    if filter_values:
        if "start_date" in filter_values.keys() and "end_date" in filter_values.keys() and \
                filter_values["start_date"] and filter_values["end_date"]:
            query_sql += """  and rdate >= '{start_date}'
                                     and rdate <= '{end_date}'
                   """.format(start_date=filter_values["start_date"], end_date=filter_values["end_date"])
        if "begin_month" in filter_values.keys() and "end_month" in filter_values.keys() and \
                filter_values["begin_month"] and filter_values["end_month"]:
            query_sql += """  and to_char(rdate,'YYYY-MM') >= '{begin_month}'
                                     and to_char(rdate,'YYYY-MM') <= '{end_month}'
                   """.format(begin_month=filter_values["begin_month"], end_month=filter_values["end_month"])
        if "city_level" in filter_values.keys() and filter_values["city_level"]:
            # 长度大于1 循环处理
            citys = tuple(str(c) for c in filter_values["city_level"]) if len(filter_values['city_level']) > 1 \
                else "(" + str(filter_values['city_level'][0]) + ")"
            query_sql += """ and city_level in {city_level}""".format(city_level=citys)
        if "channel" in filter_values.keys() and filter_values["channel"]:
            channels = tuple(c for c in filter_values["channel"]) if len(filter_values['channel']) > 1 \
                else "(" + filter_values['channel'][0] + ")"
            query_sql += """ and businessname in {channel}""".format(channel=channels)

        # if values["store_age"]:
        #     query_sql += """
        #     """
    return query_sql


def find_allsale_list(filter_values: dict) -> DataFrame:
    time_start = time.time()
    query_sql = """
        select businessname,star,areaname4,dealtotal,vctype,areasize,city_level
        from chunbaiwei.fact_storesale_weather
        """
    allsale = db_util.read_by_pd(query_sql, default_dbname)
    time_end = time.time()
    print('find_allsale_list: Running time:{} seconds'.format(time_end - time_start))
    return allsale


def find_trademoney_list(filter_values: dict) -> DataFrame:
    time_start = time.time()
    query_sql = """
        select billcount,dealtotal,rdate,city_name,county_name,businessname,areasize
        from chunbaiwei.fact_storesale_weather
        """
    trademoney = db_util.read_by_pd(query_sql, default_dbname)
    time_end = time.time()
    print('find_trademoney_list: Running time:{} seconds'.format(time_end - time_start))
    return trademoney


def find_mapdata_list(filter_values: dict) -> DataFrame:
    time_start = time.time()
    query_sql = """
        SELECT * FROM
        (SELECT ad_name FROM chunbaiwei.dim_area WHERE city ='00'AND county ='00') c
        LEFT JOIN 
        (SELECT province_name,"sum"(dealtotal) as sales FROM chunbaiwei.fact_storesale_weather GROUP BY province_name) b
        ON c.ad_name = b.province_name
            """
    mapdata = db_util.read_by_pd(query_sql, default_dbname)
    time_end = time.time()
    print('find_mapdata_list: Running time:{} seconds'.format(time_end - time_start))
    return mapdata


def sales_day() -> DataFrame:
    """
    销售日数据
    """
    query_sql = """
         select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='2021-03-21' OR rdate='2021-03-22'               
             """
    mapdata = db_util.read_by_pd(query_sql, default_dbname)
    return mapdata


def sales_month(range_choice:str) -> DataFrame:
    """
    销售月数据
    """
    current_montn_all_days = get_current_month_all_day(range_choice)
    query_sql = """
            select dealtotal,areaname3,to_char(rdate,'MM月dd日') as day  from chunbaiwei.fact_storesale_weather where rdate in {}
             """.format(current_montn_all_days)
    mapdata = db_util.read_by_pd(query_sql, default_dbname)
    return mapdata


def get_all_areaname():
    """
    获取所有战区名
    """
    sql = """
    select areaname3  from chunbaiwei.fact_storesale_weather GROUP BY areaname3
    """
    data = db_util.query_list(sql, default_dbname)
    return data
