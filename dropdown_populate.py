import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dropdown_tables import *
import pandas as pd
 
engine = create_engine('sqlite:///dropdowns.db', echo=True)
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("admin","password", True)
session.add(user)
 
user = User("normal", "password", False)
session.add(user)


data = pd.read_excel('dropdowns.xlsx')

ped_data = data['Pedigree']
fab_data = data['Fabrication']
post_data = data['Post-Processing']
test_data = data['Testing']

for item in ped_data.dropna():
	session.add(Drop_ped(item))

for item in fab_data.dropna():
	session.add(Drop_fab(item))

for item in post_data.dropna():
	session.add(Drop_post(item))

for item in test_data.dropna():
	session.add(Drop_test(item))

session.commit()
