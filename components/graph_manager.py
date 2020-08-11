# Components
from components import db_manager

def getGraphData(values):
    home_data = db_manager.home_graph()
    home_elements = []
    for data in home_data:
        # 0 = id, 1 = title, 2 = authors, 3 = doi, 4 = abstract, 5 = target
        # Add paper nodes
        if "paper" in values:
            paper_id = f"paper:{data[3]}"
            element = {"data": {"id": paper_id, "label": data[1]}}
            home_elements.append(element)
            
            # Add paper paper edges
            if len(data) == 6:
                if data[5] != None:
                    targets = data[5].split(",")
                    for target in targets:
                        target_id = f"paper:{target}"
                        element_target = {"data": {"source": paper_id, "target": target_id}}
                        home_elements.append(element_target)
                    
        if "author" in values:
            authors = data[2].split(",")
            for author in authors:
                # Add author nodes
                aux_author = author.replace(" ", "_")
                author_id = f"author:{aux_author}"
                element = {"data": {"id": author_id, "label": author}}
                home_elements.append(element)
                # Add author paper edges
                if "paper" in values:
                    element = {"data": {"source": author_id, "target": paper_id}}
                    home_elements.append(element)
                
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
                            home_elements.append(element)
                            
    return home_elements
        