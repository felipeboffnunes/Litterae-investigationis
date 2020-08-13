import dash_bootstrap_components as dbc

research_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Go back", id="return-review-button", n_clicks=0),
            href="/page-3",
            id="page-3-link"
            ),
            id="return-review-col", 
            width={"size": "3"}),
        dbc.Col(
            dbc.NavLink(dbc.Button("Search", id="search-button", n_clicks=0),
            href="/page-3",
            id="page-3-link"
            ),
            id="search-col", 
            width={"size": "3", "offset": "2"}),
    ],

)
research_menu = dbc.Navbar(
    [
        research_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")
