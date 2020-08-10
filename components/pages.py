
# Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
# Components
from components import db_manager


# Home
#
# Home data
home_data = db_manager.home_graph()

home_elements = []
for data in home_data:
    # 0 = id, 1 = title, 2 = authors, 3 = doi, 4 = abstract, 5 = target
    element = {"data": {"id": data[3], "label": data[1]}}
    home_elements.append(element)
    
    if len(data) == 6:
        if data[5] != None:
            targets = data[5].split(",")
            for target in targets:
                element_target = {"data": {"source": data[3], "target": target}}
                home_elements.append(element_target)


home = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'cose'},
        style={'width': '100%', 'height': '400px'},
        elements=home_elements
    ),
    html.P(id="cytoscape-tapNodeData-output")
])



pages = {'home': home}
