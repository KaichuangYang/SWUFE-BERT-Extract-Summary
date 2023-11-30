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
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6([html.Strong("作者&小组成员 "),]),
                                            dbc.Row("杨开创"),
                                            dbc.Row("赵心研"),
                                            dbc.Row("王媛"),
                                            dbc.Row("樊宇鑫"),
                                        ],
                                        className="author",
                                    )
                                ],
                                className="three columns",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H4([html.Strong("项目简介 "),dbc.Badge("Introduction", pill=True, className="badge")]),
                                            html.P(get_text("p1_introduction.txt"),
                                                style={"color": "#ffffff"},
                                            ),
                                        ],
                                        className="intro",
                                    )                                    
                                ],
                                className="nine columns",
                            ),
                        ],
                        className="row"
                    ),    
                ],
                className="sub_page",
            ),
            
        ],
        className="page",
    )

