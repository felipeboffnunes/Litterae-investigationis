# -*- coding: utf-8 -*-

# Libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Components
from components.pages import pages

# App setup
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

# App content
content = html.Div(id="page-content")

menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(html.I("Reader"),
            href="/page-1",
            id="page-1-link"
        ), width="auto"),
        dbc.Col(
            dbc.NavLink(html.I("Review"),
            href="/page-2",
            id="page-2-link"
        ), width="auto"),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

menu = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Museaum", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(menu_items, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
    id="menu")

# App layout
app.layout = html.Div([dcc.Location(id="url"),menu, content], id="layout")

# Callbacks
#
# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 3)]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return pages["home"]
    elif pathname in ["/page-2"]:
        return pages["home"]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Pages callbacks
#
# Home callbacks
@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
                  [Input('cytoscape-two-nodes', 'tapNodeData')])
def displayTapNodeData(data):
    if data:
        return "You recently clicked/tapped the city: " + data['label']