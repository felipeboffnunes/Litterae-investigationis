import dash_bootstrap_components as dbc

create_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Create Review", id="created-review-button", n_clicks=0),
            href="/page-3",
            id="page-3-link"
            ),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.NavLink(dbc.Button("Cancel Review", id="cancel-review-button", n_clicks=0),
            href="/page-2",
            id="page-2-link"
            ),
            id="sq", 
            width={"size": "3", "offset": "2"}),
    ],

)

create_menu = dbc.Navbar(
    [
        create_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="menu")