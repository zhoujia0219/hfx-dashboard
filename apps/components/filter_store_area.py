import dash_bootstrap_components as dbc


def filter_store_area(label_name: str,
                      options: list,
                      default_values: list):
    """
      门店面积筛选组件
      :param label_name ： 组件标签名称
      :param options: 选项
      :param default_values: 默认选中值
      :return 组件
    """
    return dbc.FormGroup([
        dbc.Label(label_name, className='sidebar-label'),
        dbc.Checklist(
            id="f_store_area",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
