#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
import datetime
import requests
from bs4 import BeautifulSoup
from dbhelper import SqliteDBHelper, ItemChecker
from DataModel import BaseItem
from DataModel import Movie


sqliteHelper = SqliteDBHelper()

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


if __name__ == '__main__':

    update_data()

    #query a moive list by date range from local database
    items = sqliteHelper.get_movies_by_date('2016-01-01', '2016-12-30')
    print(len(items))

    sqliteHelper.close()




