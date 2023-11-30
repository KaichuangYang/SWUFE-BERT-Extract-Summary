import dash_html_components as html
from utils import Header, make_dash_table
import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_para_select = pd.read_csv(DATA_PATH.joinpath("df_para_select.csv"))
df_para_compare = pd.read_csv(DATA_PATH.joinpath("df_para_compare.csv"))

def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 6
            html.Div(
                [                    
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6([html.Strong("评价指标选择")],className="subtitle padded"),
                                ],
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "BECLoss函数: 常用来处理二分类问题的损失函数。",className="minipara" 
                                    ),
                                    html.P(
                                        "AUC-ROC: 在对不同模型进行比较时，若不同模型的ROC曲线发生交叉，则很难比较哪个效果更好，此时比较更为合理，即AUC的大小。\
                                            ROC曲线是基于混淆矩阵得出的，曲线越靠近左上角，模型的准确性越高。",className="minipara" 
                                    ),
                                ],                                
                            ),
                            html.Br([]),
                            html.Div(
                                [                                
                                    html.H6([html.Strong("参数选择与指标对比")],className="subtitle padded"),
                                ],
                            ),
                            html.Div(
                                [
                                    html.Table(
                                        make_dash_table(df_para_select)
                                    ),                                        
                                    html.P(
                                        "Hidden_size较大 (大于等于input_size的一倍) 及layers较大 (大于等于2层) 时模型训练速度太慢，\
                                            数值较小时训练结果不理想。因此，我们结合运行时间和训练结果筛选出以下两组较优参数组。",className="minipara" 
                                    ), 
                                    html.Br([]),
                                    html.Table(
                                        make_dash_table(df_para_compare),
                                    )
                                ],
                                className="twelve columns",
                            ),                         
                        ],
                        className="row",
                    ),                    
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
