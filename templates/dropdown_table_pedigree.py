from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///dropdowns.db', echo=True)
Base = declarative_base()
 
########################################################################
class Drop_Pedigree(Base):
    """"""
    __tablename__ = "dropdown_ped"
 
    id = Column(Integer, primary_key=True)
    pedigree = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, pedigree):
        """"""
        self.pedigree = pedigree
 
# create tables
Base.metadata.create_all(engine)