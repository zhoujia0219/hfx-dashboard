import dash_bootstrap_components as dbc

# 渠道信息获取
from services.srv_comm_dim import get_dim_channel


def filter_channels():
    """
      销售渠道筛选组件
      :return 组件
    """
    options = get_dim_channel()
    default_values = [r["value"] for r in options]
    return dbc.FormGroup([
        dbc.Label("销售渠道", className='sidebar-label'),
        dbc.Checklist(
            id="f_channels",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
