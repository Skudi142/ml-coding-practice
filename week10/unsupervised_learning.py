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

k = 5
kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
y_pred = kmeans.fit_predict(X)

def plot_clusters(X, y=None):
    plt.scatter(X[:, 0], X[:, 1], c=y, s=1)
    plt.xlabel("$x_1$")
    plt.ylabel("$x_2$", rotation=0)

plt.figure(figsize=(8, 4))
plot_clusters(X)
plt.gca().set_axisbelow(True)
plt.grid()
plt.show()

# 각 샘플은 5개의 클러스터 중 하나에 할당
print(y_pred)

# 5개의 _센트로이드_(즉, 클러스터 중심)을 추정
print(kmeans.cluster_centers_)

print(kmeans.labels_)

# 이너셔
print(kmeans.inertia_)

print(kmeans.score(X))
