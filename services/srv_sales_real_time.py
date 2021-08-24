from pandas import DataFrame
from utils import db_util
from utils.date_util import get_current_month_all_day

default_dbname = "data_analysis"


def sales_day() -> DataFrame:
    """
    销售日数据
    """
    query_sql = """
         select sale, substr(times,0,3) as times,rdate from chunbaiwei.fact_salebill where rdate='2021-03-21' OR rdate='2021-03-22'               
             """
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
