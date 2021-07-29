import dash_bootstrap_components as dbc


def filter_store_star(label_name: str,
                      options: list,
                      default_values: list):
    return dbc.FormGroup([
        dbc.Label(label_name, className='sidebar-label'),
        dbc.Checklist(
            id="f_store_star",
            options=options,
            value=default_values,
            inline=True,
            labelStyle={'min-width': 70},
            persistence=True,
        ),
    ])
