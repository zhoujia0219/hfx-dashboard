import dash_bootstrap_components as dbc


def filter_city_level(label_name,
                      options: list,
                      default_values: list):
    """
      城市级别筛选组件
      :param label_name ： 组件标签名称
      :param options: 选项
      :param default_values: 默认选中值
      :return 组件
    """
    return dbc.FormGroup([
        dbc.Label(label_name, className='sidebar-label'),
        dbc.Checklist(
            id="f_cities",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
