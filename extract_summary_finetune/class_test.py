import os
import numpy as np
from torch.utils.data import Dataset
from extract_summary_finetune.performance_measures import auc_score

class SummaryData():
    def __init__(self, order:int, data_path:str):
        self.order = order
        self.data_path = data_path

    def load_data(self):
        files = os.listdir(self.data_path)
        files = [file for file in files if file[-3:]=="npz"]
        names = np.load(os.path.join(self.data_path,files[0])).files
        token_name = names[0]
        lable_name = names[1]
        token_data = [np.load(file= os.path.join(self.data_path,file),allow_pickle=True)[token_name] for file in files]
        label_data = [np.load(file= os.path.join(self.data_path,file),allow_pickle=True)[lable_name] for file in files]
        return token_data, label_data

    def divide_data(self):
        token, label = self.load_data()
        self.test_token = token[self.order]
        self.test_label = label[self.order]
        self.train_token = np.concatenate([token[i] for i in range(len(token)) if i != self.order], axis=0)
        self.train_label = np.concatenate([label[i] for i in range(len(token)) if i != self.order], axis=0)
        return self.train_label

import torch
a = SummaryData(0,"/home/yuxin.fan/data_from_swufe_bert")
b = torch.Tensor(a.divide_data())
b = b.view(b.size()[0],-1,1).detach().cpu().numpy()
c = np.concatenate([b,b], axis=0)
#print(c.ndim,c.shape)
print(auc_score(b,b))