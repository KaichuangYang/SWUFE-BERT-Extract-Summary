import dill
import os
import re
import numpy as np
import pandas as pd
import torch
from extract_summary_finetune.model import lstm,transformer
from transformers import BertTokenizer , BertModel
from cli.cmd_run import model_dict

class NewsToSummary():
    def __init__(self,
                 network:str,
                 bert:str,
                 loss:str,
                 text:str):
        
        self.network = network
        self.bert = bert
        self.loss = loss
        self.text = text

        
        self.load_model()
        self.select_bert()
        self.gen_token()
        self.extract_summary()
        self.modify_summary()

        
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
    
    def select_bert(self):
        if self.bert == "cn_bert":
            self.bert_tokenizer = BertTokenizer.from_pretrained("hfl/rbt3")
            self.bert_model = BertModel.from_pretrained("hfl/rbt3")
        elif self.bert == "wwm_bert":
            self.bert_tokenizer = BertTokenizer.from_pretrained("hfl/chinese-roberta-wwm-ext-large")
            self.bert_model = BertModel.from_pretrained("hfl/chinese-roberta-wwm-ext-large")       
        elif self.bert == "swufe_bert":
            return "InputError: can not have acess to swufe_bert."
        else:
            return"InputError: can not have acess to swufe_bert."
        
    def gen_token(self):
        token_ids = self.bert_tokenizer([self.text],padding="max_length",truncation=True,max_length=512,return_tensors='pt')
        self.token = self.bert_model(token_ids['input_ids'])['last_hidden_state']
    
    def pred_label(self):
        predict = self.pred_network(self.token)
        predict = predict.ge(0.2)
        predict = predict.view(predict.size()[0],512).numpy()
        self.predict_label = predict
        return predict
    
    def fill_news(self):
        news_content = [self.text]
        news_content_filled = []
        for news in news_content:
            if len(news) < 512:
                news_filled = news+' '*(512 - len(news))
                news_content_filled.append(news_filled)
            else:
                news_filled = news[:512]
                news_content_filled.append(news_filled) 
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
        news_content_filled = self.fill_news()
        for content in news_content_filled:
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
                if sum(label_divided) > 0.45*len(label_divided):
                    label_modified = [True for item in label_divided]
                elif sum(label_divided) < 0.2*len(label_divided):
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
        self.word = word
        self.predict = predict