
# Libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import igraph as ig
import chart_studio.plotly as py
import plotly.graph_objs as go

import dash_table
# Components
from components.graph_manager import getGraphData, get3DGraphData
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
data2 = getGraphData("Code_Summarization_SL", ["paper", "author"])
data = get3DGraphData("Code_Summarization_SL", ["paper", "author"])

N=len(data['nodes'])
L=len(data['links'])
Edges=[(data['links'][k]['source'], data['links'][k]['target']) for k in range(L)]

G=ig.Graph(Edges)

labels=[]
group=[]
for node in data['nodes']:
    labels.append(node['name'])
    group.append(node['group'])


layt=G.layout_auto( dim=3)


Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]
for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    
trace1=go.Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=dict(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=go.Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=dict(symbol='circle',
                             size=6,
                             color=group,
                             colorscale='Viridis',
                             line=dict(color='rgb(50,50,50)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = go.Layout(
         title="Network of coappearances of characters in Victor Hugo's novel<br> Les Miserables (3D visualization)",
         width=1000,
         height=1000,
         showlegend=False,
         scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
     margin=dict(
        t=100
    ),
    hovermode='closest',
    annotations=[
           dict(
           showarrow=False,
            text="Data source: <a href='http://bost.ocks.org/mike/miserables/miserables.json'>[1] miserables.json</a>",
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
            size=14
            )
            )
        ],    )

data=[trace1, trace2]
fig=go.Figure(data=data, layout=layout)

Graph = cyto.Cytoscape(
            id='cytoscape-two-nodes',
            style={'width': '100%', 'height': '80vh'},
            layout={"name": "klay", "animate":True},
            elements=data2,
            stylesheet=[
                {
                'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'text-halign':'center',
                        'text-valign':'center',
                        'width':'label',
                        'height':'label',
                        'shape':'square'
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
        )
# Home layout
home = html.Div([
    html.Div([
        #dcc.Graph(figure=fig, style={"width": "50%"}),
        Graph,
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
# change review table take out
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
