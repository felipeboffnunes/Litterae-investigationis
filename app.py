# -*- coding: utf-8 -*-

# Libraries
import pandas as pd
import sqlite3
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Components
from components.pages import pages, table_div
from components.graph_manager import getGraphData
from components.create_review_form import review_form
from components.create_research_form import research_form

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
app.layout = html.Div([dcc.Location(id="url"),menu, content], id="layout", style={"overflow":"hidden"})

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
        return pages["review"]
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
@app.callback([Output('cytoscape-tapNodeData-output', 'children'),
               Output("home-graph-content", "style"), 
               Output("home-graph", "style")],
                  [Input('cytoscape-two-nodes', 'tapNodeData')])
def displayTapNodeData(data):
    if data:
        if data["id"][:6] == "paper:":
            doi = data["id"][6:]
            try:
                conn = sqlite3.connect("./database/home_graph.db")
                
                cursor = conn.cursor()
                
                
                cursor.execute(f"""
                SELECT * FROM papers WHERE doi = "{doi}";
                """)    
                
                result = cursor.fetchone()
                return [html.Div([
                        html.H3(result[1]),
                        html.P(result[2]),
                        html.P(result[3]),
                        html.Hr(),
                        html.P(result[4])
                        ]), {"width": "60%"}, {"width": "40%"}]
            except: 
                pass
        
        elif data["id"][:7] == "author:":
            name = data["label"].replace("_", " ")
            try:
                conn = sqlite3.connect("./database/authors.db")
                
                cursor = conn.cursor()
                
                
                cursor.execute(f"""
                SELECT * FROM authors WHERE name = "{name}";
                """)    
                
                result = cursor.fetchone()
                return [html.Div([
                        html.H3(result[1]),
                        html.P(result[2]),
                        ]), {"width": "60%"}, {"width": "40%"}]
            except:
                pass
            
        return ["We haven't found any data on: " + data['label'], {"width": "60%"}, {"width": "40%"}]
    return [None, {"width": "0%"}, {"width": "100%"} ]


@app.callback(Output('cytoscape-two-nodes', 'elements'),
                  [Input('dropdown-graph-filter', 'value')])
def filterGraphData(data):
    return getGraphData(data)

# Review data
review_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Go back", id="return-review-button", n_clicks=0),
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

review_menu = dbc.Navbar(
    [
        review_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="menu")


# Review callbacks
@app.callback([Output('review-content-output', 'children'),
              Output('review-content', 'style'),
              Output("callback-open-description-div", "children")],
                  [Input('select-review-button', 'n_clicks'),
                   Input("reviews-table", "value")],
                  [State("reviews-table", "active_cell")])
def open_description(data, table, state):
    if state and data:
        idx = state["row_id"]
        try:
            conn = sqlite3.connect("./database/reviews.db")
                    
            cursor = conn.cursor()
            
            cursor.execute(f"""
            SELECT * FROM reviews WHERE id = "{idx}";
            """)   
            
            result = cursor.fetchone()
            
            return [html.Div([
                    html.H3(result[1]),
                    html.P(result[2]),
                    html.P(result[3]),
                    html.P(result[4]),
                    review_menu
                    ], id="description-review"), {"width": "100%"}, None]
        except:
            pass
    return

@app.callback([Output("callback-return-description-div", "children"),
               Output("description-review", "children")],
                  [Input('return-review-button', 'n_clicks')])
def return_to_reviews(data):
    if data:
        return [html.Div([
                table_div
                ], id="callback-open-description-div"), None]
    return


@app.callback(Output("confirm-download", "displayed"),
              [Input('download-csv-button', 'n_clicks')])
def download_reviews(data):
    try:
        conn = sqlite3.connect("./database/reviews.db")
        db_df = pd.read_sql_query("SELECT * FROM reviews", conn)
        db_df.to_csv("reviews.csv", index=True)
    except:
        pass
    if data:
        return True
    return False


# Create Review

create_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Create Review", id="created-review-button", n_clicks=0),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.Button("Cancel Review", id="cancel-review-button", n_clicks=0),
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

@app.callback([Output("callback-create-review-div", "children"),
               Output("review-create-output", "children"),
               Output("review-create", "style")],
              [Input('create-review-button', 'n_clicks')])
def create_review(data):
    
    if data:
        return [None, html.Div([review_form,create_menu]), {"width": "97%", "padding-left": "2em"}]
        
    return [html.Div([
            html.Div([
                table_div
                ], id="callback-open-description-div")
        ], id="callback-return-description-div", style={"width": "100%"}), html.P(id="review-create-output"), {"width": "0%"}]
    

@app.callback(Output("callback-cancel-review-div", "children"),
              [Input("cancel-review-button", "n_clicks")])
def cancel_review(data):
    if data:
        return html.Div([
                html.Div([
                    html.Div([
                        table_div
                        ], id="callback-open-description-div")
                ], id="callback-return-description-div", style={"width": "100%"}),
            ], id="callback-create-review-div"),
    return


review2_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Go back", id="return2-review-button", n_clicks=0),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.Button("Do research", id="research2-review-button", n_clicks=0),
            id="sq", 
            width={"size": "3", "offset": "2"}),
    ],

)
review2_menu = dbc.Navbar(
    [
        review2_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")

@app.callback([Output("created-review", "children"),
               Output("created-review", "style"),
               Output("view-review-callback-div", "children")],
              [Input("created-review-button", "n_clicks")],
              [State("review-title-row", "value"),
               State("authors-row", "value"),
               State("keywords-row", "value"),
               State("description-row", "value")])
def view_created_review(data, title, authors, keywords, description ):
    if(data):
        try:
            conn = sqlite3.connect("./database/reviews.db")
            
            cursor = conn.cursor()

            cursor.execute(f"""
            INSERT INTO reviews (name, authors, tags, description)
            VALUES ("{title}", "{authors}", "{keywords}", "{description}")
            """)
            
            conn.commit()
        except:
            pass
        try:
            conn = sqlite3.connect("./database/reviews.db")
            
            cursor = conn.cursor()
            cursor.execute(f"""
            SELECT * FROM reviews WHERE name = "{title}";               
            """)
            
            result = cursor.fetchone()
            return [html.Div([
                        html.H3(result[1]),
                        html.P(result[2]),
                        html.P(result[3]),
                        html.P(result[4]),
                        review2_menu
                        ], id="description-review"), {"padding-left": "2em","width": "100%"}, 
                    
                    html.Div([html.P(id="review-create-output")], 
                    id="review-create",  style={"width": "0%"})]
        except:
            pass
    return html.P("hey")


@app.callback([Output("callback-created-review-div", "children"),
               Output("callback-return-created-review-div", "children")],
              [Input("return2-review-button", "n_clicks")])
def return_created_review(data):
    if data:
        return [html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            table_div
                        ], id="callback-open-description-div")
                    ], id="callback-return-description-div", style={"width": "100%"}),
                ], id="callback-create-review-div"),
            ], id="callback-cancel-review-div"), 
                
                html.Div([html.P(id="created-review-output")], 
                id="created-review",  style={"width": "0%"})]
    return


research_menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Go back", id="return2-review-button", n_clicks=0),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.Button("Do research", id="research2-review-button", n_clicks=0),
            id="sq", 
            width={"size": "3", "offset": "2"}),
    ],

)
research_menu = dbc.Navbar(
    [
        review2_menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "left":0, "width": "100%"},
    id="review-menu")
@app.callback([Output("research-output", "children"),
               Output("research", "style"),
               Output("review-content", "children")],
              [Input("research-review-button", "n_clicks")])
def research(data):
    if data:
        return [html.Div([research_form, research_menu], style={"padding-left": "2em", "width": "100%", "height": "90vh"}), 
                {"width": "100%"}, html.Div([html.P(id="review-content-output")], id="review-content",  style={"width": "0%"})]
    return

@app.callback([Output("do-research-output", "children"),
               Output("do-research", "style"),
               Output("callback-do-research-div", "children")],
              [Input("research-review-button", "n_clicks")])
def do_research(data):
    pass