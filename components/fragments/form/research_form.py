import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

search_string_input = dbc.FormGroup(
    [
        dbc.Label("Search String", html_for="search-string-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="search-string-row", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    row=True,
)

date_input = dbc.FormGroup(
    [
        dbc.Label("Date", html_for="date-row", width=2),
        dbc.Col(
            dcc.DatePickerRange(
                id="date-row",
                display_format="D/M/Y"
            ),
            width=10,
        ),
    ],
    row=True,
)


inclusion_input = dbc.FormGroup(
    [
        dbc.Label("Inclusion", html_for="inclusion-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text",
                id="inclusion-row",
                placeholder="Enter inclusion criteria",
            ),
            width=10,
        ),
    ],
    row=True,
)

exclusion_input = dbc.FormGroup(
    [
        dbc.Label("Exclusion", html_for="exclusion-row", width=2),
        dbc.Col(
            dbc.Textarea(
                id="exclusion-row",
                placeholder="Enter exclusion criteria",
            ),
            width=10,
        ),
    ],
    row=True,
)

databases_input = dbc.FormGroup(
    [
        dbc.Label("Databases", html_for="databases-row", width=2),
        dbc.Col(
            dbc.Checklist(
                id="databases-row",
                options=[
                    {"label": "ACM Library", "value": 1},
                    
                    {
                        "label": "Google Scholar", 
                        "value": 2,
                        "disabled": True,
                    },
                    
                    {
                        "label": "Elsevier",
                        "value": 3,
                        "disabled": True,
                    },
                ],
            ),
            width=10,
        ),
    ],
    row=True,
)


research_form = dbc.Form([search_string_input, date_input, inclusion_input, exclusion_input, databases_input], style={"width": "100%"})