# -*- coding: utf-8 -*-
import os
# Libraries
import pandas as pd
import sqlite3
import time

from flask_caching import Cache
import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Components
from components.pages import pages, table_div
from components.graph_manager import getGraphData
from components.acm_scraper.call_processes import call_processes
from components.csv_manager import get_search_df
# Fragments
from components.fragments.form.create_review_form import review_form

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
WAIT_SEARCH = False
GET_SEARCH = False
START_LOADING = False
END_LOADING = False


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
    elif pathname in ["/page-5"]:
        return pages["research"]
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
                ], id="review-content", style={"widht": "100%"})
    except:
        pass
    return 

@app.callback(Output('open-review', 'children'),
                  [Input('review-output', 'children')])
def load_review(click):
    global REVIEW_ID
    if click:
        return store_review(REVIEW_ID)    

@app.callback(Output('start-loading', 'children'),
                  [Input('review-output', 'children')])
def start_loader(click):
    global WAIT_SEARCH
    global GET_SEARCH
    global START_LOADING
    global END_LOADING
    if click and START_LOADING:
        while not WAIT_SEARCH and not GET_SEARCH and not END_LOADING:
            time.sleep(20)
        
        spinner = dbc.Spinner()
        return spinner
    return None
    
@app.callback(Output('end-loading', 'children'),
                  [Input('review-output', 'children')])
def end_loader(click):
    global WAIT_SEARCH
    global GET_SEARCH
    time.sleep(5)
    if click:
        if GET_SEARCH:
            return html.Div(id="start-loading")
        while WAIT_SEARCH:
            time.sleep(5)
    return html.Div(id="start-loading")

# Review callbacks
@app.callback([Output('callback-open-review', 'children')],
                  [Input('select-review-button', 'n_clicks'),
                   Input("reviews-table", "value")],
                  [State("reviews-table", "active_cell")])
def open_review(click, table, state):
    if click:  
        if state == None:
            idx = 1
        else:
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

def get_name_by_id():
    global REVIEW_ID
    conn = sqlite3.connect("./database/reviews.db")
            
    cursor = conn.cursor()
        
    cursor.execute(f"""
    SELECT name FROM reviews WHERE id = "{REVIEW_ID}";               
    """)

    result = cursor.fetchone()
    return result[0]

def get_csv_name(name):
    name = name.replace(" ", "_")
    if len(name) > 20:
        i = name.rfind(" ", 0, 20)
        name = name[:i]
    return name

@app.callback([Output("results-search", "children")],
              [Input("callback-wait-search", "children")])
def get_search(click):
    global WAIT_SEARCH
    global GET_SEARCH
    global REVIEW_ID
    if WAIT_SEARCH:
        while not GET_SEARCH:
            time.sleep(5)
        if GET_SEARCH:
            WAIT_SEARCH = False
            END_LOADING = True
            name = get_name_by_id()
            name = get_csv_name(name)
            
            search_data = get_search_df(name)
            search_table = dash_table.DataTable(
                id="search-table",
                #style_table={'overflowX': 'auto'},
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                data=search_data.to_dict("rows"),
                columns=[{"name": i, "id": i, "editable": False if i == "id" else True} for i in search_data.columns]
            )
            
            return [search_table]
    return [None]    
        

@app.callback([Output("callback-search", "children")],
              [Input("search-button", "n_clicks")],
              [State("search-string-row", "value")])
def search(click, url):
    if click:
        name = get_name_by_id()
        name = get_csv_name(name)
            
        global GET_SEARCH
        global WAIT_SEARCH
        global START_LOADING
        START_LOADING = True
        WAIT_SEARCH = True
        GET_SEARCH = call_processes(url, name) 
        START_LOADING = False
        
    return None