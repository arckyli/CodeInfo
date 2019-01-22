#!/usr/bin/env python3 
#coding: utf-8
import requests
from bs4 import BeautifulSoup 
from urllib.parse import urlencode
from requests import RequestException
from json.decoder import JSONDecodeError
import json,time
import pandas as pd

def get_page_index(): 
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    url = 'https://www.zhipin.com/job_detail/'
    try:
        response = requests.get(url=url,headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')

def job_city_list(html):
    if html:
        html = BeautifulSoup(html,'lxml')
        citys = html.select(".city-wrapper a")    
        for city in citys: 
            if city.attrs['href'] != 'javascript:;':
                
                yield {
                    city.get_text(): city.attrs['ka'].split('-')[2]
                }


def get_page_detail(scity): 
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    data = {
        'query': u'高级网络工程师',
        'scity': scity,
    }
    url = 'https://www.zhipin.com/job_detail/'
    try:
        time.sleep(3)
        response = requests.post(url=url,headers=header,data=data)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求失败')
        

                
def job_list(html):
    if (html):
        soup = BeautifulSoup(html,'lxml')
        jobs = soup.select('.job-list ul li')
        for job_list in jobs:
            yield {
                '公司名称': job_list.select('.company-text h3 a')[0].text,
                '公司信息': job_list.select('.company-text p')[0].text,
                '招聘职位': job_list.select('.job-title')[0].text,
                '基本工资': job_list.select('.red')[0].text,
                '工作地点': job_list.select('.info-primary p')[0].text.split(' ')[0],
                }
    
def job_list_detail(k):
    df = pd.DataFrame(k)   
    print(df)             
        
def run():
    k = []
    response = get_page_index()
    for scity in job_city_list(response):
        html=get_page_detail(list(scity.values())[0])
        for job in job_list(html):
            k.append(job)
        job_list_detail(k)
    
    
if __name__ == '__main__':
    run()
