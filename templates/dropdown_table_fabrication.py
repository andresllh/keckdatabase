from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///dropdowns.db', echo=True)
Base = declarative_base()
 
########################################################################
class Drop_Fabrication(Base):
    """"""
    __tablename__ = "dropdown_fab"
 
    id = Column(Integer, primary_key=True)
    fabrication = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, fabrication):
        """"""
        self.fabrication = fabrication
 
# create tables
Base.metadata.create_all(engine)