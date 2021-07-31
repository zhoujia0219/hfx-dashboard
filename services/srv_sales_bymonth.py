from datetime import datetime
from typing import List, Dict

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from flask_app import cache
from utils import date_util
from utils import db_util

default_dbname = "data_analysis"


###########################
# 取数据缓存
###########################

@cache.memoize()
def global_store(filter_values: dict) -> List[Dict]:
    """
    全局缓存
    @:param filter_values: 筛选值 json类型参数 { 'begin_month': begin_month, 'end_month': end_month,
                                'city_level':city_level, 'channel':channel,
                                'store_age':store_age, 'store_area':store_area, 'store_star':store_star}
    @:return:
    """
    d = cache.get(str(filter_values))
    if d:
        return d
    else:
        result = find_sales_list(filter_values)
        if result:
            cache.set(str(filter_values), result)
        return result


# 换算单位、百万
trans_num = 100000


def calculate_cards(filter_values: dict) -> Dict:
    """
    计算头部的4个card 的数据
    :param filter_values :
                    { 'begin_month': 开始时间: 字符串类型，格式 YYYY-MM,
                      'end_month': 结束时间: 字符串类型，格式 YYYY-MM,
                      'city_level': 城市级别: List类型,
                      'channel': 渠道: List类型,
                      'store_age': 店龄: List类型 ,
                      'store_area': 门店面积: List类型,
                      'store_star': 门店星级: List类型}
    :return dict :
            {"total_sale": 总销售量: 浮点类型，单位百万(M),
            "last_month_total": 上月销售量：浮点类型，单位百万(M),
            "tb_percentage": 同比百分比（上月的数据比去年的数据）：字符串类型，单位%,
            "hb_percentage": 环比百分比（上月的数据比上上月的数据）：字符串类型，单位%,
            "c_month_total_sale": 本月总销售量：浮点类型，单位百万(M),
            "m_growth_rate": 增长率（本月比上月）：字符串类型，单位%,
            "group_sales": 12个月的销售趋势：Dataframe类型，包含字段[month_group:月份, dealtotal:当月销量]}
    """
    card_datas = global_store(filter_values)
    df = pd.DataFrame(card_datas)

    # 总营业额
    total_sale = round((df["dealtotal"].sum() / trans_num), 2) if len(df) > 0 else 0.00
    # 当前月份(以时间筛选的截止日期为准)的上月数据
    ve_date = datetime.strptime(filter_values["end_month"], "%Y-%m")
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

    # 近12月销售趋势
    group_df = df
    month_groups = group_df.groupby(by=["month_group"], as_index=False)["dealtotal"].sum() if len(group_df) > 0 else []
    group_sales = pd.DataFrame(month_groups)
    # 封装结果数据
    return {"total_sale": total_sale, "last_month_total": last_month_total,
            "tb_percentage": tb_percentage, "hb_percentage": hb_percentage,
            "c_month_total_sale": c_month_total_sale, "m_growth_rate": m_growth_rate,
            "group_sales": group_sales}


# 展示图数据
def calculate_graph_data(filter_values: dict) -> DataFrame:
    """
    计算销售图的数据
    :param filter_values: 过滤值
    :return:
    """
    data = global_store(filter_values)
    if len(data) > 0:
        df = pd.DataFrame(data)
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
        return df
    return []


def calculate_top_graph(filter_values: dict, month_value: str, order_value: int) -> DataFrame:
    """
    计算排名图数据
    :param filter_values:  过滤值
    :param month_value: 月份
    :param order_value: 排序
    :return: 返回一组Dataframe类型的数据
    """
    # 取数据
    fig3_data = global_store(filter_values)
    if len(fig3_data) > 0:
        df = pd.DataFrame(fig3_data)

        group_df = df
        # 当月数据
        c_month = datetime.strptime(month_value, "%Y-%m")
        cs_date = date_util.get_month_first_day(c_month).date()
        ce_date = date_util.get_month_last_day(c_month).date()
        current_month_df = group_df[(group_df["rdate"] >= cs_date) &
                                    (group_df["rdate"] < ce_date)]

        # 上月数据
        ls_date = date_util.get_last_month_first_day(c_month).date()
        le_date = date_util.get_last_month_last_day(c_month).date()
        last_month_df = group_df[(group_df["rdate"] >= ls_date) &
                                 (group_df["rdate"] < le_date)]

        # 本月战区分组聚合
        c_group_data = current_month_df.groupby(by=["areaname3", "month_group"],
                                                as_index=False)["dealtotal"].sum()
        c_df = pd.DataFrame(c_group_data)

        # 上月战区分组聚合
        l_group_data = last_month_df.groupby(by=["areaname3", "month_group"],
                                             as_index=False)["dealtotal"].sum()
        l_df = pd.DataFrame(l_group_data)

        l_df["dealtotal"] = l_df["dealtotal"] * (-1)
        # 根据战区分组并排序
        if order_value == 1:
            c_df.sort_values(by="dealtotal", ascending=True, inplace=False)
            l_df.sort_values(by="dealtotal", ascending=True, inplace=False)
        elif order_value == 2:
            c_df.sort_values(by="dealtotal", ascending=False, inplace=False)
            l_df.sort_values(by="dealtotal", ascending=False, inplace=False)

        # 合并数据
        fig_df = c_df.append(l_df)

        return fig_df
    return []


def find_sales_list(filter_values: dict) -> List[Dict]:
    query_sql = """
                   SELECT 
                   areauid3, areaname3, areauid4, areaname4, storeuid, storename, weeks, rdate :: date, province, 
                   province_name, city, city_name, county, county_name, businessname, vctype, areasize, 
                   billcount, dealtotal::float, rebillcount, redealtotal, weather, weather_desc, temperature, 
                   wind_direction, "month", "year", city_level, to_char(rdate,'YYYY年MM月') as month_group
                   FROM chunbaiwei.fact_storesale_weather
                   WHERE areauid3 is not null  and areauid4 is not null and province is not null and city is not null 
                   and county is not null
           """
    if filter_values:
        if filter_values["begin_month"] and filter_values["end_month"]:
            query_sql += """  and to_char(rdate,'YYYY-MM') >= '{begin_month}'
                                     and to_char(rdate,'YYYY-MM') <= '{end_month}'
                   """.format(begin_month=filter_values["begin_month"], end_month=filter_values["end_month"])
        if filter_values["city_level"]:
            # 长度大于1 循环处理
            citys = tuple(str(c) for c in filter_values["city_level"]) if len(filter_values['city_level']) > 1 \
                else "(" + str(filter_values['city_level'][0]) + ")"
            query_sql += """ and city_level in {city_level}""".format(city_level=citys)
        if filter_values["channel"]:
            channels = tuple(c for c in filter_values["channel"]) if len(filter_values['channel']) > 1 \
                else "(" + filter_values['channel'][0] + ")"
            query_sql += """ and businessname in {channel}""".format(channel=channels)
        # if values["store_age"]:
        #     query_sql += """
        #     """
    # 从数据库查询
    data = db_util.query_list(query_sql, default_dbname)

    result = [{"areauid3": d[0], "areaname3": d[1], "areauid4": d[2], "areaname4": d[3], "storeuid": d[4],
               "storename": d[5], "weeks": d[6], "rdate": datetime.strptime(str(d[7]), '%Y-%m-%d').date(),
               "province": d[8], "province_name": d[9], "city": d[10], "city_name": d[11], "county": d[12],
               "county_name": d[13], "businessname": d[14], "vctype": d[15], "areasize": d[16],
               "billcount": d[17], "dealtotal": d[18], "rebillcount": d[19], "redealtotal": float(d[20]),
               "weather": d[21], "weather_desc": d[22], "temperature": d[23], "wind_direction": d[24],
               "month": d[25], "year": d[26], "city_level": int(d[27]) if d[27] else 0, "month_group": d[28]} for d in
              data]
    return result


def find_channel_list() -> List[Dict]:
    query_sql = """
        select distinct businessname from  chunbaiwei.fact_storesale_weather
    """

    data = db_util.query_list(query_sql, default_dbname)

    return [{"channel": d[0]} for d in data]
