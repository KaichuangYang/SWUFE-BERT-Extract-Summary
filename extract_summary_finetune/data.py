import os
import numpy as np
from torch.utils.data import Dataset

class SummaryData():
    def __init__(self, order:int, data_path:str):
        self.order = order
        self.data_path = data_path
        self.divide_data()
        

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
        self.input_size = self.train_token.shape[2]
        self.time_step = self.train_token.shape[1]
        self.train_data_length = self.train_token.shape[0]

class SummaryDataset(Dataset):
    def __init__(self,token:np.array,label:np.array):
        self.token = token
        self.label = label

    def __getitem__(self, index):
        x = self.token[index]
        y = self.label[index]
        return x, y

    def __len__(self):
        return self.token.shape[0]
