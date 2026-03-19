import pandas as pd

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/sample.csv'
sample = pd.read.csv(file_url)

print(sample.head())
print(sample.tail())

sample.info()
sample.describe()

sample_dic = {'name' : ['John', 'Ann', 'Kevin'], 'age': [23,22,21]}
a = pd.DataFrame(sample_dic)

a.info()

pd.DataFrame([[1,2,], [3,4], [5,6], [7,8]])
pd.DataFrame([[1,2], [3,4], [5.6], [7,8]], columns = ['var_1', 'var_2'], index=['a','b','c','d'])

import pandas as pd
file_url =  'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/sample_df.csv'

sample_df = pd.read_csv(file_url, index_col=0)
print(sample_df.head())

print(sample_df['var_5'])

#print(sample_df['var_1', 'var_2'])   # [ ] 안에는 하나의 값만 들어갈 수 있음
print