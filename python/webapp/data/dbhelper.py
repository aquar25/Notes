# -*- coding: utf-8 -*-
import os
import sqlite3
from sqlite3 import *

from DataModel import BaseItem

watched_movieTable = "CREATE TABLE watched_movie (" \
             "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL," \
             "name TEXT NOT NULL, " \
             "rate INTEGER," \
             "date DATE," \
             "url TEXT," \
             "cover TEXT," \
             "cover_url TEXT)"

class SqliteDBHelper():

    def __init__(self, dbname):
        self.create_database(dbname)

    def create_database(self, dbname):
        bCreate = not os.path.exists(dbname)
        self.db = sqlite3.connect(dbname)
        self.cursor = self.db.cursor()
        if bCreate:
            self.create_tables()


    def create_tables(self):
        self.cursor.execute(movieTable)
        self.db.commit()

    def add_baseItem(self, baseItem):
        self.add_movie(baseItem.name, baseItem.rate, baseItem.date,
                      baseItem.url, baseItem.cover, baseItem.coverUrl)

    def add_movie(self, name, rate, date, url, cover, cover_url):
        add = "INSERT INTO watched_movie (name, rate, date, url, cover, cover_url) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(add, (name, rate, date, url, cover, cover_url))

    def get_last_movie(self):
        """Get the last item by date"""
        query = "SELECT * FROM `watched_movie`  ORDER BY `date` DESC LIMIT 1;"
        self.cursor.execute(query)
        contents = []
        contents = self.cursor.fetchall()
        if len(contents) > 0:
            return BaseItem(*contents[0])

    def get_movies_by_date(self, start, end):  
        """ query data by date range like '2016-01-01', '2016-12-30', and return data item list     """
        query = "SELECT * FROM `watched_movie` WHERE `date` Between '"+start+"' AND '"+end+"' ORDER BY `date` DESC;"          
        self.cursor.execute(query)
        contents = []
        contents = self.cursor.fetchall()
        
        items = [ BaseItem(*content) for content in contents]
        return items

    def get_movies_watched_duration(self):
        query = "SELECT  title, alt, duration, episodes_count FROM movie "\
         "INNER JOIN watched_movie ON watched_movie.url = movie.alt "\
         "WHERE watched_movie.date Between '2017-01-01' AND '2017-01-15' "\
         "ORDER BY watched_movie.date  DESC;"
        self.cursor.execute(query)
        contents = []
        contents = self.cursor.fetchall()
        total_duration = 0
        for title, alt, duration, episodes_count in contents:
            if episodes_count != None:
                total_duration += episodes_count*duration
            else:
                total_duration += duration
        print(total_duration/60)

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataModel import Decalarative_Base


class DBHelper(object):
    '''
    Database helper class with sqlalchemy
    '''
    def __init__(self, dbname):
        self.tables = []
        self.dbname = dbname
        self.engine = create_engine("sqlite:///"+self.dbname, echo = True)
        Decalarative_Base.metadata.create_all(self.engine)
        self.DBsession = sessionmaker(bind=self.engine)        

    def create_tables(self):
        Decalarative_Base.metadata.create_all(self.engine)

    def add_movie(self, movie):
        session = self.DBsession()
        session.add(movie)
        session.commit()
        session.close()

    def query_movie(self, movie):
        pass

class ItemChecker(object):
    """Check the data to avoid add same item into database"""
    def __init__(self):
        pass

    def set_last_item(self, item):
        self.item = item

    def is_last_item(self, item):
        return self.item.name == item.name
        