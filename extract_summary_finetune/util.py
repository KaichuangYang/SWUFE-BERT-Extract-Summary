

from extract_summary_finetune.log import BatchLog
import pendulum
import torch
import math
import numpy as np

def set_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)

def loss_weighted(pred,label):
    if (pred.ndim == 3)+(label.ndim == 3)==2:
        weight = []
        for i in range(label.shape[0]):
            sumamary_sign_postion  = -1
            distance_score = [0 for i in range(label.shape[1])]
            for j in range (label.shape[1]):
                distance_score[j] = math.log((j-sumamary_sign_postion)+1)
                if (j>0) & (label[i][j-1][0].item()==1) :
                    distance_score[j] = distance_score[j-1]
                if label[i][j][0].item()==1:
                    sumamary_sign_postion = j
            row_weight = [[label.shape[1]*item/sum(distance_score)] for item in distance_score]
            weight.append(row_weight)
        return torch.tensor(weight,dtype=float)
    else:
        return "InputError: true_label and pred_label must be .ndim=3 "
    
    
def process_epoch(
        model,
        loss_func,
        optimizer,
        dataloader,
        is_weighted,
        epoch,
        timezone='Asia/Shanghai'
):

    mode = 'train' if model.training else 'test'
    batch_log = BatchLog(mode)
    for step, (token, label) in enumerate(dataloader):
        batch_start_time = pendulum.now(timezone)
        token = token.type(torch.FloatTensor)
        label = label.type(torch.FloatTensor)
        label = label.view(label.size()[0],-1,1)
        pred = model(token).view(label.size()[0],-1,1)
        #writerpr.add_pr_curve(tag=f'{model}_{loss_func}_{optimizer}',labels= label, predictions= pred)
        if is_weighted:
            loss = loss_func(weight=loss_weighted(pred,label).float())(pred, label)
            #writerloss.add_scalar(f'{model}_{loss_func}_{optimizer}_weighted', loss, step)
        else:
            loss = loss_func()(pred, label)
            #writerloss.add_scalar(f'{model}_{loss_func}_{optimizer}_unweighted', loss, step)
        if model.training:
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        batch_log.add_log(epoch, loss, pred, label)
        batch_end_time = pendulum.now(timezone)
        batch_log.add_execution_time(batch_start_time, batch_end_time)
    #writerloss.close()
    #writerpr.close()
    return batch_log

    