import dash_bootstrap_components as dbc
import dash_core_components as dcc

title_input = dbc.FormGroup(
    [
        dbc.Label("Title", html_for="review-title-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="review-title-row", placeholder="Enter title"
            ),
            width=10,
        ),
    ],
    row=True,
)

authors_input = dbc.FormGroup(
    [
        dbc.Label("Authors", html_for="authors-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text",
                id="authors-row",
                placeholder="Enter authors",
            ),
            width=10,
        ),
    ],
    row=True,
)

keywords_input = dbc.FormGroup(
    [
        dbc.Label("Keywords", html_for="keywords-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text",
                id="keywords-row",
                placeholder="Enter keywords",
            ),
            width=10,
        ),
    ],
    row=True,
)

description_input = dbc.FormGroup(
    [
        dbc.Label("Description", html_for="description-row", width=2),
        dbc.Col(
            dbc.Textarea(
                id="description-row",
                placeholder="Enter description",
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
            dbc.RadioItems(
                id="databases-row",
                options=[
                    {"label": "ACM Library", "value": 1},
                    {"label": "Google Scholar", "value": 2},
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

review_form = dbc.Form([title_input, authors_input, keywords_input, description_input, databases_input])