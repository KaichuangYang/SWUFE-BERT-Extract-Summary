import numpy as np
import pandas as pd


class LogAtom(object):
    def __init__(self,mode):
        self.loss = []
        self.execution_time = []
        self.epoch =[]
        self.mode=mode
    def add_execution_time(self, start_time, end_time):
        self.execution_time.append((end_time.timestamp() - start_time.timestamp()))

    def to_dataframe(self, prefix):
        log_df = pd.DataFrame({
            f'{self.mode}_{prefix}_epoch':self.epoch,
            f'{self.mode}_{prefix}_loss':self.loss,
            f'{self.mode}_{prefix}_execution_time':self.execution_time,
        })
        return log_df

class BatchLog(LogAtom):
    def __init__(self,mode):
        super(BatchLog, self).__init__(mode)
        self.label_true = []
        self.label_pred = []

    def add_log(self, epoch, loss, label_pred, label_true):
        self.epoch.append(epoch)
        self.loss.append(loss.item())
        self.label_true.append(label_true.detach().cpu().numpy())
        self.label_pred.append(label_pred.detach().cpu().numpy())

    def get_complete_labels(self):
        label_pred = np.concatenate(self.label_pred, axis=0)
        label_true = np.concatenate(self.label_true, axis=0)
        return label_pred, label_true


class BatchMetric(LogAtom):
    def __init__(self, mode, extra_metric:dict, is_classification:bool):
        super(BatchMetric, self).__init__(mode)
        self.metric_name = []
        self.extra_metric = extra_metric
        self.is_classification = is_classification
        self._initialize_metric()

    def _initialize_metric(self):
        for metric_name in self.extra_metric.keys():
            setattr(self, metric_name,[])
            self.metric_name.append(metric_name)

    def add_metric(self, batch_log: BatchLog):
        if batch_log.mode != self.mode:
            raise ValueError(f'batch_log mode {batch_log.mode} is not equal to batch_metric mode {self.mode}')
        for pred, label in zip(batch_log.label_pred, batch_log.label_true):
            #pred = np.argmax(pred,axis=1) if self.is_classification else pred
            pred = pred.ge(0.2) if self.is_classification else pred
            for name, metric_func in self.extra_metric.items():
                try:
                    getattr(self, f'{name}').append(metric_func(label, pred))
                except:
                    getattr(self, f'{name}').append(np.NAN)
        self.epoch.extend(batch_log.epoch)
        self.loss.extend(batch_log.loss)
        self.execution_time.extend(batch_log.execution_time)

    def to_dataframe(self, prefix='batch'):
        log_df = super(BatchMetric,self).to_dataframe(prefix)
        for metric in self.metric_name:
            log_df[f'{self.mode}_{prefix}_{metric}']=getattr(self, f'{metric}')
        return log_df

class EpochMetric(BatchMetric):
    def __init__(self, mode, extra_metric:dict, is_classification:bool):
        super(EpochMetric, self).__init__(mode, extra_metric, is_classification)

    def add_metric(self, batch_log: BatchLog):
        if batch_log.mode != self.mode:
            raise ValueError(f'batch_log mode {batch_log.mode} is not equal to epoch_metric mode {self.mode}')
        if len(np.unique(batch_log.epoch))!=1:
            raise ValueError(f'batch_log epoch is not unique')
        self.epoch.append(batch_log.epoch[0])
        pred, label = batch_log.get_complete_labels()
        #pred = np.argmax(pred,axis=1) if self.is_classification else pred
        pred = pred.ge(0.2) if self.is_classification else pred
        for name, metric_func in self.extra_metric.items():
            try:
                getattr(self, f'{name}').append(metric_func(label, pred))
            except:
                getattr(self, f'{name}').append(np.NAN)
        self.loss.append(np.mean(batch_log.loss))

    def to_dataframe(self, prefix='epoch'):
        log_df = super(EpochMetric, self).to_dataframe(prefix)
        return log_df

    def display(self, epoch):
        info = f'epoch {self.epoch[epoch] + 1}/{self.mode}, loss: {self.loss[epoch]:.3f}, '
        for name in self.metric_name:
            val = getattr(self, f'{name}')[epoch]
            info += f'{name}: {val:.3f},'
        info += f'execution_time: {self.execution_time[epoch]:.6f}'
        print(info)