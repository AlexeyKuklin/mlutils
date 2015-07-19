# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler 
import random

class DataFrameDictVectorizer():
    def __init__(self):
        self.vec = None
        self.cols = None

    def _transformation(self, sm, df, replace):
        vecData = pd.DataFrame(sm.toarray())
        vecData.columns = self.vec.get_feature_names()
        vecData.index = df.index
        if replace is True:
            df = df.drop(self.cols, axis=1)
            df = df.join(vecData)
        return df, vecData

    def _column_as_str(self, df):
        for i in self.cols:
            df[i] = 'c' + df[i].astype(str)    

    def fit_transform(self, df, cols, replace=False):
        self.cols = [i for i in cols if i in df.columns.values.tolist()] #self.cols = cols
        self.vec = DictVectorizer()
        self._column_as_str(df)       
        sm = self.vec.fit_transform(df[self.cols].to_dict(orient='records'))
        return self._transformation(sm, df, replace)

    def transform(self, df, replace=False):
        if self.vec == None:
           return None
        self._column_as_str(df)                       
        sm = self.vec.transform(df[self.cols].to_dict(orient='records'))
        return self._transformation(sm, df, replace)


class DataFrameStandardScaler():
    def __init__(self):
        self.stsc = None
        self.cols = None
        with_mean = True
        with_std = True

    def _transform(self, df, t, replace):
        t = t.T
        if replace == True:
            for i, c in enumerate(self.cols):
                df[c] = t[i]
        return df, t
        
    def fit_transform(self, df, cols, replace=True, with_mean=True, with_std=True):
        self.cols = [i for i in cols if i in df.columns.values.tolist()]
        self.with_mean = with_mean
        self.with_std = with_std
        self.stsc = StandardScaler(copy=False, with_mean=with_mean, with_std=with_std)
        t = self.stsc.fit_transform(df[self.cols])
        return self._transform(df, t, replace)

    def transform(self, df, replace=True):
        if self.stsc == None:
           return None
        t = self.stsc.transform(df[self.cols])
        return self._transform(df, t, replace)


     
def test():
    df = pd.DataFrame(np.random.randn(25, 3)*10, columns=['a', 'b', 'c'])
    df['d'] = [random.choice(('A', 'B', 'C')) for i in range(df.shape[0])]
    df['e'] = [random.choice((4, 5, 6, 7)) for i in range(df.shape[0])]
    df.to_csv('test.csv', index=False, sep=';', decimal='.')

    df1 = df.copy(deep=True)
    v = DataFrameDictVectorizer()
    df1, _ = v.fit_transform(df1, ['d', 'e'], replace=True)
    df1.to_csv('test1.csv', index=False, sep=';', decimal='.')

    df2 = df.copy(deep=True)
    df2['d'] = df2['d'].apply(lambda x: 'D' if x=='A' else x)
    df2, _ = v.transform(df2, replace=True)
    df2.to_csv('test2.csv', index=False, sep=';', decimal='.')

    df3 = df.copy(deep=True)
    sts = DataFrameStandardScaler()
    sts.fit_transform(df3, ['a', 'c'])
    df3.to_csv('test3.csv', index=False, sep=';', decimal='.')

    df4 = df.copy(deep=True)
    sts.transform(df4)
    df4.to_csv('test4.csv', index=False, sep=';', decimal='.')        

if __name__ == '__main__':
    test()
