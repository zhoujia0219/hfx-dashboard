import calendar
from datetime import timedelta, datetime
from datetime import date

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


def get_current_month_all_day(range_choice: str):
    """
    获取所有日期：yyyy-mm-dd
    by:本月到目前的所有天数
    zj：最近30天
    """
    if range_choice == "zj":
        range_count = 30
    else:
        # range_count = datetime.now().day
        range_count = 12  # todo 测试数据  后面换回来
    # today = date.today()
    today = datetime.strptime("2021-04-12", '%Y-%m-%d')  # todo 测试数据  后面换回来
    date_data = list()
    for i in range(1, range_count + 1):
        if i == 1:
            date_data.append(today.strftime("%Y-%m-%d"))
            continue
        oneday = timedelta(days=1)
        yesterday = today - oneday
        date_data.append(yesterday.strftime("%Y-%m-%d"))
        today = yesterday
    return tuple(date_data)
