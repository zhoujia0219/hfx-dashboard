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


def get_day_hour(x_choice_time):
    """一天24小时
        param x_choice_time:选择的时间范围
        return: data_list:所有时间点的空数据，列表嵌元组形式
                all_time_list:所有时间点，列表嵌列表，第一个列表是昨日时间点，第二个列表是今日时间点
    """
    data_list = list()  # 所有时间点的空数据，列表嵌元组形式
    all_time_list = [[], []]  # 所有时间点，列表嵌列表，第一个列表是昨日时间点，第二个列表是今日时间点
    today = datetime.today()  # 今天的时间
    current_hour = today.hour  # 当前的小时
    current_hour = 11
    choice_str_list = x_choice_time.split("-")
    try:
        choice_str_list_begin = int(choice_str_list[0])  # 开始时间
        choice_str_list_end = int(choice_str_list[1])  # 结束时间
        print(choice_str_list_begin, 1, choice_str_list_end)
    except:
        print(1)
        choice_str_list_begin = 5
        choice_str_list_end = 12  # 表示前端数据传错了，则依据采用默认的时间
    # 当天的时间范围内
    # 1.当前时间<开始时间
    if current_hour < choice_str_list_begin:
        for i in range(choice_str_list_begin, choice_str_list_end + 1):
            all_time_list[0].append(str(i) if len(str(i)) == 2 else '0' + str(i))

    # 2.当前时间处于时间范围中间
    elif current_hour > choice_str_list_begin and current_hour < choice_str_list_end:
        for i in range(choice_str_list_begin, current_hour + 1):
            # 今天的范围时间
            all_time_list[1].append(str(i) if len(str(i)) == 2 else '0' + str(i))
        for j in range(current_hour + 1, choice_str_list_end + 1):
            # 剩下的部分是属于昨天的时间点，暂时将当前时间点放到了今天，在取数据那部分验证今天是否有数据
            all_time_list[0].append(str(j) if len(str(j)) == 2 else '0' + str(j))
    # 3.当前时间>结束时间
    else:
        for i in range(choice_str_list_begin, choice_str_list_end + 1):
            all_time_list[1].append(str(i) if len(str(i)) == 2 else '0' + str(i))
    for i in range(choice_str_list_begin, choice_str_list_end + 1):
        i = str(i) if len(str(i)) == 2 else '0' + str(i)
        data_list.append((i, 0))  # 创建完整的时间点
    return data_list, all_time_list


def get_everyDay(begin_date, end_date):
    """获取两个时间中间的所有时间"""
    date_list = []
    begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += timedelta(days=1)
    return date_list


def current_week_month():
    """
    本周本月的日期
    return:当前周的所有日期，当前月的所有日期
    """
    today = '2021-01-21'  # todo 测试的日期
    monday, sunday = datetime.strptime(today, '%Y-%m-%d').date(), datetime.strptime(today, '%Y-%m-%d').date()
    one_day = timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    week_list = get_everyDay(monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d"))  # 当前周的所有日期
    first_day = today[:8] + "01"  # 当前月的第一天的日期
    month_list = get_everyDay(first_day, today)
    return tuple(week_list), tuple(month_list)


def year_month_count(year, month):
    """某年某月有多少天"""
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
        return 31
    elif (month == 4 or month == 6 or month == 9 or month == 11):
        return 30
    elif month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
        return 29
    else:
        return 28


def get_week_day(date):
    """
    根据日期输出星期格式
    """
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


if __name__ == '__main__':
    current_week_month()
