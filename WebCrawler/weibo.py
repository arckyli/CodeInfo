import requests,json
from requests import RequestException
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

def get_page_index(page):
    params = {
        'page':page
    }
    headers = {
    'Host': 'm.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    }
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0' 
    url = url + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except RequestException:
        print("请求索引页出错")

def parse_page_detail(html):
    if html:
        items = html.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if item:
                weibo = {}
                weibo['id'] = item.get('id')
                
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo


def main():
    for page in range(1,5):
        html =get_page_index(page)
        result=parse_page_detail(html)
        for res in result:
            print (res)
    
if __name__ == '__main__':
    main()
