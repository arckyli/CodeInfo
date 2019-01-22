#!/usr/bin/env python3 

import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from requests import RequestException
from json.decoder import JSONDecodeError
import json ,re
import base64
import time
import random


headers = {
        'User-Agent'  : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Host'  :  'www.douban.com',
    }
url = 'https://www.douban.com/search?'

def get_page_info():

    try:
        response = requests.get(url,headers=headers)
    
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')

def  get_search_id(page_info):
    soup = BeautifulSoup(page_info,'lxml')
    items = soup.select('.search-cate li a')
    for item in items:
        search_name = item.get_text()
        item =item['href'].split('?')
        search_id = re.findall('(\d+)',str(item))
        if search_id:
            yield{
                search_name : search_id[0]
            }
            
def get_key_valuse(info):
    for k in info:
        if k == '电影':
            movie = list(info.values())[0]
            return movie
        
def get_movie_index(m): 
    url = 'https://www.douban.com/search?'
    data = {
        'cat': m,
        'q': '张国荣',
    }
    url = url+ urlencode(data)
    try:
        response = requests.get(url,headers=headers)
    
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')
    
def get_movie_info(m_info): 
    soup = BeautifulSoup(m_info,'lxml')
    items = soup.select('.result')
    for item in items:
        yield{
            '分类' : item.select('h3 span')[0].text,
            '片名' : item.select('.subject-cast')[0].text,
            '详细' : item.select('p')[0].text,
        }
    
def run():
    page_info = get_page_info()
    for info in get_search_id(page_info):
        m=get_key_valuse(info)
        if m:
            m_info = get_movie_index(m)
            for move in get_movie_info(m_info):
                print(move)
                

if __name__ == '__main__':
    run()
