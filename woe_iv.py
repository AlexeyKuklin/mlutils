# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def woe_iv(df, col_name, target_name, missing=np.nan, replace_missing='NaN'):
    
    """
    IV statistic can be interpreted as follows:
    Less than 0.02, then the predictor is not useful for modeling (separating the Goods from the Bads)
    0.02 to 0.1, then the predictor has only a weak relationship to the Goods/Bads odds ratio
    0.1 to 0.3, then the predictor has a medium strength relationship to the Goods/Bads odds ratio
    0.3 or higher, then the predictor has a strong relationship to the Goods/Bads odds ratio.
    """    
    
    g = df.replace(missing, replace_missing).groupby([col_name, target_name]).count()
    g = pd.DataFrame(g).reset_index()
    g.columns = ['VALUE', 'Y', 'COUNT']
    
    #Test
        
    g = pd.DataFrame({ 'VALUE' : ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F'],
                           'Y' : [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       'COUNT' : [63, 42, 82, 52, 188, 87, 90, 23, 128, 46, 149, 50]
                     })
    """
    g = pd.DataFrame({ 'VALUE' : ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'],
                           'Y' : [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                       'COUNT' : [110, 80, 74, 27, 172, 85, 108, 24, 236, 84]
                     })
    """
    
    p1=g[g['Y']==1][['VALUE', 'COUNT']]
    p0=g[g['Y']==0][['VALUE', 'COUNT']]
    
    res = pd.merge(p1, p0, how='outer', on=['VALUE'])
    res.fillna(0, inplace=True)
    res.columns = ['VALUE', 'Y1', 'Y0']
    
    res['TOTAL'] = res['Y1'] + res['Y0']
    res['D1'] = res['Y1']/(res['Y1'].sum())
    res['D0'] = res['Y0']/(res['Y0'].sum())
    res['WOE'] = np.log(res['D1']/res['D0'])
    res = res.replace(np.inf, 20)
    res['IV'] = (res['D1'] - res['D0']) * res['WOE']
    res.sort_values(by=['IV'], inplace=True, ascending=False)
    res.reset_index(inplace=True, drop=True)    
    return res

#res.to_csv('woe.csv', index=False)
 
#####
np.random.seed(45) 

df = pd.DataFrame({'COL_A' : [np.nan, 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A'],
                   'COL_B' : ['C', 'D', 'E', 'C', 'D', 'C', 'D', 'C', 'C', 'F'],
                   'Y' : np.random.randint(2, size=10)
                  })

print df

print woe_iv(df, 'COL_A', 'Y')


 