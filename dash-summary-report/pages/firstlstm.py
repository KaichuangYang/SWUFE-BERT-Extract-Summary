import dash_html_components as html
from utils import Header
import pandas as pd

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [
                    # Row 1    
                    html.Div(
                        [
                            html.H6([html.Strong("LSTM的选择与搭建")],className="subtitle padded"),                             
                            html.Div(
                                [
                                    html.P(
                                        "RNN是用于处理序列数据的深度神经网络, 该神经网络会对前面的信息进行记忆并应用于当前输出的计算中。但RNN模型如果需要实现长期记忆则在每次计算时需与前n次计算相结合, 使计算量呈指数式增长, 因此RNN不适合进行长期记忆计算。"
                                    ),
                                    html.P(
                                        "LSTM是一种特殊的RNN, 主要是为了解决长序列训练过程中的梯度消失和梯度爆炸问题, 相比普通的RNN, LSTM能够在更长的序列中有更好的表现。"
                                    ),
                                ],
                                className="minipara",    
                            ),
                            html.Div(
                                [
                                    html.Img(
                                        src=app.get_asset_url("lstm.png"),  #gif static
                                        className="midimg",   # center photo
                                    ),
                                    html.Br([]), 
                                    html.Br([]), 
                                    html.Br([]), 
                                ],
                                className="twelve columns",
                            ), 
                            html.Div(
                                [
                                    html.Div(
                                        [                                        
                                            html.Div(
                                                [
                                                    html.H6([html.Strong("Forget Gate")],className="subtitle padded"),
                                                    html.P(
                                                        "输入的 hₜ₋₁, xₜ 连接起来后通过 σ 函数将每个元素映射到0到1之间，得到 fₜ ，与输入的 Cₜ₋₁ 相乘，当 fₜ 的某一位的值为 0 时，\
                                                            Cₜ₋₁ 中对应位置的数据也为零，对应的信息即被遗忘。",className="minipara" 
                                                        )
                                                ],
                                                className="four columns ",                                                        
                                            ), 
                                            html.Img(
                                                src=app.get_asset_url("lstm1.png"), 
                                                className="lstm-png ",
                                            ),
                                        ],    
                                        className="row",   
                                    ),                                    
                                ],
                            ),
                            html.Div(        
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H6([html.Strong("Input Gate")],className="subtitle padded"),
                                                    html.P(
                                                        "与遗忘门类似，σ 函数决定我们要保留和更新哪些信息，得到输入门的输出，tan 层创建新的候选值向量。",className="minipara" 
                                                        )
                                                ],
                                                className="four columns ",                                                        
                                            ), 
                                            html.Img(
                                                src=app.get_asset_url("lstm2.png"), 
                                                className="lstm-png ",
                                            ),
                                        ],   
                                        className="row",                                     
                                    ),                                    
                                ],
                            ), 
                            html.Div(        
                                [   
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H6([html.Strong("New Cell State")],className="subtitle padded"),
                                                    html.P(
                                                        "细胞旧状态 Cₜ₋₁ 与遗忘门中得到的 fₜ 相乘，再与输入门中的两个计算结果的乘积相加，得到更新后的细胞状态。",className="minipara" 
                                                        )
                                                ],
                                                className="four columns ",                                                        
                                            ), 
                                            html.Img(
                                                src=app.get_asset_url("lstm3.png"), 
                                                className="lstm-png ",
                                            ),
                                        ],        
                                        className="row",  
                                    ),                                    
                                ],
                            ), 
                            html.Div(        
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.H6([html.Strong("Output Gate")],className="subtitle padded"),
                                                    html.P(
                                                        "通过sigmoid层得输出门的输出，再与经tan处理后的新的细胞状态 Cₜ 相乘，得到输出的新的隐藏细胞状态 hₜ 。",className="minipara" 
                                                        )
                                                ],
                                                className="four columns ",                                                        
                                            ), 
                                            html.Img(
                                                src=app.get_asset_url("lstm4.png"), 
                                                className="lstm-png ",
                                            ),  
                                        ],
                                        className="row ",  
                                    ),                                             
                                ],                  
                            ),                            
                        ],                       
                    ),    
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
