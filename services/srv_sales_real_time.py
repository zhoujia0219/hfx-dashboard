from datetime import datetime

from pandas import DataFrame
from utils import db_util
from utils.date_util import get_current_month_all_day, current_week_month

default_dbname = "data_analysis"


def sales_day(all_time_list):
    """
    销售日数据
    param all_time_list:所有时间点
    param x_choice_time:选择的时间范围标志区间
    """
    to_day = '2021-03-21'  # todo 测试的date
    yes_day = '2021-03-20'  # todo 测试的date
    current_hour = datetime.today().hour  # 当前的小时
    current_hour = str(current_hour) if len(str(current_hour)) else '0' + str(current_hour)
    current_hour = 11
    has_data_sql = """
            select 1 from  (select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='{}' ) a  
            where times='{}'""".format(to_day, current_hour)
    has_data = db_util.read_by_pd(has_data_sql, default_dbname)
    if not len(has_data):
        # 今天这个临界点没有数据则用昨天的数据
        all_time_list[0].append(current_hour)
    today_sql = """
    select sale, times,rdate from  (select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='{}' ) a  
        where times in {} """.format(to_day,
                                     str(set(all_time_list[1])).replace('{', "(").replace("}", ')') if all_time_list[
                                         1] else ('215', '261'))
    yesterday_sql = """
    select sale, times,rdate from  (select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='{}' ) a  
        where times in {} """.format(yes_day,
                                     str(set(all_time_list[0])).replace('{', "(").replace("}", ')') if all_time_list[
                                         0] else ('251', '261'))
    today_data = db_util.read_by_pd(today_sql, default_dbname)
    yesterday_data = db_util.read_by_pd(yesterday_sql, default_dbname)
    return today_data, yesterday_data


# def day_area_all_data(all_time_list):
#     """
#     区域本日销售分布数据
#     """
#     to_day = '2021-03-21'  # todo 测试的date
#     yes_day = '2021-03-20'  # todo 测试的date
#     current_hour = datetime.today().hour  # 当前的小时
#     current_hour = str(current_hour) if len(str(current_hour)) else '0' + str(current_hour)
#     current_hour = 11
#     has_data_sql = """
#             select 1 from  (select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='{}' ) a
#             where times='{}'""".format(to_day, current_hour)
#     has_data = db_util.read_by_pd(has_data_sql, default_dbname)
#     if not len(has_data):
#         # 今天这个临界点没有数据则用昨天的数据
#         all_time_list[0].append(current_hour)
#     today_sql = """
#     select dealtotal, times,rdate from  (select dealtotal, substr(times,0,3) as times,rdate from chunbaiwei.fact_storesale_weather where rdate='{}' ) a
#         where times in {} """.format(to_day,
#                                      str(set(all_time_list[1])).replace('{', "(").replace("}", ')') if all_time_list[
#                                          1] else ('215', '261'))
#     yesterday_sql = """
#     select dealtotal, times,rdate from  (select dealtotal, substr(times,0,3) as times,rdate from chunbaiwei.fact_storesale_weather where rdate='{}' ) a
#         where times in {} """.format(yes_day,
#                                      str(set(all_time_list[0])).replace('{', "(").replace("}", ')') if all_time_list[
#                                          0] else ('251', '261'))
#     today_data = db_util.read_by_pd(today_sql, default_dbname)
#     yesterday_data = db_util.read_by_pd(yesterday_sql, default_dbname)
#     return today_data, yesterday_data
def sales_month(range_choice: str) -> DataFrame:
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


today = '2021-01-21'  # todo 测试的date
yesterday = '2021-01-20'  # todo 测试的date


def sale_total():
    """今日昨日销售额"""
    sql_today = """
        select sum(dealtotal)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(today)
    sql_yesterday = """
        select sum(dealtotal)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(yesterday)
    data_today = db_util.query_list(sql_today, default_dbname)
    data_yesterday = db_util.query_list(sql_yesterday, default_dbname)
    return [round(data_today[0][0], 2), round(data_yesterday[0][0], 2)]


def shop_count():
    """今日昨日门店总数"""
    sql_today = """
        select count(*) from (select storeuid  from chunbaiwei.fact_storesale_weather where rdate='{}' GROUP BY storeuid) a
    """.format(today)
    sql_yesterday = """
        select count(*) from (select storeuid  from chunbaiwei.fact_storesale_weather where rdate='{}' GROUP BY storeuid) a
    """.format(yesterday)
    data_today = db_util.query_list(sql_today, default_dbname)
    data_yesterday = db_util.query_list(sql_yesterday, default_dbname)
    return [round(data_today[0][0], 2), round(data_yesterday[0][0], 2)]


def guest_orders():
    """今日昨日客单量"""
    sql_today = """
        select sum(billcount)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(today)
    sql_yesterday = """
        select sum(billcount)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(yesterday)
    data_today = db_util.query_list(sql_today, default_dbname)
    data_yesterday = db_util.query_list(sql_yesterday, default_dbname)
    return [round(data_today[0][0], 2), round(data_yesterday[0][0], 2)]


def cost_price():
    """今日昨日的成本"""
    sql_today = """
        select sum(cost)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(today)
    sql_yesterday = """
        select sum(cost)  from chunbaiwei.fact_storesale_weather where rdate='{}'
    """.format(yesterday)
    data_today = db_util.query_list(sql_today, default_dbname)
    data_yesterday = db_util.query_list(sql_yesterday, default_dbname)
    return [round(data_today[0][0], 2), round(data_yesterday[0][0], 2)]


def dealtotal_plan_sales():
    """
    本周本月的累计销售额/计划销售额
    return:[[本周销售，本周计划销售],[本月销售，本月计划销售]]
    """
    week_list, month_list = current_week_month()  # 本周日期
    sql_sale_week = """
        select sum(dealtotal)  from chunbaiwei.fact_storesale_weather where rdate in {}
    """.format(week_list)
    sql_sale_month = """
        select sum(dealtotal)  from chunbaiwei.fact_storesale_weather where rdate in {}
    """.format(month_list)
    sql_plan_week = """
    select sum(plan_dealtotal)  from chunbaiwei.fact_storesale_weather where rdate in {}
    """.format(week_list)
    sql_plan_month = """
    select sum(plan_dealtotal)  from chunbaiwei.fact_storesale_weather where rdate in {}
    """.format(month_list)
    sale_week = db_util.query_list(sql_sale_week, default_dbname)[0][0]
    sale_month = db_util.query_list(sql_sale_month, default_dbname)[0][0]
    plan_week = db_util.query_list(sql_plan_week, default_dbname)[0][0]
    plan_month = db_util.query_list(sql_plan_month, default_dbname)[0][0]
    return [[sale_week, plan_week], [sale_month, plan_month]]
