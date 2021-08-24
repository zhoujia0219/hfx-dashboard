# 维度数据
# 部分维度为固定的，如城市级别等
# 另一些维度是从数据库中获取的

from typing import List, Dict

from services import srv_sales_bymonth


def get_dim_city_levels() -> List[Dict]:
    """
    获取城市维度，后续从数据库中读取
    :return List[dict]
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
    :return List[dict]
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
    :return List[dict]
    """
    channels = srv_sales_bymonth.find_channel_list()
    return [{"label": c, "value": c} for c in channels["channel"]]


def get_dim_store_areas() -> List[Dict]:
    """
    获取门店面积维度
    :return List[dict]
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
    :return List[dict]
    """
    return [
        {"label": "☆", "value": 1},
        {"label": "☆☆", "value": 2},
        {"label": "☆☆☆", "value": 3},
        {"label": "☆☆☆☆", "value": 4},
        {"label": "☆☆☆☆☆", "value": 5},
    ]


def get_dim_order_type() -> List[Dict]:
    """
    排序类型维度
    :return List[dict]
    """
    return [
        {'label': '排序: 正序', 'value': 1},
        {'label': '排序: 降序', 'value': 2},
    ]


def get_dim_graph_cate() -> Dict:
    """
    图形分类维度
    :return dict
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
    :return dict
    """
    return {'聚合函数: 总和': 'dff.sum()',
            '聚合函数: 平均值': 'dff.mean()',
            '聚合函数: 中位数': 'dff.median()'}


def get_dim_graph_type() -> Dict:
    """
    图形类型维度
    :return dict
    """
    return {'图形: 柱状图': 'px.bar', '图形: 线性图': 'px.line'}


def get_dim_graph_four() -> Dict:
    """
    图形分类维度
    :return dict
    """
    return {'维度: 渠道': 'businessname',
            '维度: 战区': 'areaname4',
            '维度: 店面积': 'areasize',
            '维度: 门店星级': 'star',
            '维度: 门店类型': 'vctype',
            '维度: 城市等级': 'city_level'
            }


def get_dim_graph_scatter() -> Dict:
    """
    图形分类维度
    :return dict
    """
    return {'维度: 城区': 'county_name'}


def get_dim_graph_scatter_x() -> Dict:
    """
    气泡图自定义x轴指标
    :return dict
    """
    return {'X轴:  客单价': 'price',
            'X轴:  客单量': 'billcount',
            'X轴:  面积': 'areasize',
            }


def get_dim_graph_scatter_y() -> Dict:
    """
    气泡图自定义y轴指标
    :return dict
    """
    return {'Y轴:  客单价': 'price',
            'Y轴:  客单量': 'billcount',
            'Y轴:  总销售额': 'dealtotal',
            }


def get_dim_graph_map_limits() -> Dict:
    """
    地理图自定义地图范围
    :return dict
    """
    return {'地图范围:  全国': 'ad_name'
            }


def get_dim_graph_map_index() -> Dict:
    """
    地理图自定义指标
    :return dict
    """
    return {'指标:  总销售额': 'sales'
            }


def get_ZE_PJS_ZWS() -> Dict:
    """
    总额，平均数，中位数的映射关系
    """
    return {
        "ZE": "pic_dff.sum()",
        "PJS": "pic_dff.mean()",
        "ZWS": "pic_dff.median()"  # 中位数
    }


def get_day_hour():
    """一天24小时"""
    return [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0),
            (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0)]
