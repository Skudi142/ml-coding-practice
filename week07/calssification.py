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

sgd_clf.predict([some_digit])

# 성능 측정 - 교차 검증을 사용한 정확도 측정
from sklearn.model_selection import cross_val_score

cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")

from sklearn.dummy import DummyClassifier

dummy_clf = DummyClassifier()
dummy_clf.fit(X_train, y_train_5)
print(any(dummy_clf.predict(X_train)))

print(cross_val_score(dummy_clf, X_train, y_train_5, cv=3, scoring="accuracy"))

# 오차 행렬
from sklearn.model_selection import cross_val_predict

y_train_pred = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_train_5, y_train_pred)
print(cm)

y_train_perfect_predictions = y_train_5  # 완벽한 분류기일 경우
print(confusion_matrix(y_train_5, y_train_perfect_predictions))

# 정밀도와 재현율
from sklearn.metrics import precision_score, recall_score

print(precision_score(y_train_5, y_train_pred))  # == 3530 / (687 + 3530)

print(recall_score(y_train_5, y_train_pred))  # == 3530 / (1891 + 3530)

from sklearn.metrics import f1_score

print(f1_score(y_train_5, y_train_pred))

# ROC 곡선
from sklearn.metrics import roc_auc_score

y_scores = cross_val_predict(sgd_clf, X_train, y_train_5, cv=3,
                             method="decision_function")
roc_auc_score(y_train_5, y_scores)

#다음은 실행하는데 몇 분이 걸릴 수 있음
from sklearn.ensemble import RandomForestClassifier
