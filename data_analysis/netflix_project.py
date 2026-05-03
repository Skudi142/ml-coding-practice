# -*- coding: utf-8 -*-
# 넷플릭스 데이터 분석 프로젝트

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 세션 저장소에 업로드한 csv 파일을 읽어 변수에 할당
netflix = pd.read_csv('netflix_titles.csv')
netflix.head()

# .columns : 열 이름 확인
list(netflix.columns)

# .head(3) : 데이터 처음 3개의 행 출력
netflix.head(3)

# .info() : 열에 대한 요약 정보 확인
netflix.info()

# 넷플릭스 결측치 비율 확인하기
for i in netflix.columns :
    missingValueRate = netflix[i].isna().sum() / len(netflix) * 100
    if missingValueRate > 0 :
        print("{} null rate: {}%".format(i,round(missingValueRate, 2)))

# .fillna( ) : 결측치를 다른 값으로 대체하여 처리
# 결측치 비율 : country(9.44%)
netflix['country'] = netflix['country'].fillna('No Data')

# .replace(np.nan, 'b') : 결측치를 문자열 바꾸기 함수를 통해 처리
# 결측치 비율 : director(29.91%), cast(9.37%)
netflix['director'] = netflix['director'].replace(np.nan, 'No Data')
netflix['cast'] = netflix['cast'].replace(np.nan, 'No Data')

# .dropna(axis = 0) : 결측치가 있는 행 전체 제거
# 원본 객체를 수정하려면 inplace = True 옵션 추가
# 결측치 비율 : date_added(0.11%), rating(0.05%), duration(0.03%)
netflix.dropna(axis = 0, inplace=True)

# .info() : 열에 대한 요약 정보 확인
# 8807 rows(원본 데이터 행 개수) - 17 rows(결측치 행) = 8790 rows(결측치가 제거된 행 개수)
netflix.info()

# 데이터프레임의 각 컬럼별 결측치 개수 반환
# isna() == isnull() : 결측 값은 True 반환하고, 그 외에는 False 반환
netflix.isna().sum()

# 시청 등급 기준표를 참고하여 Netflix의 rating 변수를 이용한 age_group_dic 변수 생성
# rating 컬럼의 값을 age_group이라는 새로운 컬럼으로 복사
netflix['age_group'] = netflix['rating']

# 시청 등급 코드를 더 이해하기 쉬운 표현으로 매핑할 딕셔너리 정의(key, value 선언)
age_group_dic = {
    'G': 'All',
    'TV-G': 'All',
    'TV-Y': 'All',
    'PG': 'Older Kids',
    'TV-Y7': 'Older Kids',
    'TV-Y7-FV': 'Older Kids',
    'TV-PG': 'Older Kids',
    'PG-13': 'Teens',
    'TV-14': 'Young Adults',
    'NC-17': 'Adults',
    'NR': 'Adults',
    'UR': 'Adults',
    'R': 'Adults',
    'TV-MA': 'Adults'
    }

# map 함수를 이용하여 rating 컬럼의 값을 딕셔너리를 기반으로 변환하여 age_group 컬럼에 저장
# .map( ) : 사전에 정의한 내용을 변수에 적용
netflix['age_group'] = netflix['age_group'].map(age_group_dic)
netflix.head(2)

# 데이터 전처리 완료한 데이터셋 csv 파일로 저장
# index=False: 데이터프레임의 인덱스 열을 포함하지 않겠다는 뜻
netflix.to_csv('netflix_preprocessed.csv', index=False)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 전처리가 완료된 데이터셋 불러오기
netflix = pd.read_csv('netflix_preprocessed.csv')

# 넷플릭스 브랜드 상징 색깔 시각화
sns.palplot(['#221f1f', '#b20710', '#e50914', '#f5f5f1'])

# 제목 정하기
plt.title('Netflix brand palette', loc='left', fontfamily='serif', fontsize=15, y=1.2)
plt.show()

netflix['title'].str.contains('squid game', na=False, case=False)

# 오징어 게임을 검색한 조건을 넷플릭스 데이터에 넣어서 True인 값만 출력
netflix[netflix['title'].str.contains('Squid Game', na=False, case=False)]

type_counts = netflix['type'].value_counts()
print(type_counts)

# 5 x 5 크기의 플롯 만들기
plt.figure(figsize=(5, 5))

plt.pie(type_counts, labels=type_counts.index, autopct='%0.f%%', startangle=100,
        explode=[0.05, 0.05], shadow=True, colors=['#b20710', '#221f1f'])

plt.suptitle('Movie & TV Show distribution', fontfamily='serif', fontsize=15, fontweight='bold')
plt.title('We see more movies than TV shows on Netflix.', fontfamily='serif', fontsize=12)
plt.show()

netflix.head(3)

# 넷플릭스 데이터셋의 장르별 등장 횟수 계산
genres = netflix['listed_in'].str.split(', ', expand=True).stack().value_counts()
genres

# [1단계] listed_in 열에 있는 장르를 쉼표로 분할하기
# 예시) 인덱스 1의 listed_in 열 값 : International TV Shows, TV Dramas, TV Mysteries
netflix['listed_in'].str.split(', ', expand=True)

# [2단계] .stack( )을 사용하면 여러 열로 구성한 데이터프레임을 1개의 열로 만들어 쌓음
# 예시) 인덱스 1의 listed_in 열 값 : International TV Shows, TV Dramas, TV Mysteries
netflix['listed_in'].str.split(', ', expand=True).stack()

# [3단계] .value_counts( )를 붙여 장르의 등장 횟수 계산
# 예시) 인덱스 1의 listed_in 열 값 : International TV Shows, TV Dramas, TV Mysteries
genres = netflix['listed_in'].str.split(', ', expand=True).stack().value_counts()
genres

plt.figure(figsize=(12, 6))

sns.barplot(x=genres.values, y=genres.index, hue=genres.index, palette='RdGy')

plt.title('Distribution of Genres for Movies and TV Shows on Netflix', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Genre', fontsize=14)
plt.grid(axis='x')
plt.show()

netflix[netflix['title'].str.contains('Sankofa', na=False, case=False)]

# 출력할 최대 행 수를 None으로 설정해서 모두 출력
pd.set_option('display.max_rows', None)

# 쉼표로 country 열의 값을 파이썬 리스트로 만들기
netflix['country'] = netflix['country'].str.split(', ')
netflix['country']

# 파이썬 리스트로 바꾼 country 열의 값에 explode( ) 함수를 적용하여 개별 행으로 분리
netflix_age_country = netflix.explode('country')
netflix_age_country

# title열의 값이 ‘Sankofa’인 행 전체를 확인하여 country 열과 age_group 열의 값이 어떻게 이루어져 있는지 확인
netflix_age_country[netflix_age_country['title'].str.contains('Sankofa', na=False, case=False)]

# 각 나이 그룹에 따른 국가별 넷플릭스 콘텐츠 수 구하기
netflix_age_country_unstack = netflix_age_country.groupby('age_group')['country'].value_counts().unstack()
netflix_age_country_unstack

# 특정 나이 그룹에 따른 특정 나라별 콘텐츠로 필터링
# 연령, 국가 리스트
age_order = ['All', 'Older Kids', 'Teens', 'Adults']
country_order = ['United States', 'India', 'United Kingdom', 'Canada', 'Japan',
                 'France', 'South Korea', 'Spain', 'Mexico', 'Turkey']

# 데이터 필터링
# .loc[] : 데이터프레임의 행과 열의 이름을 사용
netflix_age_country_unstack = netflix_age_country_unstack.loc[age_order, country_order]

# 결측치 0으로 처리
netflix_age_country_unstack = netflix_age_country_unstack.fillna(0)
netflix_age_country_unstack

# 나이 그룹에 따른 국가별 넷플릭스 콘텐츠 비율 구하기
netflix_age_country_unstack = netflix_age_country_unstack.div(netflix_age_country_unstack.sum(axis=0), axis=1)
netflix_age_country_unstack

plt.figure(figsize=(15, 5))

# 사용자 정의 컬러맵 만들기
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('', ['#221f1f','#b20710','#f5f5f1'])

sns.heatmap(netflix_age_country_unstack, cmap = cmap, linewidth=2.5, annot=True, fmt='.0%')

plt.suptitle('Target ages proportion of total content by country',
             fontweight='bold', fontfamily='serif', fontsize=15)
plt.title('Here we see interesting differences between countries. Most shows in South Korea are targeted to adults, for instance.',
          fontsize=12, fontfamily='serif')
plt.show()

# 넷플릭스 데이터의 description 열 이용한 워드 클라우드 생성

# WordCloud : 워드 클라우드 생성에 필요한 모듈
# Image : 워드 클라우드를 원하는 형태로 그리기 위해 그림을 불러오는 패키지
from wordcloud import WordCloud
from PIL import Image

plt.figure(figsize=(15, 5))

# wordcolud에서 작동할 수 있도록 데이터프레임을 list로 1차 변환시키고 str(문자열)로 2차 변환
text = str(list(netflix['description']))

# mask : 단어를 그릴 위치 설정, 흰색(#FFFFFF) 항목은 마스킹된 것으로 간주
# 로고 이미지 열고 넘파이 배열로 변환
mask = np.array(Image.open('netflix_logo.jpg'))

# 워드 클라우드 색상맵 만들기
cmap = plt.matplotlib.colors.LinearSegmentedColormap.from_list('', ['#221f1f','#b20710'])

# 워드 클라우드 생성
# WordCloud( ).generate(text) : 선언해준 text에서 wordcloud를 생성
wordcloud = WordCloud(background_color = 'white', width = 1400, height = 1400,
                      max_words = 170, mask = mask, colormap=cmap).generate(text)

plt.suptitle('Keywords in the description of Movies and TV shows',
             fontweight='bold', fontfamily='serif', fontsize=15)

# 워드 클라우드 표시
# plt.imshow( ) : array에 색을 채워서 이미지로 표시
plt.imshow(wordcloud)

# 축 감추기
plt.axis('off')
plt.show()