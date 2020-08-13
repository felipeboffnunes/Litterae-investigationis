@app.callback(Output('review-output', 'children'),
                  [Input('select-review-button', 'n_clicks'),
                   Input("reviews-table", "value")],
                  [State("reviews-table", "active_cell")])
def open_description(data, table, state):
    print("hey")
    if state and data:
        idx = state["row_id"]
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
    return html.P(id="review-output")
