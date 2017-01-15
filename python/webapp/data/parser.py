#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup

from DataModel import Movie




def get_movie_from_web(item_id, movie):
    url = 'http://movie.douban.com/subject/' + item_id    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'accept':'text/html, application/xhtml+xml, image/jxr, */*'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    info = soup.select('#info')[0]
    texts = [text for text in info.stripped_strings]
    # print(info.get_text("|", strip=True))
    index = 0
    for text in texts:        
        if text == '语言:':
            print(text, texts[index+1])
            movie.language = texts[index+1].strip()
        if text == '首播:' or text == '上映日期:':
            datestr = texts[index+1].split('(')[0]
            print(text, datestr.strip())
            movie.pubdates = datetime.datetime.strptime(datestr.strip(), '%Y-%m-%d')
            
        if text == '单集片长:' or text == '片长:':
            duration = texts[index+1].split('分')[0]
            print(text, duration.strip())
            movie.duration = int(duration.strip())       
        
        index+=1

def get_movie_from_api(item_id):
    api_url = "http://api.douban.com/v2/movie/subject/" + item_id
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'accept':'text/html, application/xhtml+xml, image/jxr, */*'}
    resp = requests.get(api_url, headers=headers)
    if resp.status_code == requests.codes.ok:
        data = resp.json()
        movie = Movie(
            subid=data['id'], 
            title=data['title'], 
            original_title=data['original_title'],
            alt = data['alt'],
            rating = data['rating']['average'],
            collect_count = data['collect_count'],
            images = data['images']['medium'],
            subtype = data['subtype'],                       
            year = data['year'],
            genres = data['genres'][0],
            countries = data['countries'][0],
            summary = data['summary'],
            current_season = data['current_season'],
            episodes_count = data['episodes_count'],
            )
        if len(data['directors'])>0:
            movie.director = data['directors'][0]['name']

        get_movie_from_web(item_id, movie)
        return movie

    




