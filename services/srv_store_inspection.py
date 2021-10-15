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
    环形图—门店巡检完成率
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
    环形图—门店巡检合格率
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

def find_store_inspect_finish_rate(area_val,year_value) -> DataFrame:
    """
    折线图—门店巡检完成率--添加区域和月份选项
    """
    query_sql = """
        select 
        tab1.d_date as months,
				case 
					when RIGHT(tab1.d_date,2) = '01' then '一月'
					when RIGHT(tab1.d_date,2) = '02' then '二月'
					when RIGHT(tab1.d_date,2) = '03' then '三月'
					when RIGHT(tab1.d_date,2) = '04' then '四月'
					when RIGHT(tab1.d_date,2) = '05' then '五月'
					when RIGHT(tab1.d_date,2) = '06' then '六月'
					when RIGHT(tab1.d_date,2) = '07' then '七月'
					when RIGHT(tab1.d_date,2) = '08' then '八月'
					when RIGHT(tab1.d_date,2) = '09' then '九月'
					when RIGHT(tab1.d_date,2) = '10' then '十月'
					when RIGHT(tab1.d_date,2) = '11' then '十一月'
					when RIGHT(tab1.d_date,2) = '12' then '十二月'
				end,
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
                WHERE 1 = 1 and left(d_date,4) = '"""+year_value+"""'
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and tab1.area = '"""+area_val+"""' order by RIGHT(tab1.d_date,2), tab1."num1" asc
            """
    store_inspect_finish_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_finish_rate


def find_store_inspect_regular_rate(area_val) -> DataFrame:
    """
    门店巡检合格率--添加区域选项
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
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and tab1.area = '"""+area_val+"""' order by tab1."num1" asc
            """
    store_inspect_regular_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_regular_rate

def find_store_inspect_rectify_rate(area_val)-> DataFrame:
    """
    门店巡检整改率--添加区域选项
    """
    query_sql = """
            select 
            tab1.d_date as months,
            tab1.area as areas,
            tab1.num1 as store_rectify_rate,
            tab2.num2 as times_rectify_rate from (
                select 
                d_date,
                area,
                round((sum(rectify)/count(rectify))*100,0) as "num1" 
                 from chunbaiwei.inspection_plan 
                where 1 = 1 
             GROUP BY d_date,area) as tab1,
                    (SELECT
                    d_date,
                    area,
                    COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                     FROM chunbaiwei.inspection_plan 
                    WHERE 1 = 1 
                 GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and tab1.area = '""" + area_val + """' order by tab1."num1" asc
                """
    store_inspect_rectify_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_rectify_rate

def find_store_inspect_finish_rate_01(month,val) -> DataFrame:
    """
    门店巡检完成率--添加月份选项
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
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and right(tab1.d_date, 2) = '"""+month+"""' and left(tab1.d_date, 4) = '2020' order by tab1."num1"
            """ + val
    store_inspect_finish_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_finish_rate


def find_store_inspect_regular_rate_01(month,val) -> DataFrame:
    """
    门店巡检合格率--添加月份选项
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
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and right(tab1.d_date, 2) = '"""+month+"""' and left(tab1.d_date, 4) = '2020' order by tab1."num1"
            """ + val
    store_inspect_regular_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_regular_rate

def find_store_inspect_rectify_rate_01(month,val) -> DataFrame:
    """
    门店巡检合格率--添加月份选项
    """
    query_sql = """
        select 
        tab1.d_date as months,
        tab1.area as areas,
        tab1.num1 as store_rectify_rate,
        tab2.num2 as times_rectify_rate from (
            select 
            d_date,
            area,
            round((sum(rectify)/count(rectify))*100,0) as "num1" 
             from chunbaiwei.inspection_plan 
            where 1 = 1 
         GROUP BY d_date,area) as tab1,
                (SELECT
                d_date,
                area,
                COALESCE(round((SUM(real_time)/SUM(plan_times)) * 100, 0 ),0) as "num2"
                 FROM chunbaiwei.inspection_plan 
                WHERE 1 = 1 
             GROUP BY d_date,area) as tab2 where tab1.d_date = tab2.d_date and tab1.area = tab2.area and right(tab1.d_date, 2) = '"""+month+"""' and left(tab1.d_date, 4) = '2020' order by tab1."num1"
            """ + val
    store_inspect_rectify_rate = db_util.read_by_pd(query_sql, default_dbname)
    return store_inspect_rectify_rate

def find_store_inspect_item_rate(area_val) ->DataFrame:
    """
    门店巡检项总合格率--添加区域选项
    :return:
    """
    query_sql = """
    SELECT
    area,
    round((sum(ispass)/count(ispass))*100,0) as "item_regular_rate" 
    FROM chunbaiwei.inspection_item
    where 1 = 1 and area = '""" + area_val + """'
    group by area"""
    store_inspect_item_rate = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_item_rate


def find_store_inspect_style_rate(area_val) ->DataFrame:
    """
    不合格巡检项类型分布--添加区域选项
    :param area_val:
    :return:
    """
    query_sql = """
    select tab.*,round(usm::numeric / cn::numeric *100,0) as unqualified_value from (
        select
        area,
        inspect_category,
        sum(case when ispass='0' then 1 else 0 end) as usm,
        count(ispass) as cn
        FROM chunbaiwei.inspection_item
        group by area,inspect_category
        ORDER BY area
        ) 
    as tab where area = '""" + area_val + """' and round(usm::numeric / cn::numeric,4) > 0
    """
    store_inspect_style_rate = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_style_rate


def find_store_table() ->DataFrame:
    """
    table图
    :param area_val:
    :return:
    """
    query_sql = """
        select * from chunbaiwei.inspection_plan_stat
    """
    store_inspect_table = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_table


def find_inspect_style_regular(area_val) ->DataFrame:
    """
    treemap图
    合格巡检类型
    :return:
    """
    query_sql = """
    	select tab.* from (
        select
        area,
        inspect_category,
		inspect_item,
        sum(case when ispass='1' then 1 else 0 end) as usm,
        count(ispass) as cn
        FROM chunbaiwei.inspection_item
        group by area,inspect_category,inspect_item
        ORDER BY area
        ) 
    as tab where area = '""" + area_val + """'and round(usm::numeric / cn::numeric,4) > 0
    """
    store_inspect_tree = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_tree

# 新增环形图sql语句
def find_inspect_style_regular_pie(area_val) ->DataFrame:
    """
    环形图—巡检项评估占比
    :return:
    """
    query_sql = """
    	select tab.*,round(tab.usm ::numeric / (select sum(case when ispass='1' then 1 else 0 end) as usm from chunbaiwei.inspection_item where area = '""" + area_val + """') ::numeric,2) * 100 as "ispass_rate"  from (
        select
        area,
        inspect_category,
        sum(case when ispass='1' then 1 else 0 end) as usm,
        count(ispass) as cn
        FROM chunbaiwei.inspection_item
        --where left(d_date,4) = '2020' 
        group by area,inspect_category
        ORDER BY area
        ) 
    as tab where area = '""" + area_val + """' and round(usm::numeric / cn::numeric,4) > 0
    """
    store_inspect_pie = db_util.read_by_pd(query_sql, default_dbname).values
    return store_inspect_pie

