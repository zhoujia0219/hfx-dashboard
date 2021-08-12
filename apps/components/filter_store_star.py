import dash_bootstrap_components as dbc

from services.srv_comm_dim import get_dim_store_star


def filter_store_star():
    """
      门店星级筛选组件
      :return 组件
    """

    # 门店星级
    options = get_dim_store_star()
    default_values = [r["value"] for r in options]
    return dbc.FormGroup([
        dbc.Label("门店星级", className='sidebar-label'),
        dbc.Checklist(
            id="f_store_star",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
