import pandas as pd


def get_date_list(begin, end):
    """
    随机生成一个年月列表
    """
    date_list = [x.strftime('%Y-%m') for x in list(pd.date_range(start=begin, end=end, freq="M"))]
    return date_list
