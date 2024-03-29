from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///dropdowns.db', echo=True)
Base = declarative_base()
 
########################################################################
class Drop_test(Base):
    """"""
    __tablename__ = "dropdown_test"
 
    id = Column(Integer, primary_key=True)
    test = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, test):
        """"""
        self.test = test

class Drop_post(Base):
    """"""
    __tablename__ = "dropdown_post"
 
    id = Column(Integer, primary_key=True)
    post = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, post):
        """"""
        self.post = post

class Drop_fab(Base):
    """"""
    __tablename__ = "dropdown_fab"
 
    id = Column(Integer, primary_key=True)
    fab = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, fab):
        """"""
        self.fab = fab

class Drop_ped(Base):
    """"""
    __tablename__ = "dropdown_ped"
 
    id = Column(Integer, primary_key=True)
    ped = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, ped):
        """"""
        self.ped = ped
 
# create tables
Base.metadata.create_all(engine)