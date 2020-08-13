import pandas as pd
import numpy as np
# Components
from components import db_manager
from components.csv_manager import get_search_df

  
def parse_search_df(search):
    data = search.filter(["Title", "Authors", "DOI", "Abstract"], axis=1)
    
    data["id"] = data.index
    data["target"] = None
    data = data[["id", "Title", "Authors", "DOI", "Abstract", "target"]]
    data.columns=["id", "title", "authors", "doi", "abstract", "target"]
    return data
    
def get_home_graph():
    home_data = db_manager.home_graph()
    elements = getGraphData(home_data, ["paper", "author"])
    return elements



def getGraphData(name, values):
    
    df = get_search_df(name)
    df = parse_search_df(df)
    df = df.values.tolist()
    
    elements = []
    for data in df:
        # 0 = id, 1 = title, 2 = authors, 3 = doi, 4 = abstract, 5 = target
        # Add paper nodes
        if "paper" in values:
            paper_id = f"paper:{data[3]}"
            element = {"data": {"id": paper_id, "label": data[1]}}
            elements.append(element)
            
            # Add paper paper edges
            if len(data) == 6:
                if data[5] != None:
                    if data[5] != "r":
                        targets = data[5].split(",")
                        for target in targets:
                            target_id = f"paper:{target}"
                            element_target = {"data": {"source": paper_id, "target": target_id}}
                            elements.append(element_target)
                    
        if "author" in values:
            if isinstance(data[2], str):
                authors = data[2].split(",")
                for author in authors:
                    # Add author nodes
                    aux_author = author.replace(" ", "_")
                    author_id = f"author:{aux_author}"
                    element = {"data": {"id": author_id, "label": author}}
                    elements.append(element)
                    # Add author paper edges
                    if "paper" in values:
                        element = {"data": {"source": author_id, "target": paper_id}}
                        elements.append(element)
                
            # Add author author edges
            if len(authors) > 1:
                for author in authors:
                    aux_author = author.replace(" ", "_")
                    author_id = f"author:{aux_author}"
                    for target_author in authors:
                        aux_target_author = target_author.replace(" ", "_")
                        target_author_id = f"author:{aux_target_author}"
                        if author_id != target_author_id: 
                            element = {"data": {"source": author_id, "target": target_author_id, 
                                                "source-arrow-shape": "vee"}}
                            elements.append(element)
                            
    return elements
        
def get3DGraphData(name, values):
    
    df = get_search_df(name)
    df = parse_search_df(df)
    df = df.values.tolist()
    
    nodes = []
    links = []
    author_min_id = len(df)
    for i, data in enumerate(df):
        # 0 = id, 1 = title, 2 = authors, 3 = doi, 4 = abstract, 5 = target
        # Add paper nodes
        
        if "paper" in values:
            paper_id = data[1]
            element = {"name": paper_id, "group": 1}
            nodes.append(element)
            
            # Add paper paper edges
            if len(data) == 6:
                if data[5] != None:
                    if data[5] != "r":
                        targets = data[5].split(",")
                        for target in targets:
                            for z, data in enumerate(df):
                                if data[3] == target:
                                    target_id = z
                                    break
                            element_target = {"source": i, "target": target_id, "value":5}
                            links.append(element_target)
                    
        if "author" in values:
            if isinstance(data[2], str):
                authors = data[2].split(",")
                for z, author in enumerate(authors):
                    # Add author nodes
                    aux_author = author.replace(" ", "_")
                    author_id = author_min_id + z + 1
                    
                    element = {"name": author, "group": 2}
                    nodes.append(element)
                    # Add author paper edges
                    if "paper" in values:
                        element = {"source": author_id, "target": i, "value": 3}
                        links.append(element)
                
                
            # Add author author edges
            if len(authors) > 1:
                for y, author in enumerate(authors):
                    aux_author = author.replace(" ", "_")
                    author_id = author_min_id + y + 1
                    for z, target_author in enumerate(authors):
                        target_author_id = author_min_id + z + 1
                        if author_id != target_author_id: 
                            element = {"source": author_id, "target": target_author_id, "value": 1}
                            links.append(element)
                author_min_id += len(authors)
            elif len(authors) == 1:
                author_min_id +=1
                            
    return {"nodes": nodes, "links": links}