# -*- coding: utf-8 -*-
from sklear.datasets import fetch_openml

mnist = fetch_openml('mnist_784', as_frame=False)

print(mnist.keys())  # data와 target만 사용

X, y = minst.data, mnist.target
print(X)
print(X.shape)        # 28 x 28 개의 픽셀 특징을 가진 이미지 70,000개
print(y)
print(y.shape)

import matplotlib.pyplot as plt

def plot_digit(image_data):
    image = image_data.reshape(28, 28)
    plt.imshow(image, cmap="binary")
    plt.axis("off")

some_digit = X[0]
plot_digit(some_digit)
plt.show()

print(y[0])         # 샘플 데이터 레이블 확인 (=5)

# 10x10 그림 생성
plt.figure(figsize=(9, 9))
for idx, image_data in enumerate(X[:100]):
    plt.subplot(10, 10, idx + 1)
    plot_digit(image_data)
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()

# train/test 데이터셋 나누기
X_train, X_test, y_trian, y_test = X[:60000], X[60000:], y[:60000], y[60000:]

# 이진 분류기 훈련
y_train_5 = (y_train == '5')  # 5인 경우 True, 나머지는 False
y_test_5 = (y_test == '5')

from sklearn.linear_model import SGDClassifier

sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_5)

