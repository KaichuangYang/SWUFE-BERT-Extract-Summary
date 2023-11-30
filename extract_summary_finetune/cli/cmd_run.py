import click
import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from extract_summary_finetune.data import SummaryData,SummaryDataset
from extract_summary_finetune.model import lstm,transformer
from extract_summary_finetune.util import set_seed
from extract_summary_finetune.extract_summary_finetune_train import train_model
from extract_summary_finetune.performance_measures import calc_auc_score
import dill

model_dict={
    'lstm1':lstm,
    'lstm2':lstm,
    'lstm3':lstm,
    'lstm4':lstm,   
    'transformer1':transformer,
    'transformer2':transformer,
    'transformer3':transformer,
    'transformer4':transformer 
}



@click.group(name='summary')
def cli():
    """ Run summary Experiment """
    pass

@cli.command()
@click.option('-o', '--order', required=True, type=int, default=0)
@click.option('-b', '--bert', required=True, type=str, default="swufe_bert")
@click.option('-n', '--network', required=True, type=str, default='lstm1')
@click.option('-loss', '--loss_func_method', required=True, type=str, default="BCEloss")
@click.option('-lr', '--learning_rate', required=True, type=float, default=0.0005)
@click.option('-e', '--epochs', required=True, type=int, default=2)
@click.option('-s', '--batch_size', required=True, type=int, default=100)
@click.option('-t', '--timezone', required=True, default='Asia/Shanghai')
@click.option('-op', '--output_path', required=True, type=click.Path(resolve_path=True), default="/home/yuxin.fan/result/")
def x01_run_summary_training(order, bert, network, loss_func_method, batch_size, epochs, timezone, output_path, learning_rate):
    set_seed(1)
    bert_data = 'data_from_' + bert
    data_path = os.path.join("/home/yuxin.fan/",bert_data)
    data = SummaryData(order,data_path)
    input_size = data.input_size
    time_step = data.time_step
    train_data_length  = data.train_data_length 
    train_dataset = SummaryDataset(data.train_token, data.train_label)
    test_dataset = SummaryDataset(data.test_token, data.test_label)
    train_dataloader = DataLoader(dataset=train_dataset,
                                  batch_size=batch_size,
                                  shuffle=True)
    test_dataloader = DataLoader(dataset=test_dataset,
                                 batch_size=batch_size,
                                 shuffle=False)
    model_setting_parameters = {
    'lstm1':{'input_size':input_size, 'hidden_size':64, 'num_layers':1, 'dropout':0},
    'lstm2':{'input_size':input_size, 'hidden_size':128, 'num_layers':1, 'dropout':0},
    'lstm3':{'input_size':input_size, 'hidden_size':64, 'num_layers':2, 'dropout':0.05},
    'lstm4':{'input_size':input_size, 'hidden_size':128, 'num_layers':2, 'dropout':0.05},
    'transformer1':{'d_model':input_size, 'src_len':time_step,'dim_feedforward':128, 'nhead':4, 'num_encoder_layers':1, 'activation':"relu",'dropout':0.05},
    'transformer2':{'d_model':input_size, 'src_len':time_step,'dim_feedforward':256, 'nhead':4, 'num_encoder_layers':1, 'activation':"relu",'dropout':0.05},
    'transformer3':{'d_model':input_size, 'src_len':time_step,'dim_feedforward':128, 'nhead':4, 'num_encoder_layers':2, 'activation':"relu",'dropout':0.05},
    'transformer4':{'d_model':input_size, 'src_len':time_step,'dim_feedforward':256, 'nhead':4, 'num_encoder_layers':2, 'activation':"relu",'dropout':0.05}
    }
    model = model_dict[network](**model_setting_parameters[network])
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_func_dict = {
    'BCEloss':nn.BCELoss,
    'w_BCEloss':nn.BCELoss
    }
    loss_func = loss_func_dict[loss_func_method]
    extra_metric = {'auc_score': calc_auc_score}
    
    is_weighted = True if loss_func_method =='w_BCEloss' else False
    is_classification = False
    
    #writermodel = SummaryWriter(log_dir=os.path.join('/home/yuxin.fan/tensorboard_log/',f'tensorboard_{network}_{bert}_{loss_func_method}/model'), flush_secs=1)
    #model_size = (train_data_length,time_step,input_size)
    #writerloss = SummaryWriter(log_dir=os.path.join('/home/yuxin.fan/tensorboard_log/',f'tensorboard_{network}_{bert}_{loss_func_method}/loss'), flush_secs=1)
    #writerpr = SummaryWriter(log_dir=os.path.join('/home/yuxin.fan/tensorboard_log/',f'tensorboard_{network}_{bert}_{loss_func_method}/pr'), flush_secs=1)
    result = train_model(
        model,
        loss_func,
        optimizer,
        train_dataloader,
        test_dataloader,
        epochs,
        is_weighted,
        is_classification,
        extra_metric,
        timezone
    )
    result['network_setting_parameters'] = model_setting_parameters[network]
    output_path = os.path.join(output_path,f'summary_{network}_{bert}_{loss_func_method}.dil')
    with open(output_path, "wb") as f:
        dill.dump(result, f)
    del model
    torch.cuda.empty_cache()
