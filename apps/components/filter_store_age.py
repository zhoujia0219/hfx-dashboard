import dash_bootstrap_components as dbc

from services.srv_comm_dim import get_dim_store_ages


def filter_store_age():
    """
      店龄筛选组件
      :return 组件
    """
    # 店龄
    options = get_dim_store_ages()
    default_values = [r["value"] for r in options]
    return dbc.FormGroup([
        dbc.Label("店龄", className='sidebar-label'),
        dbc.Checklist(
            id="f_store_age",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
