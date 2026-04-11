# -*- coding: utf-8 -*-
import urllib.request
import datetime
import json
import pandas as pd

ServiceKey = ""

"""### [CODE 0]"""

def main():
    jsonResult = []
    result = []

    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >> ")
    nat_cd = input('국가 코드를 입력하세요(중국 : 112 / 일본: 130 / 미국: 275) :')
    nStartYear = int(input('데이터를 몇 년 부터 수입할까요? : '))
    nEndYear = int(input("데이터를 몇 년 까지 수집할까요? :"))
    ed_cd = "E" 		                      # E : 방한외래관광객, D : 해외 출국

    jsonResult, result, natName, dataEND = getTourismStarsService(nat_cd, ed_cd, nStartYear, nEndYear)  #[CODE 3]

    #파일저장 : csv 파일
    columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
    result_df = pd.DataFrame(result, columns = columns)
    result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed_cd, nStartYear, dataEND), index = False, encoding = 'cp949')

    """### [CODE 3]"""