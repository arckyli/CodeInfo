#!/usr/bin/env python3
#coding:utf-8
import requests,json
from requests import RequestException
from bs4 import BeautifulSoup

def get_page_index():
    url = 'https://book.douban.com/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")

def parse_page_detail(html):
    soup = BeautifulSoup(html,'lxml')
    m = soup.select('.slide-list li')
    try:
        for k in m:
            yield {
                'title': k.select('.cover a')[0].attrs['title'],
                'link': k.select('.cover a')[0].attrs['href'],
                'autho': k.select('.author')[0].string.strip(),
                'abstract':k.select('.abstract')[0].string.strip(),
                'img': k.select('.cover img')[0].attrs['src'],
            }
    except:
        pass

def main():
    html =get_page_index()
    for result in parse_page_detail(html):
        print (result)
    
if __name__ == '__main__':
    main()
