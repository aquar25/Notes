# -*- coding: utf-8 -*-
import os
import sqlite3
from sqlite3 import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataModel import BaseItem

movieTable = "CREATE TABLE movie (" \
             "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL," \
             "name TEXT NOT NULL, " \
             "rate INTEGER," \
             "date DATE," \
             "url TEXT," \
             "cover TEXT," \
             "cover_url TEXT)"

class SqliteDBHelper():

    def __init__(self):
        self.create_database("douban.db")

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
        add = "INSERT INTO movie (name, rate, date, url, cover, cover_url) " \
              "VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.execute(add, (name, rate, date, url, cover, cover_url))

    def get_last_movie(self):
        """Get the last item by date"""
        query = "SELECT * FROM `movie`  ORDER BY `date` DESC LIMIT 1;"
        self.cursor.execute(query)
        contents = []
        contents = self.cursor.fetchall()
        if len(contents) > 0:
            return BaseItem(*contents[0])

    def get_movies_by_date(self, start, end):  
        """ query data by date range like '2016-01-01', '2016-12-30', and return data item list     """
        query = "SELECT * FROM `movie` WHERE `date` Between '"+start+"' AND '"+end+"' ORDER BY `date` DESC;"          
        self.cursor.execute(query)
        contents = []
        contents = self.cursor.fetchall()
        
        items = [ BaseItem(*content) for content in contents]
        return items

    def commit(self):
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()

class DBHelper(object):
    '''
    Database helper class
    '''
    def __init__(self, dbname):
        self.tables = []
        self.dbname = dbname
        self.engine = create_engine("sqlite:///"+self.dbname)
        self.DBsession = sessionmaker(bind=self.engine)


    def add_movie(self, moive):
        session = self.DBsession()
        session.add(moive)
        session.commit()
        session.close()

    def create(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def create_table(self, model):
        createState = "create table " + model
        self.cursor.execute("")

class ItemChecker(object):
    """Check the data to avoid add same item into database"""
    def __init__(self):
        pass

    def set_last_item(self, item):
        self.item = item

    def is_last_item(self, item):
        return self.item.name == item.name
        