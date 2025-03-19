from db import config
from db import all_db_stuff
from db import sql_queries

from scraping import *
from scripts import * 

import psycopg2
from configparser import ConfigParser

#db.connect.DatabaseConfig(filename = 'database.ini', section = 'postgresql')

postgres_config = config.DatabaseConfig(filename = 'db/database.ini', section = 'postgresql')
    
db1 = all_db_stuff.Database(postgres_config.get_config_params())
db1.connect()
#print(db1.get_data(sql_queries.get_all_game_results_dates_already_in_db))
#db1.create_table('db/create_table_files/create_game_dates_already_scraped_table.sql')

db1.close()
