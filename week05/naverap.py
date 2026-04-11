# -*- coding: utf-8 -*-
import urllib.request
import datetime
import json

client_id = "YOUR_CLIENT_ID"  # 네이버 개발자 센터에서 발급받은 Client ID
client_secret = "YOUR_CLIENT_SECRET"  # 네이버 개발자 센터에서 발급받은 Client Secret

def main():

    node = 'news'                                             # 크롤링할 대상
    srcText = input('검색어를 입력하세요: ')

    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)      # [CODE 2]
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonRespionse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)                 # [CODE 3]
        
        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  # [CODE 2]

        print('전체 검색 : %d 건' %total)

        with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf-8') as outfile:
            jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True,
                                  ensure_ascii = False)
            
            outfile.write(jsonFile)

        print('가져온 데이터 : %d 건' %cnt)
        print('%s_naver_%s.json SAVED' % (srcText, node))