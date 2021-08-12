import dash_bootstrap_components as dbc

from services.srv_comm_dim import get_dim_city_levels


def filter_city_level():
    """
      城市级别筛选组件
      :return 组件
    """
    # 门店级别定义
    options = get_dim_city_levels()
    default_values = [r["value"] for r in options]
    return dbc.FormGroup([
        dbc.Label("门店所属城市", className='sidebar-label'),
        dbc.Checklist(
            id="f_cities",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
