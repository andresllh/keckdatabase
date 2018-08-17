from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///dropdowns.db', echo=True)
Base = declarative_base()
 
########################################################################
class Drop_post(Base):
    """"""
    __tablename__ = "dropdown_post"
 
    id = Column(Integer, primary_key=True)
    post = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, post):
        """"""
        self.post = post
 
# create tables
Base.metadata.create_all(engine)