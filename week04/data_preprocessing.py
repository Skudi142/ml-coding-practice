# -*- coding: utf-8 -*-

# 데이터 준비
import numpy as np
import pandas as pd

housing = pd.read_csv('./week04/housing.csv')       # 오류 발생 시, ./housing.csv 파일로도 시도

# 테스트 세트 만들기
from sklearn.model_selection import train_test_split


housing["income_cat"] = pd.cut(housing["median_income"],
                               bins=[0., 1.5, 3.0,`jnmmmmmmmmmmmmmmmmmmmmmmm`])