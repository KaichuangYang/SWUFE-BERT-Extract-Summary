
import torch.nn as nn
import torch
from torch.autograd import Variable
import math


class lstm(nn.Module):
    def __init__(self, input_size:int, hidden_size:int, num_layers:int, dropout:int, batch_first:bool=True):
        super(lstm, self).__init__()
        self.rnn = nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_size,
            num_layers = num_layers,
            dropout = dropout,
            batch_first = batch_first
        )
        self.hidden_out = nn.Linear(hidden_size, 1)
        self.h_s = None
        self.h_c = None

    def forward(self, x):
        r_out, (self.h_s, self.h_c) = self.rnn(x)
        output = self.hidden_out(r_out)
        output = nn.Sigmoid()(output)
        return output


class transformer(nn.Module):
    def __init__(self, d_model, src_len, dim_feedforward=256, nhead=4, num_encoder_layers=1, activation="relu",dropout=0.05, batch_first=True):
        super(transformer,self).__init__()
        self.posemb = PositionalEncoding(d_model, dropout, len=src_len)
        self.encoder = nn.TransformerEncoder(encoder_layer= nn.TransformerEncoderLayer(d_model=d_model,nhead= nhead, 
                                             dim_feedforward= dim_feedforward,dropout=dropout,activation=activation,
                                             batch_first=batch_first),
                                             num_layers= num_encoder_layers)
        self.liner1 = nn.Linear(d_model,128)
        self.liner2 = nn.Linear(128,1)
    def forward(self, x):
        input = self.posemb(x)
        output = self.encoder(input)
        output = self.liner1(output)
        output = nn.Tanh()(output)
        output = self.liner2(output)
        output = nn.Sigmoid()(output)
        return output

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, len=512):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(len, d_model) 
        position = torch.arange(0, len).unsqueeze(1) 
        div_term = torch.exp(torch.arange(0, d_model, 2) *    
                             -(math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term) 
        pe[:, 1::2] = torch.cos(position * div_term)  
        pe = pe.unsqueeze(0) 
        self.register_buffer('pe', pe) 

    def forward(self, x):
        x = x + Variable(self.pe[:, :x.size(1)],requires_grad=False)
        return self.dropout(x)