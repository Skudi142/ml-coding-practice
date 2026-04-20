# -*- coding: utf-8 -*-
import urllib.request
import datetime
import json

client_id = "w4mKgei7nXxK78IxPOY6"
client_secret = "8J3bOoYQgu"

def main() :

    node = 'news'                                             # 크롤링할 대상
    srcText = input('검색어를 입력하세요: ')

    cnt = 0
    jsonResult = []

    jsonResponse = hetNaverSearch(node, srcText, 1, 100)      # [CODE 2]
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)) :
        for post in jsonResponse['items'] :
            cnt += 1
            getPostData(post, jsonResult, cnt)                 # [CODE 3]

            start = jsonResponse['start'] + jsonResponse['display']
            jsonResponse = getNaverSearch(node, srcText, start, 100)  # [CODE 2]

            print('전체 검색 : %d 건' % total)

            with open('%s_naver_%s.json' % (srcText, node), 'w', encoding = 'utf-8') as outfile :
jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True,
    ensure_ascii = False)

    outfile.write(jsonFile)
