import sys
import numpy as np
from extract_summary_finetune.data import SummaryData,SummaryDataset
import pytest

def setup_module():
    sys.path.append("..")


class TestSummaryData():
    
    def setup_class(self):
        for i in range(5):
            a = np.random.randn(10,512,7) 
            b = np.random.randn(10,512)
        np.savez("/home/yuxin.fan/data_for_test/file{}.npz".format(i+1),a=a,b=b)

        self.data = SummaryData(1,"/home/yuxin.fan/data_for_test")
        self.data.divide_data() 
        
    
    def test_load_data(self):
        token_data, label_data = self.data.load_data()
        s1 = np.array(token_data).shape  
        s2 = np.array(label_data).shape
        assert ((s1==(5,10,512,7)*(s2==(5,10,512))))
    
    def test_divide_data(self): 
        train_dataset = self.data.train_token, self.data.train_label   #((40,512,7),(40,512))
        test_dataset = self.data.test_token, self.data.test_label      #((10,512,7),(10,512))
        INPUT_SIZE = self.data.input_size
        TIME_STEP = self.data.time_step
        s11 = train_dataset[0].shape  
        s12 = train_dataset[1].shape
        s21 = test_dataset[0].shape
        s22 = test_dataset[1].shape 
        assert (type(train_dataset) == tuple)
        assert (len(train_dataset) == 2)
        assert (s11 == (40,512,7))
        assert (s12 == (40,512))
        assert (s21 == (10,512,7))
        assert (s22 == (10,512))
        assert (INPUT_SIZE == 7)
        assert (TIME_STEP == 512)

class TestSummaryDataset():
    
    def setup_class(self):
        self.dataset = SummaryDataset(np.random.randn(3,5,7),np.random.randn(3,6,7))
 
    def test_init_getitem_len(self):
        T = self.dataset.token
        L = self.dataset.label
        x = self.dataset.token[1]
        y = self.dataset.label[1]
        s = self.dataset.token.shape[0]
        assert(T.shape==(3,5,7))
        assert(L.shape==(3,6,7))
        assert(len(x)==5)
        assert(len(y)==6)
        assert(s==3)
