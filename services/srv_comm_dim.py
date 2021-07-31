# 维度数据
# 部分维度为固定的，如城市级别等
# 另一些维度是从数据库中获取的

from typing import List, Dict

from services import srv_sales_bymonth


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


def get_dim_channel() -> List[Dict]:
    """
    获取渠道维度 - 从数据库中获取
    """
    channels = srv_sales_bymonth.find_channel_list()
    return [{"label": c["channel"], "value": c["channel"]} for c in channels]


def get_dim_store_areas() -> List[Dict]:
    """
    获取门店面积维度
    """
    return [
        {"label": "档口店(<30㎡)", "value": 1},
        {"label": "外卖店(<30㎡)", "value": 2},
        {"label": "小店(<50㎡)", "value": 3},
        {"label": "标准店(50-70㎡)", "value": 4},
        {"label": "大店(>70㎡)", "value": 5},
    ]


def get_dim_store_star() -> List[Dict]:
    """
    获取门店星级
    """
    return [
        {"label": "☆", "value": 1},
        {"label": "☆☆", "value": 2},
        {"label": "☆☆☆", "value": 3},
        {"label": "☆☆☆☆", "value": 4},
        {"label": "☆☆☆☆☆", "value": 5},
    ]


def get_dim_order_type() -> List[Dict]:
    return [
        {'label': '排序: 正序', 'value': 1},
        {'label': '排序: 降序', 'value': 2},
    ]


def get_dim_graph_cate() -> Dict:
    """
    图形分类维度
    """
    return {'维度: 渠道': 'businessname',
            '维度: 战区': 'areaname3',
            '维度: 店面积': 'areasize_bins',
            '维度: 店龄': 'store_age',
            '维度: 门店星级': 'store_star',
            '维度: 门店所属城市': 'store_city',
            }


def get_dim_graph_agg() -> Dict:
    """
    图形聚合函数维度
    """
    return {'聚合函数: 总和': 'dff.sum()',
            '聚合函数: 平均值': 'dff.mean()',
            '聚合函数: 中位数': 'dff.median()'}


def get_dim_graph_type() -> Dict:
    """
    图形类型维度
    """
    return {'图形: 柱状图': 'px.bar', '图形: 线性图': 'px.line'}
