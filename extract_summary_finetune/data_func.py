import plotly.graph_objects as go
import pandas as pd
from dash import dcc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import os
import dill

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
    fig = go.Figure()
    for key_name,df in datasets.items():
        fig.add_trace(
            go.Scatter(
            name = key_name,
            x = df['Batch'],
            y = df['Value']))
    return fig