"""Main module."""
import torch
import pendulum
from extract_summary_finetune.util import process_epoch
from extract_summary_finetune.log import EpochMetric, BatchMetric


def train_model(
        model,
        loss_func,
        optimizer,
        train_dataloader,
        test_dataloader,
        epochs,
        is_weighted,
        is_classification,
        extra_metric: dict,
        timezone
):

    train_epoch_metric = EpochMetric('train', extra_metric, is_classification)
    train_batch_metric = BatchMetric('train', extra_metric, is_classification)
    if test_dataloader is not None:
        test_epoch_metric = EpochMetric('test', extra_metric, is_classification)
        test_batch_metric = BatchMetric('test', extra_metric, is_classification)

    for epoch in range(epochs):
        train_epoc_start_time = pendulum.now(timezone)
        model = model.train()
        train_batch_log = process_epoch(model,
                                        loss_func,
                                        optimizer,
                                        train_dataloader,
                                        is_weighted,
                                        epoch,
                                        timezone
                                        )
        train_batch_metric.add_metric(train_batch_log)
        train_epoch_metric.add_metric(train_batch_log)
        train_epoc_end_time = pendulum.now(timezone)
        train_epoch_metric.add_execution_time(train_epoc_start_time, train_epoc_end_time)
        train_epoch_metric.display(epoch)

        if test_dataloader is not None:
            test_epoc_start_time = pendulum.now(timezone)
            model = model.eval()
            with torch.no_grad():
                test_batch_log = process_epoch(model,
                                               loss_func,
                                               optimizer,
                                               test_dataloader,
                                               is_weighted,
                                               epoch,
                                               timezone
                                               )
                test_batch_metric.add_metric(test_batch_log)
                test_epoch_metric.add_metric(test_batch_log)
                test_epoc_end_time = pendulum.now(timezone)
                test_epoch_metric.add_execution_time(test_epoc_start_time, test_epoc_end_time)
                test_epoch_metric.display(epoch)

    result = {
        'epochs': epochs,
        'is_classification': is_classification,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'train_batch_metric': train_batch_metric.to_dataframe(),
        'train_epoch_metric': train_epoch_metric.to_dataframe(),
    }
    if test_dataloader is not None:
        result.update({'test_batch_metric': test_batch_metric.to_dataframe(),
                       'test_epoch_metric': test_epoch_metric.to_dataframe()
                       })
    return result