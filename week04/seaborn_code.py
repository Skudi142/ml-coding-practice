# -*- coding: utf-8 -*-

# 시본 라이브러리 불러오기
import seaborn as sns

# **팁(tips) 데이터셋 불러오기**
tips = sns.load_dataset('tips')
print(tips.head())

# ** 범주형 변수 산점도 그래프**

import matplotlib.pyplot as plt