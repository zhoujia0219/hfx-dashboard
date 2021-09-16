# 所有表格形式的设计都可以用该组件
import dash_bootstrap_components as dbc
import dash_html_components as html


def table_key_category_sale(col_number, param_list, width):
    """"重点品类销售情况
    param col_number:多少列
          param_list:数据列表
          width :width参数
    """
    col_list = []
    for i in range(col_number):
        col_list.append(
            dbc.Col(
                html.H6(
                    children="%s" % param_list[i]
                ),
                width=width
            ),
        )
    return dbc.Row(col_list)
