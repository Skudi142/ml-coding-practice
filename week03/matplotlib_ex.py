# -*- coding: utf-8 -*-
# 타이타닉 데이터셋 불러오기
import pandas as pd

# 타이타닉 csv 파일 불러오기
titanic = pd.read_csv('3.1.1.titanic.csv')

# head( ) 함수를 출력하여 타이타닉 데이터셋의 구성을 간단히 살펴보기

# 데이터 처음 5개의 행 출력
print(titanic.head())

# 열에 대한 요약 정보 확인
print(titanic.info())

"""### **선 그래프 : 객실 등급에 따른 생존율 표시하기**"""

# 객실 등급에 따른 생존자와 사망자의 평균 계산
pclass_survivied_maen = titanic.groupby('Pclass')['Survived'].mean().reset_index()
pclass_survivied_maen

# 맷플롯립 라이브러리 불러오기
import matplotlib.pyplot as plt

# 선 그래프 그리기
plt.plot(pclass_survivied_maen['Pcalss'], pclass_survivied_maen['Survived']),
    marker='o', linestyle='-', color='violet')