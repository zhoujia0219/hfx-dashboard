from pandas import DataFrame
from utils import db_util
from utils.date_util import get_current_month_all_day

default_dbname = "data_analysis"


def sales_day(all_time_list) -> DataFrame:
    """
    销售日数据
    param all_time_list:所有时间点
    param x_choice_time:选择的时间范围标志区间
    """
    today = '2021-03-21'  # todo 测试的date
    yes_day = '2021-03-20'  # todo 测试的date
    query_sql = ""
    if all_time_list[0] and not all_time_list[1]:
        # 表示只查询今天的数据
        query_sql = """
            select sale, times,rdate from  (select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='{}' ) a  
            where times in {}
        """.format(today, tuple(all_time_list[0]))
    elif all_time_list[0] and all_time_list[1]:
        # 今天昨天的数据
        begin_time = all_time_list[0][0] + ':00:00'
        end_time = all_time_list[1][-1] + ':00:00'
        query_sql = """
                select sale, substr(times,0,3) as times,rdate  from  chunbaiwei.fact_salebill where 
                (rdate='{}' and times BETWEEN '{}' and '24:00:00') or 
                (rdate='{}' and times BETWEEN '00:00:00'  and '{}')
        """.format(yes_day, begin_time, today, end_time)
    mapdata = db_util.read_by_pd(query_sql, default_dbname)
    return mapdata


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
