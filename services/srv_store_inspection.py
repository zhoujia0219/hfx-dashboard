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

def find_all_store_inspect() -> DataFrame:
    """
    门店巡检数据
    """
    query_sql = """
        select 
        (select count(distinct store) from chunbaiwei.inspection_plan where 1 = 1) as all_stores,
        count(distinct store) as inspect_store,
        sum(plan_times) as plan_inspect_times,
        sum(real_time) as real_inspect_times
        from chunbaiwei.inspection_plan 
       where 1 = 1 and finish = 1;
            """
    all_store_inspect = db_util.read_by_pd(query_sql, default_dbname).values
    return all_store_inspect


def find_store_inspect_regular() -> DataFrame:
    """
    门店巡检合格
    """
    query_sql = """
            SELECT 
            SUM(tab.finish) as all_inspects,
            SUM(tab.ispass) as pass ,
            round((select count(atb.*) from chunbaiwei.inspection_plan atb where atb.fraction >= round(avg(tab.fraction), 0) and finish = 1 limit 1) / sum(tab.finish) *100,0)||'%',
            round((select count(btb.*) from chunbaiwei.inspection_plan btb where btb.fraction < round(avg(tab.fraction), 0) and finish = 1  limit 1)  / sum(tab.finish) *100,0)||'%'
            FROM chunbaiwei.inspection_plan tab;
             """
    store_inspect_regular = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_regular


def find_store_inspect_finish_rate_col_name() -> DataFrame:
    """
    门店巡检完成率
    """
    query_sql = """
            select area,area from chunbaiwei.inspection_plan group by area;
            """
    store_inspect_finish_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_finish_rate

def find_store_inspect_finish_rate(area_val) -> DataFrame:
    """
    门店巡检完成率
    """
    query_sql = """
        select 
        tab1.d_date as months,
        tab1.area as areas,
        tab1.num1 as store_finish_rate,
        tab2.num2 as times_finish_rate from (
            select 
            d_date,
            area,
            round((sum(finish)/count(finish))*100,0) as "num1" 
             from chunbaiwei.inspection_plan 
            where 1 = 1 
         GROUP BY d_date,area) as tab1,
                (SELECT
                d_date,
                area,
                COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                 FROM chunbaiwei.inspection_plan 
                WHERE 1 = 1 
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and tab1.area = '"""+area_val+"""' order by tab1.d_date asc
            """
    store_inspect_finish_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_finish_rate


def find_store_inspect_regular_rate(area_val) -> DataFrame:
    """
    门店巡检合格率
    """
    query_sql = """
        select 
        tab1.d_date as months,
        tab1.area as areas,
        tab1.num1 as store_regular_rate,
        tab2.num2 as times_regular_rate from (
            select 
            d_date,
            area,
            round((sum(ispass)/count(ispass))*100,0) as "num1" 
             from chunbaiwei.inspection_plan 
            where 1 = 1 
         GROUP BY d_date,area) as tab1,
                (SELECT
                d_date,
                area,
                COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                 FROM chunbaiwei.inspection_plan 
                WHERE 1 = 1 
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and tab1.area = '"""+area_val+"""' order by tab1.d_date asc
            """
    store_inspect_regular_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_regular_rate


def find_store_inspect_finish_rate_01(month,val) -> DataFrame:
    """
    门店巡检完成率
    """
    query_sql = """
        select 
        tab1.d_date as months,
        tab1.area as areas,
        tab1.num1 as store_finish_rate,
        tab2.num2 as times_finish_rate from (
            select 
            d_date,
            area,
            round((sum(finish)/count(finish))*100,0) as "num1" 
             from chunbaiwei.inspection_plan 
            where 1 = 1 
         GROUP BY d_date,area) as tab1,
                (SELECT
                d_date,
                area,
                COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                 FROM chunbaiwei.inspection_plan 
                WHERE 1 = 1 
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and right(tab1.d_date, 2) = '"""+month+"""' order by tab1.num1
            """ + val
    store_inspect_finish_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_finish_rate


def find_store_inspect_regular_rate_01(month,val) -> DataFrame:
    """
    门店巡检合格率
    """
    query_sql = """
        select 
        tab1.d_date as months,
        tab1.area as areas,
        tab1.num1 as store_regular_rate,
        tab2.num2 as times_regular_rate from (
            select 
            d_date,
            area,
            round((sum(ispass)/count(ispass))*100,0) as "num1" 
             from chunbaiwei.inspection_plan 
            where 1 = 1 
         GROUP BY d_date,area) as tab1,
                (SELECT
                d_date,
                area,
                COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                 FROM chunbaiwei.inspection_plan 
                WHERE 1 = 1 
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and right(tab1.d_date, 2) = '"""+month+"""' order by tab1.num1
            """ + val
    store_inspect_regular_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_regular_rate