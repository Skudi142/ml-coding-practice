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