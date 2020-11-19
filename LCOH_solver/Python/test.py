import numpy as np
dict = {'a':{'a1':1,
             'a2':2,
             'a3':3},
        'b':{'b1':1}
        }


arr = np.array(list(dict['a'].values()))

arr = arr * 2

if 'a' in dict.keys():
    print('Yes')