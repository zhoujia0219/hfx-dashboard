import dash_bootstrap_components as dbc
import dash_core_components as dcc


def filter_month_range(date_range, default_start_month, default_end_month):
    return dbc.FormGroup([
        dbc.Label('日期范围', className='sidebar-label'),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    id='begin_month',
                    options=[{"label": x, "value": x} for x in date_range],
                    value=default_start_month,
                    clearable=False,
                    persistence=True,
                )),
                dbc.Col(dcc.Dropdown(
                    id='end_month',
                    options=[{"label": x, "value": x} for x in date_range],
                    value=default_end_month,
                    clearable=False,
                    persistence=True,
                )),
            ], no_gutters=True,
        ),
    ])
