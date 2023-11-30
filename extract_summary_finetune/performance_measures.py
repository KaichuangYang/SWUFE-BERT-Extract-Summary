from sklearn.metrics import roc_auc_score
from sklearn.metrics import recall_score,precision_score
from rouge import Rouge
import numpy as np

#fpr,tpr,thresholds = metrics.roc_curve(labels,scores)

def calc_auc_score(true_label:np.array,pred_label:np.array)->float:
    if (true_label.ndim == 3)+(pred_label.ndim == 3)==2:
        sample_auc = []
        for i in range(true_label.shape[0]):
            sample_auc.append(roc_auc_score(true_label[i],pred_label[i]))
        auc_score = np.mean(sample_auc)
        return float(auc_score)
    else:
        return "InputError: true_label and pred_label must be .ndim=3 "


def calc_iou_score(true_label:np.array,pred_label:np.array)->float:
    rec_score = recall_score(true_label,pred_label)
    pre_score = precision_score(true_label,pred_label)
    iou_score = 1/((1/rec_score)+(1/pre_score)-1)
    return iou_score

# rougr sklearn

def rouge(a,b):
    rouge = Rouge()
    rouge_score = rouge.get_scores(a,b, avg=True) # a和b里面包含多个句子的时候用
    rouge_score1 = rouge.get_scores(a,b) # a和b里面只包含一个句子的时候用
    # 以上两句可根据自己的需求来进行选择
    r1 = rouge_score["rouge-1"]
    r2 = rouge_score["rouge-2"]
    rl = rouge_score["rouge-l"]

    return r1, r2, rl
