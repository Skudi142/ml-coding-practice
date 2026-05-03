# -*- coding: utf-8 -*-
from sklear.datasets import fetch_openml

mnist = fetch_openml('mnist_784', as_frame=False)

print(mnist.keys())  # data와 target만 사용

X, y = minst.data, mnist.target
print(X)
print(X.shape)        # 28 x 28 개의 픽셀 특징을 가진 이미지 70,000개
print(u)
print(u.shape)