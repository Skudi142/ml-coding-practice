# -*- coding: utf-8 -*-

# 시본 라이브러리 불러오기
import seaborn as sns

# **팁(tips) 데이터셋 불러오기**
tips = sns.load_dataset('tips')
print(tips.head())

# ** 범주형 변수 산점도 그래프**

import matplotlib.pyplot as plt

# figure에 2개의 서브 플롯을 생성
fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# stripplot( ) 그리기
sns.stripplot(x='day', y='tip', hue='sex', data=tips, alpha=0.7, ax=ax1)

# swarmplot( ) 그리기
snssns.stripplot(x='day', y='tip', hue='sex', data=tips, palette='Set2', alpha=0.7, ax=ax2)

# 서브 플롯의 제목 설정
ax1.set_title('Strip Plot of Tip by Day and Gender')
ax2.set_title('Swarm Plot of Tip by Day and Gender')
plt.savefig('./week04/Seaborn_Figure01.jpg')

# **빈도 그래프**
# figure에 2개의 서브 플롯을 생성
fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# 식사가 이루어진 시간대 파악

# x축 변수, 데이터셋, axe 객체(1번째 그래프)
sns.countplot(x='time', data=tips, ax=ax1)

# 식사가 이루어진 시간대 파악과 식사가 이루어진 요일로 색상 분류
# x축 변수, hue로 색상 분류, 데이터 셋, 색상 설정, axe 객체(2번째 그래프)
sns.countplot(x='time', hue='day', data=tips, palette='Set2', ax=ax2)

ax1.set_title('Frequency of Tips by Time')
ax2.set_title('Frequency of Tips by Time and Day')
plt.savefig('./week04/Seaborn_Figure02.jpg')

# **선형 회귀선 있는 산점도**
# figure에 2개의 서브 플롯을 생성
fig = plt.figure(figsize=(15, 5))
ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2)

# 산점도에 선형 회귀선 표시(fit_reg=True)
sns.regplot(x='total_bill', y='tip', data=tips, color='blue', scatter_kws={'s': 50, 'alpha: 0.5'}, line_kws={'linestyle': '--'}, ax=ax1)

# 산점도에 선형 회귀선 미표시(fit_reg=False)
sns.regplot(x='total_bill', y='tip', data=tips, color='blue', scatter_kws={'s': 50, 'alpha: 0.5'}, line_kws={'linestyle': '--'}, ax=ax1)