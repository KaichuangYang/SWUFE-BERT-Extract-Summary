from dash import dcc,html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from utils import Header, make_dash_table, get_text
from news_to_summary import NewsToSummary
import dash

color_dict ={1:"#97151c",2:"#b5b5b5",3:"#EABA66"}
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
                                    html.H6([html.Strong("抽取摘要")],className="subtitle padded"),
                                    html.P(get_text("p8_p1.txt"),className="para"),
                                    html.H6([html.Strong("新闻示例")],className="subtitle padded"),
                                    html.Br([]),
                                    html.Br([]),
                                    html.P(get_text("p8_ex_news1.txt"),style={"border-style":"outset"},className="minipara",),
                                    html.Br([]),
                                    html.Br([]),
                                    html.H6([html.Strong("摘要结果")],className="subtitle padded"),
                                    html.Br([]),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            dbc.Alert(get_text("p8_summary1_l_c.txt"),color=color_dict[2],style={"color":"white"}),
                                            dbc.Alert(get_text("p8_summary1_l_w.txt"),color=color_dict[3],style={"color":"white"}),
                                            dbc.Alert(get_text("p8_summary1_l_s.txt"),color=color_dict[1],style={"color":"white"}),
                                            dbc.Alert(get_text("p8_summary1_t_c.txt"),color=color_dict[2],style={"color":"white"}),
                                            dbc.Alert(get_text("p8_summary1_t_w.txt"),color=color_dict[3],style={"color":"white"}),
                                            dbc.Alert(get_text("p8_summary1_t_s.txt"),color=color_dict[1],style={"color":"white"}),
                                        ],
                                        className="minipara",
                                        style={"font-weight":"bold"}
                                    )                                        
                                ],
                            ),
                        ],
                        className="sub_page",
                    ), 
                    # html.Div(
                    #     [
                    #         html.Div(
                    #             [
                    #                 html.P(get_text("p8_ex_news2.txt")),
                    #                 html.Div(
                    #                     [
                    #                         dbc.Alert(get_text("p8_summary2_l_c.txt"),color="#ffeaea"),
                    #                         dbc.Alert(get_text("p8_summary2_l_w.txt"),color="info"),
                    #                         dbc.Alert(get_text("p8_summary2_l_s.txt"),color="primary"),
                    #                         dbc.Alert(get_text("p8_summary2_t_c.txt"),color="secondary"),
                    #                         dbc.Alert(get_text("p8_summary2_t_w.txt"),color="info"),
                    #                         dbc.Alert(get_text("p8_summary2_t_s.txt"),color="primary"),
                    #                     ]
                    #                 )                                        
                    #             ],
                    #             className="para",
                    #         ),
                    #     ],
                    #     className="sub_page",
                    # ),                        
                ],
                
            ),
            
        ],
        className="page",
    )
