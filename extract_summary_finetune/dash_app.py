
from sqlite3 import Row
import time
from extract_summary_finetune.news_to_summary import NewsToSummary
import dash
from dash import html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# device = "cuda" if torch.cuda.is_available() else "cpu"
# print(f"Device: {device}")

# Load Model
# pretrained = "sshleifer/distilbart-xsum-12-6"
# model = BartForConditionalGeneration.from_pretrained(pretrained)
# tokenizer = BartTokenizer.from_pretrained(pretrained)

# Switch to cuda, eval mode, and FP16 for faster inference
# if device == "cuda":
#     model = model.half()
# model.to(device)
# model.eval()

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

radios_input = dbc.Card(
    [   
        dbc.CardImg(
            src="/assets/tech.png",
            top=False,
            style={"opacity": 0.1},
        ),
        dbc.CardImgOverlay(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col([
                                dbc.Row(
                                    [
                                        dbc.Label("BERT", html_for="example-radios-row", width=4),
                                        dbc.Col(
                                            dbc.RadioItems(
                                                id="which-bert",
                                                options=[
                                                    {"label": "CN bert", "value": "cn_bert"},
                                                    {"label": "WWM bert", "value": "wwm_bert"},
                                                    {"label": "SWUFE bert","value": "swufe_bert","disabled": True
                                                    },
                                                ],
                                            ),
                                            width=5,
                                        ),
                                    ],
                                    className="pretty_container"
                                    #style={'padding':5,'flex':1,},
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("NETWORK", html_for="example-radios-row", width=4),
                                        dbc.Col(
                                            dbc.RadioItems(
                                                id="which-network",
                                                options=[
                                                    {"label": "Transformer  ", "value": "transformer1"},
                                                    {"label": "LSTM ", "value": "lstm1"},
                                                ],
                                            ),
                                            width=5,
                                        ),
                                    ],
                                    className="pretty_container",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("LOSS", html_for="example-radios-row", width=4),
                                        dbc.Col(
                                            dbc.RadioItems(
                                                id="which-loss",
                                                options=[
                                                    {"label": "Unweighted ", "value": False},
                                                    {"label": "Weighted", "value": True},
                                                ],
                                            ),
                                            width=5,
                                        ),
                                    ],
                                    className="pretty_container",
                                ),
                            ],width = 8            
                            ),
                            dbc.Col(
                                [   
                                    dbc.Row(),
                                    dbc.Row(
                                        [
                                            dbc.Button("Summarize", id="button-run",size='lg', outline=True, color="primary"),
                                            html.Div(id="time-taken"),
                                        ],className="pretty_container",
                                    ),
                                    dbc.Row(),
                                ],style={'textAlign':'center'},align="center"
                            ),
                        ],
                )
                ],
            ),
        ),       

    ],     
    body=True,
    style={"height": "350px"},
)


# Define Layout
tab1_content = dbc.Container(
    fluid=True,
    children=[
        html.H1(["Extract summary",dbc.Badge("Have a try!", className="ms-2",color="primary")],style={"color":"white"}),
        dbc.Row(
            [
                dbc.Col(
                    width=4,
                    children=[
                        radios_input,
                        dbc.Card(
                            body=True,
                            children=[
                                dbc.Form(
                                    [
                                        html.H3(["Summarized Content",dbc.Badge("Your reslut!", className="ms-2",color="primary")]),
                                        dcc.Textarea(
                                            id="summarized-content",
                                            style={
                                                "width": "100%",
                                                "height": "calc(55vh - 350px)",
                                            },
                                        ),
                                    ]
                                )
                            ],
                        ),
                    ],
                ),
                dbc.Col(
                    width=5,
                    children=[
                        dbc.Card(
                            body=True,
                            children=[
                                dbc.Form(
                                    [
                                        html.H3(["Original news",dbc.Badge("Paste here!", className="ms-2",color="primary")]),
                                        dcc.Textarea(
                                            id="original-text",
                                            style={"width": "100%", "height": "55vh"},
                                        ),
                                    ]
                                )
                            ],
                        )
                    ],
                ),
            ]
        ),
    ],
)

tab2_content =  html.Div([
    html.Div(children=[
        html.Img(src='/assets/newnewlogo.png'),
        html.Br(),
        html.H1('NLP Model Training LAB',
        style={'fontsize':'3rem',
        'textAlign':'center',
        'color':'blue'})
    ]),
    html.Br(),
    html.Div([
        html.Div(children=[
            
            html.H2('Variable:Network'),
            html.Label('BERT'),
            dcc.Dropdown(
                id='which-bert1',
                options=[
                    {'label':'SWUFE bert','value':'swufe1'},
                    {'label':'WWM bert','value':'wwm1'},
                    {'label':'CN bert','value':'cn1'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('LOSS'),
            dcc.Dropdown(
                id='which-loss1',
                options=[
                    {'label':'Unweighted Loss','value':'bce1'},
                    {'label':'Weighted Loss','value':'w-bce1'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('NETWORK'),
            dcc.Checklist(
                id='which-network1',
                options=[
                    {'label':'LSTM','value':'lstm1'},
                    {'label':'Transformer','value':'transformer1'}
                ],
                className="dcc_control",
            )],className="pretty_container four columns"),
        html.Div(children=[
            html.H2('LOSS-Curve'),
            dcc.Graph(id='loss1'),
            ],style={'padding':10,'flex':1}),
        html.Div(children=[
            html.H2('AUC-Curve'),
            dcc.Graph(id='auc1'),
        ],style={'padding':10,'flex':1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Br(),
    html.Div([
        html.Div(children=[
            html.H2('Variable:LossFunction'),
            html.Label('BERT'),
            dcc.Dropdown(
                id='which-bert2',
                options=[
                    {'label':'SWUFE bert','value':'swufe2'},
                    {'label':'WWM bert','value':'wwm2'},
                    {'label':'CN bert','value':'cn2'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('LOSS'),
            dcc.Dropdown(
                id='which-network2',
                options=[
                    {'label':'LSTM','value':'lstm2'},
                    {'label':'Transformer','value':'transformer2'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('LOSS'),
            dcc.Checklist(
                id='which-loss2',
                options=[
                    {'label':'Unweighted Loss','value':'bce2'},
                    {'label':'Weighted Loss','value':'w-bce2'}
                ],
                className="dcc_control",
            )],className="pretty_container four columns"),
        html.Br(),
        html.Div(children=[
            html.H2('LOSS-Curve'),
            dcc.Graph(id='loss2'),
            ],style={'padding':10,'flex':1}),
        html.Div(children=[
            html.H2('AUC-Curve'),
            dcc.Graph(id='auc2'),
        ],style={'padding':10,'flex':1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Br(),
    html.Div([
        html.Div(children=[
            html.H2('Variable:Bert'),
            html.Label('LOSS'),
            dcc.Dropdown(
                id='which-loss3',
                options=[
                    {'label':'Unweighted Loss','value':'bce3'},
                    {'label':'Weighted Loss','value':'w-bce3'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('NETWORK'),
            dcc.Dropdown(
                id='which-network3',
                options=[
                    {'label':'LSTM','value':'lstm3'},
                    {'label':'Transformer','value':'transformer3'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('BERT'),
            dcc.Checklist(
                id='which-bert3',
                options=[
                    {'label':'SWUFE bert','value':'swufe3'},
                    {'label':'WWM bert','value':'wwm3'},
                    {'label':'CN bert','value':'cn3'}
                ],
                className="dcc_control",
            )],className="pretty_container four columns"),
        html.Div(children=[
            html.H2('LOSS-Curve'),
            dcc.Graph(id='loss3'),
            ],style={'padding':10,'flex':1}),    
        html.Div(children=[
            html.H2('AUC-Curve'),
            dcc.Graph(id='auc3'),
        ],style={'padding':10,'flex':1})
    ], style={'display': 'flex', 'flex-direction': 'row'})
], )

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Summary", tab_id="tab-1",label_style={"color": "#f9f9f9"},active_label_style={"color": "blue"}),
                dbc.Tab(label="NLP Model LAB", tab_id="tab-2",label_style={"color": "#f9f9f9"})
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)
app.layout = tabs

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return tab1_content
    elif at == "tab-2":
        return tab2_content
    return html.P("This shouldn't ever be displayed...")


@app.callback(
    [Output("summarized-content", "value"), Output("time-taken", "children")],
    [
        Input("button-run", "n_clicks"),
        Input("which-bert", "value"),
        Input("which-network", "value"),
        Input("which-loss", "value")
    ],
    [State("original-text", "value")],
)
def summarize(n_clicks, bert, network, loss, original_text):
    if original_text is None or original_text == "":
        return "", "Did not run"
    t0 = time.time()
    text = original_text
    loss = "w_BCEloss" if loss else "BCEloss"
    news_to_summary = NewsToSummary(network=network,bert=bert,loss=loss,
                  text=text)
    output = news_to_summary.summary_modified[0]
    t1 = time.time()
    time_taken = f"Summarized in {t1-t0:.2f}s"
    return output, time_taken




if __name__ == "__main__":
    #app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8060, debug=True)
