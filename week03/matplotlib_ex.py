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
pclass_survivied_mean = titanic.groupby('Pclass')['Survived'].mean().reset_index()
pclass_survivied_mean

# 맷플롯립 라이브러리 불러오기
import matplotlib.pyplot as plt

# 선 그래프 그리기
plt.plot(pclass_survivied_mean['Pclass'], pclass_survivied_mean['Survived'],
    marker='o', linestyle='-', color='violet')
plt.title('Survived Rate Varlation Across Passenger Classes')
plt.xlabel('Pclass')
plt.ylabel('Survival Rate')
plt.xticks([1, 2, 3])
plt.grid(True)
plt.savefig('Figure01.png')         # 결과를 그림파일로 저장
plt.close()                         # 다음 Plot를 새로 그리기 위해 plt 닫기

"""### **수직 막대 그래프 : 각 승선 항구에 따른 생존자 수 확인하기**"""

# 승선 항구에 따른 생존자의 수 계산
survived_counts = titanic[titanic['Survived'] == 1]['Embarked'].value_counts()
print(survived_counts)

# 막대 그래프 그리기
plt.bar(survived_counts.index, survived_counts,
        color = ['mediumorchid', 'darkviolet', 'indigo'])
plt.title('Survived Counts by Embarked Port on Titanic')
plt.xlabel('Embarked Port')
plt.ylabel('Count')
plt.xticks(survived_counts.index, ['Southampton', 'Cherbourg', 'Queentown'])
plt.legend(['Survived'], loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 생존자 수 표시
for i, value in cnumerate(survived_counts):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')

plt.savefig('Figure02.png')
plt.close()

"""### **수평 막대 그래프 : 성별에 따른 생존자 수 확인하기**"""

# 성별에 따른 생존자의 수 계산
survived_counts = titanic[titanic['Survived'] == 1]['Sex'].value_counts()
print(survived_counts)

# 수평 막대 그래프 그리기
bars = pit.barh(survived_counts.index, survived_counts, color=['darkturquoise', 'salmon'])
plt.title('Survived Counts by Gender on Titanic')
plt.xlabel('Count')
plt.ylabel('Gender')
plt.legend(bars, ['Survived - Female', 'Survived - Male'], loc='upper right')

# 차이 강조를 위해 수평선 추가
plt.axvline(x=survived_counts['male'], color='gray', linestyle='--', linewidth=1)

# 생존자 수 표시
for i, value in enumerate(survived_counts):
    plt.text(value + 1, i, str(value), he='left', va='center')

plt.savefig('Figur03.png')
plt.close()

"""### **산점도 그래프 : 나이와 요금, 생존 여부 확인하기**"""

print(titanic.info(), '\n')

# 결측치 처리
titanic = titanic.dropna(subset=['Age', 'Fare', 'Survived'])
print(titanic.info())

# 산점도 그래프 그리기
plt.figure(figsize=(12, 8))
scatter = plt.scatter(x='Age', y='Fare', data=titanic, c=titanic['Survived'],cmap='Set2', alpha=0.7)

plt.title('Age and Fare Relationship with Survival on the Titanic')
plt.xlabel('Age')
plt.ylabel('Fare')
plt.legend(handles=scatter.legend_elements()[0], title='Survived',
           labels=['Not Survived', 'Survived'], ;oc='upper right')
plt.savefig('Figure04.png')
plt.close()

"""### **파이 차트 : 생존자, 사망자 비율 표현하기**"""

# 사망자와 생존자의 수 계산
survived_counts = titanic['Survived']. value_counts()
print(survived_counts)

# 파이 차트 그리기
plt.figure(figsize=(8, 8))
plt.pie(survived_counts, labels=['Not Survived', 'Survived'], colors=['orange', 'gold'],
        autopct='%0.1f%%', startangle=90, shadow=True, explode=(0, 0.1))

plt.title('Survival Distribution on the Titanic')
plt.savefig('Figure05.png')
plt.close()

"""### **히스토그램 : 승객의 나이 분포 표시하기**"""

# 처리 전
print(titanic.info(), '\n')

# 나이 결측치 처리 후
titanic = titanic.dropna(subset=['Age'])
print(titanic.info())

# 히스토그램 그리기
plt.figure(figsize=(10, 6))
plt.hist(titanic['Age'], bins=20, color='seagreen',edgecolor='black')

plt.xlabel('Age')
plt.ylabel('Count')
plt.title('Distribution of Ages on the Titanic')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('Figure06.png')
plt.close()

## 히트맵 : 두 변수의 상관 관계를 표시하기**

# 결측치 처리
titanic = titanic.dropna(subset=['Age', 'Fare'])

# 상관 행렬 계산
correlation_matrix = titanic.drop('Passengerld', axis=1).corr(numeric_only=True)
print(correlation_matrix)

# 히트맵 그리기
plt.matshow(correlation_matrix, cmap='PuRd_r')
plt.colorbar()

# x축과 y축의 눈금 설정
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix)

plt.title('Correlation Heatmap of Titanic')
plt.savefig('Figure07.png')
plt.close()

## **영역 채우기 그래프 : 나이대별 생존자와 사망자 수 표현하기**

# 결측치 처리
titanic = titanic.dropna(subset=['Age', 'Fare'])

# 나이대별 생존자와 사망자 수 계산하기 위해 버주형 변수로 전환 
age_groups = pd.cut(titanic['Age'], bins=range(0, 81, 5))

# Age, Survived 기준으로 그룹화
survived_counts = titanic.groupby([age_groups, 'Survived'], observed=False).size().unstack().fillna(0)
print(survived_counts)

# 영역 채우기 그래프 그리기
plt.figure(figsize=(10, 6))

# 나이대별 생존자
plt.fill_between(survived_counts.index,astype(str), survived_counts[1],
                 color='purple', alpha=0.9, label='Survived')

# 나이대별 사망자
plt.fill_between(survived_counts.index,astype(str), survived_counts[0],
                 color='hotpink', alpha=0.6, label='Not Survived')

plt.title('Survival by Age Group on Titanic')
plt.xlabel('Age')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.savefig('Figure08.png')
plt.close()

## **박스 플롯 : 승객 나이의 데이터 분포, 중앙값, 이상치 살펴보기**

# 결측치 처리
titanic = titanic.dropna(subset=['Age'])
print(titanic.info())

# 승객 등급에 따른 나이의 박스 플롯
plt.boxplot([titanic[titanic['Pclass'] == 1]['Age'],
             titanic[titanic['Pclass'] == 2]['Age'],
             titanic[titanic['Pclass'] == 3]['Age']],
             labels=['1st Class', '2nd Class, 3rd Class'])

plt.title('Box Plot for Age by Pclass')
plt.xlabel('Pclass')
plt.ylabel('Age')
plt.savefig('Figure09.png')
plt.close()

"""### **바이올린 플롯 : 승객 등급에 따른 나이 분포 표시하기**"""

# 결측치 처리
titanic['Age'] = titanic['Age'].fillna(titanic['Age'].mean())
print(titanic.info())

# 바이올린 플롯 그리기
plt.figure(figsize=(10, 6))