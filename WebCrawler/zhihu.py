#!/usr/bin/evn python3 
#coding:utf-8

import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from requests import RequestException
from json.decoder import JSONDecodeError
import json 
import pandas as pd 

def get_page_index(offset):
    params ={
        'limit' : 20,
        'offset': offset,
    }
    headers = {
        'Host': 'zhuanlan.zhihu.com',
        'Referer': 'https://zhuanlan.zhihu.com/pythoncrawl',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',     
    }
    
    url = 'https://zhuanlan.zhihu.com/api2/columns/pythoncrawl/articles?'
    url = url + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200: 
            return response.json()
        return None
    except RequestException:
        print('请求索引失败')
        
def parse_page_index(html):
    if html:
        items = html.get('data')
        for item in items:
            if item:
                yield {
                    'title'   : item['title'],
                    'url'     : item['url'],
                    'name'    : item['author']['name'],
                    'headline': item['author']['headline'],
                    'des'     : item['author']['description']
                }
                
def parse_page_detail(res_list):
    df = pd.DataFrame(res_list)
    print(df)     
        
def run():
    for offset in range (1,10):
        html = get_page_index(offset*10)
        for res in   parse_page_index(html):
            print(res)
      
    
if __name__ == '__main__':
    run()
