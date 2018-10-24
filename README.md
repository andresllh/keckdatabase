## The database for the W.M. Keck Center for 3D Innovation is under development.

## Installation for local development
### Requirements 
In order to run the application and database locally, the following things must be installed on your computer:
  1. Python 3.6
  2. Sqlite
  3. Elasticsearch
  
Using pip, you will also need to install the following libraries for python 3.
  1. Pandas
  2. Numpy
  3. SQLAlchemy
  4. wtforms
  5. Flask
  6. elasticsearch
  
## How to run
#### Make sure to have elastic search up and running before running app.py
Once all requirements have been installed, go ahead and clone the repository or download the files.
After all files are in a folder, navigate to that folder in your command prompt and run the app using
the command "py app.py" or "python app.py" depending on which one utilizes python 3. Once the server
is running, open up a browser and navigate to "localhost:4000" to view it.

### Elastic Search
In order to get search results from the search engine, you need to configure your local instance of elastic search
to run on localhost:10000, by default port 9200 is used, alternatively you could modify the port inside app.py instead. 
Once elastic search is configured correctly, you need to run elasticsearch.bat (on windows) before you run app.py
so that it can actually perform queries. Keep in mind, there will be no data initially in your local instance of 
elasticsearch, therefore the data needs to be copied over at this time. In the near future, an Admin user 
will be able to add data while logged in with their admin credentials. 

## How to add more dropdown options
There is an excel file called dropdowns.xls, which contains all the filtering dropdown options
that are listed in the search page. To add more options, simply modify this file by adding the 
option directly underneath the column where you want it to be displayed.


### Developed for the W.M. Keck Center by Andres Llausas
