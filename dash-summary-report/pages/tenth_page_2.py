from turtle import Turtle, width
from webbrowser import BackgroundBrowser
from dash import dcc,html,callback
import dash_bootstrap_components as dbc
from utils import Header, make_dash_table, get_text
from news_to_summary import NewsToSummary
from dash.dependencies import Input, Output,State

radios_input = dbc.Card(
    [   
        # dbc.CardImg(
        #     src="/assets/tech.png",
        #     top=True,
        #     style={"opacity": 0.1,"width":"100%"}
                                                    
        # ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [   
                    html.Div([html.H6([html.Strong("自动抽取摘要APP")],className="subtitle padded")]),
                    html.Div(
                        [
                            dbc.Col(
                                [
                                dbc.Row(
                                        [
                                            dbc.Label("BERT", html_for="example-radios-row", width=4,style={"color":"#ffffff"},),
                                            dbc.Col(
                                                [
                                                    dcc.Dropdown(
                                                        id="which-bert",
                                                        options=[
                                                            {"label": "CN bert", "value": "cn_bert"},
                                                            {"label": "WWM bert", "value": "wwm_bert"},
                                                            {"label": "SWUFE bert","value": "swufe_bert","disabled": True
                                                            },
                                                        ],
                                                        multi=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                        className="pretty_red_container",
                                        style={'textAlign':'center'},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Label("NETWORK", html_for="example-radios-row", width=4,style={"color":"#ffffff"}),
                                            dbc.Col(
                                                [
                                                    dcc.Dropdown(
                                                        id="which-network",
                                                        options=[
                                                            {"label": "Transformer  ", "value": "transformer1"},
                                                            {"label": "LSTM ", "value": "lstm1"},
                                                        ],
                                                        multi=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                        className="pretty_red_container",
                                        style={'textAlign':'center'},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Label("LOSS", html_for="example-radios-row", width=4,style={"color":"#ffffff"},),
                                            dbc.Col(
                                                [
                                                    dcc.Dropdown(
                                                        id="which-loss",
                                                        options=[
                                                            {"label": "Unweighted ", "value": False},
                                                            {"label": "Weighted", "value": True},
                                                        ],
                                                        multi=True,
                                                    ),
                                                ],
                                            ),
                                        ],
                                        className="pretty_red_container",
                                        style={'textAlign':'center'},
                                    ),
                                ],
                                style={"height":"8em"}, 
                                className="eight columns",      
                            ),
                            dbc.Col(
                                [   
                                    dbc.Row(),
                                    dbc.Row(
                                        [
                                            dbc.Button("Summarize", id="button-run",size='lg', outline=True, className="badge"),
                                        ],
                                        className="pretty_red_container",
                                        style={"top":"8.5em"}
                                    ),
                                    dbc.Row(),
                                ],
                                style={'textAlign':'center',"height":"8em"},
                                align = True,
                                className="four columns",
                            ),
                        ],
                        style={"width":"85%","margin": "auto"},
                    ),
                ],
                #style={"width":"50%","margin": "auto"},
                #className="red-author",
            ),
        ),       
    ],     
    body=True,
    style={"height": "100px"},
)


texts_input = html.Div(
    [
        dbc.Col(
            children=[
            dbc.Card(
                    body=True,
                    children=[
                        html.H6([html.Strong("新闻短讯"),dbc.Badge("Input your original news!", className="badge")]),
                        dcc.Textarea(
                            children=[],
                            id="original-text",
                            style={"width": "85%", "height": "200px","border-style":"inset","background":"lightgrey"},
                        ),
                    ],
                    style={'textAlign':'center',"margin": "auto"},
                ),
            ],
            className="pretty_container",
            style={"top":"20.5em"}
        ),    
    ],  
    style={"width": "auto"} 
)


accordion = html.Div(
    dbc.Accordion(
        id = "summary-accordion",
        className="accordion",
        always_open=True
    )
)

texts_output = html.Div(
    [
        dbc.Col(
            children=[
            dbc.Card(
                    body=True,
                    children=[
                        html.H6([html.Strong("新闻自动摘要"),dbc.Badge("Summary", className="badge")],style={'textAlign':'center'},),
                        accordion,
                    ],
                ),
            ],
            className="pretty_container",
            style={"top":"24em"}
        ), 
        html.Div([],className="sub_page")   
    ], 
    style={"margin": "auto"}, 
)

def create_layout(app):
    return html.Div(
                         children=[
                            html.Div(
                                [
                                    Header(app)
                                ]
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            radios_input, 
                                            texts_input, 
                                            texts_output,
                                        ],
                                        className="sub_page",
                                    ),
                                ],
                                style={"border-style":"outset","border-width": "0.35em","border-color":"lightgrey"}
                            ),
                        ],
                        className="page",
                    )


     