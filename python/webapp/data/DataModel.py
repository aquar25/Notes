# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, Date

Decalarative_Base = declarative_base()

class BaseItem():
    def __init__(self, id, name, rate, date, url, cover, coverUrl):
        super().__init__()     
        self.id = id    # database auto generate
        self.name = name
        self.rate = rate
        self.date = date
        self.url  = url
        self.cover = cover
        self.coverUrl = coverUrl
    

    def __str__(self, *args, **kwargs):
        return (self.name+": Rate: "+ str(self.rate) + " date: " + self.date
                     + " Cover: " + self.cover)


class Movie(Decalarative_Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, )
    subid = Column(String(20))
    title = Column(String(60))
    original_title = Column(String(100))
    alt = Column(String(50))
    rating = Column(Float)
    collect_count = Column(Integer) # watched people count
    images = Column(String(100)) # post url
    subtype = Column(String(10)) # movie or tv
    director = Column(String(50)) # director name
    pubdates = Column(Date) # publish date
    year = Column(Integer)   
    language = Column(String(10))
    duration = Column(Integer)
    genres = Column(String(10))
    countries = Column(String(10))
    summary = Column(String(500))
    current_season = Column(Integer)
    episodes_count = Column(Integer)

    def __repr__(self):
        return "<Movie(title='%s', duration='%d'" % (self.title, self.duration)

# class Book(Decalarative_Base):
#     __tablename__ = "book"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     rate = Column(Integer)
#     date = Column(Date)
#     author = Column(String(50))
"""
subid = Column(String(50))
title = Column(String(50))
original_title = Column(String(50))
alt = Column(String(50))
rating = Column(String(50))
collect_count = Column(String(50))
images = Column(String(50))
subtype = Column(String(50))
director = Column(String(50))
pubdates = Column(String(50))
year = Column(String(50))
language = Column(String(50))
durations = Column(String(50))
genres = Column(String(50))
countries = Column(String(50))
summary = Column(String(50))
current_season = Column(String(50))
episodes_count = Column(String(50))

"""