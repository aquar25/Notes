#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
from dbhelper import SqliteDBHelper, ItemChecker, DBHelper
from DataModel import BaseItem
from DataModel import Movie

import matplotlib.pyplot as plt
import matplotlib as mlp
import parser


sqliteHelper = SqliteDBHelper("douban.db")

def handle_page(idx, checker):
    url1 = "http://movie.douban.com/people/aquar25/collect?start=" \
          + str(idx) + \
          "&sort=time&rating=all&filter=all&mode=list"
    url2 = "http://movie.douban.com/people/aquar25/collect?sort=time&amp;start=" \
          +str(idx) + \
          "&amp;filter=all&amp;mode=grid"
    print("handle page " + str(idx) + ".....")
    tmpfile = "grid.html"
    if True or not os.path.exists(tmpfile):
        page = requests.get(url2)
        with open(tmpfile, "w+", encoding="utf-8" ) as outfile:
            print("write file....")
            outfile.write(page.text)
            data = page.text
    else:
        with open(tmpfile, "r", encoding="utf-8") as datafile:
            data = datafile.read()

    soup = BeautifulSoup(data, "html.parser")
    gridview = soup.select('div[class="grid-view"]')[0]
    items = gridview.find_all('div', class_="item")
    baseItems = []
    go_on = True
    for item in items:
        picName = item.div.a.img['alt']
        picURL = item.div.a.img['src']
        infos = item.find_all('li')
        movieURL = infos[0].a['href']
        movieName = infos[0].a.em.string.strip()
        ratespan = infos[2].find('span', class_=re.compile('rat'))
        rateNum = 0
        if ratespan:
            # rating3-t , only use 3
            rateNum = int(ratespan['class'][0].split('-')[0][-1])

        datespan = infos[2].find('span', class_=re.compile('date'))
        date = datespan.string

        baseItem = BaseItem(0, movieName, rateNum, date, movieURL, picName, picURL)
        print(str(baseItem))
        # if the item is already in the database, stop it
        if checker and checker.is_last_item(baseItem):
            goOn = False
            break        
        sqliteHelper.add_baseItem(baseItem)

    sqliteHelper.commit()
    return goOn

def update_data():
    """Update the movie list from douban movie"""
    lastItem = sqliteHelper.get_last_movie()
    checker = None
    if lastItem:
        checker = ItemChecker()
        checker.set_last_item(lastItem)

    for idx in range(0, 940, 15):
        time.sleep(1)
        if not handle_page(idx, checker):
            break

def get_movie_data_by_id(subid):
    """
    https://developers.douban.com/wiki/?title=api_v2
    https://api.douban.com/v2/movie/subject/24325861
    """
    api_url = "http://api.douban.com/v2/movie/subject/" + subid
    resp = requests.get(api_url)
    if resp.status_code == requests.codes.ok:
        return resp.json()

def visual_data(items):
    databyWeekDay = {}
    databyRate = {}    
    for item in items:
        rate = item.rate
        if rate in databyRate:
            databyRate[rate] += 1
        else:
            databyRate[rate] = 1

        watchdate = datetime.datetime.strptime(item.date, '%Y-%m-%d')
        day = watchdate.weekday()
        if day in databyWeekDay:
            databyWeekDay[day].append(item)
        else:
            watchlist = []
            watchlist.append(item)
            databyWeekDay[day] = watchlist
    days = []
    movies = []
    for k,v in databyWeekDay.items():
        print('day of week {} waches {} movies, last is {}'.format(k, len(v), v[0].name))
        days.append(k+1)
        movies.append(len(v))

    rates = []
    ratecount = []
    for k, v in databyRate.items():
        rates.append(k)
        ratecount.append(v)

    plt.plot(rates, ratecount)
    #plt.plot(days, movies)
    #plt.bar(days, movies)
    #plt.savefig("hisgram.png")
    plt.show()

def update_movie_detail():
    #query a moive list by date range from local database
    items = sqliteHelper.get_movies_by_date('2016-12-01', '2017-1-30')
    print('movies count: %d ' % len(items))
    dbhelper = DBHelper("douban.db")

    for item in items:    
        print(item.name, item.url.split('/')[-2])    
        movie = parser.get_movie_from_api(item.url.split('/')[-2])
        dbhelper.add_movie(movie)
        time.sleep(1)


if __name__ == '__main__':

    #update_data()

    #query a moive list by date range from local database
    #items = sqliteHelper.get_movies_by_date('2016-01-01', '2016-12-30')
    #print(len(items)) #3754368
    # json_data = get_movie_data_by_id('24325861')
    # if json_data['subtype']:
    #     print(json_data['subtype'])
    #parser.get_movie_from_web('24325861')
    #update_movie_detail()
    sqliteHelper.get_movies_watched_duration()

    sqliteHelper.close()

    




