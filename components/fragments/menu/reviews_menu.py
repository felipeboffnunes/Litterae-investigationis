import dash_bootstrap_components as dbc
import dash_core_components as dcc

reviews_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(dbc.Button("Create Review", id="create-review-button", n_clicks=0),
            href="/page-4",
            id="page-4-link"
            ),
            id="ss", 
            width={"size": "3"}),
        
        dbc.Col(
            dbc.NavLink(dbc.Button("Open Review", id="select-review-button", n_clicks=0), 
            href="/page-3",
            id="page-3-link"
            ),
            id="sq",
            width={"size": "3"}),
        
        dbc.Col(
            dbc.Button("Download CSV", id="download-csv-button", n_clicks=0), 
            width={"size": "3"}),
        
        dcc.ConfirmDialog(
            id='confirm-download',
            message='Your reviews were downloaded as CSV!',
        )
    ],

)

reviews_menu = dbc.Navbar(
    [
        reviews_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "width": "100%"},
    id="menu")