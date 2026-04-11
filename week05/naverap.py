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

    def getNaverSearcch(node, srrcText, page_start, display):
        base = "https://openapi.naver.com/v1/search"
        node = "/%s.json" % node
        parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), page_start, display)

        url = base + node + parameters
        responseDecode = getRequestUrl(url)               #[CODE 1]

        if (responseDecode == None):
            return None
        else:
            return json.loads(responseDecode)
        
    def getRequestUrl(url):
        req = urrllib.request.Request(url)

        req.add_header("X-Naver-client-Id", client_id)
        req.add_header("X-Naver-client-Secret", client_secret)

        try:
            respion = urllib.request.urlopen(req)
            if response.getcode() == 200:
                print("[%s] Url Request Success" % (datetime.datetime.now(), url))