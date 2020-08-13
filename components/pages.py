
# Libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_table
# Components
from components.graph_manager import getGraphData
from components.db_manager import review_df


# Fragments
from components.fragments.form.create_review_form import review_form
from components.fragments.form.research_form import research_form
from components.fragments.menu.research_menu import research_menu
from components.fragments.menu.create_review_menu import create_menu
from components.fragments.menu.reviews_menu import reviews_menu
# Home
#
# Home data
home_elements = getGraphData(["paper", "author"])
# Home layout
home = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='cytoscape-two-nodes',
            style={'width': '100%', 'height': '80vh'},
            layout={"name": "circle","roots": "[id = 'a9as83019312303']", "animate": True},
            elements=home_elements,
            stylesheet=[
                {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }},
                
                {"selector": "edge",
                "style": {
                    'source-arrow-shape': 'triangle'
                    
                }},
                
                {"selector": "target",
                "style": {
                    "curve-style" : "straight",       
                }},
                
                {"selector": "[id *= 'author:']",
                "style": {
                    "shape": "rectangle",
                    "color": "blue"
                }},      
                
            ]
        ),
        
        dcc.Dropdown(id="dropdown-graph-filter", options=[
            {"label": "Papers", "value": "paper"},
            {"label": "Authors", "value": "author"}
            ], multi = True, value=["paper", "author"], 
            style={"margin-left": "2em", "margin-bottom":"6em", "width": "95%"})
        
    
    ],id="home-graph", style={"width": "100%", "height": "85vh"}),
    
    html.Div([
        html.P(id="cytoscape-tapNodeData-output")
    ], id="home-graph-content", style={"width": "0%"})
    
], className="row")



# Review data
review_table = review_df()

table_div = html.Div([
        dash_table.DataTable(
            id="reviews-table",
            #style_table={'overflowX': 'auto'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            data=review_table.to_dict("rows"),
            columns=[{"name": i, "id": i, "editable": False if i == "id" else True} for i in review_table.columns] ,
            editable=True,
            row_deletable=True
        ),
        reviews_menu
        ], id="reviews-table-div")


# Review layout
reviews = html.Div([
            table_div,
            html.Div(id="callback-open-review")      
        ], id="reviews-div", className="row", style={"padding": "1em", "height": "90vh"})


create_review = html.Div([
                    review_form,
                    create_menu, 
                    html.Div(id="callback-created-review")
                ])

review = html.Div([
            html.Div(id="open-review"), 
            html.Div(id="open-created-review"),
            html.Div([
                html.Div(id="start-loading"),
            ],id="end-loading"),
            html.Div(id="results-search"), 
            html.Div(id="callback-wait-search")
        ], id="review-output")

research = html.Div([
                html.Div([
                    research_form, 
                    research_menu
                ], id="research"), 
                html.Div(id="callback-search")
            ])

pages = {"home": home,
         "reviews": reviews,
         "create-review": create_review,
         "review": review,
         "research": research}
