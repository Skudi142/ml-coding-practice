# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')  # 윈도우: 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False  # 마이너스(-) 기호 깨짐 방지

plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# K-평균
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

blob_centers = np.array([[ 0.2,  2.3], [-1.5 ,  2.3], [-2.8,  2.8],
                         [-2.8,  4.2], [-2.8,  1.0]])
blob_std = np.array([0.4, 0.3, 0.1, 0.1, 0.1])
X, y = make_blobs(n_samples=2000, centers=blob_centers, cluster_std=blob_std,
                  random_state=7)