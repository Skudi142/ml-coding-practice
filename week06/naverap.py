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