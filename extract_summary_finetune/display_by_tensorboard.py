import os
import dill
import numpy as np
from torch.utils.tensorboard import SummaryWriter

class MyTensorboard():
    def __init__(self, log_dir, fold_path) :
        self.writer = SummaryWriter(log_dir)
        self.fold_path = fold_path
    
    def get_loss_auc(self, network, model, loss_function):
        load_path = self.fold_path + "summary_" + network + "_" + model +"_" + loss_function + ".dil"
        results_dict = dill.load(open(load_path, "rb"))
        train_loss = results_dict['train_epoch_metric']['train_epoch_loss']   
        train_auc = results_dict['train_epoch_metric']['train_epoch_auc_score']
        test_loss = results_dict['test_epoch_metric']['test_epoch_loss']   
        test_auc = results_dict['test_epoch_metric']['test_epoch_auc_score']
        return train_loss,train_auc,test_loss,test_auc
    
    def models_loss_auc(self, network, loss_function):   
        cn_train_loss,cn_train_auc,cn_test_loss,cn_test_auc = self.get_loss_auc(network, "cn_bert", loss_function)
        wwm_train_loss,wwm_train_auc,wwm_test_loss,wwm_test_auc = self.get_loss_auc(network, "wwm_bert", loss_function)
        swufe_train_loss,swufe_train_auc,swufe_test_loss,swufe_test_auc = self.get_loss_auc(network, "swufe_bert", loss_function)    
        for i in range(len(cn_train_loss)):
            self.writer.add_scalars("3models_train_loss",{'cn_train_loss':cn_train_loss[i],
                                                          'wwm_train_loss':wwm_train_loss[i],
                                                          'swufe_train_loss':swufe_train_loss[i]},i)  
            self.writer.add_scalars("3models_train_auc",{'cn_train_auc':cn_train_auc[i],
                                                         'wwm_train_auc':wwm_train_auc[i],
                                                         'swufe_train_auc':swufe_train_auc[i]},i)
        for i in range(len(cn_test_loss)):
            self.writer.add_scalars("3models_test_loss",{'cn_test_loss':cn_test_loss[i],
                                                         'wwm_test_loss':wwm_test_loss[i],
                                                         'swufe_test_loss':swufe_test_loss[i]},i)  
            self.writer.add_scalars("3models_test_auc",{'cn_test_auc':cn_test_auc[i],
                                                        'wwm_test_auc':wwm_test_auc[i],
                                                        'swufe_test_auc':swufe_test_auc[i]},i)
            
    def networks_loss_auc(self, model, loss_function):   
        lstm1_train_loss,lstm1_train_auc,lstm1_test_loss,lstm1_test_auc = self.get_loss_auc("lstm1", model, loss_function)
        transformer1_train_loss,transformer1_train_auc,transformer1_test_loss,transformer1_test_auc = self.get_loss_auc("transformer1", model, loss_function)
        for i in range(len(lstm1_train_loss)):
            self.writer.add_scalars("networks_train_loss",{'lstm1_train_loss':lstm1_train_loss[i],
                                                           'transformer1_train_loss':transformer1_train_loss[i]},i)  
            self.writer.add_scalars("networks_train_auc",{'lstm1_train_auc':lstm1_train_auc[i],
                                                          'transformer1_train_auc':transformer1_train_auc[i]},i)
        for i in range(len(lstm1_test_loss)):
            self.writer.add_scalars("networks_test_loss",{'lstm1_test_loss':lstm1_test_loss[i],
                                                           'transformer1_test_loss':transformer1_test_loss[i]},i)  
            self.writer.add_scalars("networks_test_auc",{'lstm1_test_auc':lstm1_test_auc[i],
                                                          'transformer1_test_auc':transformer1_test_auc[i]},i)           
            
    def loss_funcs_loss_auc(self, network, model):    
        BCEloss_train_loss,BCEloss_train_auc,BCEloss_test_loss,BCEloss_test_auc = self.get_loss_auc(network, model, "BCEloss")
        w_BCEloss_train_loss,w_BCEloss_train_auc,w_BCEloss_test_loss,w_BCEloss_test_auc = self.get_loss_auc(network, model, "w_BCEloss")
        for i in range(len(BCEloss_train_loss)):
            self.writer.add_scalars("loss_funcs_train_loss",{'BCEloss_train_loss':BCEloss_train_loss[i],
                                                             'w_BCEloss_train_loss':w_BCEloss_train_loss[i]},i)  
            self.writer.add_scalars("loss_funcs_train_auc",{'BCEloss_train_auc':BCEloss_train_auc[i],
                                                            'w_BCEloss_train_auc':w_BCEloss_train_auc[i]},i)
        for i in range(len(BCEloss_test_loss)):
            self.writer.add_scalars("loss_funcs_test_loss",{'BCEloss_test_loss':BCEloss_test_loss[i],
                                                            'w_BCEloss_test_loss':w_BCEloss_test_loss[i]},i)  
            self.writer.add_scalars("loss_funcs_test_auc",{'BCEloss_test_auc':BCEloss_test_auc[i],
                                                           'w_BCEloss_test_auc':w_BCEloss_test_auc[i]},i)
            
    def file_hparams(self, lr, batch_size):
        for file in os.listdir(self.fold_path): 
            path = self.fold_path + file
            result_dict = dill.load(open(path,'rb'))
            auc = np.mean(result_dict['train_batch_metric']['train_batch_auc_score'])
            loss = np.mean(result_dict['train_batch_metric']['train_batch_loss'])
            network = 'lstm' if 'lstm' in file else 'transformer'
            bert = 'cn_bert' if 'cn' in file else 'wwm_bert' if 'wwm' in file else 'swufe_bert'
            is_weighted = True if '_w_' in file else False
            self.writer.add_hparams({'lr':lr,
                                     'bsize':batch_size,
                                     'is_weighted':is_weighted,
                                     'bert':bert,
                                     'network':network},
                                    {'hparam/auc':auc,
                                     'hparam/loss':loss}, run_name = file)
      
    def tensorboard_close(self):
        self.writer.close()      
 