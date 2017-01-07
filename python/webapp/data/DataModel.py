# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date

Base = declarative_base()

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


class Movie(Base):
    __tablename__ = "moive"

    id = Column(Integer, primary_key=True, )
    name = Column(String(50))
    rate = Column(Integer)
    date = Column(Date)

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    rate = Column(Integer)
    date = Column(Date)
    author = Column(String(50))
