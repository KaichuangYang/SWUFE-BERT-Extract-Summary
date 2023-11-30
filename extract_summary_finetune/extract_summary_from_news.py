
import dill
import os
import re
import numpy as np
import pandas as pd
import torch
from extract_summary_finetune.model import lstm,transformer
from cli.cmd_run import model_dict

class ExtratSummary():
    def __init__(self,
                 network:str,
                 bert:str,
                 loss:str,
                 data_path:str='/home/yuxin.fan/feature_from_swufe_bert.npy',
                 news_path:str='/home/yuxin.fan/short_news_text1.txt'):
        
        self.network = network
        self.bert = bert
        self.loss = loss
        self.data_path = data_path
        self.news_path = news_path
        
        self.load_model()
        self.extract_summary()
        self.modify_summary()
        self.summary_to_dataframe()

        
    def load_model(self):
        file_name = f'summary_{self.network}_{self.bert}_{self.loss}.dil'
        load_path = os.path.join("/home/yuxin.fan/result/",file_name)
        with open(load_path, "rb") as file:
            network_results_dict = dill.load(file)
        network_state_dict = network_results_dict['model_state_dict']
        network_setting_parameters = network_results_dict['network_setting_parameters']
        pred_network = model_dict[self.network](**network_setting_parameters)
        pred_network.load_state_dict(network_state_dict, strict=True)
        self.pred_network = pred_network
    
    def load_data(self):
        token = torch.tensor(np.load(self.data_path,allow_pickle=True)).type(torch.float32)
        return token
    
    def pred_label(self):
        token = self.load_data()
        predict = self.pred_network(token)
        predict = predict.ge(0.2)
        predict = predict.view(predict.size()[0],512).numpy()
        self.predict_label = predict
        return predict
    
    def load_news(self):
        content_data = []
        with open(self.news_path,'r',encoding='utf-8') as f:
            for line in f:
                content_data.append(line)
        news_content = content_data[0].strip('[]').strip('\'').split('\', \'')
        self.news_content = news_content
        return news_content
    
    def fill_news(self):
        news_content = self.load_news()
        news_content_filled = []
        for news in news_content:
            if len(news) < 512:
                news_filled = news+' '*(512 - len(news))
                news_content_filled.append(news_filled)
            else:
                news_filled = news[:512]
                news_content_filled.append(news_filled) 
        self.news_content_filled = news_content_filled
        return news_content_filled
    
    def news_to_words(self):
        news_content_filled = self.fill_news()
        word_content_filled = [list(item) for item in news_content_filled]
        return word_content_filled
    
    def extract_summary(self):
        predict = self.pred_label()
        word = self.news_to_words()
        summary = []
        for i in range(predict.shape[0]):
            each_summary = ''
            for j in range(predict.shape[1]):
                each_summary = each_summary + (predict[i][j]*word[i][j])
            summary.append(each_summary)
        self.summary = summary
    
    def divide_sentences(self):
        news_to_sentences=[]
        for content in self.news_content_filled:
            news_content = re.split(r'(\!|\?|。|！|？|\.{6}|\,|，)', content)
            news_to_sentences.append(news_content)
        return news_to_sentences 
    
    def modify_labels(self):
        news_to_sentences = self.divide_sentences()
        predict_label_modified = []
        for k in range(len(news_to_sentences)):
            sentences_length_list = [len(sentence) for sentence in news_to_sentences[k]]
            start_index = 0
            label_modified_list = []
            for i in range(len(sentences_length_list)):
                end_index = start_index + sentences_length_list[i]
                label_divided = list(self.predict_label[k][start_index:end_index])
                if sum(label_divided) > 0.50*len(label_divided):
                    label_modified = [True for item in label_divided]
                elif sum(label_divided) <= 0.50*len(label_divided):
                    label_modified = [False for item in label_divided]
                else:
                    label_modified = label_divided
                label_modified_list.extend(label_modified)
                start_index = end_index
            predict_label_modified.append(np.array(label_modified_list))
        return np.array(predict_label_modified)
    
    def modify_summary(self):
        predict = self.modify_labels()
        word = self.news_to_words()
        summary_modified = []
        for i in range(predict.shape[0]):
            each_summary = ''
            for j in range(predict.shape[1]):
                each_summary = each_summary + (predict[i][j]*word[i][j])
            summary_modified.append(each_summary)
        self.summary_modified = summary_modified

    def summary_to_dataframe(self):
        content_summary = pd.DataFrame.from_dict({'summary':self.summary,'summary_modified':self.summary_modified,'content':self.news_content})
        self.results_dataframe=content_summary
        file_name = f'{self.network}_{self.bert}_{self.loss}_example.csv'
        file_path = "/home/yuxin.fan/news_summary_example/"
        content_summary.to_csv(os.path.join(file_path,file_name),index=False ,encoding='utf_8_sig')

