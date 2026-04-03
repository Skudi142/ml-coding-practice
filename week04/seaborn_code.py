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
snssns.stripplot(x='day', y='tip', hue='sex', data=tips, alpha=0.7, ax=ax1)