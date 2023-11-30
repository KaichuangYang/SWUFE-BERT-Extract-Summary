from dash import dcc,html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from utils import Header, make_dash_table, get_text
import dash



def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
 
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([html.Strong("问题")],className="subtitle padded"),
                                    html.Div(
                                        [
                                            html.P(get_text("p9_q1.txt"),className="red-author"),  
                                            html.P(get_text("p9_q2.txt"),className="author"),     
                                        ]
                                    )
                                ],
                            )
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([html.Strong("改进")],className="subtitle padded"),
                                    html.Div(
                                        [
                                            html.P(get_text("p9_s1.txt"),className="red-author"),  
                                            html.P(get_text("p9_s2.txt"),className="author"),     
                                        ]
                                    )
                                ],
                            )
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
