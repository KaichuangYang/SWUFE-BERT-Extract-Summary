from dash import html,dcc
import plotly.graph_objects as go
import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import os
import dill

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("swufe-bert-logo.jpg"),
                            className="logo",
                        ),
                        href="https://plotly.com/dash",
                    ),
                    html.A(
                        html.Button(
                            "Enterprise Demo",
                            id="learn-more-button",
                            style={"margin-left": "-10px"},
                        ),
                        href="https://plotly.com/get-demo/",
                    ),
                    html.A(
                        html.Button("Source Code", id="learn-more-button"),
                        href="https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-financial-report",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Extract Summary Finetune")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-summary-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Introduction",
                href="/dash-summary-report/introduction",
                className="tab first",
            ),
            dcc.Link(
                 "Question Description",
                 href="/dash-summary-report/question-description",
                 className="tab",
            ),
            dcc.Link(
                 "Lstm Model",
                 href="/dash-summary-report/lstm-model",
                 className="tab",
            ),
            dcc.Link(
                "Transformer Model",
                href="/dash-summary-report/transfomer-model",
                className='tab',  
            ),
            dcc.Link(
                 "Measures",
                 href="/dash-summary-report/measures",
                 className="tab",
            ),
            dcc.Link(
                 "Figures",
                 href="/dash-summary-report/plot-display",
                 className="tab",
            ),
            dcc.Link(
                "Extract Summary Dispaly",
                href="/dash-summary-report/summary-display",
                className="tab",
            ),
             dcc.Link(
                 "Question & Improvement",
                 href="/dash-summary-report/question-improvement",
                 className="tab",
            ),
            dcc.Link(
                 "Extract Your News",
                 href="/dash-summary-report/extract-summary",
                 className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

def get_text(text_file:str):
    text_path = "/home/yuxin.fan/extract_summary_finetune/dash-summary-report/text/"+text_file
    with open(text_path,'r',encoding='utf-8') as f:
        content = f.read()
    return content


def process_dil_file(data_path='/home/yuxin.fan/result'):
    filenames = os.listdir(data_path)
    filenames = [file for file in filenames if file[-3:]=="dil"]
    files = [dill.load(open(os.path.join(data_path,filenames[index]), 'rb')) for index in range(len(filenames))]
    Type = []
    Network =[]
    Bert = []
    Weighted = []
    Batch = []
    Value = []
    for index in range(len(filenames)):
        file_loss = files[index]['train_batch_metric']['train_batch_loss']
        file_auc_score = files[index]['train_batch_metric']['train_batch_auc_score']
        file_model = filenames[index].split('_')[1]
        file_bert = 'cn_bert' if filenames[index].split('_')[2]=='cn' else 'wwm_bert' if filenames[index].split('_')[2]=='wwm' else 'swufe_bert'
        file_weighted = True if filenames[index].split('_')[4]=='w' else False
        Type.extend(['loss']*len(file_loss))
        Type.extend(['auc_score']*len(file_auc_score))
        Network.extend([file_model]*(len(file_loss)+len(file_auc_score)))
        Bert.extend([file_bert]*(len(file_loss)+len(file_auc_score)))
        Weighted.extend([file_weighted]*(len(file_loss)+len(file_auc_score)))
        Value.extend(list(files[index]['train_batch_metric']['train_batch_loss']))
        Value.extend(list(files[index]['train_batch_metric']['train_batch_auc_score']))
        Batch.extend([i for i in range(len(file_loss))])
        Batch.extend([i for i in range(len(file_auc_score))])
    dataframe = pd.DataFrame({'Type':Type,
                              'Network':Network,
                              'Bert':Bert,
                              'Weighted':Weighted,
                              'Batch' : Batch,
                              'Value' : Value
                            })
    return dataframe

def get_data_network(dataset: pd.DataFrame, type: str, network: list, bert: str, weighted: bool):
    dataset = dataset[dataset['Type']==type]
    dataset = dataset[dataset['Bert']==bert]
    dataset = dataset[dataset['Weighted']==weighted]
    datasets={}
    if len(network) > 1:
        for net in network:
            df = dataset[dataset['Network']==net]
            datasets[net] = df
    else:
        datasets[network[0]] = dataset[dataset['Network']==network[0]]
    return datasets

def get_data_bert(dataset: pd.DataFrame, type: str, network: str, bert: list, weighted: bool):
    dataset = dataset[dataset['Type']==type]
    dataset = dataset[dataset['Network']==network]
    dataset = dataset[dataset['Weighted']==weighted]
    datasets={}
    if len(bert) > 1:
        for b in bert:
            df = dataset[dataset['Bert']==b]
            datasets[b] = df
    else:
        datasets[bert[0]] = dataset[dataset['Bert']==bert[0]]
    return datasets

def get_data_loss_weighted(dataset: pd.DataFrame, type: str, network: str, bert: str, weighted: list):
    dataset = dataset[dataset['Type']==type]
    dataset = dataset[dataset['Bert']==bert]
    dataset = dataset[dataset['Network']==network]
    datasets={}
    if len(weighted) > 1:
        for w in weighted:
            df = dataset[dataset['Weighted']==w]
            datasets[w] = df
    else:
        datasets[weighted[0]] = dataset[dataset['Weighted']==weighted[0]]
    return datasets

def data2fig(datasets:dict):
    colors={1:"#97151c",2:"#b5b5b5",3:"#EABA66"}
    fig = go.Figure()
    length = len(datasets)
    index=1
    for key_name,df in datasets.items():
        fig.add_trace(
            go.Scatter(
            name = key_name,
            x = df['Batch'],
            y = df['Value'],
            line={"color":colors[index]}))
        fig.layout = go.Layout(
                                                xaxis={
                                                    "autorange": True,
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                }
                                                
                                            )
        index = index+1
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    return fig

def bar_compare_loss(cn,wwm, swufe,option):
    colors={1:"#97151c",2:"#b5b5b5",3:"#EABA66"}
    index=1
    dic={'cn_bert':cn,'wwm_bert':wwm,'swufe_bert':swufe}
    fig = go.Figure()    
    for opt in option:
        fig.add_trace(
            go.Bar(
            name = opt,
            x = ['LSTM',"Transformer"],
            y = [np.mean(dic[opt]['lstm1']['Value'][-30:-1]),np.mean(dic[opt]['transformer1']['Value'][-30:-1])],
            marker={"color":[colors[index],colors[index]]},
            ))
        fig.layout = go.Layout(yaxis_range=[0.25,0.35])
        index= index+1 
    return fig

def bar_compare_auc(cn,wwm, swufe,option):
    colors={1:"#97151c",2:"#b5b5b5",3:"#EABA66"}
    index=1
    dic={'cn_bert':cn,'wwm_bert':wwm,'swufe_bert':swufe}
    fig = go.Figure()    
    for opt in option:
        fig.add_trace(
            go.Bar(
            name = opt,
            x = ['LSTM',"Transformer"],
            y = [np.mean(dic[opt]['lstm1']['Value'][-30:-1]),np.mean(dic[opt]['transformer1']['Value'][-30:-1])],
            marker={"color":[colors[index],colors[index]]},
            ))
        fig.layout = go.Layout(yaxis_range=[0.8,0.9])
        index= index+1 
    return fig