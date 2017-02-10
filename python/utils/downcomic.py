#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import time

headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept':'*/*',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate, br',
        }

def saveImg(imageURL, fileName):
    resp = requests.get(imageURL, headers = headers)
    if resp.status_code == 200:
        with open(fileName, 'wb') as f:
            f.write(resp.content)

def get_page(episode):
    s = requests.Session()
    url = 'http://www.cncomico.com/detail.nhn?titleNo=49&articleNo='+str(episode)
    req = s.get(url, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')    
    h1_tag = soup.find('h1', class_='title02__title01 _contribTitle')
    title = str(episode)+h1_tag.text
    p_tag = soup.find('p', class_='block04__area02')
    os.mkdir(title)
    print('saving' + url)
    for img in p_tag.findAll('img'):
        img_src = img['src']
        path = title+'/'+ img_src.split('/')[-1]
        saveImg(img['src'], path)

    print(str(episode)+'done')

if __name__ == '__main__':
    for x in range(61,89): 
        time.sleep(5)
        get_page(x)