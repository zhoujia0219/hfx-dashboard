from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc


def filter_month_range(date_range: List[str],
                       default_start_month: str,
                       default_end_month: str):
    """
      日期区间筛选组件
      :param date_range ： 组件标签名称
      :param default_start_month: 默认开始月份
      :param default_end_month: 默认结束月份
      :return 组件
    """
    return dbc.FormGroup([
        dbc.Label('日期范围', className='sidebar-label'),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='f_begin_month',
                    options=[{"label": x, "value": x} for x in date_range],
                    value=default_start_month,
                    clearable=False,
                    persistence=True,
                )),
                dbc.Col(dcc.Dropdown(
                    id='f_end_month',
                    options=[{"label": x, "value": x} for x in date_range],
                    value=default_end_month,
                    clearable=False,
                    persistence=True,
                )),
            ], no_gutters=True,
        ),
    ])
