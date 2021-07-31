# 维度数据
# 部分维度为固定的，如城市级别等
# 另一些维度是从数据库中获取的

from typing import List, Dict


def get_dim_city_levels() -> List[Dict]:
    """
    获取城市维度，后续从数据库中读取
    """
    return [
        {"label": "一线城市", "value": 1},
        {"label": "二线城市", "value": 2},
        {"label": "三线城市", "value": 3},
        {"label": "其它", "value": 4},
    ]


def get_dim_store_ages() -> List[Dict]:
    """
    获取新店、老店的定义
    """
    return [
        {"label": "新店（0-1年）", "value": 1},
        {"label": "1-2年", "value": 2},
        {"label": "2-3年", "value": 3},
        {"label": "3-5年", "value": 4},
        {"label": ">5年", "value": 5},
    ]