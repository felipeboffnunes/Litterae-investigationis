# -*- coding: utf-8 -*-
import os
# Libraries
import pandas as pd
import sqlite3
from flask_caching import Cache
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Components
from components.pages import pages, table_div
from components.graph_manager import getGraphData
from components.fragments.form.create_review_form import review_form
from components.fragments.form.create_research_form import research_form
from components.fragments.menu.review_menu import review_menu
from components.fragments.menu.create_review_menu import create_menu

# App setup
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

#REDIS
#CACHE_CONFIG={
#"CACHE_TYPE":"redis",
#"CACHE_REDIS_URL": os.environ.get("REDIS_URL","redis://localhost:6379")
#}
#
#cache=Cache()
#cache.init_app(server,config=CACHE_CONFIG)

# GLOBAL VARIABLES
REVIEW_ID = ""


# App content
content = html.Div(id="page-content")

menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.NavLink(html.I("Graph"),
            href="/page-1",
            id="page-1-link"
        ), width="auto"),
        dbc.Col(
            dbc.NavLink(html.I("Reader"),
            href="/page-3",
            id="page-3-link"
        ), width="auto"),
        dbc.Col(
            dbc.NavLink(html.I("Reviews"),
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
    id="main-menu")

# App layout
app.layout = html.Div([dcc.Location(id="url"),menu, content], id="layout", style={"overflow":"hidden"})

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return pages["home"]
    elif pathname in ["/page-2"]:
        return pages["reviews"]
    elif pathname in ["/page-3"]:
        return pages["review"]
    elif pathname in ["/page-4"]:
        return pages["create-review"]
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


def store_review(idx):
    try:
        conn = sqlite3.connect("./database/reviews.db")
                
        cursor = conn.cursor()
        
        cursor.execute(f"""
        SELECT * FROM reviews WHERE id = "{idx}";
        """)   
        
        result = cursor.fetchone()
        
        return html.Div([
                html.H3(result[1]),
                html.P(result[2]),
                html.P(result[3]),
                html.P(result[4]),
                review_menu
                ], id="review-output", style={"widht": "100%"})
    except:
        pass
    return 

@app.callback(Output('open-review', 'children'),
                  [Input('review-output', 'children')])
def load_review(click):
    global REVIEW_ID
    if click:
        return store_review(REVIEW_ID)    
    
create_review = html.Div([review_form,create_menu, html.Div(id="callback-created-review")])
review = html.Div([html.Div(id="open-review"), html.Div(id="open-created-review")], id="review-output")


# Review callbacks
@app.callback([Output('callback-open-review', 'children')],
                  [Input('select-review-button', 'n_clicks'),
                   Input("reviews-table", "value")],
                  [State("reviews-table", "active_cell")])
def open_review(click, table, state):
    if state and click:
        idx = state["row_id"]
        
        global REVIEW_ID
        REVIEW_ID = idx
        
    return [None]


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



@app.callback(Output("callback-created-review", "children"),
              [Input("created-review-button", "n_clicks")],
              [State("review-title-row", "value"),
               State("authors-row", "value"),
               State("keywords-row", "value"),
               State("description-row", "value")])
def view_created_review(click, title, authors, keywords, description ):
    if(click):
        try:
            conn = sqlite3.connect("./database/reviews.db")
            
            cursor = conn.cursor()

            cursor.execute(f"""
            INSERT INTO reviews (name, authors, tags, description)
            VALUES ("{title}", "{authors}", "{keywords}", "{description}")
            """)
            
            conn.commit()
            
            cursor.execute(f"""
            SELECT * FROM reviews WHERE name = "{title}";               
            """)
            
            result = cursor.fetchone()
            global REVIEW_ID
            REVIEW_ID = result[0]
            return None
            
        except:
            pass
        
    return None

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
        research_menu_items,
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