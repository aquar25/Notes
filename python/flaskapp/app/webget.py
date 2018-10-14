#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re

def download_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36Name'}
    page = requests.get(url=url, headers=headers)
    page.encoding = 'utf-8'
    with open('tmp.html', 'w', encoding='utf-8') as fd:
        fd.write(page.text)

#"http://res.wx.qq.com/voice/getvoice?mediaid=MzIxMDAzNzE0M18yNDU4ODEwMTM1"
def get_audio_url():
    with open('tmp.html', 'r', encoding='utf-8') as fd:
        data = fd.read()
        #data = '"pxx" url: "http://res.wx.qq.com/voice/getvoice?mediaid=MzIxMDAzNzE0M18yNDU4ODEwMTM1"'
        pattern = re.compile(r'"(http://res.wx.qq.com/voice/getvoice.*)"')
        match = re.findall(pattern, data)
        print(match)

if __name__ == '__main__':
    download_url('https://mp.weixin.qq.com/s?__biz=MzI4MDY4MDY1MA==&mid=2247483771&idx=2&sn=d63b203346dfee2b0a94b6649531a004&chksm=ebb580dedcc209c8f3bad3dd2394f04ff56b83d43570fe35c58411a6e6deb15aa87ef1d43fea&scene=21')
    #print(get_audio_url())


