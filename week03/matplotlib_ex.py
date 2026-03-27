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
for i, value in enumerate(survived_counts):
    plt.text(i, value + 1, str(value), ha='center', va='bottom')

plt.savefig('Figure02.png')
plt.close()

"""### **수평 막대 그래프 : 성별에 따른 생존자 수 확인하기**"""

# 성별에 따른 생존자의 수 계산
survived_counts = titanic[titanic['Survived'] == 1]['Sex'].value_counts()
print(survived_counts)

# 수평 막대 그래프 그리기
bars = plt.barh(survived_counts.index, survived_counts, color=['darkturquoise', 'salmon'])
plt.title('Survived Counts by Gender on Titanic')
plt.xlabel('Count')
plt.ylabel('Gender')
plt.legend(bars, ['Survived - Female', 'Survived - Male'], loc='upper right')

# 차이 강조를 위해 수평선 추가
plt.axvline(x=survived_counts['male'], color='gray', linestyle='--', linewidth=1)

# 생존자 수 표시
for i, value in enumerate(survived_counts):
    plt.text(value + 1, i, str(value), ha='left', va='center')

plt.savefig('Figure03.png')
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
           labels=['Not Survived', 'Survived'], loc='upper right')
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
plt.fill_between(survived_counts.index.astype(str), survived_counts[1],
                 color='purple', alpha=0.9, label='Survived')

# 나이대별 사망자
plt.fill_between(survived_counts.index.astype(str), survived_counts[0],
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
             labels=['1st Class', '2nd Class', '3rd Class'])

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

# showmeans=False는 평균값을 표시하지 않도록 하고, showmedians=True는 중앙값을 표시하도록 함
violin_plot = plt.violinplot([titanic[titanic['Pclass'] == 1]['Age'],
                              titanic[titanic['Pclass'] == 2]['Age'],
                              titanic[titanic['Pclass'] == 3]['Age']],
                              showmeans=False, showmedians=True)

plt.title('Violin Plot of Age by Pclass')
plt.xlabel('Pclass')
plt.ylabel('Age')

# x축의 눈금 설정
plt.xticks([1, 2, 3], ['1st Class', '2nd Class', '3rd Class'])

# 범례 설정
plt.legend(violin_plot['bodies'], ['1st Class', '2nd Class', '3rd Class'],
           title='Pclass', loc="upper right")
plt.savefig('Figure10.png')
plt.close()

## **에러 바 : 요금의 평균과 표준편차 표현하기**

# 각 부모와 자녀의 수에 대한 요금의 평균과 표준 편차 계산
fare_means = titanic.groupby('Parch')['Fare'].mean()  # 평균
print(fare_means, '\n')

fare_std = titanic.groupby('Parch')['Fare'].std()     # 표준 편차
print(fare_std)

"""* 에러바는 데이터의 표준 편차를 나타내는 경우에는 길이가 길수록 해당 그룹의 데이터가 퍼져 있음을 의미"""

# 에러바로 요금의 평균과 표준 편차 표현
plt.figure(figsize=(10, 6))

# 에러바 생성
plt.errorbar(fare_means.index, fare_means, yerr=fare_std, fmt='o',
             capsize=5, capthick=1, label='Fare')

plt.title('Error Bar Plot of Fare by Parch')
plt.xlabel('Parch')
plt.ylabel('Fare')
plt.xticks(fare_means.index)
plt.legend()
plt.savefig('Figure11.png')
plt.close()

## **개별 서브플롯을 하나씩 생성하기**
plt.subplot(2, 2, 1)
plt.plot([1, 2, 3])

plt.subplot(2, 2, 2)
plt.plot([4, 5, 6])

plt.subplot(2, 2, 3)
plt.plot([7, 8, 9])

plt.subplot(2, 2, 4)
plt.plot([10, 11, 12])
plt.savefig('Figure12.png')
plt.close()

## **타이타닉 데이터셋으로 개별 서브플롯 하나씩 그리기**

# Survived가 0이면 사망자를, 1이면 생존자를 나타냄
titanic = pd.read_csv('3.1.1.titanic.csv')

# 각 부모와 자녀의 수에 따른 생존자와 사망자 수 계산
parch_counts = titanic.groupby('Parch')['Survived'].value_counts().unstack().fillna(0)
print(parch_counts)

# x, y 설정
x = parch_counts.index.astype(str) # 데이터프레임의 인덱스를 문자열로 반환
y1 = parch_counts[0].values # 사망자
y2 = parch_counts[1].values # 생존자

plt.figure(figsize=(10, 10))

# plt.subplot() 함수를 사용하여 하나의 그림인 figure에 개별 서브플롯을 하나씩 추가
# 첫 번째 서브플롯 설정(선 그래프)
plt.subplot(2, 1, 1)
# 선 그래프 그리기
plt.plot(x, y1, '-o', color='indigo', markersize=7, linewidth=3, alpha=0.7,
         label='Not Survived')
plt.xlabel('Parch')
plt.ylabel('Not Survived Count', color='indigo')
plt.tick_params(axis='y', labelcolor='indigo')
plt.legend(loc='upper right')

# 두 번째 서브프롯 설정(막대 그래프)
plt.subplot(2, 1, 2)
plt.bar(x, y2, color='deeppink', alpha=0.7, width=9.5, label='Survived')