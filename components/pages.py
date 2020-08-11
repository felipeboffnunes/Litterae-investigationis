
# Libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_table

from components.graph_manager import getGraphData
from components.db_manager import review_df

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
            style={"margin-left": "2em", "width": "95%"})
        
    
    ],id="home-graph", style={"width": "100%", "height": "85vh"}),
    
    html.Div([
        html.P(id="cytoscape-tapNodeData-output")
    ], id="home-graph-content", style={"width": "0%"})
    
], className="row")



# Review data
review_table = review_df()

menu_items = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Create Review", id="create-review-button", n_clicks=0),
            id="ss", 
            width={"size": "3"}),
        dbc.Col(
            dbc.Button("Open Review", id="select-review-button", n_clicks=0), 
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

menu = dbc.Navbar(
    [
        menu_items,
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
    style={"position": "absolute", "bottom": 0, "width": "100%"},
    id="menu")

table_div = html.Div([
        dash_table.DataTable(
            id="reviews-table",
            #style_table={'overflowX': 'auto'},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
            data=review_table.to_dict("rows"),
            columns=[{"name": i, "id": i} for i in review_table.columns],
        ),
        menu
        ], id="table-div")


# Review layout
review = html.Div([
    html.Div([
        html.Div([
            html.Div([
                table_div
                ], id="table-div-content")
        ], id="reviews-table-div", style={"width": "100%"}),
    ], id="reviews-table-div2"),
    html.Div([html.P(id="review-content-output")], id="review-content",  style={"width": "0%"}),
    html.Div([html.P(id="review-create-output")], id="review-create",  style={"width": "0%"})
    
], className="row", style={"padding": "1em", "height": "83vh"})

pages = {"home": home,
         "review": review}
