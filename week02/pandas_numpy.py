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

# print(sample_df['var_1', 'var_2'])   # [ ] 안에는 하나의 값만 들어갈 수 있음
print(sample_df[['var_1', 'var_4']])   # [ [] ]를 사용하면 [] 가 하나의 값으로 인식됨

# loc 는 location의 앞글자
print(sample_df.loc['a'])              # 행 기준으로 인덱싱
print(sample_df.loc[['a','c','e']])
print(sample_df.loc['a':'c'])

# iloc: integer location의 약자
print(sample_df.iloc[[0,1,2]])
print(sample_df.iloc[0:2])
print(sample_df.iloc[0:3])
print(sample_df.iloc[0:3, 2:4])        # 컬럼까지 동시에 인덱싱

print(sample_df.drop(['var_1','var_3'], axis=1))     # 컬럼을 제거하려면 axis = 1
print(sample_df.drop(['var_1','var_2'], axis=1))
print(sample_df.drop(['a','b','c'], axis=0))         # 행을 제거하려면 axis = 0 또는 디폴트로 사용

netflix = pd.read_csv('2.1.1.netflix.csv')
print(netflix.head())

print(netflix['release_year'])
print(netfilx['release_year'] > 2015)

more2015 = netflix[netflix['release_year'] > 2015]
print(more2015.head(10))

print(~(netflix['release_year'] > 2015))
more2015 = netflix[~(netflix['release_year'] > 2015)]
print(less20215.head())

print((netflix['release_year'] > 2015) & (netflix['type'] == 'TV Show'))

more2015_tv - netflix[(netflix['release_year'] > 2015) & (netflix['type'] == 'TV Show')]
print(more2015_tv.head())

more2015_or_tv - netflix[(netflix['release_year'] > 2015) & (netflix['type'] == 'TV Show')]
print(more2015_or_tv.head())

data = {
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hannah'],
    'comment_length': [150, 200, 50, 300, 120, 180, 75, 160],
    'likes': [25, 30, 10, 45, 20, 35, 5, 28],
    'is_spam': [False, False, True, False, False, True, False, False],
    'has_image': [True, False, True, True, False, False, True, True]
}
df = pd.DataFrame(data)
print(df.head())

# 필터링 조건 설정
condition = (
    (df['comment_length'] >= 100) &       # 댓글 길이 100자 이상
    (df['likes'] >= 20) &                 # 좋아요 20개 이상
    (~df['is_spam']) &                    # 스팸 댓글이 아니어야 함
    (df['has_image'])                     # 이미지가 포함된 댓글이어야 함
)

# 조건을 만족하는 행들 필터링
winner_df = df[condition]
print(winner_df)

print(sample_df.reset_index())

print(sample_df.reset_index(drop=True))          # 기존 인덱스는 제거하기

print(sample_df.set_index('var_1'))

print(sample_df.describe())
print(sample_df.std())
print(sample_df.agg(['count', ',mean', 'std', 'min', 'max']))

file_url = 'https://media.githubusercontent.com/media/musthave-ML10/data_source/main/iris.csv'
iris = pd.read_csv(file_url)

print(iris.head())

print(iris.groupby('class').std())

print(iris.drop('class', axis=1).agg(['sum', 'mean', 'std']))

# print(iris.agg(['sum','mean', 'std']))    # class 컬럼으로 인해 에러 발생

print(iris['class'].unique())
print(iris['class'].nunique())
print(iris['class'].value_counts())

# 예제 데이터 생성
data = {
    'name' : ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [25, 30, 35, 28, 40],
    'salary' : [70000.00, 80000.00, 90000.00, 60000.00, 95000.00]
}

# Dataframe 생성
df = pd.DataFrame(data)
print(df.head())

# 개인별 과목 점수의 평균값 계산 (axis=1)
df['average'] = df[['math', 'science', 'english']].mean(axis=1)
print(df)

# 이름과 평균값만을 포함하는 새로운 데이터프레임 생성
average_df = df[['name', 'average']]
print(average_df)

# 2.2 넘파이
import numpy as np

print(np.array([1,2,3]))

print(np.array([1,2,3],
               [4,5,6],
               [7,8,9]))

print(np.array([[[1,2,3],
                 [4,5,6],
                 [7,8,9]],
                 [[1,2,3],
                 [4,5,6],
                 [7,8,9]],
                 [[1,2,3],
                 [4,5,6],
                 [7,8,9]]]))

print(np.array([1,2,3,4,5]))
print(np.array(sample_df))

sample_np = np.array(sample_df)
print(pd.DataFrame(sample_np ))      # 컬럼명이 0, 1, 2, 3, 4

print(sample_df.columns)            # 기존 프레임워크에서 컬럼명 가져오기

print(pd.DataFrame(sample_np, columns = sample_df.columns))      # 새 프레임워크에 컬럼명 붙이기

print(sample_np)
print(sample_np[0])
print(sample_np[0,2])
print(sample_np[0:3,2:4])
print(sample_np[:,2])

np_a = np.array([[1,3], [0.-2]])
print(np_a)
print(np_a + 10)
print(np_a - 5)
print(np_a * 2)
print(np_a+10 / 3)

np_b = np.array([[1,0], [0,1]])
print(np_b)
print(np_a + np_b)
print(np_a - np_b)
print(np_a * np_b)
print(np_a @ np_b)

print(np.random.randint(11))
print(np.random.randint(50, 71))
print(np.random.randint(50, 71, 10))
print(np.random.choice(['red', 'green','white','black','blue'],size=3))
print(np.random.choice(['red', 'green','white','black','blue'],size=3))
