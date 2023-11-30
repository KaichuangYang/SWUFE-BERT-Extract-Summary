from pydoc import classname
from turtle import position
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from utils import Header, make_dash_table, get_text, process_dil_file,bar_compare_auc,bar_compare_loss
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "10em",
    "left": "10em",
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "1em",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
LINK_STYLE = {
    "background-color": "#98151b",
    "font-size":"14.5px",
    "float":"left",
    "width":"85%",
    "color":"white",
    "textAlign":"center",
    "border-width":"2px",
    "boder-color":"#f0e8e8",
}
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
sidebar = html.Div(
    [
        html.Div(
            [
                html.H6(html.Strong("Comparison"),className="subtitle padded"),
            ],
            className="row"
        ),
        dbc.Nav(
            [   
                dbc.NavLink("Bar Charts", href="/dash-summary-report/plot-display/page-4", active="exact",style=LINK_STYLE),            
                dbc.NavLink("Network", href="/dash-summary-report/plot-display/page-1", active="exact",style=LINK_STYLE),
                dbc.NavLink("LossFunction", href="/dash-summary-report/plot-display/page-2", active="exact",style=LINK_STYLE),
                dbc.NavLink("Bert", href="/dash-summary-report/plot-display/page-3", active="exact",style=LINK_STYLE),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="grey-author",
    style={"height":"162vh"}
)


content = html.Div(id="plot-page-content", style=CONTENT_STYLE)


def create_layout(app):
        return html.Div(
            [
                html.Div([Header(app)]),
                html.Div(
                    [
                        dcc.Location(id="plot-url"), 
                        html.Div([sidebar],style={"width":"25%","float":"left"}),
                        html.Div([content],style={"width":"75%","float":"left"}),
                    ],
                    className="page",
                ),
            ],
            className="page",
        )

def create_full_view_layout(app):
    return html.Div(
            [
                html.Div(
                    [
                        dcc.Location(id="full-view-url"),
                        html.Div(   
                                    [
                                        html.Div([Header(app)]),
                                        html.Div(id="p1",style={"padding": "2rem 1rem"})
                                    ],
                                    className="page"
                                ),    
                        html.Div(id="p2",className="page",style={"padding": "2rem 8rem"}),
                        html.Div(id="p3",className="page",style={"padding": "2rem 8rem"}),
                        html.Div(id="p4",className="page",style={"padding": "2rem 8rem"}),
                        html.Div(id="p5",className="page",style={"padding": "2rem 8rem"}),
                    ],
                ),
            ],
        )
            


graph_loss_n = html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(
                                        "Loss", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-loss-n",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
graph_auc_n = html.Div(                        [
                            html.Div(
                                [                                    
                                    html.Strong(
                                        "AUC", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-auc-n",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
graph_loss_l = html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(
                                        "Loss", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-loss-l",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
graph_auc_l = html.Div(                        [
                            html.Div(
                                [                                    
                                    html.Strong(
                                        "AUC", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-auc-l",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
graph_loss_b = html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(
                                        "Loss", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-loss-b",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
graph_auc_b = html.Div(                        [
                            html.Div(
                                [                                    
                                    html.Strong(
                                        "AUC", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph-auc-b",
                                        config={"displayModeBar": False},
                                        style={"height":"350px"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )

def return_plot_homepage():
    return html.Div(
        [
            html.H6(html.Strong("Visualization"),className="subtitle padded"),
            html.Hr(),
            html.Div(
                [
                    html.Div([get_text("p_plot_home.txt")]),
                    html.P(["       1.不同Bert预训练情景CN/WWM/SWUFE"]),
                    html.P(["       2.不同Network训练情景Transformer/LSTM"]),
                    html.P(["       3.不同Loss Function情景 等权重(未加权)BCEloss/ 加权BCEloss"]),
                ],
                className="intro"
            )
        ],
        className="p-3 bg-light rounded-3",
    )

def return_network_compare():
    return html.Div(
        [
            html.Div(
                [
                    html.H6(html.Strong('Variable:Network'),className="subtitle padded"),
                    html.Span([html.Label('BERT'),
                    dcc.Dropdown(
                        id='which-bert-n',
                        options=[
                            {'label':'SWUFE bert','value':'swufe_bert'},
                            {'label':'WWM bert','value':'wwm_bert'},
                            {'label':'CN bert','value':'cn_bert'}
                        ],
                        className="dcc_control",
                    ),
                    html.Br(),
                    html.Label('LOSS'),
                    dcc.Dropdown(
                        id='which-loss-n',
                        options=[
                            {'label':'Unweighted Loss','value':False},
                            {'label':'Weighted Loss','value':True}
                        ],
                        className="dcc_control",
                    )]),
                    html.Br(),
                    html.Span([html.Label('NETWORK'),
                    dcc.Checklist(
                        id='which-network-n',
                        options=[
                            {'label':'LSTM','value':'lstm1'},
                            {'label':'Transformer','value':'transformer1'}
                        ],
                        className="dcc_control",
                    )]),
                ],
            ),
            graph_loss_n,
            graph_auc_n,
        ],
    )
    
def return_loss_function_compare():
    return html.Div(
        [
            html.H6(html.Strong('Variable:LossFunction'),className="subtitle padded"),
            html.Label('BERT'),
            dcc.Dropdown(
                id='which-bert-l',
                options=[
                    {'label':'SWUFE bert','value':'swufe_bert'},
                    {'label':'WWM bert','value':'wwm_bert'},
                    {'label':'CN bert','value':'cn_bert'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('LOSS'),
            dcc.Dropdown(
                id='which-network-l',
                options=[
                    {'label':'LSTM','value':'lstm1'},
                    {'label':'Transformer','value':'transformer1'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('LOSS'),
            dcc.Checklist(
                id='which-loss-l',
                options=[
                    {'label':'Unweighted Loss','value':False},
                    {'label':'Weighted Loss','value':True}
                ],
                className="dcc_control",
            ),html.Br(),graph_loss_l,graph_auc_l]
    )
def return_bert_compare():
    return html.Div(
        [
            html.H6(html.Strong('Variable:Bert'),className="subtitle padded"),
            html.Label('LOSS'),
            dcc.Dropdown(
                id='which-loss-b',
                options=[
                    {'label':'Unweighted Loss','value':False},
                    {'label':'Weighted Loss','value':True}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('NETWORK'),
            dcc.Dropdown(
                id='which-network-b',
                options=[
                    {'label':'LSTM','value':'lstm1'},
                    {'label':'Transformer','value':'transformer1'}
                ],
                className="dcc_control",
            ),
            html.Br(),
            html.Label('BERT'),
            dcc.Checklist(
                id='which-bert-b',
                options=[
                    {'label':'SWUFE bert','value':'swufe_bert'},
                    {'label':'WWM bert','value':'wwm_bert'},
                    {'label':'CN bert','value':'cn_bert'}
                ],
                className="dcc_control",
            ),graph_loss_b,graph_auc_b]
    )

def return_compare():
    checklist = dcc.Checklist(
                id='which-bert-bar',
                options=[
                    {'label':'SWUFE bert','value':'swufe_bert'},
                    {'label':'WWM bert','value':'wwm_bert'},
                    {'label':'CN bert','value':'cn_bert'}
                ],
                className="dcc_control",
            )
    graph_compare_loss = html.Div(
                        [   
                            html.Div(
                                [
                                    html.Strong(
                                        "Loss", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph_compare_loss",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )
    graph_compare_auc = html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(
                                        "auc_score", className="subtitle padded"),
                                    dcc.Graph(
                                        id="graph_compare_auc",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    )

    return html.Div(
    [
        
        # page 2
        html.Div(
            [
                html.H6(html.Strong("Bar Charts"),className="subtitle padded"),
                html.Div([html.Span([checklist],style={"width":"10px"}),
                html.Span(children= [graph_compare_loss,graph_compare_auc])],className="row"),          
                    
            ],
            
        )
    ],
  
)