# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

import numpy as np

np.random.seed(42)                        # 코드 예제를 재현 가능하게 만들기 위해
m = 100                                   # 샘플 개수
X = 2 * np.random.rand(m, 1)              # 열 벡터
y = 4 + 3 * X + np.random.randn(m, 1)     # 열 벡터

import matplotlib.pyplot as plt

plt.figure(figsize=(6, 4))
plt.plot(X, y, "b.")
