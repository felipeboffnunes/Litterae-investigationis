import dash_bootstrap_components as dbc

review_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Go back", id="return-review-button", n_clicks=0),
            href="/page-2",
            id="page-2-link",
            ),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.Button("Do research", id="research-review-button", n_clicks=0),
            id="sq", 
            width={"size": "3", "offset": "2"}),
    ],

)
review_menu = dbc.Navbar(
    [
        review_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")

