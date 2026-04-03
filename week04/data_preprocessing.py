# -*- coding: utf-8 -*-

# 데이터 준비
import numpy as np
import pandas as pd

housing = pd.read_csv('./week04/housing.csv')       # 오류 발생 시, ./housing.csv 파일로도 시도

# 테스트 세트 만들기
from sklearn.model_selection import train_test_split

housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                                labels=[1, 2, 3, 4, 5])

strat_train_set, strat_test_set = train_test_split(
    housing, test_size=0.2, stratify=housing["income_cat"], random_state=42)

for set_ in (strat_train_set, strat_train_set):
    set_.drop("income_cat", axis=1, inplace=True)

"""
* 원본 훈련 세트로 복원하고 타킷을 분리
* 'strat_train_set.drop()'은 지정한 열을 제외한 'strat_train_set'의 복사본을 만듦
* 'inplace=True'로 지정하지 않은 한 'strat_train_set' 자체를 수정하지 않음
"""

housing = strat_test_set.drop("median_house_value", axis=1)
housing_labels = strat_test_set["median_house_value"].copy()

# 데이터 정체
# null 값이 있는 행 확인하기
null_rows_idx = housing.isnull().any(axis=1)
housing.loc[null_rows_idx].head()

form sklearn.impute import Simplelmputer
