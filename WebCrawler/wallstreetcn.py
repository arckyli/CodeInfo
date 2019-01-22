#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from requests import RequestException
from json.decoder import JSONDecodeError
import json 
import base64
import time
import random


headers = {
        'origin': 'https://wallstreetcn.com',
        'referer': 'https://wallstreetcn.com/news/global',  
        'User-Agent'  : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        
def get_page_index(page):
    # 构造Base64函数
    info= ''.join(str(random.choice(range(10))) for _ in range(10))
    data = {"SlotOffset": 0,
                 "TotalCount":page,
                "ArticleLe":info
    }
    params = {
        'channel': 'global',
        'accept' : 'article',
        'cursor' :  base64.b64encode(json.dumps(data).encode('utf-8')) ,
        'limit'    : '20',
    }
    url = 'https://api-prod.wallstreetcn.com/apiv1/content/fabricate-articles?' + urlencode(params)
    try:
        time.sleep(1)
        response = requests.get(url=url, headers=headers, params=data)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print('请求失败')
        
def get_page_detail(info):
    if info:
        info = info.get('data').get('items')
        for item in info:
            item = item.get('resource')
            if item:
                yield {
                    'title'   : item.get('title'),
                    'content_short' :   item.get('content_short'),                
                }

def run():    
    page = [[(i+1)*20]  for i in range(5)]   
    info = get_page_index(page)
    for news in get_page_detail(info):
        print (news)
    
if __name__ == '__main__':
    run()
