import numpy as np
from extract_summary_finetune.performance_measures import calc_auc_score
import pytest


def test_auc_score1():
    a = np.array(np.random.randint(0,2,size=(1,50)))
    b = np.array(np.random.randint(0,2,size=(1,50)))
    print(calc_auc_score(a,b))
    return calc_auc_score(a,b)

def test_auc_score2():
    a = np.array(np.random.randint(0,5,size=(1,90)))
    b = np.array(np.random.randint(0,5,size=(1,90)))
    print(calc_auc_score(a,b))
    return calc_auc_score(a,b)


def test_auc_score3():
    a = np.array(np.random.randint(0,3,size=(1,70)))
    b = np.array(np.random.randint(0,3,size=(1,70)))
    print(calc_auc_score(a,b))
    return calc_auc_score(a,b)



if __name__=='__main__':
    pytest.main(["-s", "test_performance_measures.py"])



