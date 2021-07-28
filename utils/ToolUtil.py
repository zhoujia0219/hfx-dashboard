import calendar
from datetime import timedelta, datetime

import pandas as pd


def get_date_list(begin, end):
    """
    随机生成一个年月列表
    """
    date_list = [x.strftime('%Y-%m') for x in list(pd.date_range(start=begin, end=end, freq="M"))]
    return date_list


def get_month_first_day(p_date: datetime):
    """
    获取指定时间的月份第一天
    """
    return datetime(p_date.year, p_date.month, 1)


def get_month_last_day(p_date: datetime):
    """
    获取指定时间月份的最后一天
    """
    return datetime(p_date.year, p_date.month, calendar.monthrange(p_date.year, p_date.month)[1])


def get_last_month_first_day(p_date: datetime):
    """
    获取指定时间月份的上月第一天
    """
    if p_date.month == 1:
        # 月份为 1  上月 为 12月  年份减去1
        return datetime(p_date.year - 1, 12, 1)
    else:
        return datetime(p_date.year, p_date.month - 1, 1)


def get_last_month_last_day(p_date: datetime):
    """
     获取指定时间月份的上月最后一天
     """
    return datetime(p_date.year, p_date.month, 1) - timedelta(1)
