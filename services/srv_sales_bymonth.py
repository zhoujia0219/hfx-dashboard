from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from flask_app import cache
from utils import db_util
from utils import date_util

default_dbname = "data_analysis"


###########################
# 取数据缓存
###########################

@cache.memoize()
def global_store(values):
    """
    全局缓存
    :param values: json类型参数 { 'begin_month': begin_month, 'end_month': end_month,
                                'city':city, 'channel':channel,
                                'store_age':store_age, 'store_area':store_area, 'store_star':store_star}
    :return:
    """
    d = cache.get(str(values))
    if d:
        return d
    else:
        result = find_sales_list(values)
        cache.set(str(values), result)
        return result


# 换算单位、百万
trans_num = 100000


# 计算cards 的 展示数据
def calculate_cards(values):
    """
    计算头部的4个card 的数据
    """
    card_datas = global_store(values)
    df = pd.DataFrame(card_datas)
    # 总营业额
    total_sale = round((df["dealtotal"].sum() / trans_num), 2) if len(df) > 0 else 0.00
    # 当前月份(以时间筛选的截止日期为准)的上月数据
    ve_date = datetime.strptime(values["end_month"], "%Y-%m")
    s_date = date_util.get_last_month_first_day(ve_date).date()
    e_date = date_util.get_last_month_last_day(ve_date).date()
    last_month_df = df[(df["rdate"] >= s_date) & (df["rdate"] < e_date)]
    last_month_total = round((last_month_df["dealtotal"].sum()) / trans_num, 2) if len(last_month_df) > 0 else 0.00

    # 同比 取去年当月数据
    tb_sdate = (s_date - relativedelta(years=1))
    tb_edate = (e_date - relativedelta(years=1))
    # 去年的数据
    tb_df = df[(df["rdate"] >= tb_sdate) & (df["rdate"] < tb_edate)]
    # 去年的总营业额
    tb_total_sale = round((tb_df["dealtotal"].sum() / trans_num), 2) if len(tb_df) > 0 else 0.00

    # 同比增长率计算 =（本期数－同期数）/同期数×100%
    tb_percentage = "%.2f%%" % round(
        ((last_month_total - tb_total_sale) / tb_total_sale * 100) if tb_total_sale > 0 else 0, 2)

    # 环比 取上月数据
    hb_sdate = date_util.get_last_month_first_day(s_date).date()
    hb_edate = date_util.get_last_month_last_day(e_date).date()

    # 上月数据
    hb_df = df[(df["rdate"] >= hb_sdate) & (df["rdate"] < hb_edate)]
    # 上月总营业额
    hb_total_sale = round((hb_df["dealtotal"].sum() / trans_num), 2) if len(hb_df) > 0 else 0.00

    # 环比增长率计算= （本期数-上期数）/上期数×100%。
    hb_percentage = "%.2f%%" % round(
        ((last_month_total - hb_total_sale) / hb_total_sale * 100) if hb_total_sale > 0 else 0, 2)
    # 本月销售额
    c_sdate = date_util.get_month_first_day(ve_date).date()
    c_edate = date_util.get_month_last_day(ve_date).date()
    c_month_df = df[(df["rdate"] >= c_sdate) & (df["rdate"] < c_edate)]
    c_month_total_sale = round((c_month_df["dealtotal"].sum() / trans_num), 2) if len(c_month_df) > 0 else 0.00

    # 本月营业额与上月对比营业额 增长率 - 月增长率 =（本月营业额-上月营业额）/上月营业额*100%
    m_growth_rate = "%.2f%%" % round(
        ((c_month_total_sale - last_month_total) / last_month_total * 100) if last_month_total > 0 else 0, 2)

    # 近12月销售趋势
    group_df = df
    month_groups = group_df.groupby(by=["month_group"], as_index=False)["dealtotal"].sum()
    group_sales = pd.DataFrame(month_groups)
    # 封装结果数据
    return {"total_sale": total_sale, "last_month_total": last_month_total,
            "tb_percentage": tb_percentage, "hb_percentage": hb_percentage,
            "c_month_total_sale": c_month_total_sale, "m_growth_rate": m_growth_rate,
            "group_sales": group_sales}


# 展示图数据
def calculate_gragh_data(values):
    data = global_store(values)
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


def find_sales_list(values):
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
    if values:
        if values["begin_month"] and values["end_month"]:
            query_sql += """  and to_char(rdate,'YYYY-MM') >= '{begin_month}'
                                     and to_char(rdate,'YYYY-MM') <= '{end_month}'
                   """.format(begin_month=values["begin_month"], end_month=values["end_month"])
        if values["city"]:
            # 长度大于1 循环处理
            citys = tuple(str(c) for c in values["city"]) if len(values['city']) > 1 \
                else "(" + str(values['city'][0]) + ")"
            query_sql += """ and city_level in {city}""".format(city=citys)
        if values["channel"]:
            channels = tuple(c[0] for c in values["channel"]) if len(values['channel']) > 1 \
                else "(" + values['channel'][0] + ")"
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


def find_channel_list():
    query_sql = """
        select distinct businessname from  chunbaiwei.fact_storesale_weather
    """

    data = db_util.query_list(query_sql, default_dbname)

    return data
