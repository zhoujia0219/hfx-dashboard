import dash_bootstrap_components as dbc

from services.srv_comm_dim import get_dim_store_areas


def filter_store_area():
    """
      门店面积筛选组件
      :return 组件
    """
    # 门店面积
    options = get_dim_store_areas()
    default_values = [r["value"] for r in options]
    return dbc.FormGroup([
        dbc.Label("门店面积", className='sidebar-label'),
        dbc.Checklist(
            id="f_store_area",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
